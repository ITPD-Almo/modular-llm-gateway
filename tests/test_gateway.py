import json

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
    assert body["choices"][0]["message"]["content"] == "fake: HELLO"


def test_bad_plugin_configuration_fails_at_startup(tmp_path):
    config = tmp_path / "plugins.json"
    config.write_text(json.dumps({"plugins": ["missing.Plugin"]}), encoding="utf-8")
    try:
        create_app(str(config))
    except RuntimeError as exc:
        assert "could not load plugins" in str(exc)
    else:
        raise AssertionError("invalid plugin configuration should fail startup")
