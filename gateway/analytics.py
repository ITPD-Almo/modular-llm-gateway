"""Opt-in, bounded product analytics for configured chat use."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from queue import Full, Queue
from threading import Event, Thread
from typing import Any, Callable
from urllib.error import URLError
from urllib.request import Request as UrlRequest, urlopen
from uuid import uuid4


EVENTS = frozenset({"gateway_configuration_used", "gateway_chat_started", "gateway_chat_finished"})
SOURCES = frozenset({"web", "usability-test", "smoke"})
MAX_QUEUE = 256
MAX_EVENT_BYTES = 4096


def _env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AnalyticsSettings:
    enabled: bool = False
    endpoint: str | None = None
    source: str = "web"
    timeout_seconds: float = 0.5

    @classmethod
    def from_environment(cls) -> "AnalyticsSettings":
        source = os.getenv("GATEWAY_ANALYTICS_SOURCE", "web")
        if source not in SOURCES:
            source = "web"
        try:
            timeout = min(max(float(os.getenv("GATEWAY_ANALYTICS_TIMEOUT_SECONDS", "0.5")), 0.05), 2.0)
        except ValueError:
            timeout = 0.5
        endpoint = os.getenv("GATEWAY_ANALYTICS_ENDPOINT") or None
        return cls(_env_bool("GATEWAY_ANALYTICS_ENABLED"), endpoint, source, timeout)


class AnalyticsClient:
    """Fire-and-forget exporter. Export failures never affect a request."""

    def __init__(self, settings: AnalyticsSettings | None = None, *, sink: Callable[[dict[str, Any]], None] | None = None):
        self.settings = settings or AnalyticsSettings.from_environment()
        self._sink = sink
        self._queue: Queue[dict[str, Any] | None] = Queue(maxsize=MAX_QUEUE)
        self._worker: Thread | None = None
        if self.settings.enabled and (self.settings.endpoint or self._sink):
            self._worker = Thread(target=self._export_loop, name="gateway-analytics", daemon=True)
            self._worker.start()

    def close(self) -> None:
        if self._worker is None:
            return
        try:
            self._queue.put_nowait(None)
        except Full:
            pass
        self._worker.join(timeout=1.0)

    def emit(self, event: str, **fields: Any) -> None:
        if not self.settings.enabled or event not in EVENTS:
            return
        record = {"schema_version": 1, "event": event, "source": self.settings.source, **fields}
        encoded = json.dumps(record, separators=(",", ":"), allow_nan=False).encode("utf-8")
        if len(encoded) > MAX_EVENT_BYTES:
            return
        try:
            self._queue.put_nowait(record)
        except (Full, ValueError, TypeError):
            # Analytics is deliberately lossy and must never back-pressure the gateway.
            return

    def _export_loop(self) -> None:
        while True:
            try:
                record = self._queue.get(timeout=0.1)
            except Exception:
                continue
            if record is None:
                return
            try:
                if self._sink is not None:
                    self._sink(record)
                elif self.settings.endpoint:
                    body = json.dumps(record, separators=(",", ":")).encode("utf-8")
                    request = UrlRequest(self.settings.endpoint, data=body, headers={"Content-Type": "application/json"}, method="POST")
                    with urlopen(request, timeout=self.settings.timeout_seconds):
                        pass
            except (OSError, URLError, ValueError, TypeError):
                continue


class AnalyticsSession:
    """Per-application state used to identify first real use of a configuration."""

    def __init__(self, client: AnalyticsClient, plugin_count: int):
        self.client = client
        self.plugin_count = plugin_count
        self.configuration_run_id = uuid4().hex
        self.configuration_observed = False

    def observe_configuration(self) -> None:
        if self.configuration_observed:
            return
        self.configuration_observed = True
        self.client.emit(
            "gateway_configuration_used",
            run_id=self.configuration_run_id,
            configured_plugin_count=self.plugin_count,
        )

    def started(self, run_id: str) -> None:
        self.observe_configuration()
        self.client.emit("gateway_chat_started", run_id=run_id)

    def finished(self, run_id: str, *, status_code: int, duration_ms: float, response: dict[str, Any] | None) -> None:
        self.client.emit(
            "gateway_chat_finished",
            run_id=run_id,
            http_success=status_code < 400,
            status_code=status_code,
            configured_plugin_result_visible=bool(response and response.get("plugin_changes")),
            duration_ms=round(min(max(duration_ms, 0.0), 600000.0), 3),
        )

