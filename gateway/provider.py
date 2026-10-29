from typing import Any, Protocol


class ChatProvider(Protocol):
    name: str
    timeout_ms: int

    def __call__(self, request: dict[str, Any]) -> dict[str, Any]: ...


def fake_provider(request: dict[str, Any]) -> dict[str, Any]:
    messages = request.get("messages", [])
    prompt = messages[-1].get("content", "") if messages else ""
    return {
        "id": "fake-response",
        "model": request.get("model", "fake"),
        "provider": "fake",
        "choices": [{"message": {"role": "assistant", "content": f"fake: {prompt}"}}],
    }
