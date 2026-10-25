# Demo

One scripted walk-through of the gateway: the normal two-plugin request, a changed order, a removed plugin, a new third-party plugin, and a slow plugin that times out without breaking later requests. Everything is synthetic: the fake provider answers, and no provider key is used.

Install first with the [setup guide](setup.md). Run every step from the repository root with the virtual environment active. Each step starts the gateway in one terminal and sends requests from a second terminal. Stop the gateway with Ctrl+C before the next step, because the plugin list is read only at startup.

The requests below use this helper. The `X-Request-ID` value differs on every run.

```sh
ask() { curl -s -i -X POST http://127.0.0.1:8000/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"fake\",\"messages\":[{\"role\":\"user\",\"content\":\"$1\"}]}"; echo; }
```

## 1. Two plugins in the configured order

```sh
python -m uvicorn gateway.main:create_app --factory
```

```sh
ask hello
```

Expected: HTTP 200 and

```json
{"id":"fake-response","model":"fake","provider":"fake","choices":[{"message":{"role":"assistant","content":"fake: HELLO"}}],"plugin_trace":["metadata","uppercase"],"plugin_changes":[{"plugin":"metadata","stage":"request","change":"added metadata.gateway=modular"},{"plugin":"uppercase","stage":"request","change":"uppercased message content"},{"plugin":"metadata","stage":"response","change":"recorded metadata transformation"},{"plugin":"uppercase","stage":"response","change":"recorded uppercase transformation"}]}
```

## 2. Reverse the order

Replace `config/plugins.json` with this complete file, so `UppercasePlugin` comes first, then restart the gateway and run `ask hello` again:

```json
{
  "plugins": [
    "gateway.plugins.uppercase.UppercasePlugin",
    "gateway.plugins.add_metadata.MetadataPlugin"
  ]
}
```

Expected: the text is still `fake: HELLO`, but `plugin_trace` is `["uppercase","metadata"]` and the four `plugin_changes` entries start with `uppercase`.

## 3. Remove a plugin

Replace `config/plugins.json` with this complete file, which keeps only the metadata plugin and has no trailing comma, then restart and run `ask hello`:

```json
{
  "plugins": [
    "gateway.plugins.add_metadata.MetadataPlugin"
  ]
}
```

Expected: `"content":"fake: hello"` in lower case, `plugin_trace` is `["metadata"]`, and only the two `metadata` entries remain. Restore the file with `git checkout -- config/plugins.json`.

## 4. Add a new plugin without changing the gateway

`examples/ab_plugin.py` is a plugin outside the `gateway/` package; the [plugin guide](plugins.md#example-a-third-party-plugin) shows its code. Start the gateway with its configuration file:

```sh
GATEWAY_CONFIG=examples/ab-plugins.json python -m uvicorn gateway.main:create_app --factory
```

```sh
ask hello
```

Expected: the client receives `BBBB`, and the change list shows that the provider received `AAAA`:

```json
{"id":"fake-response","model":"fake","provider":"fake","choices":[{"message":{"role":"assistant","content":"BBBB"}}],"plugin_trace":["metadata","ab_replace"],"plugin_changes":[{"plugin":"metadata","stage":"request","change":"added metadata.gateway=modular"},{"plugin":"ab_replace","stage":"request","change":"replaced message content with AAAA"},{"plugin":"metadata","stage":"response","change":"recorded metadata transformation"},{"plugin":"ab_replace","stage":"response","change":"replaced reply ['fake: AAAA'] with BBBB"}]}
```

`git status` shows no change under `gateway/`.

## 5. A slow plugin times out and the gateway recovers

`examples/slow_plugin.py` sleeps for 5 seconds when the message is exactly `sleep`. `examples/slow-plugins.json` places it between the two default plugins.

```sh
GATEWAY_CONFIG=examples/slow-plugins.json python -m uvicorn gateway.main:create_app --factory
```

```sh
ask sleep
ask hello
curl http://127.0.0.1:8000/health
```

Expected:

- `ask sleep` returns `HTTP/1.1 504 Gateway Timeout` with `{"detail":"plugin SlowPlugin timed out during request processing"}` after about 0.3 seconds, not 5. The default 250 ms hook deadline is a team proposal.
- `ask hello` returns HTTP 200 with `fake: HELLO` and `plugin_trace` `["metadata","uppercase"]`; the slow plugin did nothing this time.
- `/health` returns `{"status":"ok"}`.

The gateway's terminal shows the lifecycle events, with no message content. For the timed-out request they are:

```json
{"schema_version":1,"event":"started","request_id":"eb3b3bd8854a4174867077a311831ac2","plugin":"MetadataPlugin","stage":"request","elapsed_ms":0.0,"reason":null}
{"schema_version":1,"event":"completed","request_id":"eb3b3bd8854a4174867077a311831ac2","plugin":"MetadataPlugin","stage":"request","elapsed_ms":0.017,"reason":null}
{"schema_version":1,"event":"started","request_id":"eb3b3bd8854a4174867077a311831ac2","plugin":"SlowPlugin","stage":"request","elapsed_ms":0.0,"reason":null}
{"schema_version":1,"event":"timed_out","request_id":"eb3b3bd8854a4174867077a311831ac2","plugin":"SlowPlugin","stage":"request","elapsed_ms":250.377,"reason":"timeout"}
```

The `request_id` equals that response's `X-Request-ID` header. The [operating guide](operations.md) explains the events, limits and settings.

## Reset

Stop the gateway, run `unset GATEWAY_CONFIG` (PowerShell: `Remove-Item Env:GATEWAY_CONFIG`), and run `git checkout -- config/plugins.json`. The [setup guide](setup.md#reset) describes a full reset.
