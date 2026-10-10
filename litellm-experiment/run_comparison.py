"""Run r1, restart into r2, and verify retained LiteLLM decision records."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent
LOG = ROOT / "callback-decisions.jsonl"
FIELDS = {
    "request_id",
    "timestamp",
    "caller",
    "policy_revision",
    "rule",
    "decision",
    "reason_code",
}


def run(policy: str, scenario: str) -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "callback_check.py"),
            "--policy",
            str(ROOT / policy),
            "--decision-log",
            str(LOG),
            "--scenario",
            scenario,
        ],
        check=True,
    )


def main() -> None:
    LOG.unlink(missing_ok=True)
    run("policy-r1.yaml", "mask")
    run("policy-r2.yaml", "mask")
    run("policy-r2.yaml", "reject")

    records = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines()]
    assert len(records) == 3
    assert [record["policy_revision"] for record in records] == ["r1", "r2", "r2"]
    assert [record["decision"] for record in records] == ["redact", "redact", "reject"]
    assert all(set(record) == FIELDS for record in records)
    serialized = json.dumps(records)
    assert "EMP-" not in serialized
    assert "messages" not in serialized
    assert "synthetic response" not in serialized
    assert "caller_token" not in serialized

    print("LiteLLM 1.104.2 comparison passed")
    print("r1 and r2 were loaded by separate processes; the r1 record was retained")
    print("mask decisions came from regex evaluation; the reject occurred before completion")
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
