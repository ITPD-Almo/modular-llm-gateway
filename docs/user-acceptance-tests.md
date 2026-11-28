# User acceptance tests

## The Tests

| Test              | Journey                                                           | Status | SPRINT-09   | SPRINT-10   |
| ----------------- | ----------------------------------------------------------------- | ------ | ----------- | ----------- |
| [UAT-01](#uat-01) | Install and try the gateway with one command                      | Active | Not yet run | Not yet run |
| [UAT-02](#uat-02) | Start the gateway with my plugins in the order I set              | Active | Not yet run | Not yet run |
| [UAT-03](#uat-03) | See what each plugin did to my request and skip a disabled plugin | Active | Not yet run | Not yet run |

## UAT-01

Install and try the gateway with one command on a clean account, without preparing Git, Python or Docker first, and confirm the deployed candidate answers.

**Status:** Active

**Start state:** The reviewed candidate source SHA is deployed to staging and reachable at `https://<production-url>:8001` from a campus client, with the private curl configuration (demo CA plus the owner code) supplied through the Moodle wrapper. Synthetic seed data and the fake provider are in use.

**Steps:** On a clean machine, run the terminal installer pinned to the same reviewed source SHA per [the terminal walkthrough](terminal.md#one-line-installation), then export the PATH line it prints. Run `llmgw demo` and `llmgw --version`. Then exercise the deployed candidate with the private curl configuration: `GET https://<production-url>:8001/health` and one `POST /v1/chat/completions` synthetic chat. Record the deployed build's tag or source SHA from the deployment receipt.

**Expected result:** All five demo scenarios pass, `llmgw --version` matches the reviewed candidate, authenticated health returns HTTP 200 with `{"status":"ok"}`, and the chat reply carries the fake provider answer with an `X-Request-ID` header.

| Sprint | Date | Runner | Build | Result | Evidence | DEC-nnn |
| ------ | ---- | ------ | ----- | ------ | -------- | ------- |

## UAT-02

Start the gateway with my plugins in the order I set.

**Status:** Active

**Start state:** The candidate ref is installed as in UAT-01 on the runner machine or the VM, and the fixture `examples/ab-plugins.json` lists the plugins in order: `gateway.plugins.add_metadata.MetadataPlugin` first, then `examples.ab_plugin.ABReplacePlugin`.

**Steps:** Run `llmgw plugins --config examples/ab-plugins.json` to show the configured order, start the test instance with `llmgw serve --config examples/ab-plugins.json`, and send `llmgw chat "hello"` from another terminal.

**Expected result:** `llmgw plugins` prints the two entries in the fixture order, and the chat trace shows `add_metadata` applied first and `ab_replace` applied second, each with its change to the request.

| Sprint | Date | Runner | Build | Result | Evidence | DEC-nnn |
| ------ | ---- | ------ | ----- | ------ | -------- | ------- |

## UAT-03

See what each plugin did to my request and skip a disabled plugin.

**Status:** Active

**Start state:** An isolated instance runs with the fixture `examples/slow-plugins.json`: `gateway.plugins.add_metadata.MetadataPlugin`, then `examples.slow_plugin.SlowPlugin`, then `gateway.plugins.uppercase.UppercasePlugin`, using synthetic seed data.

**Steps:** Start `llmgw serve --config examples/slow-plugins.json` and send one `llmgw chat "hello"` request; record the `X-Request-ID` and the per-plugin changes in the trace. Copy the fixture, remove the `gateway.plugins.uppercase.UppercasePlugin` entry, stop the instance, restart it with `llmgw serve --config <edited-fixture>` and send the same request again.

**Expected result:** The first trace shows all three plugins with their changes and a stable request ID; the second trace no longer contains `uppercase` and the reply keeps its original case, while `add_metadata` and `slow` still run.

| Sprint | Date | Runner | Build | Result | Evidence | DEC-nnn |
| ------ | ---- | ------ | ----- | ------ | -------- | ------- |
