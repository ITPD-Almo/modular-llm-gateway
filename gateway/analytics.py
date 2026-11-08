"""Export the allowlisted gateway usage events to the selected analytics scope."""

import http.client
import json
import logging
import os
import re
import ssl
from dataclasses import dataclass, field
from queue import Empty, Full, Queue
from threading import Event, Lock, Thread
from time import time_ns
from urllib.parse import SplitResult, urlsplit
from uuid import uuid4

LOGGER = logging.getLogger(__name__)
STREAM = "gateway_usage"
SOURCES = {"web", "usability-test", "smoke"}


@dataclass(frozen=True)
class AnalyticsSettings:
    endpoint: SplitResult
    environment: str
    source: str
    authorization: str = field(repr=False)
    ca_file: str | None = None

    @classmethod
    def from_environment(cls) -> "AnalyticsSettings | None":
        enabled = os.getenv("GATEWAY_ANALYTICS_ENABLED", "0")
        if enabled == "0":
            return None
        if enabled != "1":
            raise ValueError("GATEWAY_ANALYTICS_ENABLED must be 0 or 1")
        environment = os.getenv("GATEWAY_ANALYTICS_ENVIRONMENT", "")
        if environment not in {"staging", "production"}:
            raise ValueError("GATEWAY_ANALYTICS_ENVIRONMENT must be staging or production")
        source = os.getenv("GATEWAY_ANALYTICS_SOURCE", "web")
        if source not in SOURCES or (environment == "production" and source != "web"):
            raise ValueError(
                "analytics source must be web, usability-test or smoke; production uses web"
            )
        organization = os.getenv("GATEWAY_ANALYTICS_ORGANIZATION", "")
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", organization) or organization in {
            "default",
            "_meta",
        }:
            raise ValueError(
                "GATEWAY_ANALYTICS_ORGANIZATION must identify a dedicated organization"
            )
        try:
            endpoint = urlsplit(os.getenv("GATEWAY_ANALYTICS_ENDPOINT", "").rstrip("/"))
            endpoint.port
            valid = (
                bool(endpoint.hostname)
                and endpoint.username is None
                and not endpoint.query
                and not endpoint.fragment
                and endpoint.path == f"/api/{organization}"
                and (
                    endpoint.scheme == "https"
                    or (endpoint.scheme == "http" and endpoint.hostname in {"127.0.0.1", "::1"})
                )
            )
        except ValueError:
            valid = False
        if not valid:
            raise ValueError(
                "analytics endpoint must be HTTPS or loopback HTTP and match its organization"
            )
        authorization = os.getenv("GATEWAY_ANALYTICS_AUTHORIZATION", "")
        if not re.fullmatch(r"Basic [A-Za-z0-9+/]+={0,2}", authorization):
            raise ValueError("GATEWAY_ANALYTICS_AUTHORIZATION must contain an HTTP Basic value")
        return cls(
            endpoint, environment, source, authorization, os.getenv("GATEWAY_ANALYTICS_CA_FILE")
        )


class GatewayAnalytics:
    def __init__(self, settings: AnalyticsSettings, plugin_count: int):
        self._settings = settings
        self._tls = (
            ssl.create_default_context(cafile=settings.ca_file)
            if settings.endpoint.scheme == "https"
            else None
        )
        self._common: dict[str, str | int | bool] = {
            "source": settings.source,
            "environment": settings.environment,
            "run_id": uuid4().hex,
            "plugin_count": plugin_count,
        }
        self._first_use = Lock()
        self._used = False
        self._events: Queue[dict[str, str | int | bool]] = Queue(maxsize=256)
        self._stop = Event()
        self._worker = Thread(target=self._run, name="gateway-analytics", daemon=True)
        self._worker.start()

    def _add(self, event: str, **fields: str | int | bool) -> None:
        try:
            self._events.put_nowait(
                {**self._common, "event": event, "_timestamp": time_ns() // 1000, **fields}
            )
        except Full:
            pass

    def started(self) -> str:
        with self._first_use:
            if not self._used:
                self._add("gateway_configuration_used")
                self._used = True
        attempt = uuid4().hex
        self._add("gateway_chat_started", attempt_id=attempt)
        return attempt

    def finished(self, attempt: str, status: int, visible_result: bool) -> None:
        if status == 504:
            outcome = "timeout"
        elif status >= 500:
            outcome = "server_error"
        elif status >= 400:
            outcome = "client_error"
        else:
            outcome = "ok"
        self._add(
            "gateway_chat_finished",
            attempt_id=attempt,
            outcome=outcome,
            visible_result=visible_result,
        )

    def close(self) -> None:
        self._stop.set()
        self._worker.join(timeout=2.5)

    def _run(self) -> None:
        unavailable = False
        while True:
            stopping = self._stop.wait(0.2)
            batch: list[dict[str, str | int | bool]] = []
            while len(batch) < 32:
                try:
                    batch.append(self._events.get_nowait())
                except Empty:
                    break
            if batch:
                try:
                    self._export(batch)
                    unavailable = False
                except Exception:
                    if not unavailable:
                        LOGGER.warning("Analytics export unavailable; dropping usage events")
                    unavailable = True
            if stopping:
                return

    def _export(self, events: list[dict[str, str | int | bool]]) -> None:
        endpoint = self._settings.endpoint
        assert endpoint.hostname is not None
        if self._tls is None:
            connection = http.client.HTTPConnection(endpoint.hostname, endpoint.port, timeout=2)
        else:
            connection = http.client.HTTPSConnection(
                endpoint.hostname, endpoint.port, timeout=2, context=self._tls
            )
        try:
            connection.request(
                "POST",
                f"{endpoint.path}/{STREAM}/_json",
                json.dumps(events).encode(),
                {"Authorization": self._settings.authorization, "Content-Type": "application/json"},
            )
            response = connection.getresponse()
            if response.status != 200:
                raise ValueError("analytics destination rejected the batch")
            receipt = json.loads(response.read(16385))
            if receipt != {
                "code": 200,
                "status": [{"name": STREAM, "successful": len(events), "failed": 0}],
            }:
                raise ValueError("analytics destination did not acknowledge the batch")
        finally:
            connection.close()
