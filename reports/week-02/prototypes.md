# Week 2 prototypes

## Text concept of the gateway flow

- **What it is:** a short text presentation of our research, an employee request being masked before forwarding, a policy-version decision record, and a proposed first-version scope. It was a static concept, not a running gateway.
- **View:** the [proposed flow](images/gateway-flow-concept.png) and the [first-version proposal](images/gateway-scope-concept.png). The screenshots were captured after the meeting from the original prepared slides; they are not screenshots of the live call.
- **Tested:** the proposed workflow behind [GAP-01](../../docs/research/gap-analysis.md#gap-01) and [ASM-01](../../docs/assumptions.md#asm-01). No story issue's AC-nn was demonstrated, and ASM-01 remains Open.
- **Question:** does the proposed masking and request-record flow show a useful first version, and what is missing?
- **What the customer said:** the high-level flow looked fine, but it did not explain the interface between the gateway and its plugins. The Customer asked to see plugin inputs, outputs, ordering, and loading. A first usable interaction can use two simple plugins, a restart, and a fake provider.
- **What changed:** [DEC-006](../../docs/decisions.md#dec-006), listed in the [meeting report](meeting-report.md#decisions), now informs the [plugin-interface requirement](../../docs/product-vision.md#con-01). The [goal](../../docs/product-vision.md#goal) focuses on DevOps users composing plugins, per [DEC-003](../../docs/decisions.md#dec-003), and states the small usable interaction from [DEC-005](../../docs/decisions.md#dec-005). [BND-04](../../docs/product-vision.md#bnd-04) records the allowed restart. The revised story candidate and weekly summary still need to carry these changes.

## Policy decision trail spike

- **What it is:** A disposable Python prototype with a local fake provider. It
  masks a synthetic employee identifier and writes a body-free decision record
  tied to the policy revision loaded at startup. A separate LiteLLM SDK
  comparison checks callback-based records using mocked responses. Neither
  experiment was presented as the Customer's requested two-plugin interaction.
- **View:** [Masked request reaching the fake provider](images/spike-masked-request.png),
  [decision records across r1 and r2](images/spike-decision-records.png), and
  [credential rejection](images/spike-reject-record.png). The source and
  LiteLLM comparison are in [disposable PR #36](https://github.com/ITPD-Almo/modular-llm-gateway/pull/36),
  which is closed without merging as required; none of its code is on `main`.
- **Tested:** The local integration check covers masking, allow, rejection
  without a provider call, r1/r2 record retention after restart, the body-free
  schema, and unknown-ID lookup. The LiteLLM SDK check covers `CustomLogger`,
  mocked responses, separate r1/r2 processes, and explicit logging for a
  pre-provider rejection. See the [spike task and AC-01–AC-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/34).
  The task's Story field still points to [#22](https://github.com/ITPD-Almo/modular-llm-gateway/issues/22),
  which is a research-formatting issue, not a US-03 story. Ali12hamdan's
  approval of this evidence PR confirms that the real story link and its
  acceptance criteria are still missing; no US-03 issue exists in the current
  issue list. This evidence therefore does not claim story acceptance.
  [ASM-01](../../docs/assumptions.md#asm-01) remains Open.
- **Question:** For the static concept shown at the meeting, does the proposed
  masking and request-record flow show a useful first version, and what is
  missing? The runnable policy-trail spike was not demonstrated to the Customer.
- **What the customer said:** The high-level concept looked fine, but it did
  not show how plugins connect to the gateway. The Customer asked to see plugin
  inputs, outputs, execution order, and loading, and described a first usable
  interaction with two simple plugins, a restart, and a fake provider. This
  feedback is summarized in the [meeting report](meeting-report.md#summary);
  no transcript is published.
- **What changed:** The meeting report records [DEC-006](../../docs/decisions.md#dec-006),
  which directs the next design and prototype to show the plugin interface and
  loading order. The [vision](../../docs/product-vision.md#con-01) now calls for that interface. The
  disposable decision-trail spike does not implement or validate the requested
  two-plugin interaction.
