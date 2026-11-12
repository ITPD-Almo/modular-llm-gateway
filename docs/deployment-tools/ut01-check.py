#!/usr/bin/env python3
"""Export one UT-01 window or record a marker check from an offline plugin container."""

import argparse
import http.client
import json
import os
import re
import ssl
import subprocess
import sys
from pathlib import Path
from time import time_ns
from urllib.parse import urlsplit

EVENTS = ("gateway_configuration_used", "gateway_chat_started", "gateway_chat_finished")
OUTCOMES = ("ok", "client_error", "server_error", "timeout")
COMMON_FIELDS = (
    "_timestamp",
    "environment",
    "source",
    "event",
    "run_id",
    "plugin_count",
)
FIELDS = (*COMMON_FIELDS, "attempt_id", "outcome", "visible_result")
MAX_ROWS = 1000
MAX_RESPONSE_BYTES = 1024 * 1024
Row = dict[str, str | int | bool]

# Run inside the offline container so it needs neither a published port nor egress.
PROBE = """
import http.client
import json
import sys

connection = http.client.HTTPConnection('127.0.0.1', 8000, timeout=6)
try:
    payload = json.dumps({'messages': [{'role': 'user', 'content': 'usability example'}]})
    connection.request('POST', '/v1/chat/completions', payload, {'Content-Type': 'application/json'})
    response = connection.getresponse()
    if response.status != 200:
        sys.exit(1)
    result = json.loads(response.read(65537))
    content = result['choices'][0]['message']['content']
    if result.get('provider') != 'fake' or not isinstance(content, str):
        sys.exit(1)
    print(json.dumps(sys.argv[1] in content))
finally:
    connection.close()
"""


def utc_microseconds() -> int:
    return time_ns() // 1000


def query_window(start: int, end: int) -> object:
    if not 0 < start < end <= 2**63 - 1:
        raise ValueError("set an increasing UTC window in Unix microseconds")
    organization = os.getenv("UT01_ORGANIZATION", "")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", organization) or organization in {
        "default",
        "_meta",
        "production",
    }:
        raise ValueError("set UT01_ORGANIZATION to the dedicated staging test organization ID")
    url_error = "UT01_QUERY_URL must use HTTPS or loopback HTTP and match UT01_ORGANIZATION"
    try:
        base = urlsplit(os.getenv("UT01_QUERY_URL", "").rstrip("/"))
        port = base.port
    except ValueError as error:
        raise ValueError(url_error) from error
    authorization = os.getenv("UT01_QUERY_AUTHORIZATION", "")
    loopback_http = base.scheme == "http" and base.hostname in {"127.0.0.1", "::1"}
    if (
        not base.hostname
        or base.username is not None
        or base.path != f"/api/{organization}"
        or base.query
        or base.fragment
        or (base.scheme != "https" and not loopback_http)
    ):
        raise ValueError(url_error)
    if not re.fullmatch(r"Basic [A-Za-z0-9+/]+={0,2}", authorization):
        raise ValueError("set the private UT01_QUERY_AUTHORIZATION header")
    events = ", ".join(f"'{event}'" for event in EVENTS)
    sql = (
        f"SELECT {', '.join(FIELDS)} FROM gateway_usage "
        "WHERE environment = 'staging' AND source = 'usability-test' "
        f"AND event IN ({events}) AND _timestamp >= {start} AND _timestamp < {end} "
        "ORDER BY _timestamp ASC"
    )
    payload = {
        "query": {"sql": sql, "start_time": start, "end_time": end, "from": 0, "size": MAX_ROWS},
        "use_cache": False,
    }
    # A direct connection ignores shell proxy settings and never follows redirects.
    try:
        if base.scheme == "https":
            context = ssl.create_default_context(cafile=os.getenv("UT01_QUERY_CA_FILE") or None)
            connection = http.client.HTTPSConnection(
                base.hostname, port, timeout=10, context=context
            )
        else:
            connection = http.client.HTTPConnection(base.hostname, port, timeout=10)
        try:
            connection.request(
                "POST",
                f"{base.path}/_search?type=logs",
                json.dumps(payload),
                {"Authorization": authorization, "Content-Type": "application/json"},
            )
            response = connection.getresponse()
            if response.status != 200:
                raise RuntimeError(f"UT-01 analytics query failed (HTTP {response.status})")
            raw = response.read(MAX_RESPONSE_BYTES + 1)
        finally:
            connection.close()
    except (OSError, ValueError, http.client.HTTPException) as error:
        raise RuntimeError("UT-01 analytics connection or TLS verification failed") from error
    if len(raw) > MAX_RESPONSE_BYTES:
        raise ValueError("analytics response is too large for a session export")
    try:
        return json.loads(raw)
    except (ValueError, UnicodeError) as error:
        raise ValueError("analytics returned invalid JSON") from error


def opaque_id(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{32}", value) is not None


def filter_events(data: object, start: int, end: int) -> list[Row]:
    if not isinstance(data, dict) or not isinstance(hits := data.get("hits"), list):
        raise ValueError("analytics response has no hit list")
    total = data.get("total", len(hits))
    if (
        data.get("is_partial")
        or type(total) is not int
        or total > len(hits)
        or len(hits) >= MAX_ROWS
    ):
        raise ValueError("analytics result may be incomplete; query a smaller session window")
    records = []
    for row in hits:
        if not isinstance(row, dict):
            raise ValueError("analytics response contains a malformed hit")
        event = row.get("event")
        if (
            event not in EVENTS
            or row.get("environment") != "staging"
            or (row.get("source") != "usability-test")
        ):
            continue
        timestamp = row.get("_timestamp")
        if type(timestamp) is not int:
            raise ValueError("a test event has an invalid timestamp")
        if not start <= timestamp < end:
            continue
        count = row.get("plugin_count")
        if not opaque_id(row.get("run_id")) or type(count) is not int or count < 0:
            raise ValueError("a test event has invalid common fields")
        record = {field: row[field] for field in COMMON_FIELDS}
        if event != "gateway_configuration_used":
            if not opaque_id(row.get("attempt_id")):
                raise ValueError("a test event has an invalid attempt identifier")
            record["attempt_id"] = row["attempt_id"]
        if event == "gateway_chat_finished":
            if row.get("outcome") not in OUTCOMES or type(row.get("visible_result")) is not bool:
                raise ValueError("a test event has invalid outcome fields")
            record.update(outcome=row["outcome"], visible_result=row["visible_result"])
        records.append(record)
    return sorted(records, key=lambda record: record["_timestamp"])


def check_rehearsal(records: list[Row]) -> None:
    configs = [row["run_id"] for row in records if row["event"] == "gateway_configuration_used"]
    starts = {
        (row["run_id"], row["attempt_id"]): row["_timestamp"]
        for row in records
        if row["event"] == "gateway_chat_started"
    }
    finishes = [row for row in records if row["event"] == "gateway_chat_finished"]
    if len(records) == 8 and len(set(configs)) == 2 and len(starts) == len(finishes) == 3:
        first, slow, recovered = finishes
        keys = {(row["run_id"], row["attempt_id"]) for row in finishes}
        if (
            keys == starts.keys()
            and all(
                starts[row["run_id"], row["attempt_id"]] <= row["_timestamp"] for row in finishes
            )
            and [first["run_id"], slow["run_id"]] == configs
            and slow["run_id"] == recovered["run_id"]
            and [row["outcome"] for row in finishes] == ["ok", "timeout", "ok"]
            and first["visible_result"] is True
            and recovered["visible_result"] is True
        ):
            return
    raise ValueError("window does not contain the two fixture runs and three expected chat pairs")


def probe_marker(container: str, marker: str) -> Row:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", container):
        raise ValueError("provide the name or ID of the offline plugin container")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", marker):
        raise ValueError(
            "use a synthetic marker of 1–32 ASCII letters, digits, dashes or underscores"
        )
    try:
        inspection = subprocess.run(
            [
                "docker",
                "inspect",
                "--type",
                "container",
                "--format",
                "{{.Id}} {{.HostConfig.NetworkMode}}",
                container,
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        match = re.fullmatch(r"([0-9a-f]{64}) none", inspection.stdout.strip())
        if not match:
            raise ValueError("the plugin probe requires Docker network mode none")
        result = subprocess.run(
            ["docker", "exec", match[1], "python", "-I", "-c", PROBE, marker],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError) as error:
        raise RuntimeError(
            "offline plugin probe did not receive a successful fake response"
        ) from error
    if result not in {"true", "false"}:
        raise ValueError("offline plugin probe returned an invalid result")
    return {
        "event": "ut01_plugin_probe",
        "_timestamp": utc_microseconds(),
        "marker_seen": result == "true",
    }


def write_private(path: Path, data: list[Row] | Row) -> None:
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            json.dump(data, output, indent=2)
            output.write("\n")
    except OSError as error:
        raise RuntimeError(
            "cannot create a new private evidence file at the requested path"
        ) from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("now", help="print a UTC timestamp in Unix microseconds")
    export = commands.add_parser("export", help="save a filtered [start, end) event window")
    export.add_argument("--start-us", type=int, required=True)
    export.add_argument("--end-us", type=int, required=True)
    export.add_argument("--output", type=Path, required=True)
    export.add_argument("--check-rehearsal", action="store_true")
    probe = commands.add_parser("probe", help="record whether the fake reply contains a marker")
    probe.add_argument("--container", required=True)
    probe.add_argument("--marker", required=True)
    probe.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "now":
            print(utc_microseconds())
        elif args.command == "export":
            data = query_window(args.start_us, args.end_us)
            records = filter_events(data, args.start_us, args.end_us)
            if args.check_rehearsal:
                check_rehearsal(records)
            write_private(args.output, records)
            print(f"Saved {len(records)} UT-01 events to private evidence")
        else:
            record = probe_marker(args.container, args.marker)
            write_private(args.output, record)
            print("Saved UT-01 marker check to private evidence")
    except (ValueError, RuntimeError) as error:
        print(f"UT-01: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
