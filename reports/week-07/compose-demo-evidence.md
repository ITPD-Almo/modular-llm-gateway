# Compose plugin walkthrough evidence

The November 14 local walkthrough used the [merged Compose source](https://github.com/ITPD-Almo/modular-llm-gateway/commit/d909345af37db21a6d6c0168956b4e3097fd184b), the image labeled with that source revision and the fake provider. Both telemetry exporters were disabled for this synthetic run.

| Step | Observed |
| --- | --- |
| Start a pinned image | Compose reported a healthy gateway. The terminal reported `llmgw 0.7.0` for the candidate build. |
| Send `hello` before adding a plugin | HTTP 200, reply `fake: HELLO`, trace `metadata`, `uppercase`. |
| Add a request hook | The new `demo_prefix.PrefixPlugin` class and its configuration lived in the mounted folder. No gateway core changes were present. |
| Restart and send `hello` again | HTTP 200, reply `fake: DEMO: HELLO`, with `demo_prefix` appended to the trace. |
| Load the slow fixture and send `sleep` | HTTP 504 in 0.688 s. The matching request ID identified a `SlowPlugin` request timeout at 250.378 ms in the content-free hook log. |
| Check the same gateway and send `hello` | Health returned `ok` and the same container returned HTTP 200 with `fake: HELLO`. |

The [Compose instructions](../../docs/deployment.md#versioned-compose-deployment) show the pinned bring-up. The [plugin contract](../../docs/plugins.md) explains the request and response hooks and how `plugins.json` loads them. The [staging instrumentation rehearsal](https://github.com/ITPD-Almo/modular-llm-gateway/pull/129#issuecomment-6854627777) records its own UTC scope and marker check.
