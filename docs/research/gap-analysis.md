# Gap analysis

**Status:** draft for Customer discussion, based on [three alternatives](alternatives.md) and the [comparison](comparison.md). The two entries remain provisional hypotheses, not established gaps. Our [October 9 meeting](../../reports/week-02/meeting-report.md) clarified the DevOps plugin workflow but did not establish either narrower unmet need or a competitive advantage. We still need matched extension and deployment checks. The earlier other-team transcript was background; this joint meeting included our own questions. We will revise or drop these gaps if an existing tool serves the job adequately, as allowed by [DEC-004](../decisions.md#dec-004).

## GAP-01

Link each policy decision to its active policy version

- **Status:** Active
- **Who needs it and what they cannot do:** an IT operator running a small internal gateway needs to explain which policy revision was active when a request was allowed, masked, or rejected, without storing the prompt. This user need is a hypothesis to validate with the Customer; it is not a decision from the other team's meeting.
- **Evidence:** the [P5 comparison](comparison.md) separates request/spend logs from administrative audit. ALT-01 P5 and ALT-03 P5 list ready-made admin audit under Enterprise. ALT-02 P5 includes gateway logs and [Azure Activity Log](https://learn.microsoft.com/en-us/azure/api-management/monitor-api-management), which automatically records subscription-level resource changes. Administrative audit therefore exists in Azure. The reviewed page does not establish a link from each allow, redact, or reject decision to the exact policy version active for that request; that correlation is the narrower hypothesis to check, not a proven missing feature. ALT-03 P1/P5 also allow custom callbacks, so implementing decision-to-policy-version correlation in LiteLLM is a credible alternative. These observations suggest a question about packaging decision-to-version correlation, not a universal absence of audit logging.
- **What closing it looks like:** a source-open static-config gateway records request ID, policy revision, plugin ID, decision, and sanitized reason code, and records the policy revision loaded on restart. It does not record prompt bodies or pretend to provide a full administrative audit system.
- **Buildable by us in this course:** plausible for a single-instance course prototype; tamper-proof storage, compliance certification, and full identity administration are outside this scope.
- **Confidence:** medium in the documented feature split, low in the unmet user need and differentiation.
- **Rests on:** [ASM-01](../assumptions.md#asm-01), [ASM-02](../assumptions.md#asm-02), [ASM-06](../assumptions.md#asm-06).
- **Changed:**
  - Kept the policy-version idea provisional after the Customer clarified the broader plugin workflow, per [DEC-003](../decisions.md#dec-003). Existing-tool reuse is allowed by [DEC-004](../decisions.md#dec-004); feasibility and user need still need checking.

**Gap tests**

| Gap test | Current assessment |
| --- | --- |
| Someone needs it | Pending. Ask the Customer for a recent policy change or rejection they needed to explain and the minimum evidence required. |
| Alternatives do not serve it well | Not established. Compare a LiteLLM callback plus config-version logging and Azure's Activity Log and policy-version correlation options before choosing a new core. |
| Reachable | Yes as a proposed design: one event format and policy revision identifier, with no dynamic admin UI. |
| Buildable by four people | Plausible for a single-instance course prototype; tamper-proof storage, compliance certification, and full identity administration are outside this scope. |

**Validation (proposed owners, awaiting team confirmation)**

Ali12hamdan prepares an example policy event; Mohammed-Nour checks Azure decision-to-version correlation; atkond2point0 checks the LiteLLM extension path in the proposed Week 3 follow-up; confirm the outstanding questions in a Week 3 follow-up. This is a proposed team task, not an agreed meeting action.

## GAP-02

A small reproducible deployment for a fixed policy job

- **Status:** Active
- **Who needs it and what they cannot do:** a small IT team needs a private trial with one provider, static caller credentials, one masking policy, and body-free decision logs, before adopting full gateway administration. This is a narrower job than serving a whole corporation and needs Customer confirmation.
- **Evidence:** ALT-01 P6 separates SaaS, OSS, and enterprise deployment; ALT-02 P6 needs Azure and feature-specific resources; ALT-03 P2/P4/P6 documents PostgreSQL for virtual keys and separate services for Presidio. But ALT-03 P6 also permits a minimal gateway. The [P6 comparison](comparison.md) therefore does not prove a new proxy is simpler for the same job.
- **What closing it looks like:** supply a single-instance deployment recipe using static configuration and a local fixed-format masking plugin, with fake-provider fixtures for allow, redact, reject, and policy failure cases. This is a proposal for later implementation, not Week 1 code.
- **Buildable by us in this course:** plausible if provider count, policy types, and deployment mode stay narrow; production HA, general PII detection, and a management UI are excluded.
- **Confidence:** medium in documented deployment requirements, low in the claim of reduced effort.
- **Rests on:** [ASM-03](../assumptions.md#asm-03), [ASM-04](../assumptions.md#asm-04), [ASM-05](../assumptions.md#asm-05), [ASM-06](../assumptions.md#asm-06).
- **Changed:**
  - The Customer allowed a fake provider and restarting for the first plugin interaction, per [DEC-005](../decisions.md#dec-005). This does not prove the proposed starter takes less effort or confirm its credential and logging limits.

**Gap tests**

| Gap test | Current assessment |
| --- | --- |
| Someone needs it | Pending. Check that the Customer values a static, single-provider pilot and does not require virtual-key administration or SSO immediately. |
| Alternatives do not serve it well | Not established. Run the same narrow job using LiteLLM and a proposed starter; count mandatory services and manual configuration steps. |
| Reachable | Yes as a proposed design: a bounded local recipe and policy fixtures instead of full gateway administration. |
| Buildable by four people | Plausible if provider count, policy types, and deployment mode stay narrow; production HA, general PII detection, and a management UI are excluded. |

**Validation (proposed owner, awaiting team confirmation)**

spaghetti-n-spaghetti documents matched setup steps in the proposed Week 3 follow-up. Keep provider behaviour mocked for initial policy tests; no performance advantage is claimed.

## Directions rejected for now

General-purpose plugins are rejected as a claimed advantage per [DEC-002](../decisions.md#dec-002).

| Candidate | Evidence and reason |
| --- | --- |
| General-purpose request/response plugins | ALT-01 P1 has TypeScript plugins; ALT-03 P1 has Python callbacks and custom guardrails. This is a baseline feature, not a proven gap. |
| Basic PII masking or custom regex | ALT-01 P4 supports custom regex redaction; ALT-02 P4 allows regex/body transformation; ALT-03 P4 includes Presidio. Company-specific effectiveness remains a test question. |
| Body-free logs | ALT-03 P4 documents a global logging control. Include privacy defaults if required, but do not claim no alternative can do this. |
| Better routing in general | All three P3 observations show routing/fallback capabilities. No unmet routing job or benchmark has been established. |
| Full free enterprise governance | ALT-01/ALT-03 have enterprise controls, while ALT-02 has cloud management. Rebuilding SSO, delegated administration, durable audit, and HA is too broad for the course. GAP-01 deliberately covers only decision-to-policy-version correlation. |
| Guaranteed detection of confidential prose | Regex cannot establish semantic confidentiality, and the researched integrations do not establish guaranteed coverage. We have no dataset, accuracy target, or validated approach for that claim. |

## Decision still needed

The evidence supports researching a narrower workflow, not yet building a new gateway. Check the outstanding user needs with the Customer and compare an existing-tool extension, per [DEC-004](../decisions.md#dec-004). If the same job is easy to satisfy there, record the rejected gap rather than inventing a reason to build another core.
