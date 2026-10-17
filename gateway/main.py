import os
from typing import Any

from fastapi import FastAPI, HTTPException

from .config import load_plugins


def fake_provider(request: dict[str, Any]) -> dict[str, Any]:
    messages = request.get("messages", [])
    prompt = messages[-1].get("content", "") if messages else ""
    return {
        "id": "fake-response",
        "model": request.get("model", "fake"),
        "provider": "fake",
        "choices": [{"message": {"role": "assistant", "content": f"fake: {prompt}"}}],
    }


def create_app(config_path: str | None = None) -> FastAPI:
    app = FastAPI(title="Modular LLM Gateway")
    selected_path = config_path or os.getenv("GATEWAY_CONFIG", "config/plugins.json")
    try:
        plugins = load_plugins(selected_path)
    except (OSError, ValueError, ImportError, AttributeError) as exc:
        raise RuntimeError(f"could not load plugins from {selected_path}: {exc}") from exc

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/chat/completions")
    def chat(request: dict[str, Any]) -> dict[str, Any]:
        try:
            transformed = request
            for plugin in plugins:
                transformed = plugin.process_request(transformed)
            response = fake_provider(transformed)
            for plugin in plugins:
                response = plugin.process_response(response)
            return response
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"plugin failure: {exc}") from exc

    return app


app = create_app()
