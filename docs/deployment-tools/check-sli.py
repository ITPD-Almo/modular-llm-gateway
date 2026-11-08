#!/usr/bin/env python3
"""Run QR-08 QRT-01 against staging and print only sanitized evidence."""

import argparse
import json
import math
import os
import re
import ssl
import sys
from dataclasses import dataclass
from time import monotonic, sleep, time_ns
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, ProxyHandler, Request, build_opener

ROUTE = "/v1/chat/completions"
P95_QUERY = (
    "histogram_quantile(0.95, sum by (le, route, outcome) "
    "(sum_over_time(gateway_chat_duration_bucket[5m])))"
)
TIMEOUT_SAMPLES_QUERY = (
    'gateway_chat_duration_count{route="/v1/chat/completions",outcome="timeout"}[5m]'
)
POINT_FIELDS = ("request_id", "route", "outcome", "duration_ms", "environment")


class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass
class Endpoint:
    base: str
    opener: object
    authorization: str | None

    @classmethod
    def from_environment(cls, url_var, auth_var, ca_var, rehearsal):
        base = os.environ[url_var].rstrip("/")
        parsed = urlsplit(base)
        loopback = parsed.hostname in {"127.0.0.1", "::1"}
        if (
            not parsed.hostname
            or parsed.username is not None
            or parsed.path
            or parsed.query
            or parsed.fragment
            or (rehearsal and not loopback)
            or (not rehearsal and loopback)
            or (parsed.scheme != "https" and not (loopback and parsed.scheme == "http"))
        ):
            raise ValueError(f"invalid {url_var} for the selected test mode")
        authorization = os.getenv(auth_var)
        if (authorization is None and (not rehearsal or url_var == "OPENOBSERVE_URL")) or (
            authorization is not None
            and not re.fullmatch(r"Basic [A-Za-z0-9+/]+={0,2}", authorization)
        ):
            raise ValueError(f"set a valid private {auth_var}")
        context = ssl.create_default_context(cafile=os.getenv(ca_var))
        return cls(
            base,
            build_opener(ProxyHandler({}), RejectRedirects(), HTTPSHandler(context=context)),
            authorization,
        )

    def call(self, path, body=None, timeout=2):
        headers = {"Accept": "application/json"}
        if self.authorization:
            headers["Authorization"] = self.authorization
        if body is not None:
            headers["Content-Type"] = "application/json"
        payload = json.dumps(body).encode() if body is not None else None
        request = Request(self.base + path, data=payload, headers=headers)
        try:
            response = self.opener.open(request, timeout=timeout)
        except HTTPError as error:
            response = error
        with response:
            data = response.read(1024 * 1024 + 1)
            if len(data) > 1024 * 1024:
                raise ValueError("query returned an oversized response")
            try:
                result = json.loads(data)
            except (UnicodeDecodeError, ValueError):
                result = {}
            return response.status, result, response.headers.get("X-Request-ID")


def chat(gateway, text):
    return gateway.call(ROUTE, {"messages": [{"role": "user", "content": text}]}, timeout=10)


def poll(deadline, check):
    while (remaining := deadline - monotonic()) > 0:
        try:
            found = check(min(remaining, 2))
        except (TimeoutError, URLError):
            found = None
        if found is not None and monotonic() <= deadline:
            return found
        sleep(min(0.2, max(0, deadline - monotonic())))
    return None


def metric_results(observe, prefix, query, timeout=2):
    path = f"{prefix}/prometheus/api/v1/query?" + urlencode({"query": query})
    status, data, _ = observe.call(path, timeout=timeout)
    if status != 200 or data.get("status") != "success":
        raise ValueError(f"staging metrics query failed (HTTP {status})")
    return data["data"]["result"]


def latest_timeout_sample(observe, prefix, timeout=2):
    rows = metric_results(observe, prefix, TIMEOUT_SAMPLES_QUERY, timeout)
    return max(
        (timestamp for row in rows for timestamp, count in row["values"] if float(count) > 0),
        default=0,
    )


def run(rehearsal):
    commit = os.getenv("QRT_RELEASE_SHA", "")
    if not rehearsal and not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("QRT_RELEASE_SHA must contain the full deployed commit")
    org = os.environ["OPENOBSERVE_STAGING_ORG"]
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", org) or org in {"default", "_meta", "production"}:
        raise ValueError("OPENOBSERVE_STAGING_ORG must name the dedicated staging organization")
    observe = Endpoint.from_environment(
        "OPENOBSERVE_URL", "OPENOBSERVE_QUERY_AUTHORIZATION", "OPENOBSERVE_QUERY_CA_FILE", rehearsal
    )
    gateway = Endpoint.from_environment(
        "STAGING_URL", "STAGING_AUTHORIZATION", "STAGING_CA_FILE", rehearsal
    )
    prefix = f"/api/{org}"

    status, health, _ = gateway.call("/health")
    if status != 200 or health != {"status": "ok"}:
        raise ValueError("staging health did not pass")
    for _ in range(2):
        status, reply, _ = chat(gateway, "hello")
        if (
            status != 200
            or reply.get("provider") != "fake"
            or reply.get("plugin_trace") != ["metadata", "uppercase"]
        ):
            raise ValueError(
                "staging must use the fake provider and the documented slow-plugin fixture"
            )

    # An older sample can expire as a fresh one arrives. Compare timestamps, not rolling totals.
    previous_sample = latest_timeout_sample(observe, prefix)
    request_start_us = time_ns() // 1000
    status, error, request_id = chat(gateway, "sleep")
    failed_at = monotonic()
    if (
        status != 504
        or error.get("detail") != "plugin SlowPlugin timed out during request processing"
        or not re.fullmatch(r"[0-9a-f]{32}", request_id or "")
    ):
        raise ValueError("staging did not return the expected named 504 and request ID")

    def find_log(timeout):
        sql = f"SELECT {', '.join(POINT_FIELDS)} FROM gateway_requests WHERE request_id = '{request_id}'"
        query = {
            "sql": sql,
            "start_time": request_start_us - 5_000_000,
            "end_time": time_ns() // 1000 + 5_000_000,
            "from": 0,
            "size": 2,
        }
        code, data, _ = observe.call(
            f"{prefix}/_search?type=logs", {"query": query, "use_cache": False}, timeout
        )
        if code in {400, 404} and "stream" in str(data.get("message", "")).lower():
            return None  # The first export creates the stream.
        if code != 200:
            raise ValueError(f"staging log query failed (HTTP {code})")
        rows = data.get("hits", [])
        if not rows:
            return None
        if len(rows) != 1:
            raise ValueError("more than one log point matched the failed request")
        point = {field: rows[0].get(field) for field in POINT_FIELDS}
        if (
            point["request_id"] != request_id
            or point["route"] != ROUTE
            or point["outcome"] != "timeout"
            or point["environment"] != "staging"
            or type(point["duration_ms"]) not in {int, float}
            or not math.isfinite(point["duration_ms"])
            or point["duration_ms"] < 0
        ):
            raise ValueError("the matching log point did not carry the required fields")
        return point

    def find_p95(timeout):
        if latest_timeout_sample(observe, prefix, timeout) <= previous_sample:
            return None
        remaining = failed_at + 60 - monotonic()
        if remaining <= 0:
            return None
        for series in metric_results(observe, prefix, P95_QUERY, min(remaining, 2)):
            labels = series.get("metric", {})
            if labels.get("route") == ROUTE and labels.get("outcome") == "timeout":
                timestamp, value = series["value"]
                if math.isfinite(float(value)):
                    return {
                        "route": ROUTE,
                        "outcome": "timeout",
                        "p95_ms": float(value),
                        "query_time": timestamp,
                    }
        return None

    point = poll(failed_at + 5, find_log)
    log_seconds = round(monotonic() - failed_at, 3) if point is not None else None
    series = poll(failed_at + 60, find_p95)
    metric_seconds = round(monotonic() - failed_at, 3) if series is not None else None
    passed = point is not None and series is not None
    print(
        json.dumps(
            {
                "result": "Passes" if passed else "Fails",
                "mode": "rehearsal" if rehearsal else "deployed",
                "environment": "staging",
                "commit": commit or None,
                "sli": "SLI-01",
                "failed_http_status": status,
                "request_id": request_id,
                "log_seconds": log_seconds,
                "log": point,
                "metric_seconds": metric_seconds,
                "failure_series": series,
            },
            indent=2,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rehearsal", action="store_true", help="Use loopback targets and label output local"
    )
    args = parser.parse_args()
    try:
        sys.exit(run(args.rehearsal))
    except KeyError:
        sys.exit("Missing test configuration or expected query response field")
    except (OSError, URLError):
        sys.exit("A staging gateway or query endpoint could not be reached")
    except ValueError as error:
        sys.exit(str(error))
