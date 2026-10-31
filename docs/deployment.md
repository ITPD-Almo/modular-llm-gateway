# Deployment and environments

This is the manual deployment runbook for an operator on the university network.
Use [setup](setup.md) for source development, building and running locally, and [terminal installation](terminal.md) for installer prerequisites and supported platforms.
The commands below add the VM layout, separate service configuration, promotion and rollback.

## Environment map

| Environment | Product and checks | Access and state |
| --- | --- | --- |
| Development | Local source checkout; synthetic tests and developer demo | Contributor machine; local configuration, no production state |
| Integration | GitHub Actions product checks and QR-01's CI test | Hosted runners outside campus; no VM credentials and no deployment job |
| Staging | Candidate on the university VM; QR-02's deployed test | Campus clients; port 8001 by example, its own runtime, configuration and provider profile |
| Production | The same commit that passed staging; core-task verification | Customer on campus; port 8002 by example, separate runtime, configuration and provider profile |

The two ports are examples; check they are free before use.
A CI or local result does not prove campus reachability, and a staging result does not accept a story.
The product currently has no client authentication or TLS termination; this deployment uses the fake provider, synthetic messages and campus-restricted access.
Do not expose these ports to the public internet.

## VM and campus access

The course's required machine is the team's VM from the university portal: provision or recreate the assigned machine, set its password privately, and connect over SSH from campus.
Recreation destroys existing VM state: these instructions do not authorize recreating a shared or already-used machine.
Record its actual image, CPU architecture and resources in the private deployment evidence; this runbook requires Linux with systemd, a writable non-root service account, curl and tar, and internet access for the installer.

As of October 31, the owner reports that the instructor VM has not been supplied, that an existing university work VM is directly reachable on the university network, and that the TA approved its temporary use.
Tailscale/Funnel provides an additional outside access path; it does not change which client network the required deployment and tests must use.
The assignment VM is expected on Monday, November 2, according to the same owner update.
Record this temporary-host arrangement and its provenance in the week's report, preserve existing services and use an isolated application directory.
Owner-reported campus reachability still needs the actual campus deployment/test evidence; record overlay/external checks separately.

Read the address and login privately, then connect from the campus terminal:

```sh
read -r -p 'University VM IPv4 (private): ' VM_HOST
read -r -p 'VM service account: ' VM_USER
ssh "$VM_USER@$VM_HOST"
```

Verify the SSH host key against the portal or the machine administrator's trusted record.
The real address is in the private Moodle submission; there is no assumed domain name.
Keep actual IPv4 addresses, host names, overlay addresses, credentials and SSH configuration out of repository files, issue comments, CI logs and link-check exclusions.

The VM administrator must restrict the two HTTP ports to the university network and allow SSH as the university requires.
Check the existing firewall policy before changing it; preserve other applications' rules.
The administrator enables the service account's user services to survive logout and reboot once with `sudo loginctl enable-linger "$USER"` while logged in as that account.
Without lingering, do not claim that the user services survive logout.

## Configuration and service layout

Run the following VM commands as the unprivileged service account in Bash.
Do not use a shared home-wide `llmgw` installation for the two services.

```sh
umask 077
export DEPLOY_ROOT="$HOME/.local/share/llmgw-deploy"
mkdir -p "$DEPLOY_ROOT" "$HOME/.config/systemd/user"
chmod 700 "$DEPLOY_ROOT"
ss -ltn
```

Each of `$DEPLOY_ROOT/staging` and `$DEPLOY_ROOT/production` owns:

- `.env` (mode 600), the exported service settings; never inside the source repository.
- `data/llmgw/`, the private installer runtime and its source-ref receipt.
- `config/`, its private provider profile root, separate even while no key is saved.
- `bin/llmgw`, its managed launcher; `run`, the service launcher.
- `releases/<full-sha>/source/`, the exact source used for example plugins.
- `current-ref`, `previous-ref`, and `plugins.json`, the installed source record and editable normal plugin list.

The repository's `.env.example` lists the configuration shape; it contains no secrets.
`llmgw serve` does not read `.env` automatically: the `run` script below exports it and passes the host, port, provider and startup budget explicitly.
`GATEWAY_PLUGIN_TIMEOUT_MS` and `GATEWAY_MAX_WORKERS` are read by the application.
The CLI's explicit startup budget takes precedence over `GATEWAY_WORKER_STARTUP_TIMEOUT_MS`.
`PYTHONPATH` makes the pinned source's `examples.slow_plugin` importable; example modules are not part of the installed wheel.

For this release, `GATEWAY_PROVIDER=fake` prevents saved credentials from selecting a paid provider.
No API key is needed or stored for the core task.
If a later release uses DeepSeek, run `llmgw setup` with that environment's `XDG_CONFIG_HOME` and use distinct accounts/profiles; never put a key in `.env`, command arguments, a plugin dictionary or public evidence.
See [provider setup](terminal.md) for profile permissions and limitations.

## Install a candidate in staging

Before deploying, merge #92, #93, #95, #89 and the CI/QR-test task #98, and require green checks on the selected `main` commit.
Resolve and record a full 40-character SHA, rather than allowing `main` to move during promotion.
Do not pass a branch containing `/` to the installer.

In the campus terminal, determine the candidate from the reviewed repository and keep the value for both deployments:

```sh
git fetch origin main
git rev-parse origin/main
```

On the VM, paste that SHA and define this function once in the same Bash session:

```sh
while true; do
    read -r -p 'Reviewed full commit SHA: ' RELEASE_COMMIT || break
    [[ "$RELEASE_COMMIT" =~ ^[0-9a-f]{40}$ ]] && break
    printf '%s\n' 'Enter exactly 40 lowercase hexadecimal characters.' >&2
done
export RELEASE_COMMIT

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
GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=$port
GATEWAY_PROVIDER=fake
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

deploy_environment staging 8001
```

The function resets the service settings to the values above on each deploy; review them against the saved `previous.env` when promoting or rolling back an environment with intentional custom settings.
The existing `plugins.json` and private provider directory are retained.
An installer or startup failure stops this procedure: restore the prior deployment before trying a forward fix.
Do not deploy production yet.

## Staging verification and QR-02

In the campus terminal, set `STAGING_URL` privately to `http://<university-vm-ipv4>:8001`.
First verify normal operation:

```sh
curl --fail-with-body --max-time 5 "$STAGING_URL/health"
curl --fail-with-body --max-time 10 -i "$STAGING_URL/v1/chat/completions" \
    -H 'Content-Type: application/json' \
    -d '{"messages":[{"role":"user","content":"hello"}]}'
```

Expect HTTP 200, `{"status":"ok"}`, then `provider: fake`, the answer `fake: HELLO`, an `X-Request-ID`, the trace `metadata, uppercase`, and four request/response change records.
Health alone is only liveness and does not verify the plugin pipeline.

After #98 merges, run the exact QRT-01 procedure in [QR-02](quality-requirements/qr/QR-02.md) from campus.
To temporarily select that commit's slow-plugin configuration on staging, use the VM terminal:

```sh
stage="$DEPLOY_ROOT/staging"
cp "$stage/.env" "$stage/normal.env"
printf '\nGATEWAY_CONFIG="%s"\n' \
    "$stage/releases/$RELEASE_COMMIT/source/examples/slow-plugins.json" >> "$stage/.env"
systemctl --user restart llmgw-staging.service
```

The last setting overrides the normal config when the launcher sources `.env`.
Wait for staging health, then run QRT-01 without changing its commands or inventing a passing result.
After the run, including a failed run, restore the normal configuration and repeat the normal health/chat verification:

```sh
mv "$stage/normal.env" "$stage/.env"
chmod 600 "$stage/.env"
systemctl --user restart llmgw-staging.service
```

Keep the command, date, candidate SHA, environment, HTTP status/body, measured timings and the exact pass/fail comparison in private raw evidence.
Publish a sanitized result in the deployment PR description or a week-local evidence file and link it from the testing-plan row; keep QRT definitions free of results.
Remove actual addresses and host names, including those in connection errors or journal lines, before publication.
An overlay-only rehearsal is labelled as such and does not replace the deployed test from campus.
QRT-01's result covers its own criterion; it does not establish unmeasured parts of the full QR-02 scenario.

## Promote the same commit and verify production

Proceed only after the candidate's main CI and staging QRT pass, and normal staging is restored.
In the same VM session, retain the exact `RELEASE_COMMIT` and run:

```sh
deploy_environment production 8002
cmp "$DEPLOY_ROOT/staging/current-ref" "$DEPLOY_ROOT/production/current-ref"
systemctl --user is-active llmgw-staging.service llmgw-production.service
```

In a separate campus terminal, set `PRODUCTION_URL` privately to `http://<university-vm-ipv4>:8002` and perform the core task:

```sh
curl --fail-with-body --max-time 5 "$PRODUCTION_URL/health"
curl --fail-with-body --max-time 10 -i "$PRODUCTION_URL/v1/chat/completions" \
    -H 'Content-Type: application/json' \
    -d '{"messages":[{"role":"user","content":"hello"}]}'
```

Check the same normal response, trace and change records as staging, and open `$PRODUCTION_URL/docs` from campus.
Record the date, actual access network, exact deployed SHA and observed core-task outcome in sanitized release evidence for the week's report.
Share the real staging and production addresses privately for Moodle; do not commit them.
Do not run the slow-plugin quality test against production.

## Restart, inspect and roll back

```sh
systemctl --user restart llmgw-production.service
systemctl --user status llmgw-production.service --no-pager
journalctl --user -u llmgw-production.service -n 50 --no-pager
```

The launcher exports only its own `.env`; it does not depend on the operator's terminal state.
Journal output is private until sanitized.
Check `current-ref`, `previous-ref`, the install receipt, file permissions, selected port and plugin imports when startup fails.
Never restart an unrelated service or kill whatever happens to use a port.

For a previous tag that includes `install.sh`, resolve the tag to its full commit in the reviewed local repository and use the same deployment function:

```sh
git fetch origin --tags
git rev-parse 'PREVIOUS_TAG^{commit}'
```

On the VM, set `RELEASE_COMMIT` to that resolved SHA, then `deploy_environment production 8002`.
Repeat the campus core-task verification; roll back staging separately if necessary.
Restore any required custom settings from the saved environment file before restarting.
Do not move a published tag.

The existing `v0.2.0` predates the terminal installer, so it cannot be restored with `install.sh`.
For this first terminal release, keep the prior source deployment intact until verification passes.
If no prior deployment exists, record that fact; a first install has no previous running instance to restore.
To return specifically to `v0.2.0`, use its [versioned source setup](https://github.com/ITPD-Almo/modular-llm-gateway/blob/v0.2.0/docs/setup.md) in a separate directory and environment, and change this service's `run` launcher to execute that environment's `python -m uvicorn gateway.main:create_app --factory --host 0.0.0.0 --port "$GATEWAY_PORT"` from that checkout with its own default config.
Re-verify from campus before treating the rollback as recovered.
Do not claim that an older tag supports commands introduced later.

## Rework and release records

The [project plan](project-plan.md) owns the testing plan and the `REL-05` release record.
The Week 5 report owns the actual deployment evidence, access network and meeting/deployment deviations.
After code or configuration rework, repeat staging, the affected test and same-SHA production verification before tagging the commit production runs.
Verify that `llmgw --version` matches the intended release version before promotion.

If the course VM is unavailable or the alternative host is reachable only over the overlay, record the reason and the announced postponement date when known.
Coordinate a genuine `scripted`/`CI` fallback and its definition/result with the QR-test owner, or keep the deployed test `Not verified`.
Upgrade it when campus staging is available; an overlay check does not establish campus access.
