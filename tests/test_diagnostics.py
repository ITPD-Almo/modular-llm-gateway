import json
import logging
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from gateway.diagnostics import LOGGER, HookContext, emit_hook_event, new_request_id
from gateway.main import create_app

PROMPT_SECRET = "DO_NOT_LOG_PROMPT_123"
METADATA_SECRET = "DO_NOT_LOG_METADATA_456"
EXCEPTION_SECRET = "DO_NOT_LOG_EXCEPTION_789"
RESPONSE_SECRET = "DO_NOT_LOG_RESPONSE_012"


class RequestFailure:
    def process_request(self, request):
        raise RuntimeError(EXCEPTION_SECRET)

    def process_response(self, response):
        return response


class ResponseFailure:
    def process_request(self, request):
        return request

    def process_response(self, response):
        response["choices"][0]["message"]["content"] = RESPONSE_SECRET
        raise RuntimeError(EXCEPTION_SECRET)


class InvalidOutput:
    def process_request(self, request):
        return None

    def process_response(self, response):
        return response


def configuration(tmp_path, names):
    path = tmp_path / "plugins.json"
    path.write_text(json.dumps({"plugins": names}))
    return str(path)


def events(caplog):
    return [
        json.loads(record.getMessage()) for record in caplog.records if record.name == LOGGER.name
    ]


def test_success_events_have_one_safe_schema_and_follow_hook_order(caplog):
    caplog.set_level(logging.INFO, logger=LOGGER.name)
    client = TestClient(create_app())
    result = client.post(
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": PROMPT_SECRET}],
            "metadata": {"secret": METADATA_SECRET},
        },
        headers={"X-Request-ID": "untrusted-client-value"},
    )
    assert result.status_code == 200
    request_id = result.headers["X-Request-ID"]
    assert UUID(hex=request_id).version == 4
    assert result.json()["choices"][0]["message"]["content"] == f"fake: {PROMPT_SECRET}"
    assert result.json()["plugin_trace"] == ["metadata", "uppercase"]
    records = events(caplog)
    assert [(r["plugin"], r["stage"], r["event"]) for r in records] == [
        (plugin, stage, event)
        for stage in ("request", "response")
        for plugin in ("MetadataPlugin", "UppercasePlugin")
        for event in ("started", "completed")
    ]
    assert all(
        set(r)
        == {"schema_version", "event", "request_id", "plugin", "stage", "elapsed_ms", "reason"}
        for r in records
    )
    assert all(r["request_id"] == request_id and r["elapsed_ms"] >= 0 for r in records)
    encoded = json.dumps(records)
    assert PROMPT_SECRET not in encoded and METADATA_SECRET not in encoded
    assert "untrusted-client-value" not in encoded
    assert all(r.exc_info is None for r in caplog.records if r.name == LOGGER.name)
    another = client.post(
        "/v1/chat/completions", json={"messages": [{"role": "user", "content": "hello"}]}
    )
    assert another.headers["X-Request-ID"] != request_id


@pytest.mark.parametrize(
    "name,stage", [("RequestFailure", "request"), ("ResponseFailure", "response")]
)
def test_failed_hook_is_identified_without_logging_content(tmp_path, caplog, name, stage):
    caplog.set_level(logging.INFO, logger=LOGGER.name)
    client = TestClient(create_app(configuration(tmp_path, [f"tests.test_diagnostics.{name}"])))
    result = client.post(
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": PROMPT_SECRET}],
            "metadata": {"private": METADATA_SECRET},
        },
    )
    assert result.status_code == 500
    assert result.json()["detail"] == f"plugin {name} failed during {stage} processing"
    records = events(caplog)
    assert records[-1]["event"] == "failed" and records[-1]["reason"] == "plugin_exception"
    assert records[-1]["plugin"] == name and records[-1]["stage"] == stage
    assert {r["request_id"] for r in records} == {result.headers["X-Request-ID"]}
    for secret in (PROMPT_SECRET, METADATA_SECRET, EXCEPTION_SECRET, RESPONSE_SECRET):
        assert secret not in json.dumps(records) + result.text
    assert client.get("/health").status_code == 200


def test_non_dictionary_hook_result_is_a_named_failure(tmp_path, caplog):
    caplog.set_level(logging.INFO, logger=LOGGER.name)
    client = TestClient(
        create_app(configuration(tmp_path, ["tests.test_diagnostics.InvalidOutput"]))
    )
    result = client.post(
        "/v1/chat/completions", json={"messages": [{"role": "user", "content": "hello"}]}
    )
    assert result.status_code == 500
    assert "InvalidOutput" in result.json()["detail"]
    assert events(caplog)[-1]["reason"] == "invalid_output"


def test_event_helper_rejects_arbitrary_exception_reason(caplog):
    with pytest.raises(ValueError, match="unknown diagnostic"):
        emit_hook_event(
            HookContext(new_request_id(), "ExamplePlugin", "request"),
            "failed",
            reason=EXCEPTION_SECRET,
        )
    assert EXCEPTION_SECRET not in caplog.text


@pytest.mark.parametrize(
    "body",
    [
        '{"messages":"PRIVATE_INVALID_MESSAGES"}',
        '{"messages":[{"role":"user","content":{"private":"PRIVATE_INVALID_CONTENT"}}]}',
        '{"messages":[],"metadata":"PRIVATE_INVALID_METADATA"}',
        '{"messages": PRIVATE_INVALID_JSON}',
        '{"messages":[{"content":"PRIVATE_MISSING_ROLE"}]}',
    ],
)
def test_invalid_chat_is_correlated_without_reflecting_input(caplog, body):
    with TestClient(create_app()) as client:
        response = client.post(
            "/v1/chat/completions",
            content=body,
            headers={"Content-Type": "application/json", "X-Request-ID": "PRIVATE_CLIENT_ID"},
        )
        assert response.status_code == 422
        assert response.json() == {"detail": "invalid chat request"}
        assert UUID(hex=response.headers["X-Request-ID"]).version == 4
        assert "PRIVATE_" not in response.text + str(response.headers) + caplog.text
        assert events(caplog) == []
        healthy = client.post(
            "/v1/chat/completions", json={"messages": [{"role": "user", "content": "hello"}]}
        )
        assert healthy.status_code == 200
        assert healthy.headers["X-Request-ID"] != response.headers["X-Request-ID"]
