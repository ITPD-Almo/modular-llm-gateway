import json
import pytest

from fastapi.testclient import TestClient

from gateway.main import create_app


def test_plugins_run_in_config_order(tmp_path):
    config = tmp_path / "plugins.json"
    config.write_text(json.dumps({"plugins": [
        "gateway.plugins.add_metadata.MetadataPlugin",
        "gateway.plugins.uppercase.UppercasePlugin",
    ]}), encoding="utf-8")
    client = TestClient(create_app(str(config)))
    result = client.post("/v1/chat/completions", json={"model": "fake", "messages": [{"role": "user", "content": "hello"}]})
    assert result.status_code == 200
    body = result.json()
    assert body["plugin_trace"] == ["metadata", "uppercase"]
    assert {change["plugin"] for change in body["plugin_changes"]} == {"metadata", "uppercase"}
    assert body["choices"][0]["message"]["content"] == "fake: HELLO"


def test_order_and_plugin_selection_change_result(tmp_path):
    def run(names):
        config = tmp_path / "plugins.json"
        config.write_text(json.dumps({"plugins": names}), encoding="utf-8")
        return TestClient(create_app(str(config))).post(
            "/v1/chat/completions",
            json={"messages": [{"role": "user", "content": "hello"}]},
        ).json()

    reordered = run([
        "gateway.plugins.uppercase.UppercasePlugin",
        "gateway.plugins.add_metadata.MetadataPlugin",
    ])
    without_uppercase = run(["gateway.plugins.add_metadata.MetadataPlugin"])
    assert reordered["plugin_trace"] == ["uppercase", "metadata"]
    assert without_uppercase["choices"][0]["message"]["content"] == "fake: hello"
    assert reordered["choices"][0]["message"]["content"] != without_uppercase["choices"][0]["message"]["content"]


def test_bad_plugin_configuration_fails_at_startup(tmp_path):
    config = tmp_path / "plugins.json"
    config.write_text(json.dumps({"plugins": ["missing.Plugin"]}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="could not load plugins"):
        create_app(str(config))


def test_invalid_request_returns_422():
    assert TestClient(create_app()).post("/v1/chat/completions", json={"messages": "hi"}).status_code == 422


class FailingPlugin:
    def process_request(self, request):
        raise RuntimeError("boom")

    def process_response(self, response):
        return response


def test_plugin_failure_returns_named_error(tmp_path):
    config = tmp_path / "plugins.json"
    config.write_text(json.dumps({"plugins": ["tests.test_gateway.FailingPlugin"]}), encoding="utf-8")
    client = TestClient(create_app(str(config)))
    response = client.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": "hello"}]})
    assert response.status_code == 500
    assert "FailingPlugin" in response.json()["detail"]
