# Week 2 customer meeting report

## Metadata

- **Date:** 2026-10-09.
- **Duration:** about 37 minutes for the joint meeting; our presentation and main questions took about 12 minutes.
- **Participants:** Customer, Ali12hamdan, and atkond2point0 from our team. Members of two other teams also joined. The full attendance list is not confirmed by the transcript.
- **Presented:** a text presentation of our research, proposed masking and policy-decision flow, and possible first-version scope. We did not demonstrate a running gateway.
- **Recording permission:** not recorded in the supplied transcript. The host announced recording; separate permission has not been confirmed.
- **Public transcript permission:** unconfirmed. We are keeping the transcript local until the host or Customer confirms whether publication is allowed.
- **Private instructor-sharing permission:** not recorded in the supplied transcript; needs confirmation.
- **Transcript:** None published. A local transcript was used to prepare this report; public publication permission is unconfirmed.
- **Meeting script:** [the original preparation in draft PR #26](https://github.com/ITPD-Almo/modular-llm-gateway/pull/26). It was prepared locally before the meeting and uploaded afterwards, with artifact and story links still pending. Ali presented and asked our questions; the planned note-taker and observer roles are not confirmed in the supplied record.

## Previous action points

None. We had no Week 1 kickoff, so there was no earlier customer meeting report to carry actions from.

## Previous open questions

None. There was no earlier customer meeting report. Our Week 1 research hypotheses are still provisional.

## Summary

- The main user is a DevOps person who needs to adapt the gateway to company rules and integrations. A CLI is acceptable; a dashboard is not the main priority.
- The Customer confirmed request and response processing and routing as the overall direction. Existing tools may be used if they fit the required workflow.
- Our proposed masking and request-record flow was missing the plugin contract, execution order, and loading approach. These need to be shown in the next design and prototype.
- A first usable workflow can use two simple plugins and a fake provider. Restarting when adding plugins is acceptable. A finished MUP was not required next week.
- The meeting did not establish policy-version tracking as our main advantage, settle the outstanding assumptions, or give a specific verdict on the original three-story candidate.

## Decisions

- [DEC-003: Focus the gateway on DevOps users composing company-specific plugins to process requests and responses and route requests.](../../docs/decisions.md#dec-003)
- [DEC-004: Allow an existing tool to be used if it meets the required workflow.](../../docs/decisions.md#dec-004)
- [DEC-005: Use starting the system, adding two simple plugins, sending a request, and seeing the result as the first usable workflow, allowing a restart and a deterministic fake provider.](../../docs/decisions.md#dec-005)
- [DEC-006: Show the plugin inputs, outputs, execution order, and loading approach in the next design and prototype.](../../docs/decisions.md#dec-006)

DEC-005 records the Customer's clarification of the useful workflow. A verdict on the revised candidate's specific story issues is still needed.

## Action points

| Action | Owner | Due |
| --- | --- | --- |
| Draft the proposed system flow and plugin interface, including inputs, outputs, ordering, and loading, per [DEC-006](../../docs/decisions.md#dec-006). | Mohammed-Nour | Week 3, 2026-10-14. |
| Prepare a small working interaction with two simple plugins and a fake provider, per [DEC-005](../../docs/decisions.md#dec-005). Keep disposable spike code off main. | atkond2point0 | Week 3, 2026-10-15. |

Ali read back the combined follow-up as a proposed flow and a minimum working interaction, and the Customer agreed. After the meeting, Ali proposed the two rows above using the existing task split. The owners and dates are planning targets, not assignments or deadlines given by the Customer; the teammates still need to confirm them.

## Open questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| Does the revised story set cover the usable plugin workflow, and what must be included first? | The MUP candidate and story priorities. | Prepare the revised stories and ask the Customer for a specific verdict. |
| What information must a plugin receive and return, and how should plugin failures be handled? | The proposed interface, ordering, and error behaviour. | Design a small contract and test it with two simple plugins; bring the unresolved choices to the next review. |
| Is policy-version tracking needed, and what request or response content may be kept? | ASM-01, the decision record, and the provisional research gaps. | Ask about a real incident and show a concrete record. The brief agreement with our flow did not answer this. |
| Can an existing gateway support the same workflow with acceptable effort? | ASM-02 and whether a new core is justified. | Check a matched extension example and report the result. |
| Are static caller credentials and one provider enough for the first trial? | ASM-03 and the product boundary. | Confirm with the Customer; the proposed limits were not explicitly accepted. |
| What synthetic company-data examples should the first masking plugin handle? | ASM-05 and the masking acceptance criteria. | Ask for made-up examples and expected results. |
| May we publish the sanitized transcript, and what private sharing is permitted? | Transcript publication and submission evidence. | Confirm the permission answers with the meeting host or Customer. |

## Disagreements

| Your position | Customer's position | What you changed |
| --- | --- | --- |
| We mainly showed an employee masking flow and a policy-version record. | The missing part was how plugins connect to the system: their inputs, outputs, order, and loading. | The [prototype record](prototypes.md) captures the feedback. The [vision](../../docs/product-vision.md#goal) and [CON-01](../../docs/product-vision.md#con-01) now call for the plugin interface and workflow, citing DEC-003 and DEC-006. Story issues still need to carry the revised scope. |
| Our preparation centred the first version on three capabilities: provider-key handling, masking, and policy-version lookup. | The first usable workflow must let the DevOps user start the system, add plugins, and see their effect on a request and result. | DEC-005 records the clarified workflow. The [vision](../../docs/product-vision.md#goal) now includes that first usable interaction, and [BND-04](../../docs/product-vision.md#bnd-04) cites the allowed restart. The linked story candidate still needs revision and a specific verdict; the original three-story candidate is not recorded as accepted. |
