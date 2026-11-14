import importlib.util
import json
import re
import sqlite3
from pathlib import Path
from subprocess import CompletedProcess

import pytest

DOCS = Path(__file__).resolve().parents[1] / "docs"
SPEC = importlib.util.spec_from_file_location("ut01_check", DOCS / "deployment-tools/ut01-check.py")
assert SPEC is not None and SPEC.loader is not None
ut01 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ut01)


def event(event_name, timestamp, **fields):
    return {
        "_timestamp": timestamp,
        "event": event_name,
        "environment": "staging",
        "source": "usability-test",
        "run_id": "a" * 32,
        "plugin_count": 2,
        **fields,
    }


def test_export_uses_half_open_window_and_event_allowlist():
    config = event("gateway_configuration_used", 10)
    started = event("gateway_chat_started", 11, attempt_id="b" * 32)
    finished = event(
        "gateway_chat_finished", 12, attempt_id="b" * 32, outcome="ok", visible_result=True
    )
    hits = [
        event("gateway_configuration_used", 9),
        {**finished, "participant_code": "P-01", "authorization": "private", "content": "raw"},
        {**started, "ip": "private", "user_agent": "private"},
        {**config, "attempt_id": None, "outcome": None},
        {**finished, "source": "smoke"},
        {**finished, "environment": "production"},
        {**finished, "event": "unregistered"},
        {**finished, "_timestamp": 13},
    ]
    assert ut01.filter_events({"hits": hits, "total": len(hits)}, 10, 13) == [
        config,
        started,
        finished,
    ]


def test_export_rejects_incomplete_results_and_invalid_eligible_ids():
    with pytest.raises(ValueError, match="incomplete"):
        ut01.filter_events({"hits": [], "total": 1}, 10, 13)
    with pytest.raises(ValueError, match="invalid attempt identifier"):
        ut01.filter_events({"hits": [event("gateway_chat_started", 11, attempt_id="P-01")]}, 10, 13)


def test_export_requires_the_configured_organization_in_the_query_url(monkeypatch):
    monkeypatch.setenv("UT01_ORGANIZATION", "ut01generatedid")
    monkeypatch.setenv("UT01_QUERY_URL", "http://127.0.0.1:5080/api/anotherid")
    with pytest.raises(ValueError, match="match UT01_ORGANIZATION"):
        ut01.query_window(10, 13)


def test_rehearsal_requires_timeout_and_recovery_in_same_reset():
    first_run, slow_run = "a" * 32, "c" * 32
    records = [event("gateway_configuration_used", 10, run_id=first_run)]
    for timestamp, outcome, run in [
        (11, "ok", first_run),
        (14, "timeout", slow_run),
        (16, "ok", slow_run),
    ]:
        if timestamp == 14:
            records.append(event("gateway_configuration_used", 13, run_id=slow_run))
        attempt = f"{timestamp:032x}"
        records.append(event("gateway_chat_started", timestamp, run_id=run, attempt_id=attempt))
        records.append(
            event(
                "gateway_chat_finished",
                timestamp + 1,
                run_id=run,
                attempt_id=attempt,
                outcome=outcome,
                visible_result=outcome == "ok",
            )
        )
    ut01.check_rehearsal(records)
    records[-2]["run_id"] = first_run
    records[-1]["run_id"] = first_run
    with pytest.raises(ValueError, match="expected chat pairs"):
        ut01.check_rehearsal(records)


def test_probe_refuses_a_networked_container_before_sending_chat(monkeypatch):
    container = "a" * 64
    calls = []

    def docker(arguments, **options):
        calls.append(arguments)
        return CompletedProcess(arguments, 0, stdout=f"{container} bridge\n")

    monkeypatch.setattr(ut01.subprocess, "run", docker)
    with pytest.raises(ValueError, match="network mode none"):
        ut01.probe_marker("gateway", "marker")
    assert len(calls) == 1
    assert calls[0][:2] == ["docker", "inspect"]


def test_evidence_uses_private_mode_and_refuses_to_overwrite(tmp_path):
    path = tmp_path / "evidence.json"
    original = {"event": "ut01_plugin_probe", "_timestamp": 10, "marker_seen": False}
    ut01.write_private(path, original)
    assert path.stat().st_mode & 0o777 == 0o600
    with pytest.raises(RuntimeError, match="new private evidence file"):
        ut01.write_private(path, [])
    assert json.loads(path.read_text()) == original


def test_all_usage_metrics_ignore_smoke_and_usability_chats():
    sql = re.findall(r"```sql\n(.*?)\n```", (DOCS / "analytics.md").read_text(), re.S)
    dashboard = json.loads((DOCS / "deployment-tools/analytics-dashboard.json").read_text())
    chart = dashboard["tabs"][0]["panels"][0]["queries"][0]["query"]
    assert len(sql) == 4 and chart == sql[2]
    with sqlite3.connect(":memory:") as backend:
        backend.execute(
            "CREATE TABLE gateway_usage (event, source, plugin_count, outcome, visible_result, run_id)"
        )
        for source in ("web", "smoke", "usability-test"):
            backend.executemany(
                "INSERT INTO gateway_usage VALUES (?, ?, 2, ?, ?, ?)",
                [
                    ("gateway_configuration_used", source, None, None, source),
                    ("gateway_chat_started", source, None, None, source),
                    ("gateway_chat_finished", source, "ok", True, source),
                    ("gateway_chat_started", source, None, None, source),
                    ("gateway_chat_finished", source, "timeout", False, source),
                ],
            )
        assert [backend.execute(query).fetchone()[0] for query in [*sql, chart]] == [
            1,
            50.0,
            2,
            1,
            2,
        ]
