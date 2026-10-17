import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import load_plugins


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
    selected_path = config_path or os.getenv("GATEWAY_CONFIG", str(Path(__file__).resolve().parent.parent / "config" / "plugins.json"))
    try:
        plugins = load_plugins(selected_path)
    except (OSError, ValueError, ImportError, AttributeError) as exc:
        raise RuntimeError(f"could not load plugins from {selected_path}: {exc}") from exc

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/chat/completions")
    def chat(request: ChatRequest) -> dict[str, Any]:
        transformed = request.model_dump()
        try:
            for plugin in plugins:
                try:
                    transformed = plugin.process_request(transformed)
                except Exception as exc:
                    raise HTTPException(status_code=500, detail=f"plugin {type(plugin).__name__} failed during request processing") from exc
            try:
                response = fake_provider(transformed)
            except Exception as exc:
                raise HTTPException(status_code=502, detail="provider failed") from exc
            for plugin in plugins:
                try:
                    response = plugin.process_response(response)
                except Exception as exc:
                    raise HTTPException(status_code=500, detail=f"plugin {type(plugin).__name__} failed during response processing") from exc
            response["plugin_changes"] = transformed.get("plugin_changes", []) + response.get("plugin_changes", [])
            return response
        except HTTPException:
            raise

    return app
