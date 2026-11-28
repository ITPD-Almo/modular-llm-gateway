# User acceptance tests

## The Tests

| Test              | Journey                                                            | Status | SPRINT-09    | SPRINT-10    |
| ----------------- | ------------------------------------------------------------------ | ------ | ------------ | ------------ |
| [UAT-01](#uat-01) | Install and try the gateway with one command                       | Active | Not yet run  | Not yet run  |
| [UAT-02](#uat-02) | Start the gateway with my plugins in the order I set               | Active | Not yet run  | Not yet run  |
| [UAT-03](#uat-03) | See what each plugin did to my request and skip a disabled plugin  | Active | Not yet run  | Not yet run  |

## UAT-01

Install and try the gateway with one command on a clean account, without preparing Git, Python or Docker first.

**Status:** Active

**Start state:** A test account on a clean machine with the reviewed candidate build available at <production-url>, using synthetic seed data and the fake provider.

**Steps:** Run the terminal installer shown at <production-url>, export the PATH line it prints, then run `llmgw demo`, followed by `llmgw serve`, `llmgw health` and `llmgw chat "hello"`.

**Expected result:** All five demo scenarios pass, `llmgw health` returns `{"status":"ok"}`, and the chat reply shows the fake provider answer with a generated request ID.

| Sprint | Date | Runner | Build | Result | Evidence | DEC-nnn |
| ------ | ---- | ------ | ----- | ------ | -------- | ------- |

## UAT-02

Start the gateway with my plugins in the order I set.

**Status:** Active

**Start state:** The gateway is installed as in UAT-01, and a configuration file lists at least two plugins with an explicit order using synthetic seed data.

**Steps:** Run `llmgw plugins` to show the configured order, then `llmgw serve` in one terminal and `llmgw chat "hello"` in another, and read the ordered plugin trace in the reply.

**Expected result:** The trace applies the enabled plugins in the configured order and shows the change each plugin made to the request.

| Sprint | Date | Runner | Build | Result | Evidence | DEC-nnn |
| ------ | ---- | ------ | ----- | ------ | -------- | ------- |

## UAT-03

See what each plugin did to my request and skip a disabled plugin.

**Status:** Active

**Start state:** The server is running with at least two enabled plugins and synthetic seed data.

**Steps:** Send one `llmgw chat` request and record the request ID and the per-plugin changes in the trace, then disable one plugin in the configuration, restart the server, and send the same request again.

**Expected result:** The first reply identifies each enabled plugin's change with a stable request ID, and the second reply skips the disabled plugin while the remaining plugins still apply.

| Sprint | Date | Runner | Build | Result | Evidence | DEC-nnn |
| ------ | ---- | ------ | ----- | ------ | -------- | ------- |
