"""Integration checks for the disposable prototype."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).parent
TOKEN = "local-demo-token-for-tests"
EXPECTED_FIELDS = {
    "request_id",
    "timestamp",
    "caller",
    "policy_revision",
    "rule",
    "decision",
    "reason_code",
}


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class RunningServer:
    def __init__(self, policy: Path, log: Path) -> None:
        self.port = free_port()
        env = os.environ.copy()
        env["DEMO_CALLER_TOKEN"] = TOKEN
        self.process = subprocess.Popen(
            [
                sys.executable,
                str(ROOT / "proxy.py"),
                "--port",
                str(self.port),
                "--policy",
                str(policy),
                "--decision-log",
                str(log),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
        )
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            try:
                with socket.create_connection(("127.0.0.1", self.port), timeout=0.1):
                    return
            except OSError:
                time.sleep(0.05)
        self.stop()
        raise RuntimeError("server did not start")

    def stop(self) -> str:
        if self.process.poll() is None:
            self.process.terminate()
        output, _ = self.process.communicate(timeout=5)
        return output


def post(port: int, body: dict, token: str | None = TOKEN) -> tuple[int, dict, str]:
    headers = {"Content-Type": "application/json"}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers=headers,
        method="POST",
    )
    try:
        response = urllib.request.urlopen(request, timeout=3)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        return response.status, json.load(response), response.headers["X-Request-ID"]


class SpikeTest(unittest.TestCase):
    def test_mask_allow_reject_restart_and_lookup(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            policy = temp_path / "policy.yaml"
            decision_log = temp_path / "decisions.jsonl"
            base_policy = json.loads((ROOT / "policy.yaml").read_text(encoding="utf-8"))
            policy.write_text(json.dumps(base_policy), encoding="utf-8")

            server = RunningServer(policy, decision_log)
            status, masked, r1_id = post(
                server.port,
                {"model": "fake", "messages": [{"role": "user", "content": "Check EMP-123456"}]},
            )
            self.assertEqual(status, 200)
            self.assertIn("[EMPLOYEE-ID]", json.dumps(masked))
            self.assertNotIn("EMP-123456", json.dumps(masked))

            status, _, allow_id = post(server.port, {"model": "fake", "messages": []})
            self.assertEqual(status, 200)

            status, rejected, reject_id = post(server.port, {"messages": []}, token=None)
            self.assertEqual(status, 401)
            self.assertEqual(rejected["error"], "unauthorized")
            first_output = server.stop()
            self.assertEqual(first_output.count("FAKE PROVIDER RECEIVED"), 2)
            self.assertIn("provider_called=false", first_output)

            base_policy["revision"] = "r2"
            policy.write_text(json.dumps(base_policy), encoding="utf-8")
            server = RunningServer(policy, decision_log)
            _, _, r2_id = post(
                server.port,
                {"model": "fake", "messages": [{"role": "user", "content": "Again EMP-654321"}]},
            )
            server.stop()

            records = [json.loads(line) for line in decision_log.read_text(encoding="utf-8").splitlines()]
            by_id = {record["request_id"]: record for record in records}
            self.assertEqual(by_id[r1_id]["policy_revision"], "r1")
            self.assertEqual(by_id[r1_id]["decision"], "redact")
            self.assertEqual(by_id[allow_id]["decision"], "allow")
            self.assertEqual(by_id[reject_id]["decision"], "reject")
            self.assertEqual(by_id[reject_id]["rule"], "credential-check")
            self.assertEqual(by_id[r2_id]["policy_revision"], "r2")
            for record in records:
                self.assertEqual(set(record), EXPECTED_FIELDS)
                serialized = json.dumps(record)
                self.assertNotIn("EMP-", serialized)
                self.assertNotIn(TOKEN, serialized)

            found = subprocess.run(
                [sys.executable, str(ROOT / "lookup.py"), r1_id, "--decision-log", str(decision_log)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn('"policy_revision": "r1"', found.stdout)
            missing = subprocess.run(
                [sys.executable, str(ROOT / "lookup.py"), "missing-id", "--decision-log", str(decision_log)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(missing.returncode, 1)
            self.assertIn("No decision record exists", missing.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)

