# Observability

A system operator can investigate a failed chat by its gateway request ID and see whether that outcome is slow across a recent window. The gateway emits both observations from the parent application without copying message content.

## The Signals

| Signal | What the gateway emits |
| --- | --- |
| Metric | `gateway_chat_duration`, an OpenTelemetry explicit-bucket histogram in milliseconds. OpenObserve stores `gateway_chat_duration_bucket` and `gateway_chat_duration_count`. The only request dimensions are the fixed route and outcome. |
| Log | One `gateway_chat_finished` record for each handled chat outcome, carrying `request_id`, `route`, `outcome`, `duration_ms` and the `environment` resource attribute. |
| Trace | The gateway currently emits no distributed trace. `X-Request-ID` correlates one request with logs. |

`route` is always `/v1/chat/completions`. `outcome` is `ok`, `client_error` (4xx), `server_error` (other 5xx), or `timeout` (504). `duration_ms` uses a monotonic clock from the chat middleware to the response headers being ready. Both signals use that same observation. Client disconnects before a response and failures rejected at the reverse proxy are outside this application measurement. Existing [hook lifecycle events](operations.md#event-contract) continue to identify the hook and stage in operator logs.

## The SLIs

### SLI-01

Chat response latency by outcome

- **Status:** Active
- **Definition:** P95 elapsed application response time grouped by `route` and `outcome`. Find the individual observation by `request_id` in the log, with the same route, outcome and duration. The deliberate failure in the deployed check has `outcome=timeout`.
- **Unit:** milliseconds
- **Window:** rolling five minutes. The failed request's log point must be queryable within five seconds of its response. The numeric failure-series P95 must be queryable within one minute.
- **Source:** OpenObserve `gateway_chat_duration_bucket` and `gateway_requests` in the same environment organization.
- **Query:** `histogram_quantile(0.95, sum by (le, route, outcome) (sum_over_time(gateway_chat_duration_bucket[5m])))`

The exporter sends delta histograms, so the query sums the observed counts in the window before computing the quantile. Each exported point covers observations since the preceding export. OpenObserve stores cumulative counts across bucket boundaries within each point. An outcome with no observations in the window has no numeric P95.

The per-request query runs against the same organization, in a narrow interval around the failed request. Substitute its gateway-generated identifier:

```sql
SELECT request_id, route, outcome, duration_ms, environment
FROM gateway_requests
WHERE request_id = '<request_id>'
```

### SLI-02

Chat admission rejection under load

- **Status:** Planned
- **Definition:** share of chat attempts rejected specifically because no worker slot was available, for the [capacity scenario](quality-requirements/qr/QR-05.md).
- **Unit:** percent of chat attempts
- **Window:** five minutes
- **Source:** proposed admission-outcome counter in the gateway parent. The active signal currently groups other 503 responses with server errors.
- **Query:** worker-slot rejections divided by all attempts in the same interval, multiplied by 100. Undefined when no attempts were observed.

The repeat-timeout resource bound and recoverability stopwatch stay in their direct test procedures. Their process counts and deployment receipts are outside the active request-latency signal.

## The Pipeline

The `gateway` parent sends structured logs and histograms over OTLP/HTTP. Log batches are scheduled every 500 ms and histogram exports every two seconds. The log queue is capped at 512 records. The exporter keeps its network operations off the request path. An outage can lose telemetry and the gateway can keep serving chats. The `staging` and `production` scopes use separate organizations and ingestion credentials. `GATEWAY_OBSERVABILITY_ENABLED=0` disables collection. See the [deployment runbook](deployment.md#telemetry-pipelines) for provisioning, private access and the dashboard definition.

The deployment template retains observations for seven days, which covers the five-minute windows. The team and Customer use the campus HTTPS route with private dashboard access. The deployed check uses a private staging query credential.

Use the same `SLI-01` chart in each environment. The staging chart is evidence for the [deployed diagnosability test](quality-requirements/qr/QR-08.md#qrt-01). Leave production collection free of synthetic test traffic.
