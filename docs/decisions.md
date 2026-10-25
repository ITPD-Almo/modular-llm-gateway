# Decisions

## DEC-001

Research Portkey, Azure API Management, and LiteLLM in detail, and keep the other seven candidates at overview level.

- **Status:** Active
- **Date:** 2026-10-05
- **Made by:** Team
- **Source:** the Week 1 research selection, recorded in the [candidate list](https://github.com/ITPD-Almo/modular-llm-gateway/blob/main/reports/week-01/candidate-list.md) and [PR #5](https://github.com/ITPD-Almo/modular-llm-gateway/pull/5).
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
- **Source:** [the joint Week 2 meeting](https://github.com/ITPD-Almo/modular-llm-gateway/blob/main/reports/week-02/meeting-report.md).
- **Why:** companies have different policies and integrations. The Customer confirmed Ali's read-back of a system where parts can be added or removed for each company, and explicitly included routing.

## DEC-004

Allow an existing tool to be used if it meets the required workflow.

- **Status:** Active
- **Date:** 2026-10-09
- **Made by:** Customer
- **Source:** [the joint Week 2 meeting](https://github.com/ITPD-Almo/modular-llm-gateway/blob/main/reports/week-02/meeting-report.md).
- **Why:** building a new gateway core is not a requirement by itself. We still need to show whether an existing tool supports the company's plugin workflow with acceptable effort; no tool was selected in this meeting.

## DEC-005

Use starting the system, adding two simple plugins, sending a request, and seeing the result as the first usable workflow, allowing a restart and a deterministic fake provider.

- **Status:** Active
- **Date:** 2026-10-09
- **Made by:** Customer
- **Source:** [the joint Week 2 meeting](https://github.com/ITPD-Almo/modular-llm-gateway/blob/main/reports/week-02/meeting-report.md).
- **Why:** the Customer wants a small system they can try and evaluate. A fixed provider response makes plugin behaviour easier to check. Ali read back our next step as a proposed flow and a minimum working interaction with mock data, and the Customer agreed. This clarifies the MUP direction; it does not accept our original three story drafts as a complete candidate or require a finished MUP next week.

## DEC-006

Show the plugin inputs, outputs, execution order, and loading approach in the next design and prototype.

- **Status:** Active
- **Date:** 2026-10-09
- **Made by:** Customer
- **Source:** [the joint Week 2 meeting](https://github.com/ITPD-Almo/modular-llm-gateway/blob/main/reports/week-02/meeting-report.md).
- **Why:** our text flow showed masking and a request record, but did not explain how the gateway and its plugins work together. The Customer asked for this missing interface and left the implementation approach to the team.

## DEC-007

Build the first gateway as a Python 3.12 FastAPI service with plugins loaded from a JSON configuration file and a fake provider.

- **Status:** Active
- **Date:** 2026-10-17
- **Made by:** Team
- **Source:** task #43 acceptance criteria.
- **Why:** a small in-process interface makes plugin order, transformations, and failure behaviour explicit and testable before a real provider or production deployment is added.

## DEC-008

Prioritize a documented plugin-management system for developers and DevOps operators that another operator can support, rather than a fixed catalogue of example plugins.

- **Status:** Active
- **Date:** 2026-10-23
- **Made by:** Customer
- **Source:** [the October 23 review report](https://github.com/ITPD-Almo/modular-llm-gateway/blob/41530d7c5ad25028dcfe5a0d28d8103802b14a5d/reports/week-04/meeting-report.md).
- **Why:** The Customer clarified the intended developer/DevOps users and asked for enough documentation to create a compatible plugin and hand the system to another operator; a larger set of examples alone does not provide that value.

## DEC-009

Use a simple plugin that replaces incoming content with A text and the provider reply with B text to explain how a new plugin enters the gateway.

- **Status:** Active
- **Date:** 2026-10-23
- **Made by:** Customer
- **Source:** [the October 23 review report](https://github.com/ITPD-Almo/modular-llm-gateway/blob/41530d7c5ad25028dcfe5a0d28d8103802b14a5d/reports/week-04/meeting-report.md).
- **Why:** The plugin-addition process remained unclear in the attempted demonstration. The requested two-stage replacement is a concrete explanation/test example, not a new default transformation or a requirement for automatic discovery.

## DEC-010

Handle badly written or sleeping plugins without leaving the gateway unusable, identifying the problematic plugin and providing diagnostic information.

- **Status:** Active
- **Date:** 2026-10-23
- **Made by:** Customer
- **Source:** [the October 23 review report](https://github.com/ITPD-Almo/modular-llm-gateway/blob/41530d7c5ad25028dcfe5a0d28d8103802b14a5d/reports/week-04/meeting-report.md).
- **Why:** The Customer agreed that management includes a plugin which stalls and an operator who must locate the problem. The meeting did not select a timeout number, status code, isolation design, capacity or fail-versus-skip policy.

## DEC-011

Show progress against a plan beyond one iteration and use asynchronous questions when clarification is needed.

- **Status:** Active
- **Date:** 2026-10-23
- **Made by:** Customer
- **Source:** [the October 23 review report](https://github.com/ITPD-Almo/modular-llm-gateway/blob/41530d7c5ad25028dcfe5a0d28d8103802b14a5d/reports/week-04/meeting-report.md).
- **Why:** The Customer wants evidence of planning, execution, progress tracking and adjustment over several weeks, and explicitly allowed questions between meetings. Flexibility about presentations does not waive the course requirements.
