from typing import Any, Protocol


class Plugin(Protocol):
    """A plugin may transform the request and/or provider response."""

    def process_request(self, request: dict[str, Any]) -> dict[str, Any]: ...

    def process_response(self, response: dict[str, Any]) -> dict[str, Any]: ...
