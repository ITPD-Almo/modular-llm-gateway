# Plugins

The gateway loads plugins from the JSON file named by `GATEWAY_CONFIG` (default: `config/plugins.json`). Each entry is a Python import path ending in a class name. Imports and class construction are validated at startup, and that configured list is frozen until restart.
Each chat request then runs the complete pipeline in a fresh supervised worker process, with new plugin instances shared by that request's request and response hooks.
Instance state does not persist between separate chat requests; keep request-scoped state in the payload or the instance, and use an explicitly designed external store for any durable state.
Keep imports and constructors cheap and free of external side effects: they run during initial validation and again inside request workers.

Each plugin receives a request dictionary in `process_request(request)` and must return a request dictionary. The gateway calls plugins in the exact order listed in the configuration. The returned request is sent to the fake provider. The provider response dictionary is then passed through every plugin's `process_response(response)` in that same order. A plugin may add, remove, or transform fields, and should preserve fields it does not own.

The example metadata plugin adds `metadata.gateway` and a `plugin_trace` entry. The uppercase plugin changes each text message to uppercase and adds its own trace entry. The response also contains `plugin_changes`, with the plugin name, stage, and human-readable change for every transformation. The trace and change list in the curl example make ordering and effects visible.

Configuration, import, and initial class-construction errors stop startup with a clear error.
A hook exception, abrupt worker exit during a hook, or invalid hook output returns HTTP 500 naming the plugin and stage; the provider is not called after a failing request hook.
Hooks must return JSON-compatible dictionaries with valid message/choice shapes, list-shaped trace/change fields when supplied, and an encoded payload within the worker limit.
Provider errors are returned separately as HTTP 502.
A hook deadline returns HTTP 504 and fails only the affected request; it never silently skips a transformation.
Worker startup/transfer failures or exhausted worker capacity return HTTP 503, and a request over the worker JSON limit returns HTTP 413.
See the [operating guide](operations.md#execution-and-recovery) for limits, cleanup, configuration and the instance-lifecycle compatibility change.
