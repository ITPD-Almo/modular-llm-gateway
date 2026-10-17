import importlib
import json
from pathlib import Path
from typing import Any


def load_plugins(path: str | Path) -> list[Any]:
    config_path = Path(path)
    data = json.loads(config_path.read_text(encoding="utf-8"))
    names = data.get("plugins")
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise ValueError("config.plugins must be a list of import paths")
    plugins = []
    for name in names:
        module_name, separator, class_name = name.rpartition(".")
        if not separator:
            raise ValueError(f"plugin path must contain a class name: {name}")
        cls = getattr(importlib.import_module(module_name), class_name)
        plugins.append(cls())
    return plugins
