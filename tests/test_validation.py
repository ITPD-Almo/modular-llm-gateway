import pytest

from gateway.validation import (
    MAX_PAYLOAD_BYTES,
    validate_json,
    validate_request,
    validate_response,
)


def test_validate_request_accepts_a_chat_request() -> None:
    validate_request({"model": "fake", "messages": [{"role": "user", "content": "hi"}]})


@pytest.mark.parametrize(
    "request_body",
    [
        {"messages": []},
        {"messages": [{"role": "user"}]},
        {"messages": [{"role": "user", "content": "hi"}], "model": 1},
        {"messages": [{"role": "user", "content": "hi"}], "plugin_trace": "metadata"},
    ],
)
def test_validate_request_rejects_a_malformed_hook_output(request_body) -> None:
    with pytest.raises(ValueError):
        validate_request(request_body)


def test_validate_response_rejects_a_response_without_choices() -> None:
    validate_response({"choices": [{"message": {"role": "assistant", "content": "ok"}}]})
    with pytest.raises(ValueError):
        validate_response({"choices": []})


def test_validate_json_rejects_a_payload_over_the_worker_limit() -> None:
    with pytest.raises(ValueError):
        validate_json({"content": "x" * MAX_PAYLOAD_BYTES})
