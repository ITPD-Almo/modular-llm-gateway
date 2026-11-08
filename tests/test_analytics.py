import json
import time

from fastapi.testclient import TestClient

from gateway.analytics import AnalyticsClient, AnalyticsSettings
from gateway.main import create_app


def test_analytics_uses_allowlisted_fields_and_first_configuration_use():
    records = []
    client = AnalyticsClient(AnalyticsSettings(enabled=True, source="smoke"), sink=records.append)
    with TestClient(create_app(analytics_client=client)) as http:
        assert http.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": "hello"}]}).status_code == 200
        assert http.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": "again"}]}).status_code == 200
    client.close()
    time.sleep(0.01)
    assert [record["event"] for record in records] == [
        "gateway_configuration_used", "gateway_chat_started", "gateway_chat_finished",
        "gateway_chat_started", "gateway_chat_finished",
    ]
    assert all(set(record) <= {"schema_version", "event", "source", "run_id", "configured_plugin_count", "http_success", "status_code", "configured_plugin_result_visible", "duration_ms"} for record in records)
    assert all("content" not in json.dumps(record) for record in records)
    assert records[0]["source"] == "smoke"


def test_analytics_export_failure_does_not_change_http_flow():
    def broken_sink(record):
        raise OSError("synthetic exporter outage")

    client = AnalyticsClient(AnalyticsSettings(enabled=True, source="web"), sink=broken_sink)
    with TestClient(create_app(analytics_client=client)) as http:
        response = http.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": "hello"}]})
    client.close()
    assert response.status_code == 200


def test_analytics_source_guard_defaults_unknown_values_to_web(monkeypatch):
    monkeypatch.setenv("GATEWAY_ANALYTICS_SOURCE", "production-secret")
    assert AnalyticsSettings.from_environment().source == "web"
