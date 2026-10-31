"""Synthetic provider callable, importable by spawned workers; never uses a key/network."""

from dataclasses import dataclass, field
import json
from time import sleep

from gateway.deepseek import ProviderError


@dataclass(frozen=True)
class SyntheticProvider:
    timeout_ms: int = 2000
    delay: float = 0
    name: str = "synthetic"
    api_key: str = field(default="SYNTHETIC_PROVIDER_SECRET", repr=False)

    def __call__(self, request: dict) -> dict:
        if self.api_key in json.dumps(request):
            raise RuntimeError("credential was passed as plugin data")
        text = request["messages"][-1]["content"]
        if text == "provider-sleep":
            sleep(5)
        if text == "provider-fail":
            raise ProviderError("authentication")
        sleep(self.delay)
        return {"id": "test", "model": "synthetic", "provider": self.name,
                "choices": [{"message": {"role": "assistant", "content": "upstream:" + text}}]}
