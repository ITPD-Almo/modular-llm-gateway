# SPRINT-04 retrospective

Written by Mohammed-Nour at the sprint close on 2026-10-25 from the sprint's issues, pull requests and meeting record, with Ali12hamdan's input on [#61](https://github.com/ITPD-Almo/modular-llm-gateway/issues/61).
No separate retrospective meeting was held; Ali12hamdan reviews this file as the Accountable member.

## What Went Well

| What went well |
| --- |
| The supervised plugin runtime shipped to main in [#81](https://github.com/ITPD-Almo/modular-llm-gateway/pull/81): a 5-second hook returns HTTP 504 in about 0.3 seconds, and later requests and `/health` still succeed. |
| The quality and functional requirements ([#73](https://github.com/ITPD-Almo/modular-llm-gateway/pull/73)) and ADR-001 to ADR-004 ([#77](https://github.com/ITPD-Almo/modular-llm-gateway/pull/77)) merged before the runtime integration, so its review checked the code against accepted numbers. |
| The Customer's A-input/B-output request from October 23 became a configuration-loaded example and a scripted demo in [#76](https://github.com/ITPD-Almo/modular-llm-gateway/pull/76), replayed by a second member. |
| Independent reviews reproduced failures over real HTTP and requested changes on [#69](https://github.com/ITPD-Almo/modular-llm-gateway/pull/69) and [#71](https://github.com/ITPD-Almo/modular-llm-gateway/pull/71) before approval, and a field readback caught an issue-field overwrite before it was lost. |

## What Did Not

| Problem | Root cause |
| --- | --- |
| The October 23 review's local setup failed, so the Customer saw no working demonstration and gave no story verdict. | The demo had not been rehearsed from `docs/setup.md` on a clean machine before the meeting. |
| The sprint was replanned and estimated only on October 25, the day after the formal due date. | No planning session was held at the start of the sprint; the plan, task issues and Planned Velocity were written after the review. |
| Fourteen pull requests were opened on October 25, several stacked on each other, which caused retargeting, repeated branch updates and bunched reviews. | Work was split into dependent branches that could only merge in order, and all of it started on the last day. |

## Actions

| Action | Owner | Impact | Reason | Carried |
| --- | --- | --- | --- | --- |
| Rehearse the released demo from `docs/setup.md` on the presentation machine the day before each Customer review. | Mohammed-Nour | High | The October 23 setup failed live. | Yes |
| Ask the Customer in writing for an AC-by-AC verdict on US-01 to US-04 and record the reply. | Ali12hamdan | High | No story was accepted, so Actual Velocity is 0. | Yes |
| Hold sprint planning on the sprint's first day: set Planned Velocity and open the task issues before any work starts. | Ali12hamdan | High | SPRINT-04 was replanned only on its last day. | Yes |
| Branch each task from main with one pull request, avoid stacked and integration pull requests, and record the rule in `CONTRIBUTING.md` through a SPRINT-05 task issue. | Mohammed-Nour | Medium | Stacked pull requests caused the October 25 review backlog. | Yes |

## Carried Actions

This is the first retrospective, so there is no previous retrospective to carry actions from.
