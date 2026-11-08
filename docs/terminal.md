# Terminal installation and supervisor demo

Install once, then run `llmgw` from any directory. The installer downloads a private uv toolchain and Python 3.12.13, installs the gateway in an isolated environment and runs a real HTTP demo. It does not change system Python, install a system service, edit shell profiles or require sudo, Git, Docker, an account or a provider key.

The installed tool is included in v0.5.0. Its demo uses a deterministic fake provider. Users may explicitly connect their own DeepSeek account using the guided setup below. Gateway client authentication, server TLS, persistent request storage and fleet deployment are not delivered by this installer; outbound DeepSeek calls use HTTPS. The shared university deployment adds its own HTTPS/access gate, described in the [runbook](deployment.md).

## Supported targets and requirements

Targets are Linux (glibc 2.28 or newer) and macOS 13 or newer, on x86_64 or ARM64. They need an ordinary POSIX shell, `tar`, `curl` or `wget`, a writable home directory and outbound HTTPS to GitHub, Astral and PyPI. Allow several hundred MB of writable disk space for the isolated runtime and caches. The initial install downloads dependencies; subsequent demo/server runs work offline.

Windows, older systems, restricted networks and other CPU architectures are not covered by this shell installer. Automated platform checks and the review notes state what has actually been exercised; a target is not a claim that every operating system/version has been tested.

## One-line installation

Install the published v0.5.0 release:

```sh
curl -fsSL https://raw.githubusercontent.com/ITPD-Almo/modular-llm-gateway/v0.5.0/install.sh | sh -s -- --ref v0.5.0 && export PATH="$HOME/.local/bin:$PATH"
```

For another reviewed candidate, use its full commit in both places below. `FULL_COMMIT_SHA` is a placeholder to replace, not an executable example:

```sh
curl -fsSL https://raw.githubusercontent.com/ITPD-Almo/modular-llm-gateway/FULL_COMMIT_SHA/install.sh | sh -s -- --ref FULL_COMMIT_SHA && export PATH="$HOME/.local/bin:$PATH"
```

Use a full commit for a reproducible demonstration. The installer prints the selected source ref and stores it in its installation receipt. Do not select v0.2.0: it predates the command and packaged default configuration. A download failure or demo failure must be treated as a failed install, even if a command was already installed previously.

If only wget is available, replace the `curl -fsSL URL` part with `wget -qO- URL`. To inspect before running, download `install.sh`, read it, then run `sh install.sh --ref FULL_COMMIT_SHA`.

The final `export` makes the command available in the current terminal, including macOS terminals where `~/.local/bin` is not normally on PATH. In another terminal, either set that PATH again or use `"$HOME/.local/bin/llmgw"` directly. The installer prints both forms; it cannot change its parent shell's environment.

Expected final output:

```text
PASS  Configured plugin order
PASS  Reversed plugin order
PASS  Uppercase plugin disabled
PASS  A/B plugin: request AAAA, reply BBBB
PASS  Five-second hook stopped early (...s); health and next chat recovered
All 5 scenarios passed. Next: llmgw serve
```

The demo owns temporary files and ephemeral loopback ports, stops its servers and request workers, and leaves any existing gateway on port 8000 alone.

## Show it to the supervisor

```sh
llmgw --version
llmgw doctor
llmgw demo
llmgw serve
```

Without a saved DeepSeek profile, this starts the fake provider. Leave the server running. In another terminal:

```sh
export PATH="$HOME/.local/bin:$PATH"
llmgw health
llmgw plugins
llmgw chat "hello supervisor"
```

The health result is `{"status":"ok"}`. Chat shows `fake: HELLO`, the ordered plugin trace, the plugin changes and a generated request ID. Open `http://127.0.0.1:8000/docs` for interactive API documentation. Ctrl+C stops the server. If port 8000 is occupied, use `llmgw serve --port 8080` and `llmgw chat "hello" --url http://127.0.0.1:8080`.

The server binds to `127.0.0.1` by default. The CLI allows a longer worker-startup budget of five seconds for laptops, while the individual hook deadline remains 250 ms. This is a local development tool with no authentication; keep it on loopback. See the [operating guide](operations.md) for the existing limits and cleanup policy.

## Connect your own DeepSeek account

No file editing, environment variables or key command-line arguments are needed:

```sh
llmgw setup
```

The guide asks you to paste your API key into a hidden terminal prompt and choose a model from your account's available models. Press Enter for the default model. [DeepSeek's first-call guide](https://api-docs.deepseek.com/) links to the account console where you can obtain a key. Do not paste keys into chat, shell commands or the API documentation's request body.

Setup checks the key with the [read-only models endpoint](https://api-docs.deepseek.com/api/list-models/). It makes no paid chat-generation request and does not verify your balance. An invalid key, network failure, bad model choice or Ctrl+C leaves the previous saved profile unchanged. It refuses to accept the key when hidden input is unavailable.

After setup, stop and restart the gateway:

```sh
llmgw serve
```

It prints `Provider: deepseek` and your selected model. In another terminal:

```sh
llmgw chat "Say hello in one short sentence"
```

This sends the plugin-transformed conversation to DeepSeek and uses your account balance. Provider/model selection comes from your local profile, not the chat request's `model` field. Responses are limited to 128 generated tokens with thinking disabled and no automatic retries. Network/model/account errors are reported without echoing upstream error bodies. Provider waiting has its own 45-second supervised deadline; plugin hooks keep their separate 250 ms limit. An interrupted upstream request may still have been processed/billed by DeepSeek.

Check or remove saved settings without showing the key:

```sh
llmgw status
llmgw logout
```

`logout` removes the saved key. Restart any running server to clear the old credential from its memory; removing the file cannot revoke a key held by an existing process. Rotate/revoke a key in your DeepSeek account if needed. To run offline regardless of saved settings, use `llmgw serve --provider fake`. `llmgw demo` always uses fake providers and never reads or spends your saved DeepSeek account.

The profile is stored outside the project at `${XDG_CONFIG_HOME:-$HOME/.config}/llmgw/provider.json`, with directory permissions 0700 and file permissions 0600. Writes are atomic and symlink/unsafe-permission profiles are rejected. This is permission-protected local storage, **not encryption or an OS keychain**. The key is never passed in plugin dictionaries or logged. Plugins remain trusted Python code running as your OS user and share the worker process with the provider adapter; this is not credential isolation from malicious plugins. Install only plugins you trust.

The real-provider adapter is included in v0.5.0. Automated tests use synthetic credentials and mocked provider responses, including failure and timeout cases; they make no paid DeepSeek calls. Separate owner-authorized live checks are recorded in [the deployment evidence](https://github.com/ITPD-Almo/modular-llm-gateway/pull/102); neither kind of check establishes Customer acceptance.

## Show an editable plugin without touching gateway core

Stop the default server first, then:

```sh
llmgw init "$HOME/my-gateway-demo"
llmgw serve --config "$HOME/my-gateway-demo/plugins.json"
```

In the other terminal:

```sh
llmgw chat "hello"
```

The reply is `BBBB`; the plugin change records show that the provider received `AAAA`. Edit `my_plugin.py` in that workspace, stop the server and restart it to load changes. Both `plugins.json` and the sibling Python plugin work from any directory. `init` refuses to overwrite an existing workspace. Python plugins are trusted executable code, not sandboxed or downloaded automatically from a plugin registry; the [plugin contract](plugins.md) still applies.

## Updates, installation location and removal

Run the installer again with a new explicit ref to update. The isolated toolchain lives in `${XDG_DATA_HOME:-$HOME/.local/share}/llmgw`; its launcher is `~/.local/bin/llmgw`. `GATEWAY_BIN_DIR` selects another launcher directory. The installer refuses to replace an unrelated command and never edits shell startup files.

For a default installation, run `llmgw logout` if you want to remove the saved key, stop the server and remove `~/.local/bin/llmgw` and `~/.local/share/llmgw`. If you set XDG_DATA_HOME or GATEWAY_BIN_DIR, use the actual paths printed at installation instead. Keep or remove your own plugin workspace separately. Shared uv download caches may remain; removing the app does not require deleting other tools' caches.

## Contributor verification

Build a wheel and install it in a clean environment. Run `llmgw doctor`, `llmgw demo`, and a custom workspace/server/chat from an unrelated directory. The wheel must contain its default JSON file and demo plugins; an editable repository install alone cannot prove that. The installer pins runtime dependencies in `requirements-runtime.txt`, generated with `uv pip compile pyproject.toml --universal --output-file requirements-runtime.txt`.

The bootstrap uses the [official uv installer](https://docs.astral.sh/uv/reference/installer/) with shell modification disabled. [uv-managed Python](https://docs.astral.sh/uv/guides/install-python/) avoids dependence on an existing system interpreter. The installer trusts these HTTPS sources and PyPI; it does not claim signed binaries, an offline bundle or a complete enterprise software supply chain.
