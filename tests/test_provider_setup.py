"""No live credentials or external API calls: local profiles and synthetic transports only."""

import getpass
import errno
import json
import os
import pty
import select
import stat
import subprocess
import sys
from time import monotonic

from fastapi.testclient import TestClient
import pytest

from gateway.cli import main
from gateway.credentials import Credentials, load_credentials, profile_directory, remove_credentials, save_credentials
from gateway.deepseek import DeepSeekProvider, ProviderError, authenticated_json, available_models
from gateway.main import create_app
from tests.provider_fixtures import SyntheticProvider

KEY = "synthetic-key-for-tests-only"


@pytest.fixture(autouse=True)
def private_profile(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "user-settings"))


def test_setup_hides_key_checks_models_and_saves_private_profile(monkeypatch, capsys):
    monkeypatch.setattr(getpass, "getpass", lambda prompt: KEY)
    monkeypatch.setattr("gateway.setup.available_models", lambda credentials: ["deepseek-flash", "other-model"])
    monkeypatch.setattr("builtins.input", lambda prompt: "")
    assert main(["setup"]) == 0
    saved = load_credentials()
    assert saved == Credentials(KEY, "deepseek-flash")
    assert stat.S_IMODE(profile_directory().stat().st_mode) == 0o700
    assert stat.S_IMODE((profile_directory() / "provider.json").stat().st_mode) == 0o600
    assert main(["status"]) == 0
    assert KEY not in repr(saved) + repr(DeepSeekProvider(saved))
    captured = capsys.readouterr()
    assert KEY not in captured.out + captured.err
    assert "saved (hidden)" in captured.out


@pytest.mark.parametrize("failure", ["authentication", "unavailable", "balance"])
def test_setup_failure_never_replaces_a_working_profile(monkeypatch, capsys, failure):
    old = Credentials("previous-synthetic-test-key")
    save_credentials(old)
    monkeypatch.setattr(getpass, "getpass", lambda prompt: KEY)
    def rejected(credentials):
        raise ProviderError(failure)
    monkeypatch.setattr("gateway.setup.available_models", rejected)
    assert main(["setup"]) == 1
    assert load_credentials() == old
    captured = capsys.readouterr()
    assert KEY not in captured.out + captured.err


def test_setup_refuses_visible_getpass_fallback(monkeypatch, capsys):
    def unavailable(prompt):
        raise getpass.GetPassWarning("cannot hide input")
    monkeypatch.setattr(getpass, "getpass", unavailable)
    assert main(["setup"]) == 1
    assert load_credentials() is None
    assert "interactive terminal" in capsys.readouterr().err


def test_real_terminal_key_entry_has_no_echo_and_no_live_api_call():
    master, slave = pty.openpty()
    code = ('import gateway.setup as setup; '
            'setup.available_models=lambda credentials: ["deepseek-flash"]; '
            'from gateway.cli import main; raise SystemExit(main(["setup"]))')
    process = subprocess.Popen([sys.executable, "-c", code], stdin=slave, stdout=slave, stderr=slave,
                               start_new_session=True)
    os.close(slave)
    output = bytearray()
    key_sent = model_sent = False
    try:
        deadline = monotonic() + 15
        while process.poll() is None:
            assert monotonic() < deadline, "setup did not finish in a real PTY"
            if select.select([master], [], [], .1)[0]:
                try:
                    chunk = os.read(master, 65536)
                except OSError as error:
                    if error.errno == errno.EIO:
                        break  # Linux signals PTY EOF this way when the slave closes.
                    raise
                if not chunk:
                    break
                output.extend(chunk)
            if b"API key (hidden):" in output and not key_sent:
                os.write(master, (KEY + "\n").encode())
                key_sent = True
            if b"Model number [1]:" in output and not model_sent:
                os.write(master, b"\n")
                model_sent = True
        process.wait(timeout=5)
        while select.select([master], [], [], 0)[0]:
            try:
                part = os.read(master, 65536)
            except OSError:
                break
            if not part:
                break
            output.extend(part)
        assert process.returncode == 0, output.decode(errors="replace")
        assert key_sent and model_sent and KEY.encode() not in output
        assert load_credentials() == Credentials(KEY)
    finally:
        os.close(master)
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)


def test_redirected_input_never_falls_back_to_echoing_or_saving_key():
    result = subprocess.run([sys.executable, "-m", "gateway", "setup"], input=KEY + "\n", text=True,
                            capture_output=True, timeout=15, start_new_session=True)
    assert result.returncode == 1 and KEY not in result.stdout + result.stderr
    assert load_credentials() is None


def test_cancel_setup_keeps_existing_key(monkeypatch):
    old = Credentials(KEY)
    save_credentials(old)
    def canceled(prompt):
        raise KeyboardInterrupt
    monkeypatch.setattr(getpass, "getpass", canceled)
    assert main(["setup"]) == 130
    assert load_credentials() == old


def test_bad_model_choice_does_not_save(monkeypatch):
    monkeypatch.setattr(getpass, "getpass", lambda prompt: KEY)
    monkeypatch.setattr("gateway.setup.available_models", lambda credentials: ["deepseek-flash"])
    monkeypatch.setattr("builtins.input", lambda prompt: "99")
    assert main(["setup"]) == 1
    assert load_credentials() is None


def test_logout_and_no_key_status(capsys):
    save_credentials(Credentials(KEY))
    assert main(["logout"]) == 0
    assert load_credentials() is None and not remove_credentials()
    assert main(["status"]) == 0
    assert KEY not in capsys.readouterr().out


def test_profile_symlink_and_public_permissions_are_rejected(tmp_path):
    save_credentials(Credentials(KEY))
    path = profile_directory() / "provider.json"
    path.chmod(0o644)
    with pytest.raises(ValueError):
        load_credentials()
    path.chmod(0o600)
    path.unlink()
    target = tmp_path / "unrelated.json"
    target.write_text("keep me")
    path.symlink_to(target)
    with pytest.raises(ValueError):
        save_credentials(Credentials(KEY))
    with pytest.raises(ValueError):
        load_credentials()
    with pytest.raises(ValueError):
        remove_credentials()
    assert target.read_text() == "keep me"


def test_models_are_discovered_without_chat_and_untrusted_identifiers_are_not_printed(monkeypatch):
    calls = []
    def transport(credentials, path, payload=None):
        calls.append((path, payload))
        return {"data": [{"id": KEY}, {"id": "unsafe\x1bcommand"}, {"id": "other"}, {"id": "deepseek-flash"}]}
    monkeypatch.setattr("gateway.deepseek.authenticated_json", transport)
    assert available_models(Credentials(KEY)) == ["deepseek-flash", "other"]
    assert calls == [("/models", None)]


def test_deepseek_transport_keeps_key_only_in_header_and_limits_payload(monkeypatch):
    seen = {}
    class Reply:
        status = 200
        def read1(self, size):
            if seen.get("read"):
                return b""
            seen["read"] = True
            return b'{"choices":[{"message":{"content":"synthetic answer"}}]}'
    class Connection:
        sock = None
        def __init__(self, host, timeout):
            seen["host"] = host
        def request(self, method, path, body, headers):
            seen.update(method=method, path=path, body=body, headers=headers)
        def getresponse(self):
            return Reply()
        def close(self):
            seen["closed"] = True
    monkeypatch.setattr("gateway.deepseek.http.client.HTTPSConnection", Connection)
    result = DeepSeekProvider(Credentials(KEY))({"model": "caller-model", "messages": [{"role": "user", "content": "synthetic prompt"}],
                                               "metadata": {"do_not_forward": True}, "api_key": KEY})
    payload = json.loads(seen["body"])
    assert seen["host"] == "api.deepseek.com" and seen["path"] == "/chat/completions"
    assert seen["headers"]["Authorization"] == "Bearer " + KEY
    assert KEY.encode() not in seen["body"] and "metadata" not in payload
    assert payload["model"] == "deepseek-flash" and payload["max_tokens"] == 128
    assert payload["stream"] is False and payload["thinking"] == {"type": "disabled"}
    assert result["choices"][0]["message"]["content"] == "synthetic answer"
    assert seen["closed"]


@pytest.mark.parametrize("status,reason", [(400, "request"), (401, "authentication"), (402, "balance"), (429, "rate_limit"), (500, "unavailable"), (302, "unavailable")])
def test_remote_error_bodies_and_redirects_are_never_exposed(monkeypatch, status, reason):
    seen = []
    class Reply:
        def __init__(self):
            self.status = status
        def read1(self, size):
            pytest.fail("error bodies should not be read or reflected")
    class Connection:
        def __init__(self, host, timeout):
            seen.append(host)
        def request(self, *args, **kwargs):
            pass
        def getresponse(self):
            return Reply()
        def close(self):
            pass
    monkeypatch.setattr("gateway.deepseek.http.client.HTTPSConnection", Connection)
    with pytest.raises(ProviderError) as caught:
        authenticated_json(Credentials(KEY), "/models")
    assert caught.value.reason == reason and KEY not in str(caught.value)
    assert seen == ["api.deepseek.com"]


def configured_app(tmp_path, provider, plugins=()):
    config = tmp_path / "plugins.json"
    config.write_text(json.dumps({"plugins": list(plugins)}))
    return create_app(str(config), provider=provider, startup_timeout_ms=1000)


def chat(client, message="hello"):
    return client.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": message}]})


def test_provider_wait_is_not_mistaken_for_worker_startup_or_hook_timeout(tmp_path):
    app = configured_app(tmp_path, SyntheticProvider(delay=1.15), ["gateway.plugins.uppercase.UppercasePlugin"])
    with TestClient(app) as client:
        response = chat(client)
        assert response.status_code == 200
        assert response.json()["choices"][0]["message"]["content"] == "upstream:HELLO"
        assert response.json()["plugin_trace"] == ["uppercase"]
        assert response.headers["X-Request-ID"]
        assert app.state.pipeline_executor.active_worker_count == 0


def test_slow_provider_is_terminated_and_next_request_recovers(tmp_path, caplog):
    app = configured_app(tmp_path, SyntheticProvider(timeout_ms=150))
    with TestClient(app) as client:
        started = monotonic()
        failed = chat(client, "provider-sleep")
        assert failed.status_code == 504 and monotonic() - started < 2
        assert app.state.pipeline_executor.active_worker_count == 0
        assert client.get("/health").status_code == 200
        assert chat(client).status_code == 200
        assert "SYNTHETIC_PROVIDER_SECRET" not in failed.text + caplog.text


def test_provider_failure_is_actionable_and_does_not_hold_capacity(tmp_path, caplog):
    app = configured_app(tmp_path, SyntheticProvider())
    with TestClient(app) as client:
        failed = chat(client, "provider-fail")
        assert failed.status_code == 502 and "llmgw setup" in failed.json()["detail"]
        assert app.state.pipeline_executor.active_worker_count == 0
        assert chat(client).status_code == 200
        assert "SYNTHETIC_PROVIDER_SECRET" not in failed.text + caplog.text


def test_slow_plugin_still_fails_with_real_provider_mode_before_upstream_work(tmp_path):
    app = configured_app(tmp_path, SyntheticProvider(), ["gateway.plugins.demo_slow.SlowPlugin"])
    with TestClient(app) as client:
        failed = chat(client, "sleep")
        assert failed.status_code == 504 and "SlowPlugin" in failed.text
        assert chat(client).status_code == 200
