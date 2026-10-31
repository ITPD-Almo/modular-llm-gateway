# SPRINT-05 retrospective

Written by Mohammed-Nour at the sprint close on 2026-10-31 from the sprint's issues, pull requests and meeting record, with input from Ali12hamdan and atkond2point0 on [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100).
Ali12hamdan reviews this file as the Accountable member.

## What Went Well

| What went well |
| --- |
| The one-command installer ([#92](https://github.com/ITPD-Almo/modular-llm-gateway/pull/92)) and its install check ([#93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93)) ran green on Linux and macOS, on both x86_64 and ARM64, before review. |
| The Week 5 work was split into one task and one pull request per member ([#98](https://github.com/ITPD-Almo/modular-llm-gateway/issues/98), [#99](https://github.com/ITPD-Almo/modular-llm-gateway/issues/99), [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100)), each branched from main, with no integration pull request. |
| TODO (after the deploy and the meeting): one row on the staging and production deploy, or on the Sprint Review result. |

## What Did Not

| Problem | Root cause |
| --- | --- |
| SPRINT-05 was planned, and its task issues opened, only on its due date, 2026-10-31. | After the Week 4 close, product work on the installer and provider setup started before anyone held sprint planning, and no planning slot was fixed in the calendar. |
| The installer and provider-setup pull requests ([#93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93), [#95](https://github.com/ITPD-Almo/modular-llm-gateway/pull/95)) were stacked on each other again and had to be retargeted before merging. | They were opened on October 25–30, before the one-branch rule was written into `CONTRIBUTING.md`, so the old dependency-stack rule still applied. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Hold sprint planning on the sprint's first day: set Planned Velocity and open the task issues before any work starts. | Ali12hamdan | High | SPRINT-05 was again planned only on its last day. | Yes |
| Merge the CI and test pull request at least one day before the deploy, so the release candidate is fixed before the Customer meeting. | atkond2point0 | Medium | In SPRINT-05 the CI checks, the deploy and the meeting all fell on the due date. | Yes |
| TODO (after the meeting): one action from the Sprint Review, or delete this row. | | | | |

## Carried Actions

| Action | Outcome |
| --- | --- |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Rehearse the released demo from `docs/setup.md` on the presentation machine the day before each Customer review." | TODO: Done or Not done, with what the rehearsal found. |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Ask the Customer in writing for an AC-by-AC verdict on US-01 to US-04 and record the reply." | TODO (after the meeting): Done or Not done, citing the verdict `DEC-nnn` entries. |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Hold sprint planning on the sprint's first day: set Planned Velocity and open the task issues before any work starts." | Not done: SPRINT-05 was planned on 2026-10-31, its last day; re-listed in [Actions](#actions). |
| [reports/week-04/sprint-retrospective.md#actions](../week-04/sprint-retrospective.md#actions): "Branch each task from main with one pull request, avoid stacked and integration pull requests, and record the rule in `CONTRIBUTING.md` through a SPRINT-05 task issue." | Done: the rule is in [CONTRIBUTING.md](../../CONTRIBUTING.md#how-a-change-gets-in) through [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100), and the Week 5 tasks each have one pull request from main. |
