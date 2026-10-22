# Week 4 prototypes

## Two-plugin workflow on LiteLLM Proxy

- **What it is:** a disposable code spike that rebuilds the [v0.1.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.1.0) workflow on LiteLLM Proxy 1.106.2. The metadata and uppercase plugins run as proxy callbacks in the configured order, in front of an echoing fake provider and without a real provider key. A third callback copies each plugin's changes into the response. Further runs add a plugin that fails and one that never returns.
- **View:** [the runs on October 22](images/litellm-plugin-workflow.png). The code is in a disposable pull request, closed without merging; none of it is on `main`.
- **Tested:** the workflow of [US-01, #40](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40) AC-01 to AC-03 and [US-03, #42](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42) AC-01 to AC-03, rebuilt on an existing gateway, and [ASM-02](../../docs/assumptions.md#asm-02), because whether an existing gateway already serves the workflow decides whether our own core is justified. This is the Week 3 action point "Compare the same small plugin workflow with an existing gateway and record whether it changes the provisional gaps" from [the Week 3 meeting report](../week-03/meeting-report.md#action-points).
- **Question:** can an existing gateway run the same configured plugin workflow, with acceptable effort, and what does the operator see when a plugin fails or hangs?
- **What the customer said:** not shown yet; planned for the October 23 meeting.
- **What changed:** nothing yet. The observed results are below; ASM-02 and the gaps change only after the Customer's answer.

The same request gave these results on both gateways:

| Check | Our gateway, v0.1.0 | LiteLLM Proxy 1.106.2 |
| --- | --- | --- |
| Plugins run in the configured order, and reversing or removing one in the configuration takes effect after a restart | Yes | Yes |
| `fake: HELLO`, with four ordered `plugin_changes` entries | Yes | Yes, through the extra trace callback; LiteLLM has no per-plugin change list of its own |
| Repeat run without a real provider key | Identical JSON | Identical apart from the generated `id` and `created` fields |
| A plugin raises an error | HTTP 500 `plugin FailingPlugin failed during request processing` | HTTP 500 with only the error text, `boom`; the plugin is named only in the server log's traceback |
| A plugin never returns | No timeout in the code | No response within 30 seconds, twice; the proxy had to be killed |
| Code for the two plugins | 45 lines, including the interface | 82 lines, including the fake provider, the trace callback, and the failing and hanging plugins |
| Setup | `pip install`, one JSON file | `pip install 'litellm[proxy]'`, one YAML file, and a required master key |
| Installed size | 30 packages, 75 MB | 118 packages, 730 MB |

The spike shows that LiteLLM serves the US-01 and US-03 workflow with comparable effort, which is evidence against ASM-02. Neither gateway stops a hanging plugin, and ours names the failing plugin to the caller while LiteLLM does not. Policy-version records ([GAP-01](../../docs/research/gap-analysis.md#gap-01)) and the deployment comparison of [GAP-02](../../docs/research/gap-analysis.md#gap-02) were not tested here.
