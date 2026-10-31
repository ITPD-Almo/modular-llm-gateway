#!/usr/bin/env python3
"""Collect normal HTTP evidence; this does not implement #98's quality test."""

import argparse
import base64
import ipaddress
import json
import os
import re
import ssl
import stat
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, ProxyHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        return None


def fetch(base, endpoint, payload=None, *, context=None, authorization=None):
    started = time.monotonic()
    result = {"status": None}
    try:
        data = None if payload is None else json.dumps(payload).encode()
        headers = {"Content-Type": "application/json"}
        if authorization:
            headers["Authorization"] = authorization
        request = Request(base + endpoint, data=data, headers=headers)
        opener = build_opener(ProxyHandler({}), NoRedirect(), HTTPSHandler(context=context))
        try:
            response = opener.open(request, timeout=10)
        except HTTPError as error:
            response = error
        with response:
            raw = response.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                raise ValueError("Response size limit exceeded")
            result.update(
                status=response.status,
                body=raw.decode("utf-8", errors="replace"),
                request_id=response.headers.get("X-Request-ID"),
            )
    except Exception as error:
        # Connection errors can include the actual deployment address.
        result.update(error_type=type(error).__name__, private_error=str(error))
    result["elapsed_seconds"] = round(time.monotonic() - started, 3)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Private base URL; never publish raw evidence")
    parser.add_argument("--environment", choices=("staging", "production"), required=True)
    parser.add_argument(
        "--network", choices=("campus", "tailnet", "external", "local"), required=True
    )
    parser.add_argument(
        "--expected-sha", required=True, help="Operator-supplied SHA; compare the VM receipt"
    )
    parser.add_argument("--runner", required=True, help="Runner's GitHub username")
    parser.add_argument("--ca-cert", type=Path, help="Explicitly trusted demo CA certificate")
    parser.add_argument(
        "--access-file", type=Path, help="Private exported demo-code file; never a provider key"
    )
    parser.add_argument("--access-user", choices=("owner", "ta", "customer"), default="owner")
    parser.add_argument("--output", type=Path, default=Path("private/campus-evidence"))
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.expected_sha):
        parser.error("Use a full 40-character SHA")
    url = urlsplit(args.url)
    if (
        url.scheme not in ("http", "https")
        or not url.hostname
        or url.username
        or url.password
        or url.query
        or url.fragment
        or url.path not in ("", "/")
    ):
        parser.error("Use an http(s) base URL without credentials, query or path")
    if args.network == "campus":
        try:
            address = ipaddress.IPv4Address(url.hostname)
        except ValueError:
            parser.error("Campus verification uses the direct university IPv4, not a domain name")
        if address.is_loopback or address in ipaddress.IPv4Network("100.64.0.0/10"):
            parser.error("Use the university LAN IPv4 rather than loopback or the Tailscale IPv4")

    context = ssl.create_default_context(cafile=str(args.ca_cert)) if args.ca_cert else None
    authorization = None
    if args.access_file:
        if url.scheme != "https":
            parser.error("Demo access credentials require verified HTTPS")
        try:
            info = args.access_file.lstat()
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
                raise ValueError
            descriptor = os.open(args.access_file, os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(descriptor, encoding="utf-8") as source:
                info = os.fstat(source.fileno())
                if (
                    not stat.S_ISREG(info.st_mode)
                    or info.st_uid != os.getuid()
                    or info.st_mode & 0o077
                ):
                    raise ValueError
                code = json.load(source)["environments"][args.environment][args.access_user]
            if not isinstance(code, str) or not re.fullmatch(r"[A-Za-z0-9_-]{24,128}", code):
                raise ValueError
            authorization = (
                "Basic " + base64.b64encode((args.access_user + ":" + code).encode()).decode()
            )
        except (OSError, ValueError, KeyError, TypeError):
            parser.error("Invalid or unsafe private demo-code file")

    os.umask(0o077)
    args.output.mkdir(parents=True, exist_ok=True, mode=0o700)
    directory = Path(tempfile.mkdtemp(prefix=args.environment + "-", dir=args.output))
    base = args.url.rstrip("/")
    raw = {
        "health": fetch(base, "/health", context=context, authorization=authorization),
        "chat": fetch(
            base,
            "/v1/chat/completions",
            {"messages": [{"role": "user", "content": "hello"}]},
            context=context,
            authorization=authorization,
        ),
        "docs": fetch(base, "/docs", context=context, authorization=authorization),
    }
    try:
        health = json.loads(raw["health"].get("body", ""))
    except ValueError:
        health = {}
    try:
        chat = json.loads(raw["chat"].get("body", ""))
        answer = chat["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        chat, answer = {}, None
    checks = {
        "health_http_200": raw["health"]["status"] == 200,
        "health_body_ok": health == {"status": "ok"},
        "chat_http_200": raw["chat"]["status"] == 200,
        "fake_provider": chat.get("provider") == "fake",
        "expected_answer": answer == "fake: HELLO",
        "default_plugin_order": chat.get("plugin_trace") == ["metadata", "uppercase"],
        "four_plugin_changes": isinstance(chat.get("plugin_changes"), list)
        and len(chat["plugin_changes"]) == 4,
        "chat_request_id_present": bool(raw["chat"].get("request_id")),
        "docs_html_served": raw["docs"]["status"] == 200
        and "swagger-ui" in raw["docs"].get("body", ""),
    }
    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "environment_label": args.environment,
        "runner_github_username": args.runner,
        "client_network_self_reported": args.network,
        "expected_source_sha_supplied_by_operator": args.expected_sha,
        "provenance_note": "Compare the VM install receipt/current-ref; this script cannot prove campus location or server SHA.",
        "scope": "Normal core-task HTTP checks only; run #98 QRT-01 separately. HTTP /docs is not a browser-rendering check.",
        "authenticated_demo_access": bool(authorization),
        "transport": url.scheme,
        "checks": checks,
        "elapsed_seconds": {name: item["elapsed_seconds"] for name, item in raw.items()},
        "passed": all(checks.values()),
    }
    (directory / "private-raw.json").write_text(
        json.dumps({"base_url": base, "responses": raw}, indent=2) + "\n"
    )
    (directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print("Evidence directory: " + str(directory))
    print("Share summary.json only; private-raw.json contains the actual deployment address.")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
