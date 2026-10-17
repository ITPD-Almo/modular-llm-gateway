# Week 3 joint meeting report

## Metadata

- **Date:** 2026-10-16.
- **Status:** Prepared from the shared joint-meeting transcript.
- **Duration:** about 46 minutes for the joint meeting.
- **Source speakers:** Customer and speakers from two other teams, as identified in the shared transcript.
- **Presented:** another team showed its architecture, configuration, plugin interface, and a masking prototype. No demonstration of our stories US-01, US-02, or US-03 is recorded.
- **Recording permission:** the host announced recording; the separate permission question and answer are not in the supplied transcript.
- **Public transcript permission:** the Customer referred to a public transcript, but the scope of permission to publish our sanitized copy on GitHub has not been confirmed.
- **Private instructor-sharing permission:** no separate answer is recorded.
- **Transcript:** None published while sharing permission remains unconfirmed. The source stays local.
- **Meeting script:** no original preparation for this call was supplied. The [written validation script](meeting-script.md) was prepared on October 17 for the later follow-up; it is not a pre-meeting script for October 16.

## Previous action points

| Action | Outcome | Decision |
| --- | --- | --- |
| [Week 2 action points](../week-02/meeting-report.md#action-points): "Draft the proposed system flow and plugin interface, including inputs, outputs, ordering, and loading". | Carried out after the meeting through task [#43](https://github.com/ITPD-Almo/modular-llm-gateway/issues/43) and [PR #48](https://github.com/ITPD-Almo/modular-llm-gateway/pull/48). [docs/plugins.md](../../docs/plugins.md) documents inputs, outputs, ordering, loading and failure behaviour. The [October 17 checks](gateway-check.md#week-2-action-points) record the technical outcome separately from this call. | None from this meeting. The original direction remains [DEC-006](../../docs/decisions.md#dec-006). |
| [Week 2 action points](../week-02/meeting-report.md#action-points): "Prepare a small working interaction with two simple plugins and a fake provider". | Carried out after the meeting through [#43](https://github.com/ITPD-Almo/modular-llm-gateway/issues/43) and [PR #48](https://github.com/ITPD-Almo/modular-llm-gateway/pull/48). [docs/setup.md](../../docs/setup.md) runs two plugins and the fake provider; the [local checks](gateway-check.md#week-2-action-points) confirm the interaction. Customer demonstration and verdict were not completed for this submission. | None from this meeting. [DEC-005](../../docs/decisions.md#dec-005) remains the earlier workflow clarification. |

## Previous open questions

| Question | Answer | Decision |
| --- | --- | --- |
| [Week 2 open questions](../week-02/meeting-report.md#open-questions): "Does the revised story set cover the usable plugin workflow, and what must be included first?" | Stories [#40](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [#41](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), and [#42](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42) now exist, but no verdict on them appears in this meeting. Carry the question forward. | None. |
| [Week 2 open questions](../week-02/meeting-report.md#open-questions): "What information must a plugin receive and return, and how should plugin failures be handled?" | The Customer asked the other teams to explain their contracts, execution order, failures, and debugging information. Our contract and failure behaviour were not demonstrated in this meeting. The later implementation is described in [the separate gateway check](gateway-check.md). | None specific to our interface. |
| [Week 2 open questions](../week-02/meeting-report.md#open-questions): "Is policy-version tracking needed, and what request or response content may be kept?" | Unanswered for our team. The discussion of debugging does not settle content retention or establish our policy-version gap. | None; [ASM-01](../../docs/assumptions.md#asm-01) stays Open. |
| [Week 2 open questions](../week-02/meeting-report.md#open-questions): "Can an existing gateway support the same workflow with acceptable effort?" | No matched comparison for our team was presented. Carry the check forward. | None; [ASM-02](../../docs/assumptions.md#asm-02) stays Open. |
| [Week 2 open questions](../week-02/meeting-report.md#open-questions): "Are static caller credentials and one provider enough for the first trial?" | A fake provider was again acceptable in the joint discussion. Our proposed caller credentials and trial limits were not explicitly accepted. | None on the remaining limits; [ASM-03](../../docs/assumptions.md#asm-03) stays Open. |
| [Week 2 open questions](../week-02/meeting-report.md#open-questions): "What synthetic company-data examples should the first masking plugin handle?" | The other team's phone-number example was not a supplied requirement for our masking plugin. Our examples still need confirmation. | None; [ASM-05](../../docs/assumptions.md#asm-05) stays Open. |
| [Week 2 open questions](../week-02/meeting-report.md#open-questions): "May we publish the sanitized transcript, and what private sharing is permitted?" | The Customer mentioned a public transcript, but the three separate answers and the permitted sharing scope remain unconfirmed. Ask for the written follow-up's permissions separately. | None. |

## Summary

- The Customer wanted a runnable workflow that a DevOps operator could start, use, and extend by following the documentation. A fake provider remained acceptable.
- The discussion stressed plugin contracts and the reasons behind architectural choices. A diagram containing only a plugin-runner box was not enough to explain the design.
- The Customer asked how an operator would identify a plugin that failed or hung, including its progress through the chain.
- The Customer mentioned three plugins while addressing the other teams. We need to clarify how that affects our two-example-plugin candidate.
- Our three story issues were not demonstrated or accepted in the supplied recording. A separate review of our implementation is still needed; no Customer verdict was available for this submission.

## Decisions

None recorded for our three stories. General feedback to another team is not an accept or reject verdict on our implementation. No DEC-008 or later verdict is added without the actual Customer reply.

## Action points

| Action | Owner | Due |
| --- | --- | --- |
| Check the merged gateway from a clean checkout and send the written demo for #40, #41, and #42, one criterion at a time. Ask for each verdict and clarify the two-plugin or three-plugin scope. | Ali12hamdan | Week 4, 2026-10-20. |
| Propose and demonstrate how a failing or stuck plugin is identified, including what the caller and operator see. | atkond2point0 | Week 4, 2026-10-23. |
| Compare the same small plugin workflow with an existing gateway and record whether it changes the provisional gaps. | Mohammed-Nour, confirmed after the meeting. | Week 4, 2026-10-22. |

These are proposed team follow-ups prepared after reviewing the recording. The transcript does not assign these owners or dates; Mohammed-Nour confirmed the existing-gateway comparison and its October 22 due date in [the review comment](https://github.com/ITPD-Almo/modular-llm-gateway/pull/47#issuecomment-6235286671). The other owners and dates remain proposed. The first row carries the Customer demonstration forward. Later technical outcomes for both Week 2 actions are in [the separate gateway check](gateway-check.md#week-2-action-points).

## Open questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| Does each of #40, #41, and #42 pass its acceptance criteria, and do they complete the useful workflow? | Story acceptance and the candidate's scope. | Send the checked written demo and ask for an individual verdict. |
| Are two example plugins sufficient for this sprint, or is a third required? | The candidate, example plugins, and release scope. | Ask explicitly; the joint discussion did not settle this for our team. |
| What contract, failure result, timeout, and debugging information must a plugin support? | The interface and the next failure-handling work. | Show the actual contract and one observed failure, then ask what is missing. |
| Is policy-version tracking needed, and what request or response content may be kept? | ASM-01 and the provisional policy-record gap. | Ask about a real incident and show a concrete record. |
| Can an existing gateway support the same workflow with acceptable effort? | ASM-02 and the case for a new core. | Complete the matched extension check and report the result, including an existing tool winning. |
| Are static caller credentials and the proposed provider limits enough for the trial? | ASM-03 and the boundary. | Ask for the limits separately from the fake-provider demonstration. |
| Which synthetic company-data examples should the masking plugin handle? | ASM-05 and masking criteria. | Request made-up examples and expected outputs. |
| May we publish a sanitized transcript, and what private sharing is permitted? | Public and private submission evidence. | Confirm the sharing scope for each meeting and written exchange. |

## Disagreements

None directly recorded between our team and the Customer. The Customer challenged another team's unexplained plugin runner and asked for a runnable multi-plugin workflow. We will test our own design against those concerns, without presenting their exchange as a verdict on our stories.
