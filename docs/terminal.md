# Terminal installation and supervisor demo

Install once, then run `llmgw` from any directory. The installer downloads a private uv toolchain and Python 3.12.13, installs the gateway in an isolated environment and runs a real HTTP demo. It does not change system Python, install a system service, edit shell profiles or require sudo, Git, Docker, an account or a provider key.

This is a preview of the next version, not a production deployment or a new published release. The provider is deterministic and fake. Authentication, TLS, real-provider integration, persistence and fleet deployment are not delivered by this installer.

## Supported targets and requirements

Targets are Linux (glibc 2.28 or newer) and macOS 13 or newer, on x86_64 or ARM64. They need an ordinary POSIX shell, `tar`, `curl` or `wget`, a writable home directory and outbound HTTPS to GitHub, Astral and PyPI. Allow several hundred MB of writable disk space for the isolated runtime and caches. The initial install downloads dependencies; subsequent demo/server runs work offline.

Windows, older systems, restricted networks and other CPU architectures are not covered by this shell installer. Automated platform checks and the review notes state what has actually been exercised; a target is not a claim that every operating system/version has been tested.

## One-line installation

After the terminal changes are reviewed and merged, the main-branch command is:

```sh
curl -fsSL https://raw.githubusercontent.com/ITPD-Almo/modular-llm-gateway/main/install.sh | sh && export PATH="$HOME/.local/bin:$PATH"
```

For a preview, use the full commit from the reviewed branch in both places below. `FULL_COMMIT_SHA` is a placeholder to replace, not an executable example:

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

Leave the server running. In another terminal:

```sh
export PATH="$HOME/.local/bin:$PATH"
llmgw health
llmgw plugins
llmgw chat "hello supervisor"
```

The health result is `{"status":"ok"}`. Chat shows `fake: HELLO`, the ordered plugin trace, the plugin changes and a generated request ID. Open `http://127.0.0.1:8000/docs` for interactive API documentation. Ctrl+C stops the server. If port 8000 is occupied, use `llmgw serve --port 8080` and `llmgw chat "hello" --url http://127.0.0.1:8080`.

The server binds to `127.0.0.1` by default. The CLI allows a longer worker-startup budget of five seconds for laptops, while the individual hook deadline remains 250 ms. This is a local development tool with no authentication; keep it on loopback. See the [operating guide](operations.md) for the existing limits and cleanup policy.

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

For a default installation, stop the server and remove `~/.local/bin/llmgw` and `~/.local/share/llmgw`. If you set XDG_DATA_HOME or GATEWAY_BIN_DIR, use the actual paths printed at installation instead. Keep or remove your own plugin workspace separately. Shared uv download caches may remain; removing the app does not require deleting other tools' caches.

## Contributor verification

Build a wheel and install it in a clean environment. Run `llmgw doctor`, `llmgw demo`, and a custom workspace/server/chat from an unrelated directory. The wheel must contain its default JSON file and demo plugins; an editable repository install alone cannot prove that. The installer pins runtime dependencies in `requirements-runtime.txt`, generated with `uv pip compile pyproject.toml --universal --output-file requirements-runtime.txt`.

The bootstrap uses the [official uv installer](https://docs.astral.sh/uv/reference/installer/) with shell modification disabled. [uv-managed Python](https://docs.astral.sh/uv/guides/install-python/) avoids dependence on an existing system interpreter. The installer trusts these HTTPS sources and PyPI; it does not claim signed binaries, an offline bundle or a complete enterprise software supply chain.
