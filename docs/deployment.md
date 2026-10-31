# Deployment

Use [setup](setup.md) for source development and [terminal installation](terminal.md) for supported platforms, the installer and hidden-input provider setup. This guide owns the shared deployment; it does not repeat the local build recipe.

## Four environments

| Environment | Purpose | Access and configuration |
| --- | --- | --- |
| Development | Local implementation and synthetic plugin checks | Developer workstation, loopback by default |
| Integration | GitHub Actions lint, formatting, types, wheel build and tests | Hosted runners; synthetic credentials/providers; no deployment job or VM secrets |
| Staging | The reviewed candidate and deployed QR tests | University VM, HTTPS frontend 8001, separate runtime/profile/settings, private backend 18001 |
| Production | The identical source commit after staging verification | University VM, HTTPS frontend 8002, separate runtime/profile/settings, private backend 18002 |

The gateway application itself has no client authentication or TLS termination. The shared deployment puts an independent Nginx HTTPS/Basic-auth gate in front of both loopback-only backends. Anonymous health, documentation, OpenAPI and chat requests are denied. Codes prove possession, not a person's identity; `owner`, `ta` and `customer` have the same gateway API permissions. Each environment has different codes.

## VM and campus access

The required host is the team's university-portal VM, with SSH and production verification from a campus machine. Never recreate a shared VM or change its existing services without authorization.

On October 31, the owner reported that the TA approved temporary use of an existing university VM because the assignment VM had not been supplied. The replacement is expected November 2. Ali12hamdan confirmed campus Wi-Fi presence; Codex executed the recorded HTTP checks from that workstation with the VPN left running. The initial staging installation preceded that campus confirmation. Administration used Tailscale SSH; HTTP verification used the direct university IPv4 over Wi-Fi. These access levels and the host exception are recorded in the [Week 5 evidence](https://github.com/ITPD-Almo/modular-llm-gateway/pull/102).

Use `<university-vm-ipv4>` or a privately supplied SSH alias, never a real address in the repository. Real addresses, codes, route output and instructor access instructions belong in the private Moodle PDF. The administrator maintains network restrictions and account lingering; the recorded host has lingering enabled. The runbook does not change firewall rules or existing Nginx/Tailscale services.

The VM needs Linux with systemd user services, a non-root account, curl, tar, Python 3, OpenSSL and Nginx with SSL/Basic-auth support. An administrator supplies missing system packages. The helpers run as the service account without sudo and never write `/etc/nginx`.

## Configuration and layout

```sh
umask 077
DEPLOY_ROOT="$HOME/.local/share/llmgw-deploy"
mkdir -p "$DEPLOY_ROOT"
chmod 700 "$DEPLOY_ROOT"
```

Each environment owns `.env` (600), `config/` (700), installer runtime `data/`, `bin/llmgw`, `run`, `plugins.json`, versioned source under `releases/<sha>/source/`, and `current-ref`/`previous-ref` receipts. The launcher exports `.env`; `llmgw serve` does not load it itself. `.env.example` contains placeholders only. A provider key belongs only in the private profile, never `.env`, arguments, plugin dictionaries or public evidence.

`access-control/` owns its independent Nginx configuration, PID, disabled access log, private error log, temporary directories, salted SHA-512 password hashes and TLS files. Its private export contains the original high-entropy demo codes for private distribution. Protect it as a credential store. Server/CA keys and exports are mode 600 under a 700 directory. The user service is `llmgw-demo-access.service`; it leaves system Nginx unchanged.

Public frontends use TLS 1.2/1.3. The project demo CA certificate is [available here](deployment-tools/demo-ca.crt); it contains no deployment address or private key. Verify its fingerprint against the Moodle PDF before trusting it in a dedicated browser profile, or supply it explicitly to curl. Never disable certificate verification. The existing CA signs a 90-day server certificate for the privately supplied VM IPv4 and loopback; administrators must renew it before expiry and distribute changed trust material privately when migrating hosts.

TA/Customer chats have a six-per-minute sustained limit with an initial burst of thirteen requests (HTTP 429 when exceeded); the private Owner code is exempt for operator checks. Request bodies are capped at 16 KiB. The provider adapter caps generated output at 128 tokens and retries none. These are request/output controls, not a monetary spending cap.

## Manual deployment and promotion

Use the maintained [installer helper](deployment-tools/deploy-on-vm.sh), [access-gate helper](deployment-tools/configure-demo-access.py), [QRT helper](deployment-tools/campus-qr02.sh) and [normal core collector](deployment-tools/collect-core-evidence.py). Review their source before execution and copy them into a private VM operator directory. Keep the reviewed operator-tool revision with the private deployment receipt. `export` writes secrets: redirect its output to a private file and never paste it into chat or a PR.

Before installing, require reviewed `main` and green CI, resolve a full 40-character SHA once, and keep it for both environments. `--ref` accepts a SHA or tag, not a branch containing `/`. Choose free ports, preserve existing applications, and enable account lingering through the administrator if needed.

On the VM, using the copied helpers:

```sh
read -r -p 'Reviewed full source SHA: ' RELEASE_COMMIT
bash deploy-on-vm.sh staging "$RELEASE_COMMIT" 8001
read -r -p 'University VM IPv4 (private): ' VM_HOST
python3 configure-demo-access.py prepare --vm-ip "$VM_HOST" --ref "$RELEASE_COMMIT"
python3 configure-demo-access.py rehearse
python3 configure-demo-access.py activate --ref "$RELEASE_COMMIT"
umask 077
python3 configure-demo-access.py export > private-demo-access.json
```

The initial installer binds staging to loopback. The gate moves that backend to loopback 18001 and exposes authenticated HTTPS on 8001. It also prepares the protected production frontend, which is not ready until the production backend is installed. Activation is first-time only and refuses to overwrite an existing access service. Preparation rehearses TLS/auth against an isolated stub; it is not the deployed QRT. A startup failure leaves backends private rather than silently restoring anonymous LAN access.

On an already protected host, the installer helper detects the gate, keeps loopback backend ports, retains the selected provider and private profiles, and stops only the environment being upgraded. It downloads the pinned source, installs that ref in its own runtime, retains the normal plugin list and writes its receipt. An install failure stops promotion; follow rollback below.

## Staging verification and QR-02

From the campus client, set `STAGING_URL=https://<university-vm-ipv4>:8001` privately. Supply the verified CA and stage code using a mode-600 curl configuration, not a password in shell history:

```text
cacert = "/private/path/demo-ca.crt"
user = "owner:PRIVATE_STAGING_CODE"
```

A private environment-specific `CURL_HOME` containing this as `.curlrc` also lets the exact curl commands in [QR-02 QRT-01](quality-requirements/qr/QR-02.md#qrt-01) use those credentials. Do not share that file publicly. The supplied QRT helper accepts the same private configuration through `GATEWAY_CURL_CONFIG` and bypasses HTTP proxies; neither mechanism overrides VPN routing. Confirm physical campus presence and inspect the destination route; the recorded checks also matched the actual socket source to Wi-Fi.

The QRT uses the prescribed fake provider and slow-plugin configuration. On the VM:

```sh
stage="$DEPLOY_ROOT/staging"
test ! -e "$stage/normal.env"
cp "$stage/.env" "$stage/normal.env"
printf '\nGATEWAY_PROVIDER=fake\nGATEWAY_CONFIG="%s"\n' \
  "$stage/releases/$RELEASE_COMMIT/source/examples/slow-plugins.json" >> "$stage/.env"
chmod 600 "$stage/.env" "$stage/normal.env"
systemctl --user restart llmgw-staging.service
```

After authenticated staging health is ready, run from the campus client:

```sh
GATEWAY_CURL_CONFIG=/private/path/staging-curl.conf \
  bash campus-qr02.sh "$STAGING_URL" "$RELEASE_COMMIT" YOUR_GITHUB_USERNAME campus
```

Keep its raw bodies/errors privately and publish only sanitized statuses, timings, runner, date, source receipt and the actual client network. The pass criterion is named HTTP 504 within one second, subsequent health 200 within one second and ten correct healthy chats. This QRT does not measure the full scenario's thread/process-growth condition.

Whatever the result, restore normal staging on the VM, then verify its normal pipeline:

```sh
mv "$stage/normal.env" "$stage/.env"
chmod 600 "$stage/.env"
systemctl --user restart llmgw-staging.service
```

For fake normal operation, the [core collector](deployment-tools/collect-core-evidence.py) accepts `--ca-cert`, `--access-file` (the private export), `--access-user`, `--expected-sha`, environment and actual network. Expect health, `fake: HELLO`, the `metadata, uppercase` trace, four change records and a request ID. For a configured live provider, verify HTTP 200, the selected provider/model, a nonempty synthetic reply and the same trace/change/request-ID fields; do not apply the collector's fake-answer assertion to a real provider. Served Swagger HTML is distinct from a browser-rendering check.

## Production and provider profiles

Only after the actual campus staging QRT passes and normal staging is restored:

```sh
STAGING_QRT_PASSED=1 bash deploy-on-vm.sh production "$RELEASE_COMMIT" 8002
```

The guard checks the staged ref, active service and normal-configuration restoration. The gate is already present, so the new production backend binds to loopback 18002 and its protected frontend remains 8002. Match server-side `current-ref`/install receipts in both environments; HTTP metadata alone cannot prove the deployed source SHA.

Verify production from campus at `https://<university-vm-ipv4>:8002`: health, one chat through the actual plugins, provider/model, response content, both plugin stages and request ID. Record status, timings, exact commit and access network. If it fails, roll back before release. Do not infer Customer acceptance from passing tests.

For an optional live provider, run hidden-input `llmgw setup` with the target environment's `XDG_CONFIG_HOME` set to its private `config/` directory. This validates the key by listing models, not paid generation. After success set only `GATEWAY_PROVIDER=deepseek` in `.env`, restart staging, run one bounded synthetic live chat, then repeat for production. An owner-authorized profile may instead be copied over encrypted SSH stdin through `save_credentials`; never embed the value in arguments, `.env`, curl bodies or logs. Stored profiles are permission-protected plaintext, not encrypted; administrators and trusted plugins running as that user can read them.

The October 31 deployment uses separate private profile files containing the same owner-supplied `deepseek-flash` account key, so both environments spend that account's balance. TA/Customer codes grant HTTP access only and are not provider keys. Users installing their own copy retain `llmgw setup`; shared per-visitor provider-key storage is not implemented. A changed/removed profile requires a service restart, and local logout does not revoke other copies of the key. Revoke/rotate at the provider when necessary. Prefer distinct provider keys/accounts for later staging/production operation.

## Rollback and continuity

Resolve the previous known-good tag to its full SHA and reinstall it in staging with the helper, rerun the appropriate QRT and normal checks, then promote that same SHA to production. Keep the HTTPS gate, loopback bindings, private profiles and normal plugin configuration throughout. On first deployment there may be no previously verified shared release; stop the affected service and report the failure rather than claiming an unavailable rollback was tested. Do not move a published tag to repair a deployment.

For `v0.2.0`, which predates the installed CLI, use its [versioned setup](https://github.com/ITPD-Almo/modular-llm-gateway/blob/v0.2.0/docs/setup.md) in a separate private runtime and launch its app on the same loopback backend port behind the gate. Preserve a compatible normal configuration and verify before switching. Never restore the older public-bind recipe on a protected host.

When the assignment VM arrives, prepare it without recreating this shared host, deploy the reviewed ref, provision new private credentials/certificates as required, and repeat staging QRT plus campus production verification. Update instructor access privately and preserve old submitted endpoints until instructors have usable replacement access. Keep all addresses, hostname mappings, private keys and codes out of the repository.
