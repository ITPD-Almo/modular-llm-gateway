# Plugin diagnostics

For each validated chat request the gateway generates a fresh UUID and returns it in `X-Request-ID`, including a handled plugin or provider failure.
An incoming client header cannot choose that identifier.
Input rejected before the chat handler, such as HTTP 422, has no plugin lifecycle events or correlation header.
Successful response JSON, plugin order and the fake provider's behavior remain as described in the [plugin contract](plugins.md).

## Event contract

The `gateway.plugin_events` Python logger writes one JSON message per hook start, completion or failure.
The gateway uses the application's logging handlers when configured, or a stderr handler by default.
The logger runs at INFO; an operator's logging configuration may route or filter it.

```json
{"schema_version":1,"event":"completed","request_id":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","plugin":"UppercasePlugin","stage":"request","elapsed_ms":0.083,"reason":null}
```

The allowlist is `schema_version`, `event`, `request_id`, `plugin`, `stage`, `elapsed_ms` and `reason`.
Plugin is the configured class's identifier; stage is `request` or `response`.
The elapsed value measures hook work in milliseconds and is nonnegative.
Failure reasons are fixed codes such as `plugin_exception` and `invalid_output`, rather than arbitrary exception messages.
The execution supervisor also emits `timed_out` and, if the OS has not reaped a stopped worker, `cleanup_failed` using the same schema.

Request messages, provider replies, metadata, credentials, exception text and tracebacks are not copied into these events or handled plugin-error details.
Plugins are trusted operator-supplied Python code: their own logging and other side effects are outside this event contract.
The existing `plugin_changes` response is plugin-provided transformation information, not this content-free operating log.

## Reading and keeping events

Start the gateway using the [setup recipe](setup.md), send the synthetic `curl` request, and find its `X-Request-ID` in the logger output.
Each hook produces `started` followed by `completed` or `failed`, in configured order, for request hooks and then response hooks.
A failed request hook prevents provider execution and later hooks; a failed response hook stops the remaining response chain.
HTTP 500 identifies the plugin and stage without returning its exception message.

The application adds no log database or retention policy.
Stderr and Python logging are the sink boundary; the operator controls collection, access, rotation and retention in the deployment.
These events do not claim durable, tamper-proof or compliance-grade audit storage.

## Execution and recovery

Each validated chat runs the configured request hooks, fake provider and response hooks inside a fresh Python `spawn` worker process.
The parent supervises each hook, terminates an over-budget worker, waits for cleanup, and escalates to killing the worker when termination is ignored.
All joins have a finite grace period; no background thread continues the timed-out hook.
The failure policy is to fail that request, never silently bypass a transformation, while health checks and later requests remain available.
These defaults and this policy are the team's proposed implementation for review against the functional/quality requirements and ADR; they are not an assertion of a Customer acceptance verdict.

| Setting | Default | Meaning |
| --- | --- | --- |
| `GATEWAY_PLUGIN_TIMEOUT_MS` | `250` | Deadline for each request or response hook, including output validation |
| `GATEWAY_MAX_WORKERS` | `4` | Maximum concurrent request workers per application process; excess requests receive 503 |
| `GATEWAY_WORKER_STARTUP_TIMEOUT_MS` | `1000` | Worker initialization or between-stage/result-transfer wait budget |

Timing settings accept integers from 1 to 60000 milliseconds; worker count accepts 1 to 32.
The app factory also accepts `plugin_timeout_ms`, `max_workers`, and `startup_timeout_ms` keyword overrides for integration tests.
The cleanup grace is 100 milliseconds per join; a successful worker is allowed to exit normally before termination is attempted.
The worker sends small bounded control frames and chunks large results; the parent enforces an overall protocol deadline and a one-MiB encoded JSON payload/result limit.
Result chunks do not extend the transfer deadline.

HTTP 504 identifies the timed-out plugin/stage and returns the gateway-generated correlation header.
The next request starts a new worker and does not inherit the timed-out plugin's instance state.
Malformed or non-JSON hook outputs fail with a named 500 instead of passing damaged data to a later stage.
If the OS has not reaped a worker after termination and kill, its capacity slot stays reserved until reaped; repeated requests cannot grow an unbounded set of unreaped workers.
When all slots are unavailable, chat returns 503 while `/health` stays responsive.

The complete pipeline shares plugin instances within one request, so a request hook can prepare state for its response hook.
This changes the earlier process-global instance lifecycle: mutable instance state resets between requests.
The default plugins and the ordinary request/response format remain compatible.
The new lifecycle and process-startup overhead must be reviewed in the architecture decision before merge.

Configuration loading and initial import/construction validation in the app factory remain trusted startup work outside hook deadlines.
Worker-side initialization is bounded, but this change does not make an unsafe initial import safe or stop a hanging constructor during that initial validation.
Only trusted operator-supplied plugins are supported: process separation is an execution boundary, not a security sandbox or a rollback of external side effects.
Managed daemon workers cannot create multiprocessing children; arbitrary external subprocesses created by plugin code are outside the managed-worker contract and are not supported.
Worker stdout/stderr are discarded, and only the parent's allowlisted events are forwarded; a plugin's own ad-hoc prints are not its diagnostics interface.

## Verifying the boundary

Run `python -m pytest` from a clean install to reproduce the synthetic request-hook and response-hook five-second sleeps, CPU loop, ignored termination, abrupt exit and malformed-output checks.
The timeout fixtures set a 250 ms budget and assert the HTTP result arrives within one second, followed by a healthy request and zero managed workers.
Ten repeated timeouts also verify there is no accumulated active worker and that the single admission slot is reusable.
These are measured software checks on the tested environment, rather than a hard real-time guarantee for every OS, logging sink or deployment.
