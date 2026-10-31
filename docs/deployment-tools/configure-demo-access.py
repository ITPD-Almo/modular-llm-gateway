#!/usr/bin/env python3
"""Private VM operations: isolated Nginx HTTPS/code gate; no product changes."""

import argparse
import base64
import ipaddress
import json
import os
import re
import secrets
import shutil
import signal
import socket
import ssl
import subprocess
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import HTTPSHandler, ProxyHandler, Request, build_opener

BASE = Path.home() / ".local/share/llmgw-deploy"
ROOT = BASE / "access-control"
SHA = "ba6d8a050e443dc13e69e4c052f4d5b766201e75"
ROLES = ("owner", "ta", "customer")
ENVIRONMENTS = {"staging": (8001, 18001), "production": (8002, 18002)}
MARKER = "LLMGW private demo access"


def run(args, *, stdin=None):
    result = subprocess.run(args, input=stdin, text=True, capture_output=True, timeout=60)
    if result.returncode:
        (ROOT / "private-command-error.log").write_text(result.stdout + result.stderr)
        raise RuntimeError("Command failed; inspect the private command log")
    return result.stdout.strip()


def write(path, text):
    path.write_text(text)
    path.chmod(0o600)


def config(servers, *, rehearsal=False):
    blocks = []
    for environment, listen, backend in servers:
        blocks.append(f'''
    server {{
        listen {listen} ssl;
        server_name _;
        ssl_certificate "{ROOT / "server.crt"}";
        ssl_certificate_key "{ROOT / "server.key"}";
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_session_cache shared:LLMGW_TLS:1m;
        ssl_session_timeout 5m;
        auth_basic "LLMGW {environment}";
        auth_basic_user_file "{ROOT / (environment + ".htpasswd")}";
        limit_req zone=LLMGW_DEMO burst=2 nodelay;
        limit_req_status 429;
        location / {{
            proxy_pass http://127.0.0.1:{backend};
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_set_header Authorization "";
            proxy_set_header Proxy-Authorization "";
            proxy_set_header Host $http_host;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-For "";
            proxy_connect_timeout 3s;
            proxy_read_timeout 60s;
            proxy_send_timeout 10s;
            proxy_next_upstream off;
            proxy_cache off;
            proxy_hide_header Cache-Control;
            add_header Cache-Control "no-store" always;
        }}
    }}''')
    pid = "rehearsal.pid" if rehearsal else "nginx.pid"
    return f'''# {MARKER}; independent of all system Nginx configuration.
worker_processes 1;
pid "{ROOT / pid}";
error_log "{ROOT / "private-nginx-error.log"}" warn;
events {{ worker_connections 128; }}
http {{
    access_log off;
    server_tokens off;
    client_max_body_size 16k;
    map $uri $llmgw_chat_path {{
        default 0;
        ~^/v1/chat/completions/?$ 1;
    }}
    map "$llmgw_chat_path:$remote_user" $llmgw_rate_key {{
        default "";
        ~^1:(ta|customer)$ "$server_port:$remote_user";
    }}
    limit_req_zone $llmgw_rate_key zone=LLMGW_DEMO:1m rate=6r/m;
    client_body_temp_path "{ROOT / "client-temp"}";
    proxy_temp_path "{ROOT / "proxy-temp"}";
    send_timeout 15s;
    keepalive_timeout 15s;
{"".join(blocks)}
}}
'''


def nginx_args(path):
    nginx = shutil.which("nginx")
    if not nginx:
        raise RuntimeError("Nginx is required; do not install or alter system services implicitly")
    return [nginx, "-p", str(ROOT) + "/", "-c", str(path)]


def prepare(host):
    host = str(ipaddress.IPv4Address(host))
    if ROOT.is_symlink():
        raise RuntimeError("Refusing a symlink access-control root")
    ROOT.mkdir(mode=0o700, parents=True, exist_ok=True)
    ROOT.chmod(0o700)
    for name in ("client-temp", "proxy-temp"):
        (ROOT / name).mkdir(mode=0o700, exist_ok=True)
    if (ROOT / "private-codes.json").exists():
        existing = json.loads((ROOT / "private-codes.json").read_text())
        if existing["vm_ipv4"] != host:
            raise RuntimeError("Prepared certificate belongs to a different host; review migration")
    else:
        credentials = {
            "vm_ipv4": host,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "environments": {
                env: {role: secrets.token_urlsafe(24) for role in ROLES} for env in ENVIRONMENTS
            },
        }
        write(ROOT / "private-codes.json", json.dumps(credentials, indent=2) + "\n")
        for env, users in credentials["environments"].items():
            rows = [
                name + ":" + run(["openssl", "passwd", "-6", "-stdin"], stdin=code + "\n")
                for name, code in users.items()
            ]
            write(ROOT / (env + ".htpasswd"), "\n".join(rows) + "\n")
    if not (ROOT / "ca.crt").exists():
        run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:3072",
                "-nodes",
                "-sha256",
                "-days",
                "365",
                "-subj",
                "/CN=LLMGW University Demo CA",
                "-addext",
                "basicConstraints=critical,CA:TRUE,pathlen:0",
                "-addext",
                "keyUsage=critical,keyCertSign,cRLSign",
                "-keyout",
                str(ROOT / "ca.key"),
                "-out",
                str(ROOT / "ca.crt"),
            ]
        )
    if not (ROOT / "server.crt").exists():
        run(
            [
                "openssl",
                "req",
                "-new",
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-sha256",
                "-subj",
                "/CN=LLMGW University Demo",
                "-keyout",
                str(ROOT / "server.key"),
                "-out",
                str(ROOT / "server.csr"),
            ]
        )
        write(
            ROOT / "server-extensions.cnf",
            f"subjectAltName=IP:{host},IP:127.0.0.1\nbasicConstraints=critical,CA:FALSE\n"
            "keyUsage=critical,digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth\n",
        )
        run(
            [
                "openssl",
                "x509",
                "-req",
                "-in",
                str(ROOT / "server.csr"),
                "-CA",
                str(ROOT / "ca.crt"),
                "-CAkey",
                str(ROOT / "ca.key"),
                "-CAcreateserial",
                "-days",
                "90",
                "-sha256",
                "-extfile",
                str(ROOT / "server-extensions.cnf"),
                "-out",
                str(ROOT / "server.crt"),
            ]
        )
    for path in ROOT.iterdir():
        if path.is_file():
            path.chmod(0o600)
    write(
        ROOT / "nginx.conf",
        config([(env, str(front), back) for env, (front, back) in ENVIRONMENTS.items()]),
    )
    run(nginx_args(ROOT / "nginx.conf") + ["-t"])
    return {
        "prepared": True,
        "roles": list(ROLES),
        "certificate": "Private demo CA; explicit client trust required",
        "product_code_changed": False,
        "system_nginx_changed": False,
    }


def fetch(url, credentials=None, *, payload=None, trust=True):
    context = (
        ssl.create_default_context(cafile=str(ROOT / "ca.crt"))
        if trust
        else ssl.create_default_context()
    )
    headers = {"Content-Type": "application/json"}
    if credentials:
        headers["Authorization"] = (
            "Basic " + base64.b64encode(":".join(credentials).encode()).decode()
        )
    request = Request(
        url, headers=headers, data=None if payload is None else json.dumps(payload).encode()
    )
    opener = build_opener(ProxyHandler({}), HTTPSHandler(context=context))
    try:
        response = opener.open(request, timeout=5)
    except HTTPError as error:
        response = error
    with response:
        return response.status, response.read(1024 * 1024), response.headers


def rehearse():
    hits = []

    class Stub(BaseHTTPRequestHandler):
        def do_GET(self):
            hits.append(1)
            body = json.dumps(
                {
                    "authorization_forwarded": self.headers.get("Authorization"),
                    "proxy_authorization_forwarded": self.headers.get("Proxy-Authorization"),
                }
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Stub)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    path = ROOT / "rehearsal.conf"
    write(
        path,
        config(
            [
                (env, f"127.0.0.1:{18443 + index}", server.server_port)
                for index, env in enumerate(ENVIRONMENTS)
            ],
            rehearsal=True,
        ),
    )
    run(nginx_args(path) + ["-t"])
    log = open(ROOT / "private-rehearsal-process.log", "ab")
    process = subprocess.Popen(
        nginx_args(path) + ["-g", "daemon off;"], stdout=log, stderr=log, start_new_session=True
    )
    checks = []
    codes = json.loads((ROOT / "private-codes.json").read_text())["environments"]
    try:
        for _ in range(50):
            if process.poll() is not None:
                raise RuntimeError("Rehearsal proxy stopped; inspect its private log")
            try:
                if fetch("https://127.0.0.1:18443/health")[0] == 401:
                    break
            except OSError:
                pass
            time.sleep(0.1)
        for index, env in enumerate(ENVIRONMENTS):
            base = f"https://127.0.0.1:{18443 + index}"
            for endpoint in ("/health", "/docs", "/openapi.json", "/v1/chat/completions"):
                before = len(hits)
                status, body, headers = fetch(base + endpoint)
                checks.append(
                    status == 401 and bool(headers.get("WWW-Authenticate")) and len(hits) == before
                )
            for user in ROLES:
                status, body, _ = fetch(base + "/health", (user, codes[env][user]))
                checks.append(
                    status == 200
                    and json.loads(body)
                    == {"authorization_forwarded": None, "proxy_authorization_forwarded": None}
                )
            before = len(hits)
            checks.append(
                fetch(base + "/health", ("ta", "incorrect-demo-code"))[0] == 401
                and len(hits) == before
            )
            other = "production" if env == "staging" else "staging"
            checks.append(fetch(base + "/health", ("ta", codes[other]["ta"]))[0] == 401)
            statuses = [
                fetch(base + "/v1/chat/completions", ("ta", codes[env]["ta"]))[0] for _ in range(4)
            ]
            checks.append(statuses[:3] == [200, 200, 200] and statuses[3] == 429)
            checks.append(
                fetch(base + "/v1/chat/completions", ("owner", codes[env]["owner"]))[0] == 200
            )
            checks.append(
                fetch(
                    base + "/v1/chat/completions",
                    ("owner", codes[env]["owner"]),
                    payload={"oversize": "x" * 17000},
                )[0]
                == 413
            )
        try:
            fetch("https://127.0.0.1:18443/health", trust=False)
            checks.append(False)
        except OSError:
            checks.append(True)
        result = {
            "checks": len(checks),
            "all_passed": all(checks),
            "coverage": "Both proxy environments: anonymous/wrong/cross-env denial, all roles allowed, auth headers stripped, CA trust, demo chat rate limit and 16 KiB body cap",
        }
        write(ROOT / "rehearsal-summary.json", json.dumps(result, indent=2) + "\n")
        if not result["all_passed"]:
            raise RuntimeError("Access-control rehearsal failed")
        return result
    finally:
        if process.poll() is None:
            process.send_signal(signal.SIGQUIT)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=5)
        log.close()
        server.shutdown()
        server.server_close()


def activate():
    proof = json.loads((ROOT / "rehearsal-summary.json").read_text())
    assert proof["all_passed"], "Rehearse before activation"
    unit = Path.home() / ".config/systemd/user/llmgw-demo-access.service"
    if unit.exists():
        raise RuntimeError(
            "Access service already exists; review an upgrade rather than overwriting it"
        )
    present = {
        env: ports for env, ports in ENVIRONMENTS.items() if (BASE / env / "current-ref").exists()
    }
    assert "staging" in present, "Deploy staging before activating the access gate"
    for env, (front, backend) in present.items():
        directory = BASE / env
        assert (directory / "current-ref").read_text().strip() == SHA
        assert not (directory / "normal.env").exists()
        assert "examples/slow-plugins.json" not in (directory / ".env").read_text()
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", backend))
    run(nginx_args(ROOT / "nginx.conf") + ["-t"])
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for env, (front, backend) in present.items():
        directory = BASE / env
        original = (directory / ".env").read_text()
        write(directory / ("before-access-" + stamp + ".env"), original)
        lines = original.splitlines()
        assert sum(line.startswith("GATEWAY_HOST=") for line in lines) == 1
        assert sum(line.startswith("GATEWAY_PORT=") for line in lines) == 1
        lines = [
            "GATEWAY_HOST=127.0.0.1"
            if line.startswith("GATEWAY_HOST=")
            else f"GATEWAY_PORT={backend}"
            if line.startswith("GATEWAY_PORT=")
            else line
            for line in lines
        ]
        write(directory / ".env", "\n".join(lines) + "\n")
        run(["systemctl", "--user", "restart", f"llmgw-{env}.service"])
    # Backends now listen on loopback only. On a proxy-start failure leave them
    # private; do not silently restore anonymous LAN access.
    write(
        unit,
        f'''[Unit]
Description={MARKER}
After=network.target llmgw-staging.service llmgw-production.service

[Service]
Type=simple
ExecStart="{shutil.which("nginx")}" -p "{ROOT}/" -c "{ROOT / "nginx.conf"}" -g "daemon off;"
Restart=on-failure
RestartSec=2
UMask=0077
NoNewPrivileges=yes
KillMode=control-group
TimeoutStopSec=10

[Install]
WantedBy=default.target
''',
    )
    run(["systemctl", "--user", "daemon-reload"])
    run(["systemctl", "--user", "enable", "--now", "llmgw-demo-access.service"])
    codes = json.loads((ROOT / "private-codes.json").read_text())["environments"]
    for env, (front, backend) in present.items():
        for _ in range(50):
            try:
                status, body, _ = fetch(
                    f"https://127.0.0.1:{front}/health", ("owner", codes[env]["owner"])
                )
                if status == 200 and json.loads(body) == {"status": "ok"}:
                    break
            except (OSError, ValueError):
                pass
            time.sleep(0.1)
        else:
            raise RuntimeError(
                "Proxy readiness failed; backends remain private; inspect private logs"
            )
    return {
        "activated": True,
        "source_sha": SHA,
        "service": "llmgw-demo-access.service",
        "https_ports": [8001, 8002],
        "loopback_backend_ports": [18001, 18002],
        "ready_environments": list(present),
        "pending_environments": [e for e in ENVIRONMENTS if e not in present],
        "system_nginx_unchanged": True,
        "vpn_and_tailscale_configuration_unchanged": True,
    }


def main():
    global SHA
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "rehearse", "activate", "export"))
    parser.add_argument("--vm-ip")
    parser.add_argument(
        "--ref", default=SHA, help="Full reviewed source SHA already deployed to staging"
    )
    args = parser.parse_args()
    if not re.fullmatch("[0-9a-f]{40}", args.ref):
        parser.error("Use a full reviewed 40-character source SHA")
    SHA = args.ref
    if args.mode == "prepare":
        if not args.vm_ip:
            parser.error("prepare requires the private VM IPv4")
        result = prepare(args.vm_ip)
    elif args.mode == "rehearse":
        result = rehearse()
    elif args.mode == "activate":
        result = activate()
    else:
        result = json.loads((ROOT / "private-codes.json").read_text())
        result["ca_certificate"] = (ROOT / "ca.crt").read_text()
        result["ca_sha256_fingerprint"] = run(
            ["openssl", "x509", "-in", str(ROOT / "ca.crt"), "-noout", "-fingerprint", "-sha256"]
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
