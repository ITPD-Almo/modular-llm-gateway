# SPRINT-07 retrospective

Written closeout from the sprint's issues, pull requests and rehearsal records.

## What Went Well

| What went well |
| --- |
| [#129](https://github.com/ITPD-Almo/modular-llm-gateway/pull/129) delivered a pinned Compose image and a staging scope that keeps test chats out of operational usage metrics. |
| The [VM implementation rehearsal](https://github.com/ITPD-Almo/modular-llm-gateway/pull/129#issuecomment-6854627777) showed that the team could match chat attempts and the offline marker to a private session window. |
| The [local operator demo](compose-demo-evidence.md) showed a new plugin, its effect and a named failure followed by recovery on the same gateway. |
| [#140](https://github.com/ITPD-Almo/modular-llm-gateway/pull/140) turned the operator workflow into three reproducible tasks with timed end states and a common help rule. |

## What Did Not

| Problem | Root cause |
| --- | --- |
| Sprint planning took place on November 12, after the sprint had started. | Story estimates, owners and the usability design assignments were reconciled after work began. |
| The teammate dry run and instructor access were reported only on the sprint's last day, at the [#140 review](https://github.com/ITPD-Almo/modular-llm-gateway/pull/140#pullrequestreview-5907097681), and the private handoff still records instructor access as pending. | The test workstation needs scoped ingestion access, and the evidence store needs a verified recordings location and reviewer accounts. |
| Story verdicts remain open. | The evidence records implementation and rehearsal outcomes. The acceptance criteria still need the Customer's explicit verdicts. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Hold sprint planning on the sprint's first day: set Planned Velocity, open the task issues with owners, and fix the Customer meeting time before any work starts. | Ali12hamdan | High | Give each item an owner before implementation or review starts. | Yes |
| Each member posts the state of their task on its issue at mid-sprint, and a task with no pull request two days before the due date is reassigned. | Ali12hamdan | High | Leave time to resolve blockers that need another person or account. | Yes |
| Write the review script two days before the review and rehearse it on the presentation machine the day before, leading with the operator's pain points. | Mohammed-Nour | High | The product rehearsal covers the local workflow. Time the full story and evidence walkthrough. | Yes |
| Show every story in the sprint AC by AC at the review and record each verdict as a `DEC-nnn`. | Ali12hamdan | High | Keep the acceptance status tied to an explicit verdict. | Yes |

## Carried Actions

| Action | Outcome |
| --- | --- |
| [reports/week-06/sprint-retrospective.md#actions](../week-06/sprint-retrospective.md#actions) “Hold sprint planning on the sprint's first day: set Planned Velocity, open the task issues with owners, and fix the Customer meeting time before any work starts.” | Not done. Sprint planning is recorded on November 12. Carry it into the next sprint. |
| [reports/week-06/sprint-retrospective.md#actions](../week-06/sprint-retrospective.md#actions) “Each member posts the state of their task on its issue at mid-sprint, and a task with no pull request two days before the due date is reassigned.” | Not done. The issue history does not establish a complete mid-sprint check. Carry it forward. |
| [reports/week-06/sprint-retrospective.md#actions](../week-06/sprint-retrospective.md#actions) “Write the review script two days before the review and rehearse it on the presentation machine the day before, leading with the operator's pain points.” | Not done. The [script](meeting-script.md) and the [local rehearsal](compose-demo-evidence.md) are available. The full agenda timing remains to be verified. |
| [reports/week-06/sprint-retrospective.md#actions](../week-06/sprint-retrospective.md#actions) “Show every story in the sprint AC by AC at the review and record each verdict as a `DEC-nnn`.” | Not done. The [agenda](meeting-script.md#agenda) lists every carried story, and the verdicts remain pending. |
