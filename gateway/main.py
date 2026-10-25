import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

from .config import load_plugins
from .diagnostics import HookContext, PluginFailure, configure_diagnostics, new_request_id, run_hook


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str = "fake"
    messages: list[Message] = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


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
    configure_diagnostics()
    selected_path = config_path or os.getenv("GATEWAY_CONFIG", str(Path(__file__).resolve().parent.parent / "config" / "plugins.json"))
    try:
        plugins = load_plugins(selected_path)
    except (OSError, ValueError, ImportError, AttributeError) as exc:
        raise RuntimeError(f"could not load plugins from {selected_path}: {exc}") from exc

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/chat/completions")
    def chat(request: ChatRequest, http_response: Response) -> dict[str, Any]:
        request_id = new_request_id()
        headers = {"X-Request-ID": request_id}
        http_response.headers.update(headers)
        transformed = request.model_dump()
        try:
            for plugin in plugins:
                transformed = run_hook(plugin, transformed, HookContext(request_id, type(plugin).__name__, "request"))
            try:
                response = fake_provider(transformed)
            except Exception as exc:
                raise HTTPException(status_code=502, detail="provider failed", headers=headers) from None
            for plugin in plugins:
                response = run_hook(plugin, response, HookContext(request_id, type(plugin).__name__, "response"))
            response["plugin_changes"] = transformed.get("plugin_changes", []) + response.get("plugin_changes", [])
            return response
        except PluginFailure as failure:
            raise HTTPException(status_code=500, detail=str(failure), headers=headers) from None

    return app
