import os
from time import perf_counter
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .analytics import AnalyticsClient, AnalyticsSession
from .config import instantiate_plugins, read_plugin_paths
from .diagnostics import configure_diagnostics, new_request_id
from .execution import ExecutionFailure, ExecutionSettings, PipelineExecutor
from .provider import fake_provider as fake_provider  # Keep the existing import path available.
from .provider import ChatProvider


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
    provider: ChatProvider | None = None,
    analytics_client: AnalyticsClient | None = None,
) -> FastAPI:
    configure_diagnostics()
    source_default = Path(__file__).resolve().parent.parent / "config" / "plugins.json"
    packaged_default = Path(__file__).resolve().parent / "data" / "plugins.json"
    selected_path = config_path or os.getenv("GATEWAY_CONFIG") or str(
        source_default if source_default.is_file() else packaged_default
    )
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
    executor = PipelineExecutor(paths, tuple(type(plugin).__name__ for plugin in plugins), settings, provider=provider)
    analytics = analytics_client or AnalyticsClient()
    analytics_session = AnalyticsSession(analytics, len(paths))

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            yield
        finally:
            executor.close()
            if analytics_client is None:
                analytics.close()

    app = FastAPI(title="Modular LLM Gateway", lifespan=lifespan)
    app.state.pipeline_executor = executor
    app.state.analytics = analytics

    @app.middleware("http")
    async def correlate_chat(http_request: Request, call_next):
        if http_request.method != "POST" or http_request.url.path.rstrip("/") != "/v1/chat/completions":
            return await call_next(http_request)
        http_request.state.gateway_request_id = new_request_id()
        response = await call_next(http_request)
        response.headers["X-Request-ID"] = http_request.state.gateway_request_id
        return response

    @app.exception_handler(RequestValidationError)
    async def invalid_request(http_request: Request, failure: RequestValidationError):
        # Framework validation errors can reflect the input or JSON decoder text.
        # Keep the HTTP status while leaving private request values out of errors.
        return JSONResponse(status_code=422, content={"detail": "invalid chat request"})

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/chat/completions")
    def chat(request: ChatRequest, http_request: Request) -> dict[str, Any]:
        request_id = http_request.state.gateway_request_id
        headers = {"X-Request-ID": request_id}
        started = perf_counter()
        analytics_session.started(request_id)
        status_code = 200
        response: dict[str, Any] | None = None
        try:
            response = executor.execute(request.model_dump(), request_id)
            return response
        except ExecutionFailure as failure:
            status_code = failure.status_code
            raise HTTPException(status_code=failure.status_code, detail=failure.detail, headers=headers) from None
        finally:
            analytics_session.finished(request_id, status_code=status_code, duration_ms=(perf_counter() - started) * 1000, response=response)

    return app
