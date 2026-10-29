"""Behavioral checks for terminal users, including a third-party plugin workspace."""

import json
from pathlib import Path
import subprocess
import sys
import socket
import os
from time import monotonic, sleep


def cli(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "gateway", *args], cwd=cwd, text=True,
                          capture_output=True, timeout=90,
                          env={**os.environ, "XDG_CONFIG_HOME": str(cwd / "private-config")})


def test_installed_cli_demo_from_an_unrelated_directory(tmp_path):
    result = cli("demo", cwd=tmp_path)
    assert result.returncode == 0, result.stderr + result.stdout
    assert result.stdout.count("PASS  ") == 5
    assert "health and next chat recovered" in result.stdout
    assert '"schema_version"' not in result.stderr
    assert not list(tmp_path.iterdir())


def test_cli_doctor_and_plugins_use_packaged_config(tmp_path):
    doctor = cli("doctor", cwd=tmp_path)
    assert doctor.returncode == 0, doctor.stderr
    assert "PASS: 2 configured plugins" in doctor.stdout
    plugins = cli("plugins", cwd=tmp_path)
    assert plugins.returncode == 0
    assert "1. gateway.plugins.add_metadata.MetadataPlugin" in plugins.stdout
    assert "2. gateway.plugins.uppercase.UppercasePlugin" in plugins.stdout


def test_workspace_init_is_editable_importable_and_never_overwrites(tmp_path):
    directory = tmp_path / "with spaces"
    result = cli("init", str(directory), cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    plugin = directory / "my_plugin.py"
    original = plugin.read_bytes()
    assert json.loads((directory / "plugins.json").read_text())["plugins"] == ["my_plugin.ABReplacePlugin"]
    configured = cli("plugins", "--config", str(directory / "plugins.json"), cwd=tmp_path)
    assert configured.returncode == 0, configured.stderr
    assert "1. my_plugin.ABReplacePlugin" in configured.stdout
    plugin.write_bytes(original + b"\n# keep user edits\n")
    repeated = cli("init", str(directory), cwd=tmp_path)
    assert repeated.returncode != 0
    assert plugin.read_bytes() == original + b"\n# keep user edits\n"


def test_custom_workspace_is_served_from_an_unrelated_directory(tmp_path):
    workspace = tmp_path / "external plugin"
    assert cli("init", str(workspace), cwd=tmp_path).returncode == 0
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    server = subprocess.Popen([sys.executable, "-m", "gateway", "serve", "--port", str(port),
                               "--config", str(workspace / "plugins.json")], cwd=tmp_path,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                              env={**os.environ, "XDG_CONFIG_HOME": str(tmp_path / "private-config")})
    url = f"http://127.0.0.1:{port}"
    try:
        deadline = monotonic() + 15
        while cli("health", "--url", url, cwd=tmp_path).returncode != 0:
            assert server.poll() is None and monotonic() < deadline, "CLI server failed to start"
            sleep(.05)
        chat = cli("chat", "hello", "--url", url, cwd=tmp_path)
        assert chat.returncode == 0, chat.stderr
        assert json.loads(chat.stdout)["choices"][0]["message"]["content"] == "BBBB"
        assert "Request ID:" in chat.stderr
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=5)


def test_cli_failure_is_actionable_without_a_traceback(tmp_path):
    result = cli("doctor", "--config", str(tmp_path / "missing.json"), cwd=tmp_path)
    assert result.returncode == 1
    assert "missing.json" in result.stderr
    assert "Traceback" not in result.stderr
    failed = cli("health", "--url", "file:///etc/passwd", cwd=tmp_path)
    assert failed.returncode == 1
    assert "http(s)" in failed.stderr


def test_installed_default_preserves_tracked_default():
    root = Path(__file__).resolve().parent.parent
    assert json.loads((root / "gateway/data/plugins.json").read_text()) == json.loads((root / "config/plugins.json").read_text())
