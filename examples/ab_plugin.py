"""Third-party plugin example: A text into the provider, B text back to the client."""

from typing import Any

REQUEST_TEXT = "AAAA"
RESPONSE_TEXT = "BBBB"


class ABReplacePlugin:
    def process_request(self, request: dict[str, Any]) -> dict[str, Any]:
        updated = dict(request)
        updated["messages"] = [
            dict(message, content=REQUEST_TEXT) for message in updated.get("messages", [])
        ]
        updated["plugin_trace"] = list(updated.get("plugin_trace", [])) + ["ab_replace"]
        updated["plugin_changes"] = list(updated.get("plugin_changes", [])) + [
            {
                "plugin": "ab_replace",
                "stage": "request",
                "change": f"replaced message content with {REQUEST_TEXT}",
            }
        ]
        return updated

    def process_response(self, response: dict[str, Any]) -> dict[str, Any]:
        updated = dict(response)
        choices = [
            dict(choice, message=dict(choice["message"])) for choice in updated.get("choices", [])
        ]
        replaced = [choice["message"]["content"] for choice in choices]
        for choice in choices:
            choice["message"]["content"] = RESPONSE_TEXT
        updated["choices"] = choices
        updated["plugin_trace"] = list(updated.get("plugin_trace", [])) + ["ab_replace"]
        updated["plugin_changes"] = list(updated.get("plugin_changes", [])) + [
            {
                "plugin": "ab_replace",
                "stage": "response",
                "change": f"replaced reply {replaced!r} with {RESPONSE_TEXT}",
            }
        ]
        return updated
