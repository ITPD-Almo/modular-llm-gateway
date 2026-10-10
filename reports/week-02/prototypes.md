# Week 2 prototypes

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
  The task's Story field points to [#22](https://github.com/ITPD-Almo/modular-llm-gateway/issues/22),
  which is a research-formatting issue, not a US-03 story. No actual US-03
  story issue is available to link, so this evidence does not claim story
  acceptance. [ASM-01](../../docs/assumptions.md#asm-01) remains Open.
- **Question:** For the static concept shown at the meeting, does the proposed
  masking and request-record flow show a useful first version, and what is
  missing? The runnable policy-trail spike was not demonstrated to the Customer.
- **What the customer said:** The high-level concept looked fine, but it did
  not show how plugins connect to the gateway. The Customer asked to see plugin
  inputs, outputs, execution order, and loading, and described a first usable
  interaction with two simple plugins, a restart, and a fake provider. This
  feedback is summarized in draft [meeting report PR #28](https://github.com/ITPD-Almo/modular-llm-gateway/pull/28);
  no transcript is published.
- **What changed:** Draft PR #28 records [DEC-006](https://github.com/ITPD-Almo/modular-llm-gateway/pull/28),
  which directs the next design and prototype to show the plugin interface and
  loading order. The product-vision changes are still in that draft PR. The
  disposable decision-trail spike does not implement or validate the requested
  two-plugin interaction.
