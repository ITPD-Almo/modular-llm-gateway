# Plugin diagnostics

For each chat POST the gateway generates a fresh UUID before request validation and returns it in `X-Request-ID`, including validation errors and handled plugin or provider failures.
An incoming client header cannot choose that identifier.
Invalid input returns HTTP 422 with `{"detail":"invalid chat request"}` rather than reflecting input values or JSON decoder text.
Input rejected before the chat handler has a correlation header and no plugin lifecycle events.
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
The shared helper reserves `timed_out` and `cleanup_failed` events for the execution supervisor; this diagnostics change does not itself implement execution deadlines.

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
