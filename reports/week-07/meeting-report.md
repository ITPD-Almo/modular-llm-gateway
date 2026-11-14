# Week 7 customer feedback and review evidence

## Metadata

- **Record basis:** confirmed [customer guidance](../week-06/meeting-report.md#summary) and the [Week 7 operator walkthrough](compose-demo-evidence.md).
- **Review script:** [Week 7 agenda and questions](meeting-script.md).
- **Recording and transcript:** project-specific review evidence and its publication permissions are pending.

## Previous action points

| Action | Outcome | Decision |
| --- | --- | --- |
| Package the gateway as a versioned Docker image with a Docker Compose file and bring it up at the review. [Previous action points](../week-06/meeting-report.md#action-points) | [#129](https://github.com/ITPD-Almo/modular-llm-gateway/pull/129) merged. The [recorded synthetic walkthrough](compose-demo-evidence.md) verifies the configuration, chat, timeout and recovery. | [DEC-012](../../docs/decisions.md#dec-012) |
| Write and rehearse the review script with the four dashboards, QR-08 QRT-01, the story criteria and the threshold proposal. [Previous action points](../week-06/meeting-report.md#action-points) | The [script](meeting-script.md) is prepared. The local operator walkthrough and the checked quality-test results are available. | None |
| Send the carried questions through the asynchronous channel and record the replies. [Previous action points](../week-06/meeting-report.md#action-points) | The questions are carried into the agenda. Replies are pending. | None |
| Show each story criterion and record its verdict. [Previous action points](../week-06/meeting-report.md#action-points) | The agenda covers seven stories and 24 criteria. The seven story verdicts remain open. | None |
| Present the LiteLLM comparison and record what it changes. [Previous action points](../week-06/meeting-report.md#action-points) | The [comparison](../../docs/research/comparison.md) and [spike](../week-04/prototypes.md#two-plugin-workflow-on-litellm-proxy) inform the questions about the operator's adoption decision. That decision is pending. | None |

## Previous open questions

| Question | Answer | Decision |
| --- | --- | --- |
| Do US-01 to US-04, US-09, US-11 and US-12 meet their criteria? [Previous open questions](../week-06/meeting-report.md#open-questions) | Story verdicts pending. | None |
| Are the proposed 250 ms hook deadline, HTTP 504 and capacity behavior acceptable? [Previous open questions](../week-06/meeting-report.md#open-questions) | The technical walkthrough shows the timeout and recovery. Acceptance of the trial settings is pending. | None |
| Should the gateway track a policy version, and what content may it retain? [Previous open questions](../week-06/meeting-report.md#open-questions) | The current telemetry uses allowlisted fields. The trial's policy-version and retention decisions are pending. | None |
| Are static caller credentials and provider limits sufficient? [Previous open questions](../week-06/meeting-report.md#open-questions) | The trial constraints remain open. | None |
| Which synthetic examples should masking support? [Previous open questions](../week-06/meeting-report.md#open-questions) | The target cases and expected outputs remain open. | None |
| What would justify choosing this gateway over ordered functions or LiteLLM? [Previous open questions](../week-06/meeting-report.md#open-questions) | The operator demo provides a concrete config-only extension and failure diagnosis for comparison. A customer choice is pending. | None |

## Summary

- The verified operator flow starts a pinned image, adds a Python class through JSON, and shows the resulting change, trace and recovery.
- UT-01 plans five representative operators, with three valid sessions as the minimum. The main task is an unaided startup and configured chat.
- The design week records implementation evidence and a test plan. Customer verdicts and the Week 8 usability outcomes remain open.

## Decisions

The current work follows the confirmed [Compose decision](../../docs/decisions.md#dec-012), [terminal workflow decision](../../docs/decisions.md#dec-013) and [feedback-channel decision](../../docs/decisions.md#dec-014). The seven stories and the proposed usability-test plan await explicit verdicts.

## Action points

| Action | Owner | Due |
| --- | --- | --- |
| Verify staged event-window matching and the offline marker. [#132](https://github.com/ITPD-Almo/modular-llm-gateway/issues/132) | Ali12hamdan | Week 8, before the first counted session |
| Coordinate campus sessions and record valid outcomes, assistance and timings. [#133](https://github.com/ITPD-Almo/modular-llm-gateway/issues/133) | Mohammed-Nour | Week 8, November 21 |
| Verify private recordings access and preserve consent and dry-run notes in the private evidence locations. [#134](https://github.com/ITPD-Almo/modular-llm-gateway/issues/134) | atkond2point0 | Week 8, before the first counted session |

## Open questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| Do the three tasks, operator profile and pass bar answer the Customer's adoption questions? | Week 8 design and evidence plan. | Review the [UT-01 design](../../docs/usability-tests/ut-01/README.md). |
| What must the results show before the Customer would introduce the gateway into the operator workflow? | Priorities for the next product increment. | Ask the [prepared questions](meeting-script.md#questions) and record the decision. |
| Which carried stories meet their criteria? | Story status and sprint velocity. | Review each story's checklist in the [agenda](meeting-script.md#agenda). |
| Which timeout, access, retention and masking settings are suitable for the trial? | Runtime settings and the next plugin fixture. | Review the carried questions above. |

## Disagreements

None recorded in this evidence.
