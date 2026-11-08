import json
import multiprocessing as mp
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from time import monotonic, sleep

import pytest
from fastapi.testclient import TestClient

from gateway.diagnostics import LOGGER
from gateway.main import create_app


def app_for(tmp_path, *names, **settings):
    path = tmp_path / "plugins.json"
    path.write_text(json.dumps({"plugins": ["tests.worker_plugins." + name for name in names]}))
    return create_app(str(path), **settings)


def chat(client, text="hello", **extra):
    return client.post(
        "/v1/chat/completions", json={"messages": [{"role": "user", "content": text}], **extra}
    )


def records(caplog):
    return [json.loads(r.getMessage()) for r in caplog.records if r.name == LOGGER.name]


@pytest.mark.parametrize("plugin,stage", [("SlowRequest", "request"), ("SlowResponse", "response")])
def test_real_hook_timeout_is_bounded_and_a_later_request_recovers(tmp_path, caplog, plugin, stage):
    app = app_for(tmp_path, plugin)
    with TestClient(app) as client:
        started = monotonic()
        result = chat(client, "sleep", metadata={"secret": "DO_NOT_LOG_TIMEOUT_METADATA"})
        elapsed = monotonic() - started
        assert result.status_code == 504
        assert elapsed < 1.0
        assert result.json()["detail"] == f"plugin {plugin} timed out during {stage} processing"
        event = [r for r in records(caplog) if r["event"] == "timed_out"][-1]
        assert (
            event["plugin"] == plugin and event["stage"] == stage and event["reason"] == "timeout"
        )
        assert event["request_id"] == result.headers["X-Request-ID"]
        assert "DO_NOT_LOG_TIMEOUT_METADATA" not in caplog.text
        assert app.state.pipeline_executor.active_worker_count == 0
        assert client.get("/health").status_code == 200
        healthy = chat(client)
        assert healthy.status_code == 200
        assert healthy.json()["choices"][0]["message"]["content"] == "fake: hello"
        assert app.state.pipeline_executor.active_worker_count == 0


def test_twenty_timeouts_reap_each_worker_and_release_capacity(tmp_path):
    app = app_for(tmp_path, "SlowRequest", max_workers=1)
    before = {p.pid for p in mp.active_children()}
    with TestClient(app) as client:
        threads_before = threading.active_count()
        for _ in range(20):
            started = monotonic()
            assert chat(client, "sleep").status_code == 504
            assert monotonic() - started < 1.0
            assert app.state.pipeline_executor.active_worker_count == 0
            assert {p.pid for p in mp.active_children()} == before
        assert threading.active_count() <= threads_before + 2
        for _ in range(10):
            assert client.get("/health").status_code == 200
            healthy = chat(client)
            assert healthy.status_code == 200
            assert healthy.json()["choices"][0]["message"]["content"] == "fake: hello"


def test_cpu_bound_hook_is_stopped(tmp_path):
    app = app_for(tmp_path, "BusyLoop")
    with TestClient(app) as client:
        started = monotonic()
        assert chat(client, "spin").status_code == 504
        assert monotonic() - started < 1.0
        assert app.state.pipeline_executor.active_worker_count == 0
        assert chat(client).status_code == 200


def test_delayed_event_consumer_cannot_accept_a_hook_over_budget(tmp_path, monkeypatch):
    import gateway.execution as execution

    original = execution.emit_hook_event

    def delayed(context, event, **fields):
        if event == "started":
            sleep(0.4)
        original(context, event, **fields)

    monkeypatch.setattr(execution, "emit_hook_event", delayed)
    with TestClient(app_for(tmp_path, "SlightlySlow")) as client:
        assert chat(client).status_code == 504


@pytest.mark.skipif(
    os.name == "nt", reason="POSIX signal-ignore fixture; Windows terminate is already forceful"
)
def test_worker_ignoring_terminate_is_killed_and_reaped(tmp_path):
    app = app_for(tmp_path, "IgnoreTerminate")
    with TestClient(app) as client:
        started = monotonic()
        assert chat(client, "sleep").status_code == 504
        assert monotonic() - started < 1.0
        assert app.state.pipeline_executor.active_worker_count == 0
        assert chat(client).status_code == 200


@pytest.mark.parametrize("plugin", ["ExitWorker", "SystemExitPlugin"])
def test_worker_exit_is_named_and_does_not_stop_the_gateway(tmp_path, caplog, plugin):
    app = app_for(tmp_path, plugin)
    with TestClient(app) as client:
        result = chat(client, "exit")
        assert result.status_code == 500
        assert plugin in result.json()["detail"]
        assert records(caplog)[-1]["reason"] in ("worker_exit", "plugin_exception")
        assert "DO_NOT_LOG_SYSTEM_EXIT" not in caplog.text + result.text
        assert app.state.pipeline_executor.active_worker_count == 0
        assert client.get("/health").status_code == 200
        assert chat(client).status_code == 200


@pytest.mark.parametrize("mode", ["none", "messages", "trace", "json", "large"])
def test_malformed_request_hook_output_has_a_safe_error(tmp_path, caplog, mode):
    app = app_for(tmp_path, "MalformedRequest")
    with TestClient(app) as client:
        result = chat(client, mode)
        assert result.status_code == 500
        assert "MalformedRequest" in result.json()["detail"]
        event = records(caplog)[-1]
        assert event["event"] == "failed" and event["reason"] == "invalid_output"
        assert not any(r["event"] == "completed" for r in records(caplog))
        assert app.state.pipeline_executor.active_worker_count == 0


def test_malformed_response_hook_output_has_a_safe_error(tmp_path, caplog):
    with TestClient(app_for(tmp_path, "MalformedResponse")) as client:
        result = chat(client)
        assert result.status_code == 500
        event = records(caplog)[-1]
        assert event["stage"] == "response" and event["reason"] == "invalid_output"


def test_concurrent_admission_is_bounded_and_health_remains_available(tmp_path):
    app = app_for(tmp_path, "SlowRequest", max_workers=1, plugin_timeout_ms=750)
    with TestClient(app) as client, ThreadPoolExecutor(max_workers=1) as threads:
        pending = threads.submit(chat, client, "sleep")
        until = monotonic() + 1
        while app.state.pipeline_executor.active_worker_count == 0 and monotonic() < until:
            sleep(0.005)
        assert app.state.pipeline_executor.active_worker_count == 1
        overloaded = chat(client)
        assert overloaded.status_code == 503 and overloaded.headers["X-Request-ID"]
        assert client.get("/health").status_code == 200
        assert pending.result(timeout=3).status_code == 504
        assert app.state.pipeline_executor.active_worker_count == 0
        assert chat(client).status_code == 200


def test_state_is_shared_between_hooks_but_resets_for_the_next_request(tmp_path):
    with TestClient(app_for(tmp_path, "RequestState")) as client:
        assert chat(client, "first").json()["choices"][0]["message"]["content"] == "first:1"
        assert chat(client, "second").json()["choices"][0]["message"]["content"] == "second:1"


def test_configuration_is_frozen_until_restart(tmp_path):
    path = tmp_path / "plugins.json"
    path.write_text(json.dumps({"plugins": ["gateway.plugins.uppercase.UppercasePlugin"]}))
    app = create_app(str(path))
    path.write_text(json.dumps({"plugins": []}))
    with TestClient(app) as client:
        assert chat(client).json()["choices"][0]["message"]["content"] == "fake: HELLO"


def test_request_above_worker_limit_is_rejected_before_allocating_a_worker(tmp_path):
    app = app_for(tmp_path)
    with TestClient(app) as client:
        result = chat(client, "x" * (1024 * 1024))
        assert result.status_code == 413
        assert result.headers["X-Request-ID"]
        assert app.state.pipeline_executor.active_worker_count == 0


def test_large_valid_response_is_transferred_without_losing_content(tmp_path):
    app = app_for(tmp_path)
    text = "synthetic large message " * 8000
    with TestClient(app) as client:
        result = chat(client, text)
        assert result.status_code == 200
        assert result.json()["choices"][0]["message"]["content"] == "fake: " + text
        assert app.state.pipeline_executor.active_worker_count == 0


@pytest.mark.parametrize(
    "settings",
    [
        {"plugin_timeout_ms": 0},
        {"plugin_timeout_ms": True},
        {"max_workers": 0},
        {"max_workers": 33},
        {"startup_timeout_ms": -1},
    ],
)
def test_invalid_execution_settings_fail_before_serving(tmp_path, settings):
    with pytest.raises(ValueError):
        app_for(tmp_path, **settings)
