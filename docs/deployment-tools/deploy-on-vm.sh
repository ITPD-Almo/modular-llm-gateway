#!/usr/bin/env bash
# Derived from the reviewed docs/deployment.md at f07b2511cedbb501da327acd2c80bb7c966fbc4a.
# Run ON THE VM, invoked through SSH from a campus computer, after #98 lands.
# Usage: bash deploy-on-vm.sh staging FULL_SHA [PORT]
# Production additionally requires STAGING_QRT_PASSED=1 after the actual test.
set -euo pipefail
umask 077
if (( $# < 2 || $# > 3 )); then
    printf '%s\n' 'Usage: deploy-on-vm.sh staging|production FULL_SHA [PORT]' >&2
    exit 2
fi
environment=$1
RELEASE_COMMIT=$2
case "$environment" in
    staging) port=${3:-8001} ;;
    production) port=${3:-8002} ;;
    *) printf '%s\n' 'Environment must be staging or production' >&2; exit 2 ;;
esac
[[ "$RELEASE_COMMIT" =~ ^[0-9a-f]{40}$ ]] || { printf '%s\n' 'Use a full reviewed 40-character main SHA' >&2; exit 2; }
[[ "$port" =~ ^[1-9][0-9]{3,4}$ ]] || { printf '%s\n' 'Invalid port' >&2; exit 2; }
(( port > 1024 && port < 65536 )) || { printf '%s\n' 'Port must be 1025-65535' >&2; exit 2; }
DEPLOY_ROOT="$HOME/.local/share/llmgw-deploy"
[[ ! -L "$DEPLOY_ROOT" ]] || { printf '%s\n' 'Refusing a symlink deployment root' >&2; exit 2; }
bind_host=127.0.0.1
provider=fake
if [[ -f "$DEPLOY_ROOT/access-control/nginx.conf" ]]; then
    # Preserve the authenticated HTTPS front door even if its service is stopped.
    # Never fall back to an anonymous LAN backend on a protected installation.
    bind_host=127.0.0.1
    case "$environment:$port" in
        staging:8001|staging:18001) port=18001 ;;
        production:8002|production:18002) port=18002 ;;
        *) printf '%s\n' 'Protected deployments use backend ports 18001/18002' >&2; exit 2 ;;
    esac
fi
if [[ -f "$DEPLOY_ROOT/$environment/.env" ]]; then
    while IFS= read -r setting; do
        case "$setting" in
            GATEWAY_PROVIDER=fake) provider=fake ;;
            GATEWAY_PROVIDER=deepseek) provider=deepseek ;;
        esac
    done < "$DEPLOY_ROOT/$environment/.env"
fi
if [[ "$environment" == production ]]; then
    [[ "${STAGING_QRT_PASSED:-}" == 1 ]] || { printf '%s\n' 'Run the real staging QRT first; set STAGING_QRT_PASSED=1 only after a passing result' >&2; exit 2; }
    [[ -f "$DEPLOY_ROOT/staging/current-ref" ]] || { printf '%s\n' 'No staged source ref exists' >&2; exit 2; }
    [[ "$(cat "$DEPLOY_ROOT/staging/current-ref")" == "$RELEASE_COMMIT" ]] || { printf '%s\n' 'Production SHA must equal the staged SHA' >&2; exit 2; }
    [[ ! -e "$DEPLOY_ROOT/staging/normal.env" ]] || { printf '%s\n' 'Restore normal staging after the slow-plugin test first' >&2; exit 2; }
    systemctl --user is-active --quiet llmgw-staging.service
fi
mkdir -p "$DEPLOY_ROOT" "$HOME/.config/systemd/user"
chmod 700 "$DEPLOY_ROOT"
export DEPLOY_ROOT RELEASE_COMMIT

deploy_environment() (
    set -eu
    environment=$1
    port=$2
    [[ "$RELEASE_COMMIT" =~ ^[0-9a-f]{40}$ ]]
    case "$environment" in staging|production) ;; *) exit 1 ;; esac
    [[ "$port" =~ ^[0-9]+$ ]] && ((port > 1024 && port < 65536))
    root="$DEPLOY_ROOT/$environment"
    source_dir="$root/releases/$RELEASE_COMMIT/source"
    mkdir -p "$root/bin" "$root/config" "$source_dir"
    chmod 700 "$root" "$root/config"
    curl -fsSL "https://github.com/ITPD-Almo/modular-llm-gateway/archive/$RELEASE_COMMIT.tar.gz" \
        -o "$root/releases/$RELEASE_COMMIT/source.tar.gz"
    tar -xzf "$root/releases/$RELEASE_COMMIT/source.tar.gz" -C "$source_dir" --strip-components=1
    test -f "$source_dir/install.sh"
    # Stop only this application's service before replacing its private runtime.
    if systemctl --user cat "llmgw-$environment.service" >/dev/null 2>&1; then
        systemctl --user stop "llmgw-$environment.service"
    fi
    if test -f "$root/current-ref"; then
        cp "$root/current-ref" "$root/previous-ref"
        cp "$root/.env" "$root/previous.env"
    fi
    XDG_DATA_HOME="$root/data" XDG_CONFIG_HOME="$root/config" GATEWAY_BIN_DIR="$root/bin" \
        sh "$source_dir/install.sh" --ref "$RELEASE_COMMIT" --no-demo
    # Keep the operator's normal plugin configuration across upgrades.
    test -f "$root/plugins.json" || cp "$source_dir/config/plugins.json" "$root/plugins.json"
    cat > "$root/.env" <<ENV
GATEWAY_CONFIG="$root/plugins.json"
GATEWAY_PLUGIN_TIMEOUT_MS=250
GATEWAY_MAX_WORKERS=4
GATEWAY_WORKER_STARTUP_TIMEOUT_MS=5000
GATEWAY_HOST=$bind_host
GATEWAY_PORT=$port
GATEWAY_PROVIDER=$provider
GATEWAY_STARTUP_TIMEOUT_MS=5000
XDG_DATA_HOME="$root/data"
XDG_CONFIG_HOME="$root/config"
GATEWAY_BIN_DIR="$root/bin"
PYTHONPATH="$source_dir"
ENV
    chmod 600 "$root/.env"
    cat > "$root/run" <<'RUN'
#!/bin/sh
set -eu
cd -- "$(dirname -- "$0")"
set -a
. ./.env
set +a
exec ./bin/llmgw serve --host "$GATEWAY_HOST" --port "$GATEWAY_PORT" \
    --provider "$GATEWAY_PROVIDER" --config "$GATEWAY_CONFIG" \
    --startup-timeout-ms "$GATEWAY_STARTUP_TIMEOUT_MS"
RUN
    chmod 700 "$root/run"
    cat > "$HOME/.config/systemd/user/llmgw-$environment.service" <<UNIT
[Unit]
Description=Modular LLM Gateway $environment
After=network.target

[Service]
Type=simple
WorkingDirectory=$root
ExecStart="$root/run"
Restart=on-failure
RestartSec=2
UMask=0077

[Install]
WantedBy=default.target
UNIT
    systemctl --user daemon-reload
    printf '%s\n' "$RELEASE_COMMIT" > "$root/current-ref"
    systemctl --user enable --now "llmgw-$environment.service"
    systemctl --user is-active "llmgw-$environment.service"
)

deploy_environment "$environment" "$port"
