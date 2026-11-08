# Week 5 deployment evidence

These are dated operational checkpoints. Statements about pending work describe the time of that checkpoint; the final release and submission state are indexed by [the Week 5 report](README.md).

## Campus deployment and verification evidence — 2026-10-31

The release candidate is [`ba6d8a050e443dc13e69e4c052f4d5b766201e75`](https://github.com/ITPD-Almo/modular-llm-gateway/commit/ba6d8a050e443dc13e69e4c052f4d5b766201e75), package **0.5.0**. [Main product CI](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/41227201276) passed: **81 tests in 20.90 s**, with lint, format, type checking and wheel build passing. All six main workflows passed.

**Runner and network:** Ali12hamdan confirmed he was physically connected to university Wi-Fi. Codex executed the HTTP checks on his workstation; these were agent-run checks for Ali, not checks performed by Mohammed-Nour. The VM destination route used the Wi-Fi interface, and the actual HTTP connection's source address matched that interface while its peer matched the private university VM IPv4. The VPN interface remained up. HTTP proxies were bypassed for these requests, and no VPN or routing setting was changed. Physical presence is owner-confirmed; routing and socket evidence is retained privately.

**Administration:** Ali's agent installed staging and then the identical source commit in production through Tailscale SSH, using the reviewed deployment runbook. The original staging installation preceded the owner's campus-presence confirmation; production installation and the recorded campus HTTP checks followed that confirmation. Do not infer a campus origin for the earlier staging installation. The temporary university host and TA permission remain owner-reported, with the assignment VM expected November 2. Existing Tailscale Serve/Funnel configuration was unchanged; no new public exposure was configured.

### QR-02 QRT-01: Passes

Executed against staging in the selected commit's temporary `examples/slow-plugins.json` configuration at **2026-10-31 19:11:02 UTC (22:11:02 Europe/Moscow)**, with a 250 ms hook deadline and the fake provider. Helper exit status: **0**.

| Observation | Actual result | Criterion |
| --- | --- | --- |
| Initial health | HTTP 200, `{"status":"ok"}` | Expected body and status |
| Hung `sleep` request | HTTP 504 in **0.408615 s**, naming `SlowPlugin` and the request stage | HTTP 504 within 1.000 s, named plugin/stage |
| Immediate health | HTTP 200 in **0.006403 s** | HTTP 200 within 1.000 s |
| Ten subsequent `hello` chats | **10/10 HTTP 200**, each exactly `fake: HELLO` | All ten succeed with the correct content |

The ten normal-chat durations in order were **0.090018, 0.087657, 0.089023, 0.088814, 0.088824, 0.086416, 0.086370, 0.089259, 0.089211 and 0.088095 seconds**.

After the test, normal staging configuration was restored at **19:11:26 UTC**, and its normal core task was rechecked from the campus workstation at **19:11:39 UTC**. Health, chat, fake-provider identity, `fake: HELLO`, the `metadata, uppercase` trace, all four plugin-change records, a response request ID and served `/docs` HTML passed. Measured health/chat/docs times were **0.137 / 0.191 / 0.022 s**.

This result is the deployed QRT-01 result, separate from the earlier VM-local rehearsal. It does not establish the unmeasured twenty-timeout thread/process-growth part of the complete QR-02 scenario, and the numerical targets remain team proposals awaiting the Customer's verdict.

### Production core task: Passes

After the campus staging QRT and normal-configuration restoration, production was installed at the same full source commit. Campus core-task verification completed at **2026-10-31 19:13:07 UTC (22:13:07 Europe/Moscow)**, helper exit status **0**.

| Check | Result |
| --- | --- |
| Health | HTTP 200 with `{"status":"ok"}` |
| Chat through deployed plugins | HTTP 200, provider `fake`, answer `fake: HELLO` |
| Plugin order | `metadata, uppercase` |
| Change records | Four request/response plugin-change records |
| Correlation | Response `X-Request-ID` present |
| Documentation | `/docs` served Swagger UI HTML; browser rendering was not checked |
| Measured health/chat/docs times | **0.058 / 0.117 / 0.019 s** |

Final server-side inspection at **19:14:26 UTC** found both installations on the same source commit, version **0.5.0**, active and enabled user services, normal plugin configuration, fake provider, separate runtime/profile/configuration directories, settings mode **600** and profile-root mode **700**. Staging and production use separate ports. No temporary slow-plugin configuration remains active. The production HTTP socket was also confirmed to use the Wi-Fi source address with the VPN interface still up.

Real addresses, host names, route output, transport errors, complete response bodies and installation receipts remain private. The public results above contain no deployment address. Tests are not Customer acceptance. #99 remains open pending its Accountable check and release criterion; its meeting criterion belongs to Week 6. No PDF or ZIP was generated for this checkpoint.

## Current HTTPS access policy and live provider — 2026-10-31

This checkpoint supersedes the earlier anonymous HTTP/fake-provider deployment state, without changing the product source commit: both environments remain on **ba6d8a050e443dc13e69e4c052f4d5b766201e75**, version **0.5.0**.

At the owner's request, the shared deployments now require **verified HTTPS and private demo access codes**. Separate `owner`, `ta` and `customer` credentials exist for each environment. Code possession grants access; these are not verified personal identities or separate permission levels inside the application. Actual codes, addresses and certificate distribution instructions remain private.

The front door is an isolated, unprivileged `llmgw-demo-access.service` using the VM's existing Nginx binary with its own configuration, PID, logs, certificates and password files. No system Nginx configuration or service, firewall, VPN setting or existing Tailscale Serve/Funnel configuration was changed. HTTPS remains on separate frontend ports, while the two gateway backends now listen **only on loopback**, on separate backend ports.

### Access-control verification

- **25 isolated Nginx rehearsal checks passed:** anonymous, invalid and cross-environment codes denied; all three valid identities allowed; Basic/Proxy-Authorization headers stripped before forwarding; explicit demo-CA trust required; demo chat rate limiting and a 16 KiB request-body cap enforced.
- **29 campus-facing checks passed** before the live-provider activation: anonymous health, docs, OpenAPI and chat all returned HTTP 401 in both environments; wrong identities/codes and codes from the other environment were denied; valid TA/Customer/Owner chats and TA documentation requests succeeded; plaintext HTTP was rejected and neither loopback backend could be reached directly through the campus IPv4.
- TA and Customer chat requests have a **six-per-minute sustained rate**, with a small initial burst, returning HTTP 429 when exceeded. The private Owner code is exempt from that demo rate limit for operator checks. All requests retain the 16 KiB body cap. These controls are not a monetary spending limit.
- The private university IPv4 certificate is signed by a project demo CA, not a public CA. Recipients must explicitly trust the privately supplied CA after checking its fingerprint; automated checks used CA verification and never disabled TLS verification.

### Deployed QR-02 rerun through the HTTPS gate

QR-02 QRT-01 passed again from Ali12hamdan's campus workstation over authenticated, CA-verified HTTPS, with the prescribed **fake-provider slow-plugin test configuration**:

| Observation | Actual result |
| --- | --- |
| Hung request | Named HTTP 504 in **0.418300 s** |
| Subsequent health | HTTP 200 in **0.018732 s** |
| Ten normal chats | **10/10** HTTP 200 with `fake: HELLO` |
| Cleanup | Normal staging configuration restored before the live-provider setup |

The QRT measures its timeout/recovery criterion, not the unmeasured thread/process-growth portion of the full QR scenario. The numerical targets still await the Customer's verdict.

### Live DeepSeek verification

The owner entered his provider key through the existing hidden terminal setup. The key value was not pasted into chat or printed in tool output. On explicit authorization, a process transferred the local profile to the VM through encrypted SSH standard input and saved it through the gateway's credential writer in separate environment profile stores. Provider directories are mode **0700**, profile files **0600**. The stores contain the same supplied account key; separate files do not imply separate provider accounts or balances. They are permission-protected plaintext, not encrypted storage or an OS keychain. The key is absent from `.env`, command arguments, recipient instructions and public artifacts.

Three paid synthetic requests were made, one per location, with no retries:

| Location and client | HTTP | Provider/model | Duration | Observed answer |
| --- | --- | --- | --- | --- |
| Local loopback | 200 | `deepseek` / `deepseek-flash` | **1.541 s** | `GATEWAY CONNECTION VERIFIED` |
| Staging, TA code over campus HTTPS | 200 | `deepseek` / `deepseek-flash` | **1.336 s** | `GATEWAY CONNECTION VERIFIED` |
| Production, Customer code over campus HTTPS | 200 | `deepseek` / `deepseek-flash` | **1.308 s** | `GATEWAY CONNECTION VERIFIED` |

All three results included the `metadata, uppercase` trace, all four request/response plugin-change records and a response request ID. The production check completed at **2026-10-31 19:40:39 UTC (22:40:39 Europe/Moscow)**. The installed adapter's configured limit is **128 output tokens**, thinking disabled and no automatic retry; token usage is not returned by this adapter, so the table does not claim a measured token count. Calls use the owner's provider balance.

Post-activation checks again found all **eight anonymous endpoint requests denied with HTTP 401**, both direct LAN backends blocked, authorized HTTPS health returning 200 through the Wi-Fi source address, and the VPN interface still up. Inspection at **19:44:26 UTC** found all three user services active, normal configuration in both environments, profile/TLS-private-key permissions of 600, and no provider key or access-code value in the inspected application journal or proxy error log. Existing Tailscale configuration still matched the saved pre-deployment snapshot.

The existing **`llmgw setup` option remains available for a user's own installation**, with hidden key entry, model discovery and private local persistence. The shared web demo uses the server's provider profile; it does not provide per-visitor key storage. No new product code or API behavior was introduced by this operational configuration.

### Report and runbook follow-up

PR #101 must record the real runner (Codex acting for Ali12hamdan on his university Wi-Fi workstation, VPN left running), the latest HTTPS QRT receipt, the real-provider checks and updated AI usage. Statements that no key was handled by an agent process or no paid calls occurred are now historical. No Customer acceptance is inferred.

The current deployment runbook needs the authenticated-HTTPS preconditions and private backend-port mapping before finalization. Its earlier public-bind recipe must not be used unchanged on this protected installation. A local helper guard now preserves the proxy's loopback backend mapping and selected provider during upgrades. Final tag/release and report completion remain separate from this access-control checkpoint; no PDF or ZIP has been generated.
