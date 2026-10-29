"""Fixed-origin DeepSeek transport; credentials never enter plugin dictionaries."""

from dataclasses import dataclass, field
import http.client
import json
from time import monotonic
from typing import Any

from .credentials import Credentials
from .validation import MAX_PAYLOAD_BYTES, validate_response

HOST = "api.deepseek.com"


class ProviderError(Exception):
    """A fixed reason, never an upstream body, URL, key or exception string."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


def authenticated_json(credentials: Credentials, path: str, payload: dict | None = None) -> dict:
    if path not in ("/models", "/chat/completions"):
        raise ProviderError("invalid_response")
    connection = http.client.HTTPSConnection(HOST, timeout=10)
    deadline = monotonic() + 40
    try:
        data = None if payload is None else json.dumps(payload, allow_nan=False).encode("utf-8")
        connection.request("GET" if data is None else "POST", path, body=data,
                           headers={"Authorization": "Bearer " + credentials.api_key, "Content-Type": "application/json"})
        response = connection.getresponse()
        if response.status != 200:
            reason = {401: "authentication", 403: "authentication", 402: "balance", 429: "rate_limit"}.get(response.status, "unavailable")
            raise ProviderError(reason)
        content = bytearray()
        while True:
            remaining = deadline - monotonic()
            if remaining <= 0:
                raise ProviderError("timeout")
            if connection.sock is not None:
                connection.sock.settimeout(min(remaining, 10))
            chunk = response.read1(min(65536, MAX_PAYLOAD_BYTES + 1 - len(content)))
            if not chunk:
                break
            content.extend(chunk)
            if len(content) > MAX_PAYLOAD_BYTES:
                raise ProviderError("invalid_response")
        result = json.loads(content)
        if not isinstance(result, dict):
            raise ProviderError("invalid_response")
        return result
    except ProviderError:
        raise
    except TimeoutError:
        raise ProviderError("timeout") from None
    except (OSError, ValueError, http.client.HTTPException):
        raise ProviderError("unavailable") from None
    finally:
        connection.close()


def available_models(credentials: Credentials) -> list[str]:
    result = authenticated_json(credentials, "/models")
    rows = result.get("data")
    if not isinstance(rows, list):
        raise ProviderError("invalid_response")
    names = []
    for row in rows[:64]:
        if isinstance(row, dict) and isinstance(row.get("id"), str):
            name = row["id"]
            if name and credentials.api_key not in name and len(name) <= 128 and all(c.isascii() and (c.isalnum() or c in "._-") for c in name):
                names.append(name)
    if not names:
        raise ProviderError("invalid_response")
    return sorted(set(names), key=lambda name: (name != "deepseek-flash", name))


ERROR_MESSAGES = {
    "authentication": "DeepSeek rejected the key. Run llmgw setup to replace it.",
    "balance": "DeepSeek reports insufficient balance. Check your DeepSeek account.",
    "rate_limit": "DeepSeek is rate limiting requests. Wait and try again.",
    "timeout": "DeepSeek did not respond in time. No automatic retry was made.",
    "invalid_response": "DeepSeek returned an unsupported response.",
    "unavailable": "Cannot reach DeepSeek. Check internet access and try again.",
}


@dataclass(frozen=True)
class DeepSeekProvider:
    credentials: Credentials = field(repr=False)
    name: str = field(default="deepseek", init=False)
    timeout_ms: int = field(default=45000, init=False)

    def __call__(self, request: dict[str, Any]) -> dict[str, Any]:
        messages = request.get("messages", [])
        if not messages or any(m.get("role") not in ("system", "user", "assistant") or not isinstance(m.get("content"), str) for m in messages):
            raise ProviderError("invalid_response")
        # No metadata, diagnostics, plugin state or caller-selected endpoint/model
        # is forwarded. Authorization belongs only to the transport header.
        body = {"model": self.credentials.model, "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
                "stream": False, "max_tokens": 128, "thinking": {"type": "disabled"}}
        result = authenticated_json(self.credentials, "/chat/completions", body)
        try:
            choices = [{"message": {"role": "assistant", "content": c["message"]["content"]}} for c in result["choices"]]
            response = {"id": "deepseek-response", "model": self.credentials.model, "provider": self.name, "choices": choices}
            validate_response(response)
            if self.credentials.api_key in json.dumps(response):
                raise ProviderError("invalid_response")
            return response
        except (KeyError, TypeError, ValueError, RecursionError):
            raise ProviderError("invalid_response") from None
