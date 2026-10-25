# Setup and run

This recipe installs the gateway in a clean Python 3.12 virtual environment and sends one request through two plugins. It needs no provider key, no account and no local file that is not in the repository: the gateway answers with a built-in fake provider.

## Prerequisites

- Git.
- Python 3.12. Check with `python3.12 --version` (on Windows, `py -3.12 --version`); it must print `Python 3.12.x`.
- `curl` for the test request. It ships with Linux, macOS and Windows 10 or later.
- Free local port 8000.

## Install

From a clean clone:

```sh
git clone --recurse-submodules https://github.com/ITPD-Almo/modular-llm-gateway.git
cd modular-llm-gateway
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

On Windows PowerShell, use:

```powershell
git clone --recurse-submodules https://github.com/ITPD-Almo/modular-llm-gateway.git
Set-Location modular-llm-gateway
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

The PowerShell steps have not yet been run end to end on Windows.

Optionally copy `.env.example` to `.env` to change settings such as the plugin list or the hook deadline. Every setting has a default, so the gateway also starts without `.env`.

## Run

Start the gateway from the repository root with the default plugin list in `config/plugins.json`:

```console
python -m uvicorn gateway.main:create_app --factory
```

If you created `.env`, add `--env-file .env`. Check that it is up from another terminal:

```console
curl http://127.0.0.1:8000/health
```

It answers `{"status":"ok"}`. Then send a chat request:

```console
curl -i -X POST http://127.0.0.1:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"fake","messages":[{"role":"user","content":"hello"}]}'
```

The reply is HTTP 200 with an `X-Request-ID` header, `"content":"fake: HELLO"`, `"provider":"fake"`, `"plugin_trace":["metadata","uppercase"]`, and four `plugin_changes` entries in that order. The [demo](demo.md) shows the full expected output and how to change the plugins.

The gateway reads the plugin list only when it starts. After you change the configuration, stop the server with Ctrl+C and start it again. Uvicorn's `--reload` option watches Python files, not the JSON configuration.

## Test and check

```sh
python -m pytest
```

All tests use synthetic plugins and the fake provider, so they need no key and no network.

To build the documentation site as CI does:

```sh
python -m pip install -r requirements-docs.txt
python -m mkdocs build --strict
```

For the repository checks, install Node.js/npm for Markdown lint and the [lychee CLI](https://github.com/lycheeverse/lychee#installation) for links. For example, lychee can be installed with `cargo install lychee` when Rust is available, or `brew install lychee` on macOS.

```sh
npx markdownlint-cli2 "**/*.md"
lychee --exclude-path .claude/skills/itpd './**/*.md'
```

These checks also run in CI. The link checker is the Rust lychee CLI; do not install the unrelated npm package called lychee.

## Reset

To return to the clean state after a demo or experiment:

1. Stop the server with Ctrl+C.
2. Unset any configuration you exported: `unset GATEWAY_CONFIG GATEWAY_PLUGIN_TIMEOUT_MS GATEWAY_MAX_WORKERS GATEWAY_WORKER_STARTUP_TIMEOUT_MS` (PowerShell: `Remove-Item Env:GATEWAY_*`).
3. Restore the tracked configuration: `git checkout -- config/plugins.json`, and delete `.env` if you created it.
4. For a fully fresh install, leave the virtual environment with `deactivate`, delete `.venv`, and repeat the install steps.
