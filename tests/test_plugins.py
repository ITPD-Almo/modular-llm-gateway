from gateway.plugins.add_metadata import MetadataPlugin
from gateway.config import load_plugins
from gateway.plugins.base import Plugin
from gateway.plugins.uppercase import UppercasePlugin


class MinimalPlugin:
    def process_request(self, request):
        return request

    def process_response(self, response):
        return response


def test_metadata_plugin_transforms_request_and_response() -> None:
    plugin = MetadataPlugin()
    request = plugin.process_request({"metadata": {}})
    response = plugin.process_response({})
    assert request["metadata"] == {"gateway": "modular"}
    assert request["plugin_trace"] == ["metadata"]
    assert response["plugin_trace"] == ["metadata"]


def test_uppercase_plugin_transforms_message() -> None:
    result = UppercasePlugin().process_request(
        {"messages": [{"role": "user", "content": "hello"}]}
    )
    assert result["messages"][0]["content"] == "HELLO"


def test_load_plugins_and_plugin_protocol(tmp_path) -> None:
    config = tmp_path / "plugins.json"
    config.write_text(
        '{"plugins": ["gateway.plugins.uppercase.UppercasePlugin"]}',
        encoding="utf-8",
    )
    plugins = load_plugins(config)
    assert callable(plugins[0].process_request)
    assert callable(plugins[0].process_response)


def test_plugin_protocol_defines_required_methods() -> None:
    plugin: Plugin = MinimalPlugin()
    assert callable(plugin.process_request)
    assert callable(plugin.process_response)
