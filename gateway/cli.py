"""Terminal entry points for installed gateways; no repository checkout needed."""

import argparse
import json
import os
import platform
import sys
from importlib.metadata import version
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import ProxyHandler, Request, build_opener


def config_path(value: str | None) -> Path:
    selected = value or os.getenv("GATEWAY_CONFIG")
    return (
        Path(selected).expanduser().resolve()
        if selected
        else Path(__file__).parent / "data" / "plugins.json"
    )


def prepare_config(value: str | None) -> Path:
    path = config_path(value)
    # Spawned request workers inherit this path, so user-authored sibling plugins
    # work from any current directory without editing gateway core or PYTHONPATH.
    sys.path.insert(0, str(path.parent))
    return path


def request_json(
    base: str, prompt: str | None = None, timeout: float = 60
) -> tuple[int, dict, str | None]:
    url = urlparse(base)
    if url.scheme not in ("http", "https") or not url.hostname or url.username or url.password:
        raise ValueError("URL must be http(s)://host:port without embedded credentials")
    endpoint = "/health" if prompt is None else "/v1/chat/completions"
    data = (
        None
        if prompt is None
        else json.dumps({"messages": [{"role": "user", "content": prompt}]}).encode()
    )
    request = Request(
        base.rstrip("/") + endpoint, data=data, headers={"Content-Type": "application/json"}
    )
    # Avoid leaking local demo traffic to a machine's configured HTTP proxy.
    opener = (
        build_opener(ProxyHandler({}))
        if url.hostname in ("localhost", "127.0.0.1", "::1")
        else build_opener()
    )
    try:
        response = opener.open(request, timeout=timeout)
    except HTTPError as error:
        response = error
    with response:
        return response.status, json.load(response), response.headers.get("X-Request-ID")


def init_workspace(directory: str) -> None:
    root = Path(directory).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    files = {
        "plugins.json": '{"plugins": ["my_plugin.ABReplacePlugin"]}\n',
        "my_plugin.py": (Path(__file__).parent / "plugins" / "demo_ab.py").read_text(
            encoding="utf-8"
        ),
    }
    if any((root / name).exists() for name in files):
        raise ValueError(
            "workspace already contains plugins.json or my_plugin.py; choose a new directory"
        )
    for name, content in files.items():
        with (root / name).open("x", encoding="utf-8") as output:
            output.write(content)
    print(f"Created editable A/B plugin and configuration in {root}")
    print(f'Run: llmgw serve --config "{root / "plugins.json"}"')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="llmgw", description="Modular LLM Gateway — local plugin development and demo"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version('modular-llm-gateway')}"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    serve = commands.add_parser("serve", help="start the local gateway (Ctrl+C to stop)")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--config", help="JSON plugin list; sibling Python plugins are importable")
    serve.add_argument(
        "--provider", choices=("fake", "deepseek"), help="override saved provider selection"
    )
    serve.add_argument(
        "--startup-timeout-ms",
        type=int,
        default=5000,
        help="worker startup budget for laptops; hook deadline stays 250 ms",
    )
    commands.add_parser(
        "demo", help="run isolated HTTP checks including plugin timeout and recovery, then exit"
    )
    doctor = commands.add_parser(
        "doctor", help="check this installed runtime and plugin configuration"
    )
    doctor.add_argument("--config")
    health = commands.add_parser("health", help="check a running server")
    health.add_argument("--url", default="http://127.0.0.1:8000")
    chat = commands.add_parser("chat", help="send a prompt to a running server")
    chat.add_argument("prompt")
    chat.add_argument("--url", default="http://127.0.0.1:8000")
    init = commands.add_parser("init", help="create an editable third-party A/B plugin workspace")
    init.add_argument("directory", nargs="?", default="gateway-demo")
    plugins = commands.add_parser(
        "plugins", help="validate and list configured plugins in execution order"
    )
    plugins.add_argument("--config")
    commands.add_parser("setup", help="connect DeepSeek with hidden key entry; no file editing")
    commands.add_parser("status", help="show selected provider/model without showing the key")
    commands.add_parser("logout", help="remove your saved provider key; restart any running server")
    args = parser.parse_args(argv)
    try:
        if args.command == "setup":
            from .setup import run_setup

            run_setup()
            return 0
        if args.command == "logout":
            from .credentials import remove_credentials

            removed = remove_credentials()
            print(
                "Saved key removed. Restart any running gateway; existing server memory is unchanged."
                if removed
                else "No saved key to remove."
            )
            return 0
        if args.command == "status":
            from .credentials import load_credentials

            credentials = load_credentials()
            print(
                f"Provider: deepseek | Model: {credentials.model} | Key: saved (hidden)"
                if credentials
                else "Provider: fake | No key saved. Run llmgw setup to connect DeepSeek."
            )
            return 0
        if args.command in ("serve", "doctor", "plugins"):
            path = prepare_config(args.config)
            from .config import instantiate_plugins, read_plugin_paths

            paths = read_plugin_paths(path)
            instantiate_plugins(paths)
            if args.command == "doctor":
                from .credentials import load_credentials

                credentials = load_credentials()
                print(
                    f"Gateway {version('modular-llm-gateway')} | {platform.system()} {platform.machine()} | Python {platform.python_version()}"
                )
                print(f"Runtime: {sys.executable}\nConfig: {path}")
                print(
                    f"Provider: deepseek | Model: {credentials.model} | Key: saved (hidden)"
                    if credentials
                    else "Provider: fake (no account or API key required). Connect with llmgw setup."
                )
                print(f"PASS: {len(paths)} configured plugins are importable")
                return 0
            if args.command == "plugins":
                for index, name in enumerate(paths, 1):
                    print(f"{index}. {name}")
                return 0
            if not 1 <= args.port <= 65535:
                raise ValueError("port must be between 1 and 65535")
            import uvicorn

            from .credentials import load_credentials
            from .deepseek import DeepSeekProvider
            from .main import create_app

            credentials = None if args.provider == "fake" else load_credentials()
            if args.provider == "deepseek" and credentials is None:
                raise ValueError("No DeepSeek key saved. Run llmgw setup first.")
            provider = DeepSeekProvider(credentials) if credentials else None
            app = create_app(
                str(path), startup_timeout_ms=args.startup_timeout_ms, provider=provider
            )
            selected = f"deepseek ({credentials.model})" if credentials else "fake"
            print(
                f"Gateway: http://{args.host}:{args.port} | API docs: /docs | Provider: {selected}",
                flush=True,
            )
            if credentials is None:
                print(
                    "To connect your DeepSeek account, run llmgw setup once, then restart the server.",
                    flush=True,
                )
            print(
                "Ctrl+C to stop. This local demo has no authentication; keep it on loopback.",
                flush=True,
            )
            uvicorn.run(app, host=args.host, port=args.port, access_log=False)
        elif args.command == "demo":
            from .demo import run_demo

            run_demo()
        elif args.command == "init":
            init_workspace(args.directory)
        elif args.command in ("chat", "health"):
            code, body, correlation = request_json(
                args.url, args.prompt if args.command == "chat" else None
            )
            print(json.dumps(body, indent=2))
            if correlation:
                print(f"Request ID: {correlation}", file=sys.stderr)
            return 0 if code == 200 else 1
        return 0
    except (KeyboardInterrupt, EOFError):
        print("\nCanceled. Saved provider settings were not changed.", file=sys.stderr)
        return 130
    except (OSError, ValueError, RuntimeError, ImportError, AttributeError, URLError) as error:
        print(f"llmgw: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
