"""Run the real spike and create sanitized, automatically sourced evidence pages."""

from __future__ import annotations

import argparse
import html
import json
import tempfile
from pathlib import Path

from test_spike import ROOT, RunningServer, post


def page(title: str, subtitle: str, sections: list[tuple[str, str]]) -> str:
    cards = "".join(
        f"<section><h2>{html.escape(heading)}</h2><pre>{html.escape(content)}</pre></section>"
        for heading, content in sections
    )
    return f"""<!doctype html>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
body {{ margin:0; background:#0b1020; color:#e7edf8; font:18px/1.42 Consolas,monospace; }}
main {{ padding:34px 44px; }}
h1 {{ margin:0 0 8px; color:#77d8ff; font:700 30px/1.2 Segoe UI,sans-serif; }}
.note {{ margin-bottom:20px; color:#a8b6cc; font-family:Segoe UI,sans-serif; }}
section {{ margin:16px 0; padding:18px 20px; border:1px solid #334567; border-radius:12px; background:#111a2e; }}
h2 {{ margin:0 0 10px; color:#ffd479; font:600 21px Segoe UI,sans-serif; }}
pre {{ margin:0; white-space:pre-wrap; overflow-wrap:anywhere; }}
</style>
<main><h1>{html.escape(title)}</h1><div class="note">{html.escape(subtitle)}</div>{cards}</main>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp:
        temp_path = Path(temp)
        policy = temp_path / "policy.yaml"
        decision_log = temp_path / "decisions.jsonl"
        policy_data = json.loads((ROOT / "policy.yaml").read_text(encoding="utf-8"))
        policy.write_text(json.dumps(policy_data), encoding="utf-8")

        masked_input = {
            "model": "fake",
            "messages": [{"role": "user", "content": "Check EMP-123456"}],
        }
        server = RunningServer(policy, decision_log)
        masked_status, masked_response, r1_id = post(server.port, masked_input)
        allow_status, _, allow_id = post(
            server.port,
            {"model": "fake", "messages": [{"role": "user", "content": "No identifier here"}]},
        )
        reject_status, _, reject_id = post(server.port, masked_input, token=None)
        r1_console = server.stop()

        policy_data["revision"] = "r2"
        policy.write_text(json.dumps(policy_data), encoding="utf-8")
        server = RunningServer(policy, decision_log)
        r2_status, r2_response, r2_id = post(
            server.port,
            {
                "model": "fake",
                "messages": [{"role": "user", "content": "Check EMP-654321 after restart"}],
            },
        )
        r2_console = server.stop()

        records = [json.loads(line) for line in decision_log.read_text(encoding="utf-8").splitlines()]
        by_id = {record["request_id"]: record for record in records}
        assert (masked_status, allow_status, reject_status, r2_status) == (200, 200, 401, 200)
        assert by_id[r1_id]["policy_revision"] == "r1"
        assert by_id[allow_id]["decision"] == "allow"
        assert by_id[reject_id]["decision"] == "reject"
        assert by_id[r2_id]["policy_revision"] == "r2"
        assert "EMP-123456" not in json.dumps(masked_response)
        assert "EMP-654321" not in json.dumps(r2_response)

        masked_html = page(
            "Masked request reaches the fake provider",
            "Actual HTTP request and response from the running local spike; synthetic data",
            [
                ("Client input", json.dumps(masked_input, indent=2)),
                ("Fake provider received", json.dumps(masked_response["provider_received"], indent=2)),
                ("Returned correlation ID", f"X-Request-ID: {r1_id}"),
            ],
        )
        revisions_html = page(
            "Records retain the loaded policy revision",
            "Actual JSONL records from separate r1 and r2 server processes",
            [
                ("Old request before restart", json.dumps(by_id[r1_id], indent=2)),
                ("New request after restart", json.dumps(by_id[r2_id], indent=2)),
            ],
        )
        reject_line = next(line for line in r1_console.splitlines() if reject_id in line)
        reject_html = page(
            "Rejected request never reaches the fake provider",
            "Actual credential rejection and body-free JSONL record",
            [
                ("Decision record", json.dumps(by_id[reject_id], indent=2)),
                ("Server outcome", reject_line),
            ],
        )

        files = {
            "spike-masked-request.html": masked_html,
            "spike-decision-records.html": revisions_html,
            "spike-reject-record.html": reject_html,
        }
        for name, content in files.items():
            (args.output / name).write_text(content, encoding="utf-8")
        manifest = {
            "r1_request_id": r1_id,
            "r2_request_id": r2_id,
            "reject_request_id": reject_id,
            "r1_console": r1_console,
            "r2_console": r2_console,
            "records": records,
        }
        (args.output / "capture-manifest.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )

    print(f"Wrote actual-run evidence sources to {args.output}")


if __name__ == "__main__":
    main()
