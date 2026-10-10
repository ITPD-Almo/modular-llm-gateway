"""Run one policy-derived LiteLLM callback scenario in a fresh process."""

from __future__ import annotations

import argparse
import json
import re
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import litellm
from litellm.integrations.custom_logger import CustomLogger


FIELDS = (
    "request_id",
    "timestamp",
    "caller",
    "policy_revision",
    "rule",
    "decision",
    "reason_code",
)


class DecisionLogger(CustomLogger):
    """Write policy facts supplied by the policy layer, without request bodies."""

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self.callback_fired = threading.Event()

    def write(self, policy_decision: dict[str, str]) -> None:
        record = {field: policy_decision[field] for field in FIELDS}
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, separators=(",", ":")) + "\n")

    def log_success_event(self, kwargs, response_obj, start_time, end_time) -> None:
        params = kwargs.get("litellm_params") or {}
        metadata = params.get("metadata") or kwargs.get("metadata") or {}
        self.write(metadata["policy_decision"])
        self.callback_fired.set()

    def log_failure_event(self, kwargs, response_obj, start_time, end_time) -> None:
        params = kwargs.get("litellm_params") or {}
        metadata = params.get("metadata") or kwargs.get("metadata") or {}
        self.write(metadata["policy_decision"])
        self.callback_fired.set()


def load_policy(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        policy = json.load(stream)
    rule = policy["rules"][0]
    re.compile(rule["pattern"])
    return policy


def evaluate(policy: dict[str, Any], body: dict[str, Any]) -> tuple[dict[str, Any], str, str]:
    rule = policy["rules"][0]
    pattern = re.compile(rule["pattern"])
    serialized = json.dumps(body)
    sanitized, count = pattern.subn(rule["replacement"], serialized)
    decision = "redact" if count else "allow"
    reason = "employee_id_masked" if count else "no_rule_matched"
    return json.loads(sanitized), decision, reason


def decision_context(
    policy: dict[str, Any], caller: str, rule: str, decision: str, reason: str
) -> dict[str, str]:
    return {
        "request_id": uuid.uuid4().hex[:16],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "caller": caller,
        "policy_revision": policy["revision"],
        "rule": rule,
        "decision": decision,
        "reason_code": reason,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--decision-log", required=True, type=Path)
    parser.add_argument("--scenario", choices=("mask", "allow", "reject"), required=True)
    args = parser.parse_args()

    policy = load_policy(args.policy)
    logger = DecisionLogger(args.decision_log)
    litellm.callbacks = [logger]

    if args.scenario == "reject":
        context = decision_context(
            policy,
            caller="unknown",
            rule="credential-check",
            decision="reject",
            reason="invalid_caller_credential",
        )
        # A gateway credential rejection occurs before any provider completion,
        # so no LiteLLM success/failure callback exists for this path.
        logger.write(context)
        time.sleep(0.2)
        if logger.callback_fired.is_set():
            raise RuntimeError("a completion callback unexpectedly handled the pre-provider reject")
    else:
        content = "Check EMP-123456" if args.scenario == "mask" else "No identifier here"
        body = {"model": "fake", "messages": [{"role": "user", "content": content}]}
        sanitized, decision, reason = evaluate(policy, body)
        context = decision_context(
            policy,
            caller="demo-user",
            rule=policy["rules"][0]["name"],
            decision=decision,
            reason=reason,
        )
        litellm.completion(
            model="openai/sdk-mock",
            messages=sanitized["messages"],
            mock_response="synthetic response",
            metadata={"policy_decision": context},
        )
        if not logger.callback_fired.wait(5):
            raise RuntimeError("LiteLLM callback did not write the decision")

    print(json.dumps(context, indent=2))


if __name__ == "__main__":
    main()
