# Value proposition

**Status:** two draft positioning statements based on [provisional gaps](gap-analysis.md); neither is a validated competitive advantage or an implemented feature. In the [October 9 meeting](../../reports/week-02/meeting-report.md), the Customer clarified the plugin workflow but did not confirm these narrower advantages. The [new goal](../product-vision.md#goal) follows that feedback, while the research still needs an existing-tool comparison. [DEC-002](../decisions.md#dec-002) remains the record of our earlier research direction.

The two directions come from [DEC-002](../decisions.md#dec-002).

## VP-01

Explain a policy decision without keeping the prompt

- **Status:** Active
- **User:** DevOps staff in medium or large companies evaluating a small internal gateway.
- **Problem:** they need to explain which policy revision was active when a request was allowed, masked, or rejected, without storing the prompt, per [GAP-01](gap-analysis.md#gap-01).
- **What we do that the alternatives do not:** we propose a source-open policy event trail that connects each allow, redact, or reject decision to the loaded policy revision and plugin, while omitting prompt and response bodies. Provide the narrow policy revision and decision workflow in the starter rather than asking the operator to choose a paid admin-audit tier or write and connect callbacks. LiteLLM already supports custom callbacks and body-free logging; Azure Activity Log already records resource changes. We still need to check whether its existing controls can connect each policy decision to the exact active policy version. This is a packaging hypothesis, not proof those products cannot meet the need.
- **Closes:** [GAP-01](gap-analysis.md#gap-01).
- **Rests on:** [ASM-01](../assumptions.md#asm-01), [ASM-02](../assumptions.md#asm-02), [ASM-06](../assumptions.md#asm-06).
- **What it costs:** fewer administrative capabilities, static configuration, responsibility for secure log storage, and no claim of tamper-proof or compliance-grade audit. Sanitized reason codes give less debugging detail than stored prompts.
- **How a competitor would respond:** a LiteLLM callback and deployment example could implement a similar trail; Portkey could package it in OSS; Azure could document a policy-version correlation recipe. No technical moat is established.
- **Changed:**
  - Aligned the user with the DevOps role identified in [DEC-003](../decisions.md#dec-003), while keeping the proposed advantage unverified. The plugin interface is now the next design question, per [DEC-006](../decisions.md#dec-006).

**How we would check it**

Use fixture requests and two policy revisions; every recorded decision must identify the request, loaded revision, and plugin without containing fixture secrets. Then ask the Customer whether that record answers their actual troubleshooting job.

## VP-02

Start with a small private policy trial

- **Status:** Active
- **User:** DevOps staff in medium or large companies trying company-specific LLM rules.
- **Problem:** they need a private trial with one provider, static caller credentials, one masking policy, and body-free decision logs, before adopting full gateway administration, per [GAP-02](gap-analysis.md#gap-02).
- **What we do that the alternatives do not:** we propose a single-instance starter for one provider, static caller credentials, one masking policy, and body-free decision records, with repeatable allow/redact/reject/error fixtures. A deliberately limited recipe might reduce the configuration needed for this specific pilot compared with enabling broader administration and PII integrations. LiteLLM also has a minimal deployment and examples, so lower effort must be demonstrated rather than assumed.
- **Closes:** [GAP-02](gap-analysis.md#gap-02).
- **Rests on:** [ASM-03](../assumptions.md#asm-03), [ASM-04](../assumptions.md#asm-04), [ASM-05](../assumptions.md#asm-05), [ASM-06](../assumptions.md#asm-06).
- **What it costs:** no SSO, delegated administration, dynamic plugin installation, multi-instance coordination, or general-purpose PII detector in this proposed pilot. A local fixed-format rule does not replace Presidio or a production security review. New plugins/configuration require validation and restart.
- **How a competitor would respond:** LiteLLM could ship the same narrow recipe and fixtures; Portkey could offer an OSS starter; Azure could supply a policy template. If an existing option provides the same job with less work, prefer extending that option.
- **Changed:**
  - Aligned the user with the DevOps role identified in [DEC-003](../decisions.md#dec-003), while keeping the proposed advantage unverified. The plugin interface is now the next design question, per [DEC-006](../decisions.md#dec-006).

**How we would check it**

Run a matched setup exercise with a clean configuration and mocked provider, counting required services, manual steps, and policy test coverage. Later confirm real-provider request/response handling after the Customer agrees on the API and scope.

## Scope to agree

An existing tool is acceptable if it fits, per [DEC-004](../decisions.md#dec-004); no implementation path has been selected. [DEC-005](../decisions.md#dec-005) allows a fake provider and restarting for the first usable plugin interaction. Specific plugin types, credentials, body retention, streaming support, and the revised story candidate still need decisions. Python was discussed as a likely option, not selected as a final team technology choice.
