"""Self-contained, real HTTP demo using the installed package and fake provider."""

import json
import logging
import socket
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
from time import monotonic, sleep

import uvicorn

from .cli import request_json
from .main import create_app


@contextmanager
def running_gateway(config: Path):
    # Hold the ephemeral port until uvicorn takes ownership: no fixed-port conflict
    # and no race from closing/reopening a probed port.
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        base = f"http://127.0.0.1:{listener.getsockname()[1]}"
        server = uvicorn.Server(
            uvicorn.Config(
                create_app(str(config), startup_timeout_ms=5000),
                log_level="critical",
                access_log=False,
                log_config=None,
            )
        )
        thread = Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        thread.start()
        try:
            deadline = monotonic() + 10
            while not server.started:
                if not thread.is_alive() or monotonic() >= deadline:
                    raise RuntimeError("demo server did not start")
                sleep(0.02)
            yield base
        finally:
            server.should_exit = True
            thread.join(timeout=10)
            if thread.is_alive():
                raise RuntimeError("demo server did not stop")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def run_demo() -> None:
    print(
        "Modular LLM Gateway — installed-package demo\nProvider: deterministic fake; no keys or external LLM calls"
    )
    # Keep stdout readable; normal `serve` still emits content-free lifecycle events.
    events = logging.getLogger("gateway.plugin_events")
    was_disabled = events.disabled
    events.disabled = True
    try:
        with TemporaryDirectory(prefix="llmgw-demo-") as directory:
            config = Path(directory) / "plugins.json"
            scenarios = [
                (
                    "Configured plugin order",
                    [
                        "gateway.plugins.add_metadata.MetadataPlugin",
                        "gateway.plugins.uppercase.UppercasePlugin",
                    ],
                    "fake: HELLO",
                    ["metadata", "uppercase"],
                ),
                (
                    "Reversed plugin order",
                    [
                        "gateway.plugins.uppercase.UppercasePlugin",
                        "gateway.plugins.add_metadata.MetadataPlugin",
                    ],
                    "fake: HELLO",
                    ["uppercase", "metadata"],
                ),
                (
                    "Uppercase plugin disabled",
                    ["gateway.plugins.add_metadata.MetadataPlugin"],
                    "fake: hello",
                    ["metadata"],
                ),
                (
                    "A/B plugin: request AAAA, reply BBBB",
                    ["gateway.plugins.demo_ab.ABReplacePlugin"],
                    "BBBB",
                    ["ab_replace"],
                ),
            ]
            for label, plugins, expected, trace in scenarios:
                config.write_text(json.dumps({"plugins": plugins}), encoding="utf-8")
                with running_gateway(config) as base:
                    status, body, request_id = request_json(base, "hello")
                    require(status == 200 and bool(request_id), f"{label}: chat/correlation failed")
                    require(
                        body["choices"][0]["message"]["content"] == expected
                        and body["plugin_trace"] == trace,
                        f"{label}: unexpected plugin result",
                    )
                    if expected == "BBBB":
                        require(
                            "fake: AAAA" in json.dumps(body["plugin_changes"]),
                            "A/B request transformation was not observed",
                        )
                print(f"PASS  {label}")
            config.write_text(
                json.dumps({"plugins": ["gateway.plugins.demo_slow.SlowPlugin"]}), encoding="utf-8"
            )
            with running_gateway(config) as base:
                started = monotonic()
                status, body, request_id = request_json(base, "sleep")
                elapsed = monotonic() - started
                require(
                    status == 504 and bool(request_id) and "SlowPlugin" in body.get("detail", ""),
                    "slow hook did not fail with a named 504",
                )
                require(elapsed < 4, "five-second hook was not interrupted early")
                require(request_json(base)[0] == 200, "health failed after timeout")
                status, body, _ = request_json(base, "hello")
                require(
                    status == 200 and body["choices"][0]["message"]["content"] == "fake: hello",
                    "chat did not recover",
                )
            print(
                f"PASS  Five-second hook stopped early ({elapsed:.2f}s); health and next chat recovered"
            )
        print("All 5 scenarios passed. Next: llmgw serve")
    finally:
        events.disabled = was_disabled
