from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from gateway.main import create_app
from gateway.observability import CHAT_ROUTE, ChatObservability, ObservabilitySettings


@pytest.fixture
def observability_env(monkeypatch):
    monkeypatch.setenv("GATEWAY_OBSERVABILITY_ENABLED", "1")
    monkeypatch.setenv("GATEWAY_OBSERVABILITY_ENVIRONMENT", "staging")
    monkeypatch.setenv("GATEWAY_OBSERVABILITY_ORGANIZATION", "test_org")
    monkeypatch.setenv("GATEWAY_OBSERVABILITY_ENDPOINT", "http://127.0.0.1:5080/api/test_org")
    monkeypatch.setenv("GATEWAY_OBSERVABILITY_AUTHORIZATION", "Basic dGVzdA==")


def test_disabled_does_not_read_destination(monkeypatch):
    monkeypatch.delenv("GATEWAY_OBSERVABILITY_ENABLED", raising=False)
    monkeypatch.setenv("GATEWAY_OBSERVABILITY_ENDPOINT", "unused")
    assert ObservabilitySettings.from_environment() is None


@pytest.mark.parametrize(
    "endpoint",
    ["https://example.invalid/api/other_org", "http://example.invalid/api/test_org"],
)
def test_destination_is_scoped_and_remote_export_requires_tls(
    observability_env, monkeypatch, endpoint
):
    monkeypatch.setenv("GATEWAY_OBSERVABILITY_ENDPOINT", endpoint)
    with pytest.raises(ValueError, match="match its organization"):
        ObservabilitySettings.from_environment()


def test_middleware_records_the_gateway_id_once_for_each_completed_chat(
    observability_env, monkeypatch
):
    observation = Mock()
    monkeypatch.setattr("gateway.main.ChatObservability", lambda settings: observation)
    with TestClient(create_app(config_path="examples/slow-plugins.json")) as client:
        normal = client.post(CHAT_ROUTE, json={"messages": [{"role": "user", "content": "hello"}]})
        invalid = client.post(
            CHAT_ROUTE, json={"messages": []}, headers={"X-Request-ID": "private"}
        )
        slow = client.post(CHAT_ROUTE, json={"messages": [{"role": "user", "content": "sleep"}]})
        assert client.get("/health").status_code == 200

    assert [response.status_code for response in (normal, invalid, slow)] == [200, 422, 504]
    expected = [
        (response.headers["X-Request-ID"], response.status_code)
        for response in (normal, invalid, slow)
    ]
    assert [call.args[:2] for call in observation.record.call_args_list] == expected
    assert invalid.headers["X-Request-ID"] != "private"
    assert all(call.args[2] >= 0 for call in observation.record.call_args_list)
    observation.close.assert_called_once()


def test_signal_uses_one_duration_and_keeps_request_id_out_of_histogram():
    observation = ChatObservability.__new__(ChatObservability)
    observation._histogram = Mock()
    observation._logger = Mock()
    observation.record("generated-id", 504, 311.5)

    assert observation._histogram.record.call_args.args == (
        311.5,
        {"route": CHAT_ROUTE, "outcome": "timeout"},
    )
    assert observation._logger.emit.call_args.kwargs["attributes"] == {
        "request_id": "generated-id",
        "route": CHAT_ROUTE,
        "outcome": "timeout",
        "duration_ms": 311.5,
    }


def test_recording_error_does_not_replace_the_application_outcome(caplog):
    observation = ChatObservability.__new__(ChatObservability)
    observation._histogram = Mock()
    observation._histogram.record.side_effect = RuntimeError("private details")
    observation.record("generated-id", 200, 20.0)

    assert "Could not record the gateway chat observation" in caplog.text
    assert "private details" not in caplog.text
