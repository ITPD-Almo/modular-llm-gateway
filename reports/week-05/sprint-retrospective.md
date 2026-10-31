# SPRINT-05 retrospective

Draft prepared by Mohammed-Nour on 2026-10-31 from the sprint's issues and pull requests.
The final retrospective and members' personal input remain to be recorded; this draft does not establish that those contributions or a completed ceremony already exist.
Ali12hamdan reviews this file as the Accountable member.

## What Went Well

| What went well |
| --- |
| The one-command installer ([#92](https://github.com/ITPD-Almo/modular-llm-gateway/pull/92)) and its install check ([#93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93)) ran green on Linux and macOS, on both x86_64 and ARM64, before review. |
| The Week 5 ownership was recorded in three task issues ([#98](https://github.com/ITPD-Almo/modular-llm-gateway/issues/98), [#99](https://github.com/ITPD-Almo/modular-llm-gateway/issues/99), [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100)); the unpublished CI task remains pending rather than being counted as a completed pull request. |
| The [deployment runbook and 0.5.0 package version](https://github.com/ITPD-Almo/modular-llm-gateway/pull/102) were independently reviewed and merged before deployment, while the operational task stayed open for its actual evidence. |

## What Did Not

| Problem | Root cause |
| --- | --- |
| SPRINT-05 was planned, and its task issues opened, only on its due date, 2026-10-31. | After the Week 4 close, product work on the installer and provider setup started before anyone held sprint planning, and no planning slot was fixed in the calendar. |
| The Week 5 Customer meeting, the SPRINT-05 Sprint Review, was postponed to Week 6, so no story was shown against its criteria and Actual Velocity is 0 for the second sprint running. | The meeting time was left to be agreed during the sprint's last days instead of being fixed at sprint planning, and it was not agreed in time. |
| The installer and provider-setup pull requests ([#93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93), [#95](https://github.com/ITPD-Almo/modular-llm-gateway/pull/95)) were stacked on each other again and had to be retargeted before merging. | They were opened on October 25–30, before the one-branch rule was written into `CONTRIBUTING.md`, so the old dependency-stack rule still applied. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Hold sprint planning on the sprint's first day: set Planned Velocity, open the task issues and fix the Customer meeting time before any work starts. | Ali12hamdan | High | SPRINT-05 was again planned only on its last day, and its review was postponed for lack of an agreed time. | Yes |
| Merge the CI and test pull request at least one day before the deploy, so the release candidate is fixed before the Customer meeting. | atkond2point0 | Medium | The CI dependency remained unpublished on the due date while deployment and tagging waited, and the Customer review had already been postponed. | Yes |
| Rehearse the released demo on the presentation machine the day before the Week 6 Customer review. | Mohammed-Nour | High | The SPRINT-04 action could not be done because the Week 5 review was postponed, and the October 23 setup failure is still the last demo the Customer saw. | Yes |
| Show US-01 to US-04 and US-09 AC by AC at the Week 6 review and record each verdict as a `DEC-nnn`. | Ali12hamdan | High | No story has had a Customer verdict in SPRINT-04 or SPRINT-05, so Actual Velocity has stayed 0. | Yes |

## Carried Actions

| Action | Outcome |
| --- | --- |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Rehearse the released demo from `docs/setup.md` on the presentation machine the day before each Customer review." | Not done: the Week 5 review was postponed to Week 6, so there was no review to rehearse for; re-listed in [Actions](#actions). |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Ask the Customer in writing for an AC-by-AC verdict on US-01 to US-04 and record the reply." | Not done: the Week 5 review was postponed to Week 6, so no verdict was asked for; re-listed in [Actions](#actions). |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Hold sprint planning on the sprint's first day: set Planned Velocity and open the task issues before any work starts." | Not done: SPRINT-05 was planned on 2026-10-31, its last day; re-listed in [Actions](#actions). |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Branch each task from main with one pull request, avoid stacked and integration pull requests, and record the rule in `CONTRIBUTING.md` through a SPRINT-05 task issue." | Done in this draft's implementation: the matching rule is in [CONTRIBUTING.md](../../CONTRIBUTING.md#how-a-change-gets-in) and [AGENTS.md](../../AGENTS.md#conventions) through [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100); this does not assert that the still-unpublished #98 pull request already exists. |
