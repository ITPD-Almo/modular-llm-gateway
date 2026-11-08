import json

import pytest
from fastapi.testclient import TestClient

from gateway.analytics import AnalyticsSettings, GatewayAnalytics
from gateway.main import create_app


@pytest.fixture
def analytics_env(monkeypatch):
    values = {
        "ENABLED": "1",
        "ENVIRONMENT": "staging",
        "SOURCE": "smoke",
        "ORGANIZATION": "staging_org",
        "ENDPOINT": "http://127.0.0.1:5081/api/staging_org",
        "AUTHORIZATION": "Basic c3ludGhldGlj",
    }
    for name, value in values.items():
        monkeypatch.setenv(f"GATEWAY_ANALYTICS_{name}", value)


def test_analytics_disabled_ignores_the_destination(monkeypatch):
    monkeypatch.delenv("GATEWAY_ANALYTICS_ENABLED", raising=False)
    monkeypatch.setenv("GATEWAY_ANALYTICS_ENDPOINT", "unused")
    assert AnalyticsSettings.from_environment() is None


@pytest.mark.parametrize("source", ["smoke", "usability-test", "caller-supplied"])
def test_production_source_cannot_send_synthetic_traffic(analytics_env, monkeypatch, source):
    monkeypatch.setenv("GATEWAY_ANALYTICS_ENVIRONMENT", "production")
    monkeypatch.setenv("GATEWAY_ANALYTICS_SOURCE", source)
    with pytest.raises(ValueError, match="production uses web"):
        AnalyticsSettings.from_environment()


@pytest.mark.parametrize(
    "destination", ["http://example.invalid/api/staging_org", "https://example.invalid/api/wrong"]
)
def test_destination_must_match_the_configured_scope(analytics_env, monkeypatch, destination):
    monkeypatch.setenv("GATEWAY_ANALYTICS_ENDPOINT", destination)
    with pytest.raises(ValueError, match="match its organization"):
        AnalyticsSettings.from_environment()


def test_core_task_records_safe_events_for_success_and_timeout(analytics_env, monkeypatch):
    events = []
    monkeypatch.setattr(GatewayAnalytics, "_export", lambda self, batch: events.extend(batch))
    with TestClient(create_app(config_path="examples/slow-plugins.json")) as client:
        assert client.get("/health").status_code == 200
        assert client.post("/v1/chat/completions", json={"messages": []}).status_code == 422
        normal = client.post(
            "/v1/chat/completions",
            json={"messages": [{"role": "user", "content": "PRIVATE_INPUT"}]},
            headers={"X-Request-ID": "PRIVATE_HEADER", "X-Analytics-Source": "web"},
        )
        failed = client.post(
            "/v1/chat/completions", json={"messages": [{"role": "user", "content": "sleep"}]}
        )
    assert (normal.status_code, failed.status_code) == (200, 504)
    assert [record["event"] for record in events] == [
        "gateway_configuration_used",
        "gateway_chat_started",
        "gateway_chat_finished",
        "gateway_chat_started",
        "gateway_chat_finished",
    ]
    common = {"event", "_timestamp", "environment", "source", "run_id", "plugin_count"}
    assert set(events[0]) == common
    for start, end in [(events[1], events[2]), (events[3], events[4])]:
        assert set(start) == common | {"attempt_id"}
        assert set(end) == common | {"attempt_id", "outcome", "visible_result"}
        assert start["attempt_id"] == end["attempt_id"]
    assert all(event["source"] == "smoke" and event["environment"] == "staging" for event in events)
    assert (events[2]["outcome"], events[2]["visible_result"]) == ("ok", True)
    assert (events[4]["outcome"], events[4]["visible_result"]) == ("timeout", False)
    encoded = json.dumps(events)
    for private in ("PRIVATE_INPUT", "PRIVATE_HEADER", normal.headers["X-Request-ID"]):
        assert private not in encoded
