import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

from .config import instantiate_plugins, read_plugin_paths
from .diagnostics import configure_diagnostics, new_request_id
from .execution import ExecutionFailure, ExecutionSettings, PipelineExecutor
from .provider import fake_provider as fake_provider  # Keep the existing import path available.


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str = "fake"
    messages: list[Message] = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


def create_app(
    config_path: str | None = None,
    *,
    plugin_timeout_ms: int | None = None,
    max_workers: int | None = None,
    startup_timeout_ms: int | None = None,
) -> FastAPI:
    configure_diagnostics()
    selected_path = config_path or os.getenv("GATEWAY_CONFIG", str(Path(__file__).resolve().parent.parent / "config" / "plugins.json"))
    try:
        paths = read_plugin_paths(selected_path)
        plugins = instantiate_plugins(paths)
    except (OSError, ValueError, ImportError, AttributeError) as exc:
        raise RuntimeError(f"could not load plugins from {selected_path}: {exc}") from exc

    def setting(value: int | None, name: str, default: int) -> int:
        if value is not None:
            return value
        try:
            return int(os.getenv(name, str(default)))
        except ValueError:
            raise ValueError(f"{name} must contain an integer") from None

    settings = ExecutionSettings(
        plugin_timeout_ms=setting(plugin_timeout_ms, "GATEWAY_PLUGIN_TIMEOUT_MS", 250),
        max_workers=setting(max_workers, "GATEWAY_MAX_WORKERS", 4),
        startup_timeout_ms=setting(startup_timeout_ms, "GATEWAY_WORKER_STARTUP_TIMEOUT_MS", 1000),
    )
    executor = PipelineExecutor(paths, tuple(type(plugin).__name__ for plugin in plugins), settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            yield
        finally:
            executor.close()

    app = FastAPI(title="Modular LLM Gateway", lifespan=lifespan)
    app.state.pipeline_executor = executor

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/chat/completions")
    def chat(request: ChatRequest, http_response: Response) -> dict[str, Any]:
        request_id = new_request_id()
        headers = {"X-Request-ID": request_id}
        http_response.headers.update(headers)
        try:
            return executor.execute(request.model_dump(), request_id)
        except ExecutionFailure as failure:
            raise HTTPException(status_code=failure.status_code, detail=failure.detail, headers=headers) from None

    return app
