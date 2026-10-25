# Week 4 prototypes

## Two-plugin workflow on LiteLLM Proxy

- **What it is:** a disposable code spike that rebuilds the [v0.1.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.1.0) workflow on LiteLLM Proxy 1.106.2. The metadata and uppercase plugins run as proxy callbacks in the configured order, in front of an echoing fake provider and without a real provider key. A third callback copies each plugin's changes into the response. Further runs add a plugin that fails and one that never returns.
- **View:** [the runs on October 22](images/litellm-plugin-workflow.png). The spike code is in [a pull request closed without merging](https://github.com/ITPD-Almo/modular-llm-gateway/pull/74); none of it is on `main`.
- **Tested:** the workflow of [US-01, #40](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40) AC-01 to AC-03 and [US-03, #42](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42) AC-01 to AC-03, rebuilt on an existing gateway, and [ASM-02](../../docs/assumptions.md#asm-02), because whether an existing gateway already serves the workflow decides whether our own core is justified. This carries out the Week 3 action point "Compare the same small plugin workflow with an existing gateway and record whether it changes the provisional gaps" from [the Week 3 meeting report](../week-03/meeting-report.md#action-points).
- **Question:** can an existing gateway run the same configured plugin workflow, with acceptable effort, and what does the operator see when a plugin fails or hangs?
- **What the customer said:** nothing yet. The comparison was not demonstrated at the October 23 review, so there is no Customer reaction to it.
- **What changed:** the evidence is added to [ASM-02](../../docs/assumptions.md#asm-02), [ASM-04](../../docs/assumptions.md#asm-04), [ALT-03](../../docs/research/alternatives.md#alt-03) and the [GAP-02 gap tests](../../docs/research/gap-analysis.md#gap-02). No assumption changes status and no decision is recorded, because the Customer has not reacted.

### How it was run

- **Machine:** Linux 7.0, Python 3.12.3, no provider key, no network calls to a provider.
- **Our gateway:** `main` at `6bd7eef` (release v0.1.0), installed with `pip install -e ".[test]"`; resolved FastAPI 0.162.0, Uvicorn 0.54.0, Pydantic 2.14.1. Started with `python -m uvicorn gateway.main:create_app --factory` and a JSON plugin list selected by `GATEWAY_CONFIG`.
- **LiteLLM:** `pip install 'litellm[proxy]'` resolved LiteLLM Proxy 1.106.2 on 2026-10-22; to reproduce, pin it with `pip install 'litellm[proxy]==1.106.2'`, since an unpinned install can now resolve a newer version. Callbacks are registered by the dotted path of an instance under `litellm_settings.callbacks` and modify requests in `async_pre_call_hook` and responses in `async_post_call_success_hook`, as the [call hooks guide](https://docs.litellm.ai/docs/proxy/call_hooks) describes. The spike's `run.sh` starts the proxy with one YAML file per case and sends the setup guide's request twice.
- **Cases:** default order, reversed order, one plugin removed, a plugin that raises, a plugin that sleeps. Both gateways were run on 2026-10-22 with the [LiteLLM spike](https://github.com/ITPD-Almo/modular-llm-gateway/tree/c891e686bd820e32f7d7a2a3759163b3f30e33c1/spikes/litellm-check) (`run.sh` and `results.txt`).
- **Our hang cases:** measured on 2026-10-25 with the [v0.1.0 hang check](https://github.com/ITPD-Almo/modular-llm-gateway/tree/c891e686bd820e32f7d7a2a3759163b3f30e33c1/spikes/v010-hang-check). Its `run.sh` holds the sleeping plugin, the curl limits (10 seconds), the thread count from `/proc` and the server start and kill steps, and `results.txt` holds the output. Both spikes are on the branch of the [closed pull request](https://github.com/ITPD-Almo/modular-llm-gateway/pull/74), not on `main`.

### Results

| Check | Our gateway, v0.1.0 | LiteLLM Proxy 1.106.2 |
| --- | --- | --- |
| Plugins run in the configured order, and reversing or removing one in the configuration takes effect after a restart | Yes | Yes |
| `fake: HELLO`, with four ordered `plugin_changes` entries | Yes | Yes, through the extra trace callback; LiteLLM has no per-plugin change list of its own |
| Repeat run without a real provider key | Identical JSON | Identical apart from the generated `id` and `created` fields |
| A plugin raises an error | HTTP 500 `plugin FailingPlugin failed during request processing` | HTTP 500 with only the error text, `boom`; the plugin is named only in the server log's traceback |
| One request hits a plugin that hangs (ours sleeps 60 s; LiteLLM's never returns) | The request gets no response before the client's 10-second limit; `/health` still answers 200 in 0.03 s | No response within 30 seconds, twice; the proxy had to be killed |
| 45 requests hit a plugin that sleeps 30 s, then a healthy request is sent | `/health` and the healthy request both get no response within 10 s; the server holds 45 threads | Not run |
| Code for the two plugins | 45 lines, including the interface | 82 lines, including the fake provider, the trace callback, and the failing and hanging plugins |
| Setup | `pip install`, one JSON file | `pip install 'litellm[proxy]'`, one YAML file, and a required master key |
| Installed size | 30 packages, 75 MB | 118 packages, 730 MB |

### Comparison by concern

- **Extension effort:** both need one Python class per plugin and one configuration entry, then a restart. LiteLLM needs an extra callback to show each plugin's changes, a master key and a provider handler for the fake model. Measured in lines, ours is smaller (45 against 82), but the two files do not contain exactly the same extras, so the difference is indicative, not a measured productivity advantage.
- **Ordering:** both follow the configured order. LiteLLM's guide states registration order only for its model-listing hook; for request and response hooks the order was observed, not documented.
- **Failure and timeouts:** in the tested default configurations, neither gateway returned a response for a hanging plugin within the client's limit (10 seconds for ours, 30 seconds for LiteLLM). LiteLLM's [timeout settings](https://docs.litellm.ai/docs/proxy/timeout) are documented as router and call timeouts; the guides read neither describe nor rule out a limit on callbacks, and **no LiteLLM timeout setting was configured**, so whether a configured timeout bounds a hanging callback is untested. In ours, a few hung requests exhaust the server's worker threads, after which even `/health` stops answering. That is the problem [US-04, #52](https://github.com/ITPD-Almo/modular-llm-gateway/issues/52) addresses.
- **Diagnostic information:** ours names the failing plugin and stage to the caller. LiteLLM returns the raw exception text to the caller and names the plugin only in the server log.
- **Handover:** both are started from one command and one configuration file. Ours documents its plugin contract in [docs/plugins.md](../../docs/plugins.md); LiteLLM's hook contract is spread across its callback and guardrail guides. **No second person followed either setup**, so handover effort is not measured.

### Conclusion

LiteLLM serves the US-01 and US-03 workflow with comparable effort, which is evidence against ASM-02. It does not settle ASM-02, because the Customer has not reacted and the Azure half of that assumption was not checked. In the tested default configurations neither gateway answered a request held by a hanging plugin, and ours names the failing plugin to the caller while LiteLLM does not; LiteLLM with a configured timeout was not tested. These are the only observed differences in our favor. They are small, and LiteLLM could close them with more callback code. Policy-version records ([GAP-01](../../docs/research/gap-analysis.md#gap-01)) and the deployment comparison of [GAP-02](../../docs/research/gap-analysis.md#gap-02) were not tested here.
