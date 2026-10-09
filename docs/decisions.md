# Decisions

## DEC-001

Research Portkey, Azure API Management, and LiteLLM in detail, and keep the other seven candidates at overview level.

- **Status:** Active
- **Date:** 2026-10-05
- **Made by:** Team
- **Source:** the Week 1 research selection, recorded in the [candidate list](../reports/week-01/candidate-list.md) and [PR #5](https://github.com/ITPD-Almo/modular-llm-gateway/pull/5).
- **Why:** this gives us a direct product, an enterprise API platform, and a self-hosted option to compare. We can return to the other candidates later.

## DEC-002

Explore linking each policy decision to its policy version and a small private policy trial as possible gaps, without treating plugins alone as an advantage.

- **Status:** Active
- **Date:** 2026-10-05
- **Made by:** Team
- **Source:** the Week 1 research and team review in [PR #5](https://github.com/ITPD-Almo/modular-llm-gateway/pull/5).
- **Why:** existing products already offer custom logic, masking options, logs, and routing. We still need to check whether users need these two narrower jobs and whether existing extensions can handle them. Both gaps remain provisional; we have not decided to build a new gateway core.

## DEC-003

Focus the gateway on DevOps users composing company-specific plugins to process requests and responses and route requests.

- **Status:** Active
- **Date:** 2026-10-09
- **Made by:** Customer
- **Source:** [the joint Week 2 meeting](../reports/week-02/meeting-report.md).
- **Why:** companies have different policies and integrations. The Customer confirmed Ali's read-back of a system where parts can be added or removed for each company, and explicitly included routing.

## DEC-004

Allow an existing tool to be used if it meets the required workflow.

- **Status:** Active
- **Date:** 2026-10-09
- **Made by:** Customer
- **Source:** [the joint Week 2 meeting](../reports/week-02/meeting-report.md).
- **Why:** building a new gateway core is not a requirement by itself. We still need to show whether an existing tool supports the company's plugin workflow with acceptable effort; no tool was selected in this meeting.

## DEC-005

Use starting the system, adding two simple plugins, sending a request, and seeing the result as the first usable workflow, allowing a restart and a deterministic fake provider.

- **Status:** Active
- **Date:** 2026-10-09
- **Made by:** Customer
- **Source:** [the joint Week 2 meeting](../reports/week-02/meeting-report.md).
- **Why:** the Customer wants a small system they can try and evaluate. A fixed provider response makes plugin behaviour easier to check. Ali read back our next step as a proposed flow and a minimum working interaction with mock data, and the Customer agreed. This clarifies the MUP direction; it does not accept our original three story drafts as a complete candidate or require a finished MUP next week.

## DEC-006

Show the plugin inputs, outputs, execution order, and loading approach in the next design and prototype.

- **Status:** Active
- **Date:** 2026-10-09
- **Made by:** Customer
- **Source:** [the joint Week 2 meeting](../reports/week-02/meeting-report.md).
- **Why:** our text flow showed masking and a request record, but did not explain how the gateway and its plugins work together. The Customer asked for this missing interface and left the implementation approach to the team.
