# Week 6 customer review report

## Metadata

- **Date:** 2026-11-07, starting about 09:06 Europe/Moscow.
- **Duration:** about 45 minutes, online.
- **Attended:** Ali12hamdan and Customer, the two speakers in the source. Whether other members joined without speaking is not established by the source.
- **Ceremony:** the SPRINT-06 Sprint Review, which also stood in for the SPRINT-05 review postponed from Week 5.
- **Presented:** by Ali12hamdan: the one-line terminal install, the guided DeepSeek key setup and a real-provider request, the plugin configuration file and the hook execution code.
- **Not presented:** the analytics and observability dashboards, the observability test, an AC-by-AC walk through any story, the carried open questions and a threshold proposal. The telemetry did not exist yet: its first pull request, [#109](https://github.com/ITPD-Almo/modular-llm-gateway/pull/109), was opened on 2026-11-08.
- **Preparation:** no script was written before the meeting, which is a deviation from the preparation rule.
- **Roles:** Ali12hamdan moderated and presented. No note taker or observer role is established by the source.
- **Recording permission:** the Customer recorded the meeting and sent the recording and the transcript afterwards; the permission questions were not asked on the recording.
- **Transcript publication:** permitted, as confirmed to the team on 2026-11-08; the [de-identified transcript](meeting-transcript.md) uses coarse minute markers.
- **Private instructor sharing:** permitted, as confirmed to the team on 2026-11-08; the recording link is in the Moodle submission only.
- **Meeting script:** [meeting-script.md](meeting-script.md), a reconstructed agenda and a follow-up agenda written after the meeting.
- **Carried items:** the Week 5 review was postponed, so Week 5 has no meeting report; its report [carried the Week 4 action points and open questions](../week-05/README.md#deviations) to this meeting.
- **Story verdicts:** none. The Customer gave feedback and agreed with the terminal workflow, which accepts no story's criteria.

## Previous action points

| Action | Outcome | Decision |
| --- | --- | --- |
| [Week 4 action points](../week-04/meeting-report.md#action-points): "Rehearse the final reviewed/released demo together on the presentation machine, including the A/B extension, both timeout stages, capacity limit and reset procedure." | Not done: no rehearsal was held. During the call the presenter spent about eight minutes locating the demo and an expired key, and the A/B extension and timeouts were not shown. Carried as the Week 7 script rehearsal below. | None. |
| [Week 4 action points](../week-04/meeting-report.md#action-points): "Show each current story AC-by-AC, ask for its individual verdict and record any failed criteria and actual reply; carry the unfinished demonstration/diagnostic actions forward." | Not done: no story was walked through criterion by criterion and no verdict was asked for, so SPRINT-06 has no accepted story. Carried in the follow-up agenda. | None. |
| [Week 4 action points](../week-04/meeting-report.md#action-points): "Present the matched existing-gateway evidence and record what it changes about the product choice." | Not done: the [LiteLLM comparison](../week-04/prototypes.md) was not presented. The Customer asked the same question unprompted, why an operator would use this gateway instead of writing their own functions, and Ali12hamdan answered that for now there is no benefit in switching. Carried as a Week 7 action. | None. |
| [Week 4 action points](../week-04/meeting-report.md#action-points): "Ask the unresolved retention/policy-version, caller-credential/provider-boundary and synthetic masking-example questions, and confirm the next review time." | Partly done: the questions were not asked. The next review time was settled: the Customer keeps the review on Saturdays and takes questions asynchronously. | [DEC-014](../../docs/decisions.md#dec-014). |

## Previous open questions

| Question | Answer | Decision |
| --- | --- | --- |
| [Week 4 open questions](../week-04/meeting-report.md#open-questions): "Does each of US-01, US-02, US-03 and US-04 pass its own criteria and complete the useful workflow?" | Unanswered: no criterion was shown or judged. The Customer's view of the shown workflow was that a request to an LLM does not yet address a DevOps operator's pain points. Carried forward. | None. |
| [Week 4 open questions](../week-04/meeting-report.md#open-questions): "Are the proposed 250 ms hook deadline, HTTP 504 fail-request result, request-local instances and default capacity/rejection behavior acceptable for the next trial?" | Unanswered: not asked. The Customer said the gateway should report when a plugin fails and how it performs, and named malformed or oversized plugin files as checks the gateway should do, but chose no numbers or failure policy. Carried forward. | None. |
| [Week 4 open questions](../week-04/meeting-report.md#open-questions): "Is policy-version tracking needed, and what content may be retained?" | Unanswered: not asked. [ASM-01](../../docs/assumptions.md#asm-01) stays Open. Carried forward. | None. |
| [Week 4 open questions](../week-04/meeting-report.md#open-questions): "Should the next increment extend this core or an existing gateway, given the matched comparison?" | Not settled. The Customer did not choose, but asked the team to show and defend why its design beats a list of functions called in order, which bears on [ASM-02](../../docs/assumptions.md#asm-02). Carried forward with the comparison. | None. |
| [Week 4 open questions](../week-04/meeting-report.md#open-questions): "Are static credentials and the provider limits sufficient for the trial?" | Unanswered: not asked. The Customer saw the DeepSeek key stored in a permission-protected, unencrypted local file and did not object, which is not an answer on caller credentials or provider limits. [ASM-03](../../docs/assumptions.md#asm-03) stays Open. Carried forward. | None. |
| [Week 4 open questions](../week-04/meeting-report.md#open-questions): "Which made-up company-data cases and expected outputs should masking support?" | Unanswered: not asked. [ASM-05](../../docs/assumptions.md#asm-05) stays Open. Carried forward. | None. |

## Summary

- The Customer wants a demonstration that impresses a DevOps operator: how plugins are loaded and run, what happens with a badly written plugin, and how the gateway is deployed, not a request to an LLM.
- Deployment should be a Docker container brought up with Docker Compose, with versions as container versions.
- The Customer's picture of the product is a repository of plugins written against one interface, loaded by name, with the gateway reporting whether each one failed, how it performs and whether it is used.
- The team has to show and defend why its plugin system is better than a growing list of functions called from a main function.
- The terminal is an acceptable interface; reviews stay on Saturdays, with questions asynchronously between them.

## Decisions

- [DEC-012: Deliver and demonstrate the gateway as a Docker container brought up with Docker Compose, so that a released version is selected as a container version rather than through local paths and environment settings.](../../docs/decisions.md#dec-012)
- [DEC-013: Keep the terminal as the operator interface for the gateway and its plugins for now.](../../docs/decisions.md#dec-013)
- [DEC-014: Hold the customer review on Saturdays at the agreed time, without moving it, and use the asynchronous channel for questions and recorded demos between reviews.](../../docs/decisions.md#dec-014)

No decision changes a threshold goal: no threshold proposal was presented. None accepts or rejects a story.

## Action points

| Action | Owner | Due |
| --- | --- | --- |
| Package the gateway as a versioned Docker image with a Docker Compose file and bring it up at the review, per DEC-012. | Ali12hamdan | Week 7, 2026-11-13. |
| Write and rehearse the 2026-11-14 review script on the presentation machine: the four dashboards, QR-08 QRT-01, each story AC by AC and the threshold proposal. | Mohammed-Nour | Week 7, 2026-11-13. |
| Send the carried open questions to the Customer in the asynchronous channel and record the replies. | Ali12hamdan | Week 7, 2026-11-11. |
| Show each story AC by AC at the review, ask for its verdict and record each reply as a `DEC-nnn`. | Ali12hamdan | Week 7, 2026-11-14. |
| Present the LiteLLM comparison with the answer to "why this gateway rather than a list of functions or an existing gateway", and record what it changes. | Mohammed-Nour | Week 7, 2026-11-14. |

## Open questions

| Question | What it would change | Follow-up |
| --- | --- | --- |
| Does each of US-01 to US-04, US-09, US-11 and US-12 pass its criteria? | Story acceptance and SPRINT-07 velocity. | Ali12hamdan, at the 2026-11-14 review. |
| Are the 250 ms hook deadline, the 504 result and the capacity behaviour acceptable? | QR runtime targets and ADR-004. | Ali12hamdan, asynchronously by 2026-11-11. |
| Is policy-version tracking needed, and what content may be retained? | ASM-01 and the telemetry's no-content boundary. | Ali12hamdan, asynchronously by 2026-11-11. |
| Are static caller credentials and the provider limits enough for the trial? | ASM-03 and scope. | Ali12hamdan, asynchronously by 2026-11-11. |
| Which made-up company-data cases should masking support? | ASM-05 and plugin criteria. | Ali12hamdan, asynchronously by 2026-11-11. |
| What would make the Customer choose this gateway over writing functions or extending LiteLLM? | ASM-02 and the next increment's direction. | Mohammed-Nour, at the 2026-11-14 review. |

## Disagreements

| Your position | Customer's position | What you changed |
| --- | --- | --- |
| A live request to a real model through the installed gateway showed the progress since Week 4. | A request to an LLM does not impress a DevOps operator; show how plugins are loaded and run, what happens with a bad plugin, and the deployment. | The [follow-up agenda](meeting-script.md#agenda) leads with a Compose deployment, a failing plugin and the dashboards, and US-05, US-07 and US-13 were refined around them. |
| For now there is no benefit in switching to the gateway; it becomes useful once it is plug and play. | The solution has to be better than a growing list of functions called from a main function, and the team has to say why. | Nothing changed yet: the answer and the LiteLLM comparison are a Week 7 action point. |
