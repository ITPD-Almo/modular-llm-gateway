# Value proposition

**Status:** two draft positioning statements for discussion. Both depend on [provisional gaps](gap-analysis.md); neither is a validated competitive advantage or an implemented feature. Our own kickoff and Customer validation are missing. Another team's transcript was used as secondary background, not as acceptance of either proposition. Confirm them with this team's Customer and compare the LiteLLM extension path before committing to scope.

## VP-01: Explain a policy decision without keeping the prompt

- **Changed:** kept as a draft based on a provisional gap, per [DEC-002](../decisions.md#dec-002).

**Positioning:** for IT operators running a small internal LLM gateway, we propose a source-open policy event trail that connects each allow, redact, or reject decision to the loaded policy revision and plugin, while omitting prompt and response bodies.

**Closes:** [GAP-01](gap-analysis.md#gap-01-link-each-policy-decision-to-its-active-policy-version).
**Why it might be worth choosing:** provide the narrow policy revision and decision workflow in the starter rather than asking the operator to choose a paid admin-audit tier or write and connect callbacks. LiteLLM already supports custom callbacks and body-free logging; Azure Activity Log already records resource changes. We still need to check whether its existing controls can connect each policy decision to the exact active policy version. This is a packaging hypothesis, not proof those products cannot meet the need.
**What it costs:** fewer administrative capabilities, static configuration, responsibility for secure log storage, and no claim of tamper-proof or compliance-grade audit. Sanitized reason codes give less debugging detail than stored prompts.
**How competitors could respond:** a LiteLLM callback and deployment example could implement a similar trail; Portkey could package it in OSS; Azure could document a policy-version correlation recipe. No technical moat is established.
**How we would check it:** use fixture requests and two policy revisions; every recorded decision must identify the request, loaded revision, and plugin without containing fixture secrets. Then ask the Customer whether that record answers their actual troubleshooting job.

## VP-02: Start with a small private policy trial

- **Changed:** kept as a draft based on a provisional gap, per [DEC-002](../decisions.md#dec-002).

**Positioning:** for a small IT team evaluating company-specific LLM rules, we propose a single-instance starter for one provider, static caller credentials, one masking policy, and body-free decision records, with repeatable allow/redact/reject/error fixtures.

**Closes:** [GAP-02](gap-analysis.md#gap-02-a-small-reproducible-deployment-for-a-fixed-policy-job).
**Why it might be worth choosing:** a deliberately limited recipe might reduce the configuration needed for this specific pilot compared with enabling broader administration and PII integrations. LiteLLM also has a minimal deployment and examples, so lower effort must be demonstrated rather than assumed.
**What it costs:** no SSO, delegated administration, dynamic plugin installation, multi-instance coordination, or general-purpose PII detector in this proposed pilot. A local fixed-format rule does not replace Presidio or a production security review. New plugins/configuration require validation and restart.
**How competitors could respond:** LiteLLM could ship the same narrow recipe and fixtures; Portkey could offer an OSS starter; Azure could supply a policy template. If an existing option provides the same job with less work, prefer extending that option.
**How we would check it:** run a matched setup exercise with a clean configuration and mocked provider, counting required services, manual steps, and policy test coverage. Later confirm real-provider request/response handling after the Customer agrees on the API and scope.

## Assumptions

These are proposed verification tasks and owners, awaiting team confirmation. They are not decisions or action points from a Customer meeting. Customer questions stay pending until our own kickoff; no meeting preparation is being completed in this change.

| ID | Assumption | Supports | How to check | Owner and timing |
| --- | --- | --- | --- | --- |
| A-01 | The Customer needs policy revision and decision evidence but can accept a narrow event trail. | GAP-01, VP-01 | Ask for a recent incident or rule change and show an example sanitized event. | Ali12hamdan, own kickoff; date to be scheduled |
| A-02 | A LiteLLM callback or existing Azure controls do not already satisfy the same workflow with acceptable effort. | GAP-01, VP-01 | Check a LiteLLM callback with the same event fields and Azure decision-to-policy-version correlation. | atkond2point0 (LiteLLM) and Mohammed-Nour (Azure), Week 2 (Oct 5-11) |
| A-03 | Static caller credentials and one provider are acceptable for the initial trial. | GAP-02, VP-02 | Confirm the required users, identity integration, provider API, and exclusions with the Customer. | Mohammed-Nour, own kickoff; date to be scheduled |
| A-04 | The narrow starter takes fewer mandatory services or manual steps than a matched existing gateway setup. | GAP-02, VP-02 | Compare the same policy job against minimal LiteLLM; report the result even if LiteLLM wins. | spaghetti-n-spaghetti, Week 2 (Oct 5-11) |
| A-05 | A fixed-format masking rule serves a real trial need. | GAP-02, VP-02 | Collect synthetic examples and expected outcomes from the Customer; do not collect real personal data. | atkond2point0, own kickoff; date to be scheduled |
| A-06 | Four people can deliver the bounded trial with policy error handling and tests. | GAP-01, GAP-02, VP-01, VP-02 | Estimate tasks together and check team skills before choosing a language or deadline. | All four members, Week 2 (Oct 5-11) |

## Scope to agree

Decide whether this course project needs a new core or an extension of an existing gateway. Language, providers, streaming support, mandatory plugin types, log requirements, and delivery dates are still open. The other team's meeting does not settle these for our team.
