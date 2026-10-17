import importlib
import json
from pathlib import Path
from typing import Any

from .plugins.base import Plugin


def load_plugins(path: str | Path) -> list[Any]:
    config_path = Path(path)
    data = json.loads(config_path.read_text(encoding="utf-8"))
    names = data.get("plugins")
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise ValueError("config.plugins must be a list of import paths")
    plugins: list[Plugin] = []
    for name in names:
        module_name, separator, class_name = name.rpartition(".")
        if not separator:
            raise ValueError(f"plugin path must contain a class name: {name}")
        try:
            cls = getattr(importlib.import_module(module_name), class_name)
            plugin = cls()
        except Exception as exc:
            raise ValueError(f"could not construct plugin {name}: {exc}") from exc
        if not callable(getattr(plugin, "process_request", None)) or not callable(getattr(plugin, "process_response", None)):
            raise ValueError(f"plugin {name} must define process_request and process_response")
        plugins.append(plugin)
    return plugins
