"""Supervise a disposable plugin pipeline with bounded waits and worker admission."""

import base64
import json
import multiprocessing as mp
import os
import threading
from dataclasses import dataclass
from multiprocessing.connection import Connection
from multiprocessing.process import BaseProcess
from time import monotonic
from typing import Any

from .config import instantiate_plugins
from .deepseek import ERROR_MESSAGES, ProviderError
from .diagnostics import HookContext, PluginFailure, emit_hook_event, run_hook
from .provider import ChatProvider, fake_provider
from .validation import MAX_PAYLOAD_BYTES, validate_json, validate_request, validate_response

# Stay below POSIX's minimum PIPE_BUF: a pollable control frame is one atomic write.
MAX_FRAME_BYTES = 480
RESULT_CHUNK_BYTES = 128


@dataclass(frozen=True)
class ExecutionSettings:
    plugin_timeout_ms: int = 250
    startup_timeout_ms: int = 1000
    max_workers: int = 4
    cleanup_grace_ms: int = 100

    def __post_init__(self) -> None:
        for name in ("plugin_timeout_ms", "startup_timeout_ms", "cleanup_grace_ms"):
            value = getattr(self, name)
            if type(value) is not int or not 1 <= value <= 60_000:
                raise ValueError(f"{name} must be an integer between 1 and 60000")
        if type(self.max_workers) is not int or not 1 <= self.max_workers <= 32:
            raise ValueError("max_workers must be an integer between 1 and 32")


class ExecutionFailure(Exception):
    def __init__(self, status_code: int, detail: str, context: HookContext | None = None):
        self.status_code = status_code
        self.detail = detail
        self.context = context
        super().__init__(detail)


def _send(connection: Connection, message: dict[str, Any]) -> None:
    frame = json.dumps(message, allow_nan=False).encode("utf-8")
    if len(frame) > MAX_FRAME_BYTES:
        raise ValueError("worker control frame exceeds its limit")
    connection.send_bytes(frame)


def _pipeline_worker(
    connection: Connection,
    paths: tuple[str, ...],
    payload: dict[str, Any],
    request_id: str,
    provider: ChatProvider | None = None,
) -> None:
    # Only the explicit protocol reaches the parent. Plugin print/logging is not an operating event.
    with open(os.devnull, "w") as sink:
        os.dup2(sink.fileno(), 1)
        os.dup2(sink.fileno(), 2)
    try:
        try:
            plugins = instantiate_plugins(paths)
        except BaseException:
            _send(connection, {"kind": "startup_failed"})
            return
        _send(connection, {"kind": "ready"})

        def forward(
            context: HookContext, event: str, *, elapsed_ms: float = 0.0, reason: str | None = None
        ) -> None:
            _send(
                connection,
                {
                    "kind": "event",
                    "index": index,
                    "stage": context.stage,
                    "event": event,
                    "elapsed_ms": elapsed_ms,
                    "reason": reason,
                },
            )

        transformed = payload
        for index, plugin in enumerate(plugins):
            context = HookContext(request_id, type(plugin).__name__, "request")
            transformed = run_hook(
                plugin, transformed, context, emit=forward, validate=validate_request
            )
        try:
            if provider is not None:
                _send(connection, {"kind": "provider_started"})
            response = provider(transformed) if provider is not None else fake_provider(transformed)
            validate_response(response)
            if provider is not None:
                _send(connection, {"kind": "provider_completed"})
        except ProviderError as error:
            reason = error.reason if error.reason in ERROR_MESSAGES else "unavailable"
            _send(connection, {"kind": "provider_failed", "reason": reason})
            return
        except BaseException:
            _send(connection, {"kind": "provider_failed"})
            return
        for index, plugin in enumerate(plugins):
            context = HookContext(request_id, type(plugin).__name__, "response")
            response = run_hook(plugin, response, context, emit=forward, validate=validate_response)
        response["plugin_changes"] = transformed.get("plugin_changes", []) + response.get(
            "plugin_changes", []
        )
        validate_response(response)
        encoded = json.dumps(response, allow_nan=False).encode("utf-8")
        for offset in range(0, len(encoded), RESULT_CHUNK_BYTES):
            _send(
                connection,
                {
                    "kind": "result_chunk",
                    "data": base64.b64encode(encoded[offset : offset + RESULT_CHUNK_BYTES]).decode(
                        "ascii"
                    ),
                },
            )
        _send(connection, {"kind": "result_end"})
    except PluginFailure:
        # The preceding failed event already identifies the stage using safe fields.
        pass
    except BaseException:
        try:
            _send(connection, {"kind": "worker_failed"})
        except (OSError, ValueError):
            pass
    finally:
        connection.close()


class PipelineExecutor:
    def __init__(
        self,
        paths: tuple[str, ...],
        labels: tuple[str, ...],
        settings: ExecutionSettings,
        *,
        provider: ChatProvider | None = None,
    ):
        self.paths = paths
        self.labels = labels
        self.settings = settings
        self.provider = provider
        if provider is not None and (
            type(provider.timeout_ms) is not int or not 1 <= provider.timeout_ms <= 60000
        ):
            raise ValueError("provider timeout must be an integer between 1 and 60000 ms")
        self._context = mp.get_context("spawn")
        self._slots = threading.BoundedSemaphore(settings.max_workers)
        self._lock = threading.Lock()
        self._active: set[BaseProcess] = set()
        self._quarantined: set[BaseProcess] = set()
        self._closed = False

    def _reap_quarantined(self) -> None:
        with self._lock:
            for process in tuple(self._quarantined):
                if not process.is_alive():
                    process.join(0)
                    self._quarantined.remove(process)
                    self._active.remove(process)
                    process.close()
                    self._slots.release()

    @property
    def active_worker_count(self) -> int:
        self._reap_quarantined()
        with self._lock:
            return len(self._active)

    def close(self) -> None:
        with self._lock:
            self._closed = True
        self._reap_quarantined()
        # In-flight owners perform their own bounded cleanup; never race their Process handles.

    def _stop(self, process: BaseProcess, *, graceful: bool = False) -> bool:
        grace = self.settings.cleanup_grace_ms / 1000
        if graceful:
            process.join(grace)
        if process.is_alive():
            process.terminate()
        process.join(grace)
        if process.is_alive():
            process.kill()
            process.join(grace)
        return not process.is_alive()

    def execute(self, payload: dict[str, Any], request_id: str) -> dict[str, Any]:
        try:
            validate_json(payload)
        except (TypeError, ValueError, RecursionError):
            raise ExecutionFailure(413, "request exceeds the worker JSON limits") from None
        self._reap_quarantined()
        with self._lock:
            admitted = not self._closed and self._slots.acquire(blocking=False)
        if not admitted:
            raise ExecutionFailure(503, "plugin execution capacity is unavailable")
        receiver = sender = None
        try:
            receiver, sender = self._context.Pipe(duplex=False)
            process = self._context.Process(
                target=_pipeline_worker,
                args=(sender, self.paths, payload, request_id, self.provider),
                daemon=True,
            )
        except Exception:
            if receiver is not None:
                receiver.close()
            if sender is not None:
                sender.close()
            self._slots.release()
            raise ExecutionFailure(503, "plugin worker resources could not be allocated") from None
        registered = False
        started = False
        last_context = None
        completed = False
        try:
            try:
                process.start()
                started = True
            except Exception:
                raise ExecutionFailure(503, "plugin worker could not start") from None
            sender.close()
            with self._lock:
                self._active.add(process)
                registered = True
            try:
                response, last_context = self._receive(receiver, request_id)
            except ExecutionFailure as failure:
                last_context = failure.context
                raise
            completed = True
            return response
        finally:
            sender.close()
            receiver.close()
            if not started:
                process.close()
                self._slots.release()
            elif self._stop(process, graceful=completed):
                with self._lock:
                    if registered:
                        self._active.remove(process)
                process.close()
                self._slots.release()
            else:
                # Retain the slot while an OS process is unreaped: repeated requests cannot grow workers.
                with self._lock:
                    self._active.add(process)
                    self._quarantined.add(process)
                if last_context is not None:
                    emit_hook_event(last_context, "cleanup_failed", reason="cleanup_failed")

    def _receive(
        self, receiver: Connection, request_id: str
    ) -> tuple[dict[str, Any], HookContext | None]:
        idle_budget = self.settings.startup_timeout_ms / 1000
        hook_budget = self.settings.plugin_timeout_ms / 1000
        deadline = monotonic() + idle_budget
        # A faulty protocol cannot prolong a request by emitting endless progress packets.
        provider_budget = self.provider.timeout_ms / 1000 if self.provider is not None else 0
        overall = deadline + 2 * len(self.paths) * hook_budget + idle_budget + provider_budget
        expected = [
            (index, stage, event)
            for stage in ("request", "response")
            for index in range(len(self.paths))
            for event in ("started", "completed")
        ]
        position = 0
        ready = False
        current: HookContext | None = None
        last: HookContext | None = None
        hook_started = 0.0
        result_data = bytearray()
        provider_started = False
        provider_finished = self.provider is None

        def fail_worker() -> None:
            if current is not None:
                emit_hook_event(
                    current,
                    "failed",
                    elapsed_ms=(monotonic() - hook_started) * 1000,
                    reason="worker_exit",
                )
                raise ExecutionFailure(
                    500,
                    f"plugin {current.plugin} failed during {current.stage} processing",
                    current,
                )
            raise ExecutionFailure(503, "plugin worker exited without a valid result")

        while True:
            remaining = min(deadline, overall) - monotonic()
            if remaining <= 0 or not receiver.poll(max(remaining, 0)):
                if current is not None:
                    emit_hook_event(
                        current,
                        "timed_out",
                        elapsed_ms=(monotonic() - hook_started) * 1000,
                        reason="timeout",
                    )
                    raise ExecutionFailure(
                        504,
                        f"plugin {current.plugin} timed out during {current.stage} processing",
                        current,
                    )
                if provider_started and not provider_finished:
                    raise ExecutionFailure(504, "provider timed out; no automatic retry was made")
                raise ExecutionFailure(503, "plugin worker startup or transfer timed out")
            try:
                message = json.loads(receiver.recv_bytes(MAX_FRAME_BYTES))
            except (EOFError, OSError, ValueError, RecursionError):
                fail_worker()
            if not isinstance(message, dict):
                fail_worker()
            kind = message.get("kind")
            if kind == "ready" and not ready:
                ready = True
                deadline = monotonic() + idle_budget
            elif (
                kind == "provider_started"
                and self.provider is not None
                and ready
                and position == 2 * len(self.paths)
                and not provider_started
            ):
                provider_started = True
                deadline = monotonic() + provider_budget
            elif (
                kind == "provider_completed"
                and provider_started
                and not provider_finished
                and position == 2 * len(self.paths)
            ):
                provider_finished = True
                deadline = monotonic() + idle_budget
            elif kind == "event" and ready and position < len(expected):
                index, stage, event = expected[position]
                if stage == "response" and not provider_finished:
                    fail_worker()
                actual = message.get("event")
                if message.get("index") != index or message.get("stage") != stage:
                    fail_worker()
                context = HookContext(request_id, self.labels[index], stage)
                elapsed_ms = message.get("elapsed_ms")
                if type(elapsed_ms) not in (int, float):
                    fail_worker()
                try:
                    if actual == "failed" and event == "completed":
                        if message.get("reason") not in ("plugin_exception", "invalid_output"):
                            fail_worker()
                        emit_hook_event(
                            context, "failed", elapsed_ms=elapsed_ms, reason=message["reason"]
                        )
                        raise ExecutionFailure(
                            500,
                            f"plugin {context.plugin} failed during {stage} processing",
                            context,
                        )
                    if actual != event or message.get("reason") is not None:
                        fail_worker()
                    if actual == "completed" and elapsed_ms > self.settings.plugin_timeout_ms:
                        # A delayed parent/logger must not turn an over-budget hook into success.
                        emit_hook_event(
                            context, "timed_out", elapsed_ms=elapsed_ms, reason="timeout"
                        )
                        raise ExecutionFailure(
                            504,
                            f"plugin {context.plugin} timed out during {stage} processing",
                            context,
                        )
                    emit_hook_event(context, actual, elapsed_ms=elapsed_ms)
                except ValueError:
                    fail_worker()
                position += 1
                last = context
                if actual == "started":
                    current = context
                    hook_started = monotonic()
                    deadline = hook_started + hook_budget
                else:
                    current = None
                    deadline = monotonic() + idle_budget
            elif (
                kind == "result_chunk" and ready and position == len(expected) and provider_finished
            ):
                try:
                    data = message.get("data")
                    if not isinstance(data, str) or len(data) > 4 * ((RESULT_CHUNK_BYTES + 2) // 3):
                        fail_worker()
                    chunk = base64.b64decode(data, validate=True)
                    if (
                        not chunk
                        or len(chunk) > RESULT_CHUNK_BYTES
                        or len(result_data) + len(chunk) > MAX_PAYLOAD_BYTES
                    ):
                        fail_worker()
                    result_data.extend(chunk)
                except ValueError:
                    fail_worker()
                # Result transfer retains one fixed deadline; chunks do not keep extending it.
            elif kind == "result_end" and ready and position == len(expected) and provider_finished:
                try:
                    response = json.loads(result_data)
                except (ValueError, RecursionError):
                    fail_worker()
                if not isinstance(response, dict):
                    fail_worker()
                try:
                    validate_response(response)
                except (TypeError, ValueError, RecursionError):
                    fail_worker()
                return response, last
            elif kind == "provider_failed" and ready and position == 2 * len(self.paths):
                reason = message.get("reason")
                if reason is not None and reason not in ERROR_MESSAGES:
                    fail_worker()
                detail = ERROR_MESSAGES[reason] if reason is not None else "provider failed"
                raise ExecutionFailure(504 if reason == "timeout" else 502, detail)
            else:
                fail_worker()
