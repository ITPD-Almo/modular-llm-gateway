"""Export bounded chat outcomes to the configured OpenObserve organization."""

import logging
import os
import re
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from opentelemetry.context import Context
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import Histogram, MeterProvider
from opentelemetry.sdk.metrics.export import AggregationTemporality, PeriodicExportingMetricReader
from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, View
from opentelemetry.sdk.resources import Resource

CHAT_ROUTE = "/v1/chat/completions"
LOG_STREAM = "gateway_requests"
HISTOGRAM = "gateway_chat_duration"
BUCKETS_MS = (5, 10, 25, 50, 100, 150, 250, 350, 500, 750, 1000, 2500, 5000, 15000, 60000)
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class ObservabilitySettings:
    endpoint: str
    environment: str
    authorization: str = field(repr=False)
    ca_file: str | None = None

    @classmethod
    def from_environment(cls) -> "ObservabilitySettings | None":
        enabled = os.getenv("GATEWAY_OBSERVABILITY_ENABLED", "0")
        if enabled == "0":
            return None
        if enabled != "1":
            raise ValueError("GATEWAY_OBSERVABILITY_ENABLED must be 0 or 1")
        environment = os.getenv("GATEWAY_OBSERVABILITY_ENVIRONMENT", "")
        if environment not in {"staging", "production"}:
            raise ValueError("GATEWAY_OBSERVABILITY_ENVIRONMENT must be staging or production")
        organization = os.getenv("GATEWAY_OBSERVABILITY_ORGANIZATION", "")
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", organization) or organization in {
            "default",
            "_meta",
        }:
            raise ValueError(
                "GATEWAY_OBSERVABILITY_ORGANIZATION must name a dedicated organization"
            )
        endpoint = os.getenv("GATEWAY_OBSERVABILITY_ENDPOINT", "").rstrip("/")
        try:
            url = urlsplit(endpoint)
            url.port
            valid = (
                bool(url.hostname)
                and url.username is None
                and not url.query
                and not url.fragment
                and url.path == f"/api/{organization}"
                and (
                    url.scheme == "https"
                    or (url.scheme == "http" and url.hostname in {"127.0.0.1", "::1"})
                )
            )
        except ValueError:
            valid = False
        if not valid:
            raise ValueError(
                "observability endpoint must be HTTPS or loopback HTTP and match its organization"
            )
        authorization = os.getenv("GATEWAY_OBSERVABILITY_AUTHORIZATION", "")
        if not re.fullmatch(r"Basic [A-Za-z0-9+/]+={0,2}", authorization):
            raise ValueError("GATEWAY_OBSERVABILITY_AUTHORIZATION must contain an HTTP Basic value")
        return cls(endpoint, environment, authorization, os.getenv("GATEWAY_OBSERVABILITY_CA_FILE"))


class ChatObservability:
    def __init__(self, settings: ObservabilitySettings):
        resource = Resource(
            {"service.name": "modular-llm-gateway", "environment": settings.environment}
        )
        headers = {"Authorization": settings.authorization}
        logs = OTLPLogExporter(
            endpoint=f"{settings.endpoint}/v1/logs",
            headers={**headers, "stream-name": LOG_STREAM},
            certificate_file=settings.ca_file,
            timeout=2,
        )
        metrics = OTLPMetricExporter(
            endpoint=f"{settings.endpoint}/v1/metrics",
            headers=headers,
            certificate_file=settings.ca_file,
            timeout=2,
            preferred_temporality={Histogram: AggregationTemporality.DELTA},
        )
        self._logs = LoggerProvider(resource=resource, shutdown_on_exit=False)
        self._logs.add_log_record_processor(
            BatchLogRecordProcessor(
                logs, schedule_delay_millis=500, max_queue_size=512, max_export_batch_size=64
            )
        )
        self._metrics = MeterProvider(
            resource=resource,
            metric_readers=[PeriodicExportingMetricReader(metrics, export_interval_millis=2000)],
            views=[
                View(
                    instrument_name=HISTOGRAM,
                    aggregation=ExplicitBucketHistogramAggregation(
                        BUCKETS_MS, record_min_max=False
                    ),
                )
            ],
            shutdown_on_exit=False,
        )
        self._logger = self._logs.get_logger(__name__)
        self._histogram = self._metrics.get_meter(__name__).create_histogram(HISTOGRAM, unit="ms")

    def record(self, request_id: str, status_code: int, duration_ms: float) -> None:
        if status_code == 504:
            outcome = "timeout"
        elif status_code >= 500:
            outcome = "server_error"
        elif status_code >= 400:
            outcome = "client_error"
        else:
            outcome = "ok"
        labels = {"route": CHAT_ROUTE, "outcome": outcome}
        try:
            self._histogram.record(duration_ms, labels, context=Context())
            self._logger.emit(
                body="gateway_chat_finished",
                attributes={**labels, "request_id": request_id, "duration_ms": duration_ms},
                context=Context(),
            )
        except Exception:
            LOGGER.warning("Could not record the gateway chat observation")

    def close(self) -> None:
        self._metrics.shutdown(timeout_millis=3000)
        self._logs.shutdown()
