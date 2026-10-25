"""Demo plugin that hangs its request hook when the last message is exactly "sleep"."""

import time
from typing import Any


class SlowPlugin:
    def process_request(self, request: dict[str, Any]) -> dict[str, Any]:
        if request["messages"][-1]["content"] == "sleep":
            time.sleep(5)
        return request

    def process_response(self, response: dict[str, Any]) -> dict[str, Any]:
        return response
