from typing import Any


class MetadataPlugin:
    def process_request(self, request: dict[str, Any]) -> dict[str, Any]:
        updated = dict(request)
        updated["plugin_trace"] = list(updated.get("plugin_trace", [])) + ["metadata"]
        updated["metadata"] = {**updated.get("metadata", {}), "gateway": "modular"}
        updated["plugin_changes"] = list(updated.get("plugin_changes", [])) + [{"plugin": "metadata", "stage": "request", "change": "added metadata.gateway=modular"}]
        return updated

    def process_response(self, response: dict[str, Any]) -> dict[str, Any]:
        updated = dict(response)
        updated["plugin_trace"] = list(updated.get("plugin_trace", [])) + ["metadata"]
        updated["plugin_changes"] = list(updated.get("plugin_changes", [])) + [{"plugin": "metadata", "stage": "response", "change": "recorded metadata transformation"}]
        return updated
