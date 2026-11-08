# SPRINT-06 retrospective

Written closeout prepared by Mohammed-Nour on 2026-11-08 from the sprint's issues, pull requests and the 2026-11-07 review transcript. No separate synchronous retrospective or complete set of personal member feedback was recorded; the [weekly report](README.md#deviations) declares that limitation. The observations below concern the recorded workflow, not individual ratings.

## What Went Well

| What went well |
| --- |
| The Customer review was held on 2026-11-07, after the Week 4 review failed at setup and the Week 5 review was postponed. It was recorded, the transcript arrived the same day, and it settled three decisions, [DEC-012](../../docs/decisions.md#dec-012) to [DEC-014](../../docs/decisions.md#dec-014), plus a concrete picture of what the Customer expects from the product. |
| The one-command install and the guided DeepSeek setup from SPRINT-05 ran live on the presenter's machine against a real model, and the Customer called the real-provider connection a good addition. |
| The observability pipeline ([#108](https://github.com/ITPD-Almo/modular-llm-gateway/issues/108), [#109](https://github.com/ITPD-Almo/modular-llm-gateway/pull/109)) was rehearsed against a local OpenObserve before any deployment: its QR-08 checker passed twice there, with the timeout log queryable in under one second. |
| The backlog refinement checked every unscheduled story against the two new ones, and folded the Customer's 2026-11-07 feedback into US-05, US-07 and the new US-13 instead of opening duplicates. |

## What Did Not

| Problem | Root cause |
| --- | --- |
| The sprint's increment, the analytics and observability telemetry, only started on 2026-11-08, the sprint's due date, so the review could not show it and the deployed work had less than one day. | No sprint planning was held when Week 6 began: no task issue or owner existed for the telemetry until 2026-11-08, so the mid-sprint check had nothing to check and nobody was due to be reassigned. |
| The review showed an install and a request to a real model rather than the stories' criteria and the operator's pain points; no verdict was asked for, so Actual Velocity is 0 for the third sprint running. | No script was written and no rehearsal was held before the meeting, so the agenda was improvised on the call and the AC-by-AC walk, the carried questions and the comparison were left out. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Hold sprint planning on the sprint's first day: set Planned Velocity, open the task issues with owners, and fix the Customer meeting time before any work starts. | Ali12hamdan | High | SPRINT-06 was planned on 2026-11-08, its last day, for the third sprint running. | Yes |
| Each member posts the state of their task on its issue at mid-sprint, and a task with no pull request two days before the due date is reassigned. | Ali12hamdan | High | The telemetry had no issue or pull request until the due date. | Yes |
| Write the review script two days before the review and rehearse it on the presentation machine the day before, leading with the operator's pain points. | Mohammed-Nour | High | The 2026-11-07 review had no script or rehearsal, and the Customer asked for a demo aimed at a DevOps operator. | Yes |
| Show every story in the sprint AC by AC at the review and record each verdict as a `DEC-nnn`. | Ali12hamdan | High | No story has received a verdict in SPRINT-04, SPRINT-05 or SPRINT-06. | Yes |

## Carried Actions

| Action | Outcome |
| --- | --- |
| [reports/week-05/sprint-retrospective.md#actions](../week-05/sprint-retrospective.md#actions): "Hold sprint planning on the sprint's first day: set Planned Velocity, open the task issues and fix the Customer meeting time before any work starts." | Not done: the meeting time was fixed and the review held on 2026-11-07, but SPRINT-06 was planned and its task issues opened on 2026-11-08, its last day; re-listed in [Actions](#actions). |
| [reports/week-05/sprint-retrospective.md#actions](../week-05/sprint-retrospective.md#actions): "Each member posts the state of their task on its issue at mid-sprint, and a task with no pull request two days before the due date is reassigned." | Not done: no SPRINT-06 task issue existed at mid-sprint, so there was nothing to post on or reassign; re-listed in [Actions](#actions). |
| [reports/week-05/sprint-retrospective.md#actions](../week-05/sprint-retrospective.md#actions): "Rehearse the released demo on the presentation machine the day before the Week 6 Customer review." | Not done: no rehearsal was held before the 2026-11-07 review, and the presenter spent part of the call locating the demo; re-listed in [Actions](#actions) together with writing the script. |
| [reports/week-05/sprint-retrospective.md#actions](../week-05/sprint-retrospective.md#actions): "Show US-01 to US-04 and US-09 AC by AC at the Week 6 review and record each verdict as a `DEC-nnn`." | Not done: the review walked through no story's criteria and asked for no verdict; re-listed in [Actions](#actions). |
