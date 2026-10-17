from typing import Any


class UppercasePlugin:
    def process_request(self, request: dict[str, Any]) -> dict[str, Any]:
        updated = dict(request)
        messages = [dict(message) for message in updated.get("messages", [])]
        for message in messages:
            if isinstance(message.get("content"), str):
                message["content"] = message["content"].upper()
        updated["messages"] = messages
        updated["plugin_trace"] = list(updated.get("plugin_trace", [])) + ["uppercase"]
        return updated

    def process_response(self, response: dict[str, Any]) -> dict[str, Any]:
        updated = dict(response)
        updated["plugin_trace"] = list(updated.get("plugin_trace", [])) + ["uppercase"]
        return updated
