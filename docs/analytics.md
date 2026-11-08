# Product analytics

## The Value And The Metrics

The focus metric is **Completed plugin chats per seven-day window**, the count of configured chats that return HTTP success and a visible plugin result. It measures the operator benefit in [VP-02](research/value-proposition.md#vp-02); provider connectivity alone is not adoption.

### The Metric Tree

- **L0:** [Completed plugin chats](#completed-plugin-chats)
  - **L1 (counter-metric):** [Failed configured chat rate](#failed-configured-chat-rate)
  - **L1:** [Configured chat attempts](#configured-chat-attempts)
    - **L2:** [Plugin configurations observed in use](#plugin-configurations-observed-in-use)

### Why This Focus Metric

- **Value:** it counts the moment a configured plugin chain produces a visible result in a private trial.
- **Strategy:** it measures whether an operator can use the reusable plugin workflow described in VP-02.
- **Leading indicator:** repeat completion gives an early signal before the team can assess trial continuation.
- **Actionable:** the input points to trial setup and the counter-metric exposes failures that need work.
- **Understandable:** a completion means one successful chat with a visible plugin result.
- **Measurable:** the gateway records both the configured attempt and its terminal outcome.
- **Not a vanity metric:** it records a completed configured-plugin chat, not a superficial exposure or installation count.

**Rejected vanity metric:** installer downloads. A download can occur without configuring any plugins or sending a chat.

The focus metric may have no value until people outside the team use the product. Smoke traffic is excluded. A staging dashboard with only smoke traffic therefore charts the L1 input and can show zero measured attempts. Treat the metric as a count of completed chats, which can include repeat chats by the same operator.

### Completed plugin chats

- **Definition:** number of terminal configured chats with outcome `ok` and a visible plugin result per seven-day window. With no eligible terminal events there is no observation yet.
- **Source:** [`gateway_chat_finished`](#the-events).
- **Query:** the backend computes this metric using the following OpenObserve SQL query and its seven-day time filter:

```sql
SELECT CASE WHEN COUNT(*) = 0 THEN NULL
       ELSE COUNT(CASE WHEN outcome = 'ok' AND visible_result = true THEN 1 END)
       END AS completed_plugin_chats
FROM gateway_usage
WHERE event = 'gateway_chat_finished' AND plugin_count > 0 AND source <> 'smoke'
```

The zero-observation result is `not meaningful`, not zero adoption.

### Failed configured chat rate

- **Definition:** percentage of observed terminal configured chats that end in a client error, server error or timeout over the previous seven days. It has no value when the denominator is zero.
- **Source:** [`gateway_chat_finished`](#the-events).
- **Query:** apply the same seven-day window to:

```sql
SELECT 100.0 * COUNT(CASE WHEN outcome <> 'ok' THEN 1 END)
       / NULLIF(COUNT(*), 0) AS failed_configured_chat_rate
FROM gateway_usage
WHERE event = 'gateway_chat_finished' AND plugin_count > 0 AND source <> 'smoke'
```

### Configured chat attempts

- **Definition:** count of validated chat attempts with at least one configured plugin over the previous seven days. This is the dashboard input chart until there is a measured focus value.
- **Source:** [`gateway_chat_started`](#the-events).
- **Query:** the dashboard time picker supplies the previous seven days. The panel runs:

```sql
SELECT COUNT(*) AS configured_chat_attempts
FROM gateway_usage
WHERE event = 'gateway_chat_started' AND plugin_count > 0 AND source <> 'smoke'
```

### Plugin configurations observed in use

- **Definition:** number of distinct gateway process runs with at least one configured plugin that receive their first validated chat over the previous seven days. This measures configuration use at startup rather than distinct files or operators.
- **Source:** [`gateway_configuration_used`](#the-events).
- **Query:** apply the same seven-day window to:

```sql
SELECT COUNT(DISTINCT run_id) AS plugin_configurations_observed_in_use
FROM gateway_usage
WHERE event = 'gateway_configuration_used' AND plugin_count > 0 AND source <> 'smoke'
```

## The Events

Event names follow the `object_action` convention in snake case. Common required fields are `event` (bounded enum), `_timestamp` (Unix microseconds, integer), `environment` (bounded enum `staging` or `production`), `source` (bounded enum `web`, `usability-test` or `smoke`), `run_id` (random opaque string) and `plugin_count` (bounded integer). Only `smoke` is excluded by the queries. Staging source selection is controlled by deployment configuration. Production accepts only `web` as its configured source.

| Event | Fires when | Fields | Collected at |
| --- | --- | --- | --- |
| `gateway_configuration_used` | The first validated chat uses the loaded plugin configuration in this process. | Common required fields. | `gateway`, staging and production. |
| `gateway_chat_started` | A validated chat enters the request pipeline. | Common fields; `attempt_id` (required random opaque string). | `gateway`, staging and production. |
| `gateway_chat_finished` | The chat pipeline returns its result or fails. | Common fields; `attempt_id` (required random opaque string), `outcome` (required enum `ok`, `client_error`, `server_error` or `timeout`), `visible_result` (required boolean indicating a plugin trace or change record). | `gateway`, staging and production. |

The random IDs join events within one attempt or process run. The gateway does not derive them from a person or reuse its diagnostic request ID. The exporter sends no message text, response text, plugin names, client headers, IPs, account details or credentials in the event. Schema validation failures occur before this core task begins and are outside the analytics funnel.

## The Pipeline

Use a **dedicated OpenObserve instance** as the documented self-hosted alternative to OpenPanel. It stores flat JSON events and serves the SQL chart and event list without requiring a browser tracker or user identity. The separate observability deployment receives operating signals. Analytics has its own data volume, retention and credentials.

The gateway parent queues the events in batches of up to 32 for JSON over HTTPS, or loopback HTTP on a co-located VM. The queue is capped at 256 events. On shutdown, the exporter sends one final batch of at most 32 events and drops any remaining queued events. Export failures drop events and do not delay the request, so the charts measure observed traffic. `GATEWAY_ANALYTICS_ENABLED=0` disables collection. The analytics deployment retains events for 14 days. `staging` and `production` use separate organizations and ingestion credentials. The team and Customer use private dashboard access over the university network. The [deployment runbook](deployment.md#telemetry-pipelines) owns the installation steps.

Both dashboards show the same **Configured chat attempts** chart and a recent event table. The event table includes staging smoke records for verification. Synthetic events stay in staging, and the production dashboard remains unexercised until real use.

## The Dashboard

The staging and production scopes use the same **Gateway trial usage** dashboard. It shows the seven-day **Configured chat attempts** chart until real focus observations exist, the focus metric, the failed configured chat rate and a recent raw-event table. The staging smoke proof appears in raw events but is excluded by every metric query; production receives no test traffic.

## Collected Data

The backend receives only the registry fields in the table above: bounded enums, booleans, bounded numbers and opaque random IDs. It receives no request or response bodies, headers, IPs, usernames, plugin names, free text, tokens, credentials or exception text. Retention is 14 days, longer than the seven-day metric window. The opt-in switch is `GATEWAY_ANALYTICS_ENABLED=0`; exporter failure, queue saturation and disabled collection leave the normal gateway flow working.
