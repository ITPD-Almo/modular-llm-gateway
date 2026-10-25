# Gateway check for the Week 4 demo

Checked on October 25, 2026, by Mohammed-Nour, on the runtime branch of [#56](https://github.com/ITPD-Almo/modular-llm-gateway/issues/56) at `21cd475` with this task's guide and examples on top. These are local technical results. The Customer has not accepted or rejected any of these stories; no verdict is recorded here.

## Setup

- **Machine:** Linux 7.0, Python 3.12.3, no provider key, no `.env` file.
- **Clean install:** a fresh `git clone --recurse-submodules`, then the [setup guide](../../docs/setup.md)'s POSIX steps. Clone, virtual environment, install and `python -m pytest` took 58 seconds, and all 34 tests of that branch passed.
- **Not run:** Windows PowerShell. A second member has not yet followed the recipe.
- **Demo:** every step of the [demo](../../docs/demo.md) was run against `python -m uvicorn gateway.main:create_app --factory` over real HTTP with curl, restarting between configurations. Its expected outputs are copied from this run.
- **Cleanup:** the tracked configuration was restored afterwards.

## Story checks

| Story and criterion | Observed result |
| --- | --- |
| [US-01, #40](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), AC-01 | From a clean clone, following the setup guide starts the gateway with `MetadataPlugin` and `UppercasePlugin` from `config/plugins.json`; `/health` answers `{"status":"ok"}`. |
| US-01, AC-02 | `plugin_trace` is `["metadata","uppercase"]`, and the four `plugin_changes` entries follow the same order at each stage. |
| US-01, AC-03 | After reversing the list and restarting, the trace is `["uppercase","metadata"]`. After removing uppercase and restarting, the reply is `fake: hello` with trace `["metadata"]`. |
| [US-02, #41](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), AC-01 | [The plugin guide](../../docs/plugins.md) states hook inputs and outputs, field ownership, order, loading, restarting and every failure result. |
| US-02, AC-02 | Both bundled plugins and the new `examples/ab_plugin.py` use only the two documented hooks. The A/B plugin loads from `examples/ab-plugins.json` with no change under `gateway/`: the client gets `BBBB`, and the provider received `AAAA`. `tests/test_ab_example.py` passes. |
| [US-03, #42](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), AC-01 | The setup guide's curl request reaches the fake provider and returns HTTP 200. |
| US-03, AC-02 | The response's `plugin_changes` lists each plugin's change to the request and then to the response, in order. |
| US-03, AC-03 | Two identical requests return identical bodies, apart from the `X-Request-ID` header; no key is set. |
| [US-04, #52](https://github.com/ITPD-Almo/modular-llm-gateway/issues/52), AC-01 | A request hook sleeping 5 seconds under the default 250 ms deadline returns HTTP 504 `plugin SlowPlugin timed out during request processing` in 0.31 seconds. |
| US-04, AC-02 | After the request-hook timeout, `/health` returns 200 and the next request returns `fake: HELLO`. A response hook sleeping 5 seconds (`tests.worker_plugins.SlowResponse`) returns HTTP 504 `plugin SlowResponse timed out during response processing` in 0.32 seconds, and the following `/health` and request succeed the same way. |
| US-04, AC-03 | The timed-out request's events carry plugin, stage, elapsed time and reason `timeout`, with no message content. Repeated-timeout resource bounds are covered by the runtime's tests, not re-measured here. |
| US-04, AC-04 | Normal, changed-order and timeout/recovery cases are reproducible from the demo. The fail-the-request policy and the 250 ms deadline still need the Customer's verdict. |

## Before this runtime

On v0.1.0 (`6bd7eef`), one request held by a sleeping plugin never returned. With 45 such requests in flight, `/health` and a healthy request also got no answer within 10 seconds. The matched comparison of [#58](https://github.com/ITPD-Almo/modular-llm-gateway/issues/58) records how these numbers were measured.
