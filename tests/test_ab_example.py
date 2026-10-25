from pathlib import Path

from fastapi.testclient import TestClient

from gateway.main import create_app

CONFIG = Path(__file__).resolve().parent.parent / "examples" / "ab-plugins.json"


def test_ab_example_replaces_request_and_response_without_core_changes():
    with TestClient(create_app(str(CONFIG))) as client:
        result = client.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": "hello"}]})
    assert result.status_code == 200
    body = result.json()
    assert body["choices"][0]["message"]["content"] == "BBBB"
    assert body["plugin_trace"] == ["metadata", "ab_replace"]
    changes = [(change["plugin"], change["stage"], change["change"]) for change in body["plugin_changes"]]
    assert ("ab_replace", "request", "replaced message content with AAAA") in changes
    assert ("ab_replace", "response", "replaced reply ['fake: AAAA'] with BBBB") in changes
