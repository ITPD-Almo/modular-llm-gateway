"""Look up one body-free decision record by request ID."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_LOG = Path(__file__).with_name("decisions.jsonl")


def find_record(path: Path, request_id: str) -> dict[str, str] | None:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            if record.get("request_id") == request_id:
                return record
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request_id")
    parser.add_argument("--decision-log", type=Path, default=DEFAULT_LOG)
    args = parser.parse_args()
    record = find_record(args.decision_log, args.request_id)
    if record is None:
        print(f"No decision record exists for request ID {args.request_id}.")
        return 1
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

