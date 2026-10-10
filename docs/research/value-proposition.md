# Value proposition

**Status:** two draft positioning statements for discussion. Both depend on [provisional gaps](gap-analysis.md); neither is a validated competitive advantage or an implemented feature. Our own kickoff and Customer validation are missing. Another team's transcript was used as secondary background, not as acceptance of either proposition. Confirm them with this team's Customer and compare the LiteLLM extension path before committing to scope.

The two directions come from [DEC-002](../decisions.md#dec-002).

## VP-01: Explain a policy decision without keeping the prompt

**Positioning:** for IT operators running a small internal LLM gateway, we propose a source-open policy event trail that connects each allow, redact, or reject decision to the loaded policy revision and plugin, while omitting prompt and response bodies.

**Closes:** [GAP-01](gap-analysis.md#gap-01).

- **Rests on:** [ASM-01](../assumptions.md#asm-01), [ASM-02](../assumptions.md#asm-02), [ASM-06](../assumptions.md#asm-06).

**Why it might be worth choosing:** provide the narrow policy revision and decision workflow in the starter rather than asking the operator to choose a paid admin-audit tier or write and connect callbacks. LiteLLM already supports custom callbacks and body-free logging; Azure Activity Log already records resource changes. We still need to check whether its existing controls can connect each policy decision to the exact active policy version. This is a packaging hypothesis, not proof those products cannot meet the need.
**What it costs:** fewer administrative capabilities, static configuration, responsibility for secure log storage, and no claim of tamper-proof or compliance-grade audit. Sanitized reason codes give less debugging detail than stored prompts.
**How competitors could respond:** a LiteLLM callback and deployment example could implement a similar trail; Portkey could package it in OSS; Azure could document a policy-version correlation recipe. No technical moat is established.
**How we would check it:** use fixture requests and two policy revisions; every recorded decision must identify the request, loaded revision, and plugin without containing fixture secrets. Then ask the Customer whether that record answers their actual troubleshooting job.

## VP-02: Start with a small private policy trial

**Positioning:** for a small IT team evaluating company-specific LLM rules, we propose a single-instance starter for one provider, static caller credentials, one masking policy, and body-free decision records, with repeatable allow/redact/reject/error fixtures.

**Closes:** [GAP-02](gap-analysis.md#gap-02).

- **Rests on:** [ASM-03](../assumptions.md#asm-03), [ASM-04](../assumptions.md#asm-04), [ASM-05](../assumptions.md#asm-05), [ASM-06](../assumptions.md#asm-06).

**Why it might be worth choosing:** a deliberately limited recipe might reduce the configuration needed for this specific pilot compared with enabling broader administration and PII integrations. LiteLLM also has a minimal deployment and examples, so lower effort must be demonstrated rather than assumed.
**What it costs:** no SSO, delegated administration, dynamic plugin installation, multi-instance coordination, or general-purpose PII detector in this proposed pilot. A local fixed-format rule does not replace Presidio or a production security review. New plugins/configuration require validation and restart.
**How competitors could respond:** LiteLLM could ship the same narrow recipe and fixtures; Portkey could offer an OSS starter; Azure could supply a policy template. If an existing option provides the same job with less work, prefer extending that option.
**How we would check it:** run a matched setup exercise with a clean configuration and mocked provider, counting required services, manual steps, and policy test coverage. Later confirm real-provider request/response handling after the Customer agrees on the API and scope.

## Scope to agree

Decide whether this course project needs a new core or an extension of an existing gateway. Language, providers, streaming support, mandatory plugin types, log requirements, and delivery dates are still open. The other team's meeting does not settle these for our team.
