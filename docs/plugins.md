# Plugins

A plugin is a Python class that the gateway loads from its configuration file and calls twice per chat request: once on the way to the provider and once on the way back. This page is the contract a plugin author needs.

## The pipeline

For every chat request the gateway:

1. Validates the body (`model`, `messages`, `metadata`); an invalid body returns HTTP 422 `{"detail":"invalid chat request"}` and no plugin runs.
2. Passes the request dictionary through every plugin's `process_request` in the order the configuration lists them.
3. Sends the result to the provider. In this project it is the deterministic fake provider, which replies `fake:` plus a space and the last message's content.
4. Passes the provider's reply through every plugin's `process_response` in the **same** order, not reversed.
5. Returns the final reply, with the request-stage and response-stage `plugin_changes` combined.

## The hook contract

A plugin class must:

- be importable by a dotted path such as `examples.ab_plugin.ABReplacePlugin`;
- be constructible with no arguments;
- define `process_request(self, request: dict) -> dict` and `process_response(self, response: dict) -> dict`, as described by the `Plugin` protocol in `gateway/plugins/base.py`. Subclassing it is not required.

Both hooks are ordinary synchronous methods. Each receives one dictionary and must return a dictionary, which becomes the input of the next hook. Return a modified copy rather than relying on in-place changes.

Hooks must return JSON-compatible dictionaries with valid message and choice shapes, list-shaped trace and change fields when supplied, and an encoded payload within the worker limit.

### Fields a request hook receives

| Field | Owner | Meaning |
| --- | --- | --- |
| `model` | Client | Model name, `fake` by default |
| `messages` | Client | List of `{"role": ..., "content": ...}`; at least one |
| `metadata` | Client | Free dictionary, `{}` by default |
| `plugin_trace` | Plugins | Optional list of plugin names; absent until a plugin adds it |
| `plugin_changes` | Plugins | Optional list of `{"plugin", "stage", "change"}` objects |

The gateway drops any other field the client sends, so a client cannot inject `plugin_trace` or `plugin_changes`.

### Fields a response hook receives

| Field | Owner | Meaning |
| --- | --- | --- |
| `id`, `model`, `provider` | Provider | Reply identity; `provider` is `fake` |
| `choices` | Provider | List of `{"message": {"role": ..., "content": ...}}` |
| `plugin_trace` | Plugins | Starts empty: it shows response hooks only, because the provider does not copy the request trace |
| `plugin_changes` | Plugins | Response-stage changes; the gateway prepends the request-stage changes before returning |

A plugin may add, remove, or transform fields, and should preserve fields it does not own. To make its effect visible, append its name to `plugin_trace` and one entry per change to `plugin_changes`, with `stage` set to `request` or `response`.

## Loading, order and restarting

The gateway loads plugins from the JSON file named by `GATEWAY_CONFIG` (default: `config/plugins.json`):

```json
{
  "plugins": [
    "gateway.plugins.add_metadata.MetadataPlugin",
    "gateway.plugins.uppercase.UppercasePlugin"
  ]
}
```

Each entry is a Python import path ending in a class name. Imports and class construction are validated at startup, and that configured list is frozen until restart.

- **Order** is the list order. The same class may appear twice.
- **Disable** a plugin by removing its line. There is no enable flag.
- **Restart** after every configuration change; the file is read only at startup.
- **Import path:** start the gateway from the repository root, which is on Python's import path. A plugin outside the repository must be installed into the virtual environment or its directory added to `PYTHONPATH`.

Each chat request then runs the complete pipeline in a fresh supervised worker process, with new plugin instances shared by that request's request and response hooks.
Instance state does not persist between separate chat requests; keep request-scoped state in the payload or the instance, and use an explicitly designed external store for any durable state.
Keep imports and constructors cheap and free of external side effects: they run during initial validation and again inside request workers.

## Failure behavior

| Situation | Result |
| --- | --- |
| Missing configuration file, malformed JSON, `plugins` not a list of strings, an import or constructor error, or a class without both hooks | The gateway refuses to start and names the configuration path and the reason |
| Invalid request body | HTTP 422 `invalid chat request` with an `X-Request-ID` header, without echoing the input; no worker starts, no plugin runs and no lifecycle event is written |
| A hook raises an exception, the worker exits abruptly during a hook, or a hook returns invalid output | HTTP 500 naming the plugin and stage, for example `plugin FailingPlugin failed during request processing`; the exception text is not returned |
| A hook runs past its deadline (default 250 ms) | HTTP 504 naming the plugin and stage; only this request fails |
| The provider fails | HTTP 502 `provider failed` |
| Worker startup or transfer fails, or all workers are busy | HTTP 503 |
| The request is over the worker JSON limit | HTTP 413 |

The provider is not called after a failing request hook. A hook deadline fails only the affected request; it never silently skips a transformation. `/health` and later requests keep working. Every chat response, including a 422, carries a generated `X-Request-ID` header. For a validated request, the content-free hook lifecycle events use that same ID; a validation failure creates no worker and no hook events. The 250 ms deadline and the fail-the-request policy are team proposals awaiting the Customer's verdict.

See the [operating guide](operations.md#execution-and-recovery) for limits, cleanup, configuration and the instance-lifecycle compatibility change.

## Example: a third-party plugin

`examples/ab_plugin.py` lives outside the `gateway/` package and needs no change to the gateway core. Its request hook replaces every message with `AAAA`; its response hook replaces the provider's reply with `BBBB`:

```python
from typing import Any

REQUEST_TEXT = "AAAA"
RESPONSE_TEXT = "BBBB"


class ABReplacePlugin:
    def process_request(self, request: dict[str, Any]) -> dict[str, Any]:
        updated = dict(request)
        updated["messages"] = [
            dict(message, content=REQUEST_TEXT) for message in updated.get("messages", [])
        ]
        updated["plugin_trace"] = list(updated.get("plugin_trace", [])) + ["ab_replace"]
        updated["plugin_changes"] = list(updated.get("plugin_changes", [])) + [
            {
                "plugin": "ab_replace",
                "stage": "request",
                "change": f"replaced message content with {REQUEST_TEXT}",
            }
        ]
        return updated

    def process_response(self, response: dict[str, Any]) -> dict[str, Any]:
        updated = dict(response)
        choices = [
            dict(choice, message=dict(choice["message"])) for choice in updated.get("choices", [])
        ]
        replaced = [choice["message"]["content"] for choice in choices]
        for choice in choices:
            choice["message"]["content"] = RESPONSE_TEXT
        updated["choices"] = choices
        updated["plugin_trace"] = list(updated.get("plugin_trace", [])) + ["ab_replace"]
        updated["plugin_changes"] = list(updated.get("plugin_changes", [])) + [
            {
                "plugin": "ab_replace",
                "stage": "response",
                "change": f"replaced reply {replaced!r} with {RESPONSE_TEXT}",
            }
        ]
        return updated
```

`examples/ab-plugins.json` lists it after the metadata plugin. Start the gateway with that file instead of editing `config/plugins.json`:

```console
GATEWAY_CONFIG=examples/ab-plugins.json python -m uvicorn gateway.main:create_app --factory
```

On PowerShell, run `$env:GATEWAY_CONFIG = "examples/ab-plugins.json"` first. The request from the [setup guide](setup.md) now returns `"content":"BBBB"`. The response's change list shows that the provider received `AAAA`: `replaced reply ['fake: AAAA'] with BBBB`. `tests/test_ab_example.py` checks the same result.

The bundled `MetadataPlugin` (`gateway/plugins/add_metadata.py`) and `UppercasePlugin` (`gateway/plugins/uppercase.py`) use the same contract: metadata adds `metadata.gateway` and uppercase changes every message to uppercase.
