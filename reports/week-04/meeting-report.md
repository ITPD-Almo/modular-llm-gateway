# Week 4 customer review report

## Metadata

- **Date:** 2026-10-23.
- **Duration:** about 27 minutes.
- **Attended:** Mohammed-Nour, Ali12hamdan, atkond2point0 and Customer, identified from the source speakers; no claim is made about role assignments before the call.
- **Presented:** an attempted local gateway installation, the intended two-plugin curl workflow, configuration and plugin code; setup and screen-sharing problems limited the demonstration.
- **Recording permission:** the source contains a recording but no separate permission question and answer; the team owner confirmed on October 25 that the recording/transcript may be shared.
- **Transcript publication:** permitted according to the owner's October 25 confirmation; the [sanitized transcript](meeting-transcript.md) uses coarse minute markers rather than exact recording timecodes.
- **Private instructor sharing:** permitted according to the same later owner confirmation; recording links and exact timecodes remain private.
- **Original meeting script:** [meeting-script.md](meeting-script.md) is preserved unchanged from [f2b39e9](https://github.com/ITPD-Almo/modular-llm-gateway/commit/f2b39e9151c0f86d940ebfbd80f494201a5cdd6f) and [e1f0924](https://github.com/ITPD-Almo/modular-llm-gateway/commit/e1f0924be9dc8f96d6f1b4cf40b7ea377a41925b). Their author and commit metadata is dated October 22; Mohammed-Nour transferred the original history on October 25. The content and metadata have been inspected, but actual use during the call is not established.
- **Planned roles:** the original script assigns Ali12hamdan as moderator, Mohammed-Nour as note taker and atkond2point0 as observer/demo driver. Execution of those roles is not established by the source.
- **Preparation deviation:** the original agenda totals 42 minutes rather than the required 30-minute plan; it is retained as prepared. The later follow-up uses a 30-minute agenda.
- **Follow-up preparation:** [the October 25 follow-up script](meeting-script-2.md) prepares a future review; it does not replace or backdate the October 23 preparation.
- **Story verdicts:** none established in the source; the owner confirmed on October 25 that no later acceptance or rejection has been received.

## Previous action points

| Action | Outcome | Decision |
| --- | --- | --- |
| [Week 3 action points](../week-03/meeting-report.md#action-points): "Check the merged gateway from a clean checkout and send the written demo for #40, #41, and #42, one criterion at a time. Ask for each verdict and clarify the two-plugin or three-plugin scope." | Partly carried out. The October 23 setup attempt did not establish a successful criterion-by-criterion demonstration or verdict. Later clean-clone checks and a second-member replay are recorded in [PR #76](https://github.com/ITPD-Almo/modular-llm-gateway/pull/76), still under review; they are later technical evidence. The Customer clarified that plugin-management value matters more than a fixed example count. Story verdicts carry forward. | [DEC-008](../../docs/decisions.md#dec-008); no acceptance decision. |
| [Week 3 action points](../week-03/meeting-report.md#action-points): "Propose and demonstrate how a failing or stuck plugin is identified, including what the caller and operator see." | Not demonstrated during the call. The Customer confirmed the resilience/diagnostic need. After the capacity replan, Ali12hamdan implemented [diagnostics #71](https://github.com/ITPD-Almo/modular-llm-gateway/pull/71) and [bounded execution #72](https://github.com/ITPD-Almo/modular-llm-gateway/pull/72); Mohammed-Nour approved both on October 25 after reproducing the failure/privacy/recovery behavior. Diagnostics merged into main; bounded execution merged into its dependency branch and still needs main integration. These are later technical results, without a Customer verdict or a new release; demonstration carries forward. | [DEC-010](../../docs/decisions.md#dec-010). |
| [Week 3 action points](../week-03/meeting-report.md#action-points): "Compare the same small plugin workflow with an existing gateway and record whether it changes the provisional gaps." | Carried out as technical research by Mohammed-Nour and reviewed on October 25 in [PR #75](https://github.com/ITPD-Almo/modular-llm-gateway/pull/75). The [matched comparison](prototypes.md) records that LiteLLM served the narrow workflow with comparable effort, limits the hang claims to tested configurations, and updates the maintained assumptions/research. It was not presented on October 23; Customer reaction carries forward. | None; the work did not establish a Customer selection or change an assumption status. |

## Previous open questions

| Question | Answer | Decision |
| --- | --- | --- |
| [Week 3 open questions](../week-03/meeting-report.md#open-questions): "Does each of #40, #41, and #42 pass its acceptance criteria, and do they complete the useful workflow?" | Unanswered as a Customer verdict; no AC-by-AC acceptance or rejection was recorded, including in the owner's later update. | None. |
| [Week 3 open questions](../week-03/meeting-report.md#open-questions): "Are two example plugins sufficient for this sprint, or is a third required?" | The Customer emphasized the system for adding/managing plugins rather than a fixed count. The requested A-input/B-output example explains the process; it is not a mandate for an arbitrary larger plugin catalogue. | [DEC-008](../../docs/decisions.md#dec-008), [DEC-009](../../docs/decisions.md#dec-009). |
| [Week 3 open questions](../week-03/meeting-report.md#open-questions): "What contract, failure result, timeout, and debugging information must a plugin support?" | The Customer wants understandable request/response extension and identifiable handling of bad or sleeping plugins while the system stays usable. Numerical budgets, status codes, fail-versus-skip semantics, capacity and execution boundaries remain team proposals for validation. | [DEC-009](../../docs/decisions.md#dec-009), [DEC-010](../../docs/decisions.md#dec-010). |
| [Week 3 open questions](../week-03/meeting-report.md#open-questions): "Is policy-version tracking needed, and what request or response content may be kept?" | Unanswered. A request to log a failure is not permission to retain raw bodies or confirmation of the policy-version gap; [ASM-01](../../docs/assumptions.md#asm-01) remains Open. | None. |
| [Week 3 open questions](../week-03/meeting-report.md#open-questions): "Can an existing gateway support the same workflow with acceptable effort?" | The later [matched comparison](prototypes.md) shows that LiteLLM served the small two-plugin workflow. The Customer has not reacted; [ASM-02](../../docs/assumptions.md#asm-02) remains Open and this does not settle the Azure or policy-job comparisons. | None. |
| [Week 3 open questions](../week-03/meeting-report.md#open-questions): "Are static caller credentials and the proposed provider limits enough for the trial?" | Unanswered. Discussing a fake-provider example does not accept the proposed identity or production-provider boundary; [ASM-03](../../docs/assumptions.md#asm-03) remains Open. | None. |
| [Week 3 open questions](../week-03/meeting-report.md#open-questions): "Which synthetic company-data examples should the masking plugin handle?" | Unanswered. The A/B replacement exercise demonstrates extension mechanics, not an approved masking corpus or accuracy target; [ASM-05](../../docs/assumptions.md#asm-05) remains Open. | None. |
| [Week 3 open questions](../week-03/meeting-report.md#open-questions): "May we publish a sanitized transcript, and what private sharing is permitted?" | The October 23 source does not capture separate answers. The owner later confirmed sharing for this recording/transcript on October 25. That confirmation does not retrospectively supply answers for earlier meetings; future meetings ask separately. | None: later sharing confirmation is evidence handling, not a product verdict. |

## Summary

- The attempted setup did not establish a complete working demonstration; the plugin-addition process needed a clearer runnable example and developer documentation.
- The Customer confirmed developers/DevOps as the users and plugin management plus handover as the value, rather than a fixed number of example plugins.
- Bad or sleeping plugins should have identifiable outcomes while the gateway stays usable; the precise deadline, failure policy and capacity remain proposed targets.
- The Customer asked for visible progress against a multiweek plan and welcomed asynchronous clarification; no story verdict or complete A4 quality/architecture approval was recorded.

## Decisions

- [DEC-008: Prioritize a documented plugin-management system for developers and DevOps operators that another operator can support, rather than a fixed catalogue of example plugins.](../../docs/decisions.md#dec-008)
- [DEC-009: Use a simple plugin that replaces incoming content with A text and the provider reply with B text to explain how a new plugin enters the gateway.](../../docs/decisions.md#dec-009)
- [DEC-010: Handle badly written or sleeping plugins without leaving the gateway unusable, identifying the problematic plugin and providing diagnostic information.](../../docs/decisions.md#dec-010)
- [DEC-011: Show progress against a plan beyond one iteration and use asynchronous questions when clarification is needed.](../../docs/decisions.md#dec-011)

None of these decisions accepts a story or endorses the team's specific timeout, status, worker count or fail-request design.

## Action points

| Action | Owner | Due |
| --- | --- | --- |
| Rehearse the final reviewed/released demo together on the presentation machine, including the A/B extension, both timeout stages, capacity limit and reset procedure. | Mohammed-Nour | Week 5, 2026-10-26. |
| Show each current story AC-by-AC, ask for its individual verdict and record any failed criteria and actual reply; carry the unfinished demonstration/diagnostic actions forward. | Ali12hamdan | Week 5, 2026-10-27. |
| Present the matched existing-gateway evidence and record what it changes about the product choice. | Mohammed-Nour | Week 5, 2026-10-29. |
| Ask the unresolved retention/policy-version, caller-credential/provider-boundary and synthetic masking-example questions, and confirm the next review time. | Ali12hamdan | Week 5, 2026-10-28. |

These are current team follow-ups prepared on October 25, not owners or deadlines assigned by the Customer during the call.
The Customer's flexibility about presentations does not waive the course's ceremony, preparation or evidence requirements.

## Open questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| Does each of US-01, US-02, US-03 and US-04 pass its own criteria and complete the useful workflow? | Story acceptance, specific rework and actual velocity. | Ali12hamdan, Week 5 by October 27, show the criteria and record each actual verdict. |
| Are the proposed 250 ms hook deadline, HTTP 504 fail-request result, request-local instances and default capacity/rejection behavior acceptable for the next trial? | Runtime policy, capacity requirements and architectural decisions. | Ali12hamdan, Week 5 by October 27, demonstrate the concrete normal/error/overload results. |
| Is policy-version tracking needed, and what content may be retained? | ASM-01 and the data/retention boundary. | Ali12hamdan, Week 5 by October 28, ask about a real operational example without requesting real private data. |
| Should the next increment extend this core or an existing gateway, given the matched comparison? | ASM-02 and the product's next implementation direction. | Mohammed-Nour, Week 5 by October 29, show the observed comparison and its untested parts. |
| Are static credentials and the provider limits sufficient for the trial? | ASM-03 and scope. | Ali12hamdan, Week 5 by October 28, confirm those limits separately. |
| Which made-up company-data cases and expected outputs should masking support? | ASM-05 and concrete plugin criteria. | Ali12hamdan, Week 5 by October 28, request synthetic examples. |

## Disagreements

| Your position | Customer's position | What you changed |
| --- | --- | --- |
| Reported passing tests and explained configuration while the local setup was failing. | Show the working product and the concrete steps that add a new plugin. | Prepared the reproducible setup, A/B example and second-member replay in #57/PR #76; no Customer verdict is inferred from those later checks. |
| Team workflow and a chain of plugin functions explained the value. | Another developer/DevOps operator must understand, extend and support the system. | Requirements and the architecture record the operability, contract and handover targets; runtime drafts add named failure/recovery behavior. |
| The next scope question was how many plugins to add. | Basic examples are enough to explain a system which manages plugins. | Kept examples as demonstrations and prioritized management, diagnostics and resilience instead of an arbitrary plugin count. |
