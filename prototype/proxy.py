"""Disposable Week 2 policy-decision-trail prototype."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import secrets
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


DEFAULT_POLICY = Path(__file__).with_name("policy.yaml")
DEFAULT_LOG = Path(__file__).with_name("decisions.jsonl")
CHAT_PATH = "/v1/chat/completions"
CALLER = "demo-user"


def load_policy(path: Path) -> dict[str, Any]:
    """Load the JSON-compatible YAML policy once during process startup."""
    with path.open(encoding="utf-8") as stream:
        policy = json.load(stream)

    if not isinstance(policy.get("revision"), str) or not policy["revision"]:
        raise ValueError("policy revision must be a non-empty string")
    rules = policy.get("rules")
    if not isinstance(rules, list) or len(rules) != 1:
        raise ValueError("this spike expects exactly one masking rule")
    rule = rules[0]
    for field in ("name", "pattern", "replacement"):
        if not isinstance(rule.get(field), str) or not rule[field]:
            raise ValueError(f"rule {field} must be a non-empty string")
    re.compile(rule["pattern"])
    return policy


def mask_strings(value: Any, pattern: re.Pattern[str], replacement: str) -> tuple[Any, bool]:
    """Return a deep sanitized copy and whether the rule matched."""
    matched = False
    if isinstance(value, str):
        sanitized, count = pattern.subn(replacement, value)
        return sanitized, count > 0
    if isinstance(value, list):
        result = []
        for item in value:
            sanitized, item_matched = mask_strings(item, pattern, replacement)
            result.append(sanitized)
            matched = matched or item_matched
        return result, matched
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            sanitized, item_matched = mask_strings(item, pattern, replacement)
            result[key] = sanitized
            matched = matched or item_matched
        return result, matched
    return copy.deepcopy(value), False


class DecisionTrailServer(ThreadingHTTPServer):
    def __init__(
        self,
        address: tuple[str, int],
        policy: dict[str, Any],
        decision_log: Path,
        caller_token: str,
    ) -> None:
        super().__init__(address, DecisionTrailHandler)
        self.policy = policy
        self.decision_log = decision_log
        self.caller_token = caller_token

    def record(self, request_id: str, caller: str, rule: str, decision: str, reason: str) -> None:
        event = {
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "caller": caller,
            "policy_revision": self.policy["revision"],
            "rule": rule,
            "decision": decision,
            "reason_code": reason,
        }
        self.decision_log.parent.mkdir(parents=True, exist_ok=True)
        with self.decision_log.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, separators=(",", ":")) + "\n")


class DecisionTrailHandler(BaseHTTPRequestHandler):
    server: DecisionTrailServer

    def do_POST(self) -> None:
        request_id = secrets.token_hex(8)
        if self.path != CHAT_PATH:
            self.send_error(404, "not found")
            return

        if self.headers.get("Authorization") != f"Bearer {self.server.caller_token}":
            self.server.record(
                request_id,
                "unknown",
                "credential-check",
                "reject",
                "invalid_caller_credential",
            )
            print(f"REJECTED request_id={request_id} provider_called=false", flush=True)
            self.send_json(401, {"error": "unauthorized", "request_id": request_id}, request_id)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "invalid JSON", "request_id": request_id}, request_id)
            return

        rule = self.server.policy["rules"][0]
        pattern = re.compile(rule["pattern"])
        sanitized, matched = mask_strings(body, pattern, rule["replacement"])
        decision = "redact" if matched else "allow"
        reason = "employee_id_masked" if matched else "no_rule_matched"
        self.server.record(request_id, CALLER, rule["name"], decision, reason)

        print(
            "FAKE PROVIDER RECEIVED "
            f"request_id={request_id} sanitized_request={json.dumps(sanitized, separators=(',', ':'))}",
            flush=True,
        )
        response = {
            "id": f"fake-{request_id}",
            "object": "chat.completion",
            "provider_received": sanitized,
        }
        self.send_json(200, response, request_id)

    def send_json(self, status: int, body: dict[str, Any], request_id: str) -> None:
        payload = json.dumps(body, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-Request-ID", request_id)
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"HTTP {format % args}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--decision-log", type=Path, default=DEFAULT_LOG)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    caller_token = os.environ.get("DEMO_CALLER_TOKEN")
    if not caller_token:
        raise SystemExit("Set DEMO_CALLER_TOKEN to a demo-only value before starting the spike.")
    policy = load_policy(args.policy)
    server = DecisionTrailServer((args.host, args.port), policy, args.decision_log, caller_token)
    print(
        f"Loaded policy revision={policy['revision']} and listening on http://{args.host}:{args.port}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

