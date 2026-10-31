# SPRINT-05 retrospective

Written closeout prepared by Mohammed-Nour from the sprint's issues and pull requests, then finalized for Ali12hamdan with Codex on October 31. No separate synchronous retrospective or complete set of personal member feedback was recorded; the [weekly report](README.md#deviations) declares that limitation. The observations below concern the recorded workflow, not individual ratings.

## What Went Well

| What went well |
| --- |
| The one-command installer ([#92](https://github.com/ITPD-Almo/modular-llm-gateway/pull/92)) and its install check ([#93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93)) ran green on Linux and macOS, on both x86_64 and ARM64, before review. |
| The Week 5 ownership was recorded in three task issues ([#98](https://github.com/ITPD-Almo/modular-llm-gateway/issues/98), [#99](https://github.com/ITPD-Almo/modular-llm-gateway/issues/99), [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100)); when the CI task stalled on the due date, its owner and state were visible, so another member could take it over the same evening ([#103](https://github.com/ITPD-Almo/modular-llm-gateway/pull/103)). |
| The [deployment runbook and 0.5.0 package version](https://github.com/ITPD-Almo/modular-llm-gateway/pull/102) were independently reviewed and merged before deployment, while the operational task stayed open for its actual evidence. |

## What Did Not

| Problem | Root cause |
| --- | --- |
| SPRINT-05 was planned, and its task issues opened, only on its due date, 2026-10-31. | After the Week 4 close, product work on the installer and provider setup started before anyone held sprint planning, and the issue-backed planning baseline was recorded only on October 31. |
| The Week 5 Customer meeting, the SPRINT-05 Sprint Review, was postponed to Week 6, so no story was shown against its criteria and Actual Velocity is 0 for the second sprint running. | The meeting time was left to be agreed during the sprint's last days instead of being fixed at sprint planning, and it was not agreed in time. |
| The CI and test pull request ([#103](https://github.com/ITPD-Almo/modular-llm-gateway/pull/103)) was opened only on the due date, from a Week 3 branch, with unrelated files, and it required rework, so Mohammed-Nour took the task over. | No mid-sprint checkpoint for this task was recorded in its issue; with planning on the last day, the task had less than one day before the deploy and the tag depended on it. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Hold sprint planning on the sprint's first day: set Planned Velocity, open the task issues and fix the Customer meeting time before any work starts. | Ali12hamdan | High | SPRINT-05 was again planned only on its last day, and its review was postponed for lack of an agreed time. | Yes |
| Each member posts the state of their task on its issue at mid-sprint, and a task with no pull request two days before the due date is reassigned. | Ali12hamdan | High | The CI task #98 had no pull request until the due date, and the deploy and the tag waited on it until it was taken over. | Yes |
| Rehearse the released demo on the presentation machine the day before the Week 6 Customer review. | Mohammed-Nour | High | The SPRINT-04 action could not be done because the Week 5 review was postponed, and the October 23 setup failure is still the last demo the Customer saw. | Yes |
| Show US-01 to US-04 and US-09 AC by AC at the Week 6 review and record each verdict as a `DEC-nnn`. | Ali12hamdan | High | No story has had a Customer verdict in SPRINT-04 or SPRINT-05, so Actual Velocity has stayed 0. | Yes |

## Carried Actions

| Action | Outcome |
| --- | --- |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Rehearse the released demo from `docs/setup.md` on the presentation machine the day before each Customer review." | Not done: the Week 5 review was postponed to Week 6, so there was no review to rehearse for; re-listed in [Actions](#actions). |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Ask the Customer in writing for an AC-by-AC verdict on US-01 to US-04 and record the reply." | Not done: the Week 5 review was postponed to Week 6, so no verdict was asked for; re-listed in [Actions](#actions). |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Hold sprint planning on the sprint's first day: set Planned Velocity and open the task issues before any work starts." | Not done: SPRINT-05 was planned on 2026-10-31, its last day; re-listed in [Actions](#actions). |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Branch each task from main with one pull request, avoid stacked and integration pull requests, and record the rule in `CONTRIBUTING.md` through a SPRINT-05 task issue." | Done in this closeout: the matching rule is in [CONTRIBUTING.md](../../CONTRIBUTING.md#how-a-change-gets-in) and [AGENTS.md](../../AGENTS.md#conventions) through [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100); the late #98 pull request #103 still started from an old branch, which the merge of `main` fixed. |
