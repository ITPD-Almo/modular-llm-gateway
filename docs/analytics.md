# Product analytics

This page specifies the proposed privacy-safe analytics contract for [`FR-012`](functional-requirements/fr/FR-012.md), supporting [`US-11`](https://github.com/ITPD-Almo/modular-llm-gateway/issues/110) and [`VP-02`](research/value-proposition.md#vp-02). Customer acceptance of the telemetry story is not recorded yet. The architecture choice is [`ADR-007`](architecture/adr/ADR-007.md).

## Measurement tree

Nodes are listed in query order from input to outcome. A [configured plugin](glossary.md#configured-plugin) is a plugin named by the selected configuration; a [configured chat](glossary.md#configured-chat) is one chat attempt processed with at least one configured plugin.

### Plugin configurations observed in use

- **Definition:** Count distinct `configuration_run_id` values from `gateway_configuration_used`, excluding `source=smoke`.
- **Source:** One first-use event per application lifetime, emitted when the first real configured chat starts. It is not emitted merely because a process restarted or deployed.
- **Query:** `count(distinct configuration_run_id) where event = 'gateway_configuration_used' and source != 'smoke'`.

### Configured chat attempts

- **Definition:** Count distinct chat `run_id` values with a `gateway_chat_started` event, excluding `source=smoke`.
- **Source:** The parent HTTP chat handler, immediately before supervised execution.
- **Query:** `count(distinct run_id) where event = 'gateway_chat_started' and source != 'smoke'`.

### Completed plugin chats per seven-day window

- **Definition:** Count distinct configured chat `run_id` values whose finish has `http_success=true` and `configured_plugin_result_visible=true` in a rolling seven-day window.
- **Source:** The parent HTTP chat handler's `finally` path, after success or handled failure. A visible plugin result means the response contains a non-empty `plugin_changes` list.
- **Query:** `count(distinct run_id) where event = 'gateway_chat_finished' and http_success = true and configured_plugin_result_visible = true and source != 'smoke' and occurred_at >= now() - 7 days`.

This is a count, not a percentage. If there is no qualifying observation in the seven-day window, return `not meaningful` and show the observation count; do not present zero as adoption. For any rate query, a zero denominator returns `not meaningful`. Analytics retention must be at least seven days, and preferably longer to support comparison windows.

### Failed configured chat rate

- **Definition:** L1 counter-metric: failed configured chat finishes divided by configured chat attempts in the same seven-day window.
- **Source:** `gateway_chat_finished` with `http_success=false`, divided by `gateway_chat_started`.
- **Query:** `count(distinct failed run_id) / count(distinct started run_id)`, with `source != 'smoke'`; zero denominator is `not meaningful`.

The counter-metric prevents a rising completion count from hiding a degraded experience.

## Event registry

The focused implementation is in [`gateway/analytics.py`](../gateway/analytics.py). The exporter is disabled by default and bounded at 256 queued events and 4096 bytes per event. It accepts only these fields:

| Event | Collection point | Fields |
| --- | --- | --- |
| `gateway_configuration_used` | First chat start after configuration is loaded | `schema_version`, `event`, `source`, opaque `run_id`, numeric `configured_plugin_count` |
| `gateway_chat_started` | Parent handler before `PipelineExecutor.execute` | `schema_version`, `event`, `source`, opaque chat `run_id` |
| `gateway_chat_finished` | Parent handler `finally` after execution | `schema_version`, `event`, `source`, opaque chat `run_id`, boolean `http_success`, bounded numeric `status_code`, boolean `configured_plugin_result_visible`, bounded numeric `duration_ms` |

`source` is trusted from `GATEWAY_ANALYTICS_SOURCE` and is one of `web`, `usability-test` or `smoke`; unknown values become `web`. IDs are random and never supplied by the client. Bodies, headers, IPs, usernames, free text, tokens, credentials, exception text and arbitrary metadata are excluded. The existing lifecycle logger has its own allowlist; these events do not expand it.

The implementation currently uses an injected sink for tests and a generic opt-in HTTP endpoint. OpenPanel self-hosted is the pinned candidate for the university host, subject to Ali's host verification. Use one analytics instance with staging and production scopes and separate ingestion credentials. Keep those credentials, URLs and raw events private.

## Seven acceptance checks

- Capture only allowlisted scalar fields and opaque random IDs.
- Capture first configured use rather than deployment restart.
- Keep exporter failure, disabled export and queue saturation out of the normal HTTP path.
- Exclude only `source=smoke` in queries, while retaining it in raw staging events for proof.
- Define zero denominators and no focus observations as `not meaningful`.
- Keep production on the same query with no test traffic.
- Keep at least the longest seven-day window in backend retention.

## What the metric does not prove

Synthetic smoke traffic verifies instrumentation and query separation, not adoption. The focus metric requires real outside use with a configured plugin and an observable plugin result before it is meaningful. A vanity metric such as total page views was rejected because it does not show a configured chat completing or the gateway helping the operator.

## Operations handoff

After this pipeline merges, Ali should extend the deployment middleware/launcher lines that export the environment settings alongside `GATEWAY_CONFIG`, `GATEWAY_HOST` and `GATEWAY_PORT`: `GATEWAY_ANALYTICS_ENABLED`, `GATEWAY_ANALYTICS_ENDPOINT`, `GATEWAY_ANALYTICS_SOURCE` and `GATEWAY_ANALYTICS_TIMEOUT_SECONDS`. Staging and production must use separate credentials and scopes. A local rehearsal is not a live dashboard claim.
