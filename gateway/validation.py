"""Validate hook outputs before the next stage and keep worker messages bounded."""

import json
from typing import Any


MAX_PAYLOAD_BYTES = 1024 * 1024


def validate_json(value: dict[str, Any]) -> None:
    if len(json.dumps(value, allow_nan=False).encode("utf-8")) > MAX_PAYLOAD_BYTES:
        raise ValueError("payload exceeds the worker limit")


def _validate_effects(value: dict[str, Any]) -> None:
    if "plugin_trace" in value and (
        not isinstance(value["plugin_trace"], list)
        or not all(isinstance(item, str) for item in value["plugin_trace"])
    ):
        raise ValueError("plugin_trace must be a list of strings")
    if "plugin_changes" in value and (
        not isinstance(value["plugin_changes"], list)
        or not all(isinstance(item, dict) for item in value["plugin_changes"])
    ):
        raise ValueError("plugin_changes must be a list of objects")


def validate_request(value: dict[str, Any]) -> None:
    messages = value.get("messages")
    if not isinstance(messages, list) or not messages or not all(
        isinstance(message, dict) and isinstance(message.get("role"), str) and isinstance(message.get("content"), str)
        for message in messages
    ):
        raise ValueError("messages must contain role and content strings")
    if "model" in value and not isinstance(value["model"], str):
        raise ValueError("model must be a string")
    if "metadata" in value and not isinstance(value["metadata"], dict):
        raise ValueError("metadata must be an object")
    _validate_effects(value)
    validate_json(value)


def validate_response(value: dict[str, Any]) -> None:
    choices = value.get("choices")
    if not isinstance(choices, list) or not choices or not all(
        isinstance(choice, dict) and isinstance(choice.get("message"), dict)
        and isinstance(choice["message"].get("role"), str) and isinstance(choice["message"].get("content"), str)
        for choice in choices
    ):
        raise ValueError("choices must contain role and content strings")
    _validate_effects(value)
    validate_json(value)
