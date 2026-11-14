# UT-01 staging instrumentation

This runbook prepares the synthetic gateway environment and captures the events for `UT-01`. Use a dedicated staging instance on the university network. It uses the fake provider, the packaged fixtures and its own analytics scope. The facilitator observes completion, help and friction. The test events show configured chat attempts and outcomes. The custom-plugin probe shows whether a fixed synthetic reply contains the assigned marker.

## Prepare the test instance

1. Use the reviewed [versioned image](deployment.md#versioned-compose-deployment) and choose a free test loopback port. Keep the normal staging and production gateways running separately. If the facilitator uses a different campus computer, use the team's approved private access route to the test instance.
2. In the analytics backend create a dedicated staging organization named `ut01` and record its displayed ID. OpenObserve can generate a different identifier from the name. Use the displayed ID for `UT01_ORGANIZATION` and provision ingestion and query access scoped to that organization. The first synthetic chat populates `gateway_usage` with the [existing event schema](deployment-tools/analytics-stream.json). Its short-term backend retention follows the staging analytics policy. Keep the filtered export in the private usability-data repository as the durable text record.
3. In the private ingestion file set `GATEWAY_ANALYTICS_ENDPOINT` to the verified HTTPS URL ending `/api/UT01_ORG_ID` and `GATEWAY_ANALYTICS_AUTHORIZATION` to the scoped `Basic ...` header. Use a route reachable from the Docker container. Container loopback refers to that container. For a private CA, put the certificate in the directory selected by `UT01_CA_DIR` and set `GATEWAY_ANALYTICS_CA_FILE` to its container path, such as `/run/llmgw/analytics-ca.pem`. Protect the private file and keep it outside the product checkout.
4. Apply the updated [dashboard query](deployment-tools/analytics-dashboard.json) to the operational dashboards and verify the four [usage queries](analytics.md#the-metric-tree) exclude both test sources. Keep test traffic in the dedicated test organization. The launcher and the exporter check that their endpoint matches the configured test organization ID.

Put the host settings in a separate private Compose env file referenced by `UT01_COMPOSE_SETTINGS`. These placeholders show the fields. Use the actual verified image reference and reserved loopback port.

```dotenv
GATEWAY_IMAGE=llmgw:REVIEWED-IMAGE-TAG
GATEWAY_HOST_PORT=18107
UT01_INGEST_ENV_FILE=/private/path/to/ut01-ingest.env
UT01_ORGANIZATION=UT01_ORG_ID
# UT01_CA_DIR=/private/path/to/ca-directory
```

On the Docker host, define this helper from the repository root. The override uses the fake provider, disables observability export and sets `environment=staging`, `source=usability-test` and the test organization ID.

```sh
ut01() {
  docker compose --env-file "$UT01_COMPOSE_SETTINGS" -p llmgw-ut01 \
    -f compose.yaml -f docs/deployment-tools/compose.ut01.yml "$@"
}
```

Use `ut01 config --quiet` for validation. Keep rendered Compose configuration private because it can contain ingestion settings.

## Participant bring-up

For the main task, the participant starts the gateway from a clean workspace on an isolated campus test workstation. Before timing starts, the facilitator supplies the reviewed checkout and preloaded image, a free loopback port, and the location of the private `UT01_COMPOSE_SETTINGS` file. The reviewed Compose file and UT-01 override in that checkout select the packaged default plugin fixture. The settings file points at the session's separate ingestion file and, when needed, the public CA certificate.

Give the workstation only a short-lived, ingestion-only credential for the dedicated UT-01 organization. Use a facilitator-managed ingest relay when the backend cannot issue an ingestion-only credential. Query credentials, administrator accounts and provider keys stay on the facilitator's side. Revoke the session credential or disable its relay during cleanup. Use the provided workstation, separate from the shared VM's operator account and Docker access.

The participant follows the setup documentation, defines `ut01` above, and starts the gateway with `ut01 up -d --wait`. This launches the instrumented Compose service with `environment=staging` and `source=usability-test`. The participant then checks the gateway and sends the synthetic configured chat. The facilitator records the window and observes the work. A hint, command, or start performed by the facilitator after timing begins is recorded as assistance. Keep the exact rehearsal steps below in facilitator material.

## Reset and run a synthetic rehearsal

Run one session at a time in a quiet window. Use the gateway host's synchronized UTC clock to record boundaries in Unix microseconds. Reset to the packaged default plugin configuration before each session. Start the window before any chat. For the Week 7 technical rehearsal and the pre-session instrumentation check, exercise these exact requests in order. During the usability session, the participant uses the facilitator's scenario and supplied setup documentation.

```sh
unset UT01_FIXTURE
UT01_START=$(python3 docs/deployment-tools/ut01-check.py now)
ut01 up -d --wait --force-recreate
ut01 exec -T gateway llmgw health
ut01 exec -T gateway llmgw chat 'hello'

export UT01_FIXTURE=/opt/llmgw/examples/slow-plugins.json
ut01 up -d --wait --force-recreate
ut01 exec -T gateway llmgw chat 'sleep'
ut01 exec -T gateway llmgw health
ut01 exec -T gateway llmgw chat 'hello'
```

The normal chat returns `fake: HELLO` with the `metadata` and `uppercase` trace. The `sleep` check deliberately exits nonzero after the named `SlowPlugin` HTTP 504. The health and follow-up chat should pass on that same instance. The reset creates a fresh process and run ID. Each process emits `gateway_configuration_used` on its first validated chat. The opaque attempt ID joins each `gateway_chat_started` and `gateway_chat_finished` pair.

## Check a custom plugin offline

For the custom-plugin task use a separate disposable workspace with only the synthetic plugin files and its `plugins.json`. Make those files readable by the image's UID `10001`. Run the selected image with an offline network and a read-only scratch mount. Set `UT01_PLUGIN_CONTAINER` to a unique test container name, `UT01_SCRATCH` to the absolute workspace path, and `UT01_IMAGE` to the same verified image. Set `UT01_EVIDENCE_DIR` to the private output directory.

```sh
docker run -d --rm --name "$UT01_PLUGIN_CONTAINER" --network none \
  --init --read-only --tmpfs /tmp --cap-drop ALL --security-opt no-new-privileges \
  --mount "type=bind,src=$UT01_SCRATCH,dst=/scratch,readonly" \
  -e GATEWAY_CONFIG=/scratch/plugins.json "$UT01_IMAGE"
docker exec "$UT01_PLUGIN_CONTAINER" llmgw health
python3 docs/deployment-tools/ut01-check.py probe \
  --container "$UT01_PLUGIN_CONTAINER" --marker "$UT01_SYNTHETIC_MARKER" \
  --output "$UT01_EVIDENCE_DIR/plugin-probe.json"
docker stop "$UT01_PLUGIN_CONTAINER"
```

Wait for health before probing. Choose a synthetic marker of at most 32 ASCII letters, digits, dashes or underscores. The command sends a fixed synthetic request and writes `ut01_plugin_probe`, a UTC timestamp and `marker_seen`. It never saves the reply body. The probe is local to the test and uses no analytics pipeline. It cannot judge whether the participant wrote the plugin unaided or found the correct documentation.

## Export and verify a private session window

After the final task and probe, set `UT01_END` on the same clock and let buffered delivery complete. Run the query as the facilitator with the same `UT01_ORGANIZATION`, `UT01_QUERY_URL` ending in `/api/UT01_ORG_ID`, `UT01_QUERY_AUTHORIZATION` carrying the separate private query credential, and `UT01_QUERY_CA_FILE` when needed. Use verified HTTPS or loopback HTTP for a local rehearsal. Set these in the facilitator's private environment. Create a fresh output path for each export.

```sh
UT01_END=$(python3 docs/deployment-tools/ut01-check.py now)
ut01 down
unset UT01_FIXTURE
python3 docs/deployment-tools/ut01-check.py export \
  --start-us "$UT01_START" --end-us "$UT01_END" --check-rehearsal \
  --output "$UT01_EVIDENCE_DIR/rehearsal-events.json"
```

The query and exporter both apply the half-open UTC window `[start, end)`. The export keeps the allowlisted Week 6 event fields. It excludes participant identifiers, payloads, headers, IPs and free text. The export and probe refuse to overwrite files and create them with private permissions. Keep the window to `P-nn` mapping with the private session notes.

For verification, `--check-rehearsal` requires two distinct configuration runs and matching chat pairs in the order `ok`, `timeout`, `ok`. The timeout and recovery must share a run ID. Query a second window that excludes the rehearsal and confirm it returns no rehearsal events. Check the offline probe boolean and the actual result against the observer's notes. If delivery is still settling, retry the same query after it becomes visible. A missing pair or a backend error leaves the verification incomplete. Use `export` without `--check-rehearsal` for a counted session, since its attempts and outcomes can vary.

Record a sanitized verification summary with date, runner, image identity, network, checks and evidence location. Keep the raw export, local probe record and participant mapping private. The Sprint 07 teammate rehearsal is uncounted. The [Sprint 08 pre-session check](https://github.com/ITPD-Almo/modular-llm-gateway/issues/132) repeats the instrumentation check before the first counted session. The Week 8 manual usability verdict uses the observer's measured task outcomes.
