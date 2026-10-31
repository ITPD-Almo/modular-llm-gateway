# Week 05 report

## Project

Modular LLM Gateway, team 9, Assignment 5: testing, verification, deployment and REL-05.

## Summary

TODO (after the deploy): the gateway runs in staging and production on the university VM, deployed by hand from a campus machine per [docs/deployment.md](../../docs/deployment.md); the Customer reaches production from the university network at the address in the Moodle submission.

The plan's milestones already place the next increments: [MLS-05](../../docs/project-plan.md#mls-05), due in SPRINT-05, delivers a shared gateway running from a tested, identifiable build, and [MLS-07](../../docs/project-plan.md#mls-07), due in SPRINT-07, delivers people outside the team running the gateway and writing a plugin from the documentation alone.
Both were already in the plan, so no milestone was added this week.
SPRINT-05 added [US-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96) (install and try the gateway with one command), scheduled this sprint, and [US-10](https://github.com/ITPD-Almo/modular-llm-gateway/issues/97) (connect your own provider account), refined for SPRINT-06.

TODO (after Sergey's PR): the product CI runs lint, format, type check, build and tests on pull requests and on main, together with `actionlint`; the checks that do not apply and why: TODO.
[QR-01 QRT-01](../../docs/quality-requirements/qr/QR-01.md#qrt-01) runs in the CI and [QR-02 QRT-01](../../docs/quality-requirements/qr/QR-02.md#qrt-01) against staging; the tests that are not `Passes` are in the [testing plan](../../docs/project-plan.md#quality-requirement-testing-plan).

TODO (after the tag): REL-05 is [v0.5.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.5.0), cut on the commit production runs.
TODO (after the meeting): what moved out of the sprint, and to which sprint.

## Minimum usable product and Customer outcome

The candidate remains [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41) and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), with [US-04](https://github.com/ITPD-Almo/modular-llm-gateway/issues/52) and [US-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96) shown at the same review.

| Story | Customer verdict | Decision |
| --- | --- | --- |
| US-01 | TODO | TODO `DEC-nnn` |
| US-02 | TODO | TODO `DEC-nnn` |
| US-03 | TODO | TODO `DEC-nnn` |
| US-04 | TODO | TODO `DEC-nnn` |
| US-09 | TODO | TODO `DEC-nnn` |

TODO (after the meeting): the result shown for each implemented test at its level: QR-01 QRT-01 from the CI run, and QR-02 QRT-01 against staging.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan and milestones | [docs/project-plan.md#sprint-05](../../docs/project-plan.md#sprint-05) and [docs/project-plan.md#milestones](../../docs/project-plan.md#milestones): the goal, Planned Velocity 18, Actual Velocity TODO, and MLS-05 due 2026-10-31, MLS-07 due 2026-11-14 |
| New stories | [User Story issues](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=is%3Aissue%20type%3A%22User%20Story%22) and the [SPRINT-05 milestone](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/3) holding US-09 |
| Quality requirement tests | [docs/quality-requirements/qr/](../../docs/quality-requirements/qr/): [QR-02 QRT-01](../../docs/quality-requirements/qr/QR-02.md#qrt-01) and [QR-01 QRT-01](../../docs/quality-requirements/qr/QR-01.md#qrt-01), the two active High business-importance requirements |
| Testing plan | [docs/project-plan.md#quality-requirement-testing-plan](../../docs/project-plan.md#quality-requirement-testing-plan) |
| Automated tests and CI | [.github/workflows/](../../.github/workflows/), with `actionlint` and the product-code checks |
| Deployment | [docs/deployment.md](../../docs/deployment.md); TODO: the staging and production instances and the core-task verification |
| Feature documentation | [docs/features.md](../../docs/features.md) |
| Week 4 action points | [reports/week-05/meeting-report.md#previous-action-points](meeting-report.md#previous-action-points) |
| Week 4 open questions | [reports/week-05/meeting-report.md#previous-open-questions](meeting-report.md#previous-open-questions) |
| Meeting script | [reports/week-05/meeting-script.md](meeting-script.md) |
| Meeting transcript | TODO: [reports/week-05/meeting-transcript.md](meeting-transcript.md), or one line saying why there is none |
| Customer validation | [reports/week-05/meeting-report.md](meeting-report.md), and each story's verdict above |
| `REL-05` | TODO: the [v0.5.0 release](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.5.0), [CHANGELOG.md#050---2026-10-31](../../CHANGELOG.md#050---2026-10-31) and [docs/project-plan.md#rel-05](../../docs/project-plan.md#rel-05) |
| Sprint retrospective | [reports/week-05/sprint-retrospective.md](sprint-retrospective.md) |
| AI usage | [reports/week-05/ai-usage.md](ai-usage.md) |

## Contribution

| Member | Evidenced work |
| --- | --- |
| Ali12hamdan | [One-command installer #92](https://github.com/ITPD-Almo/modular-llm-gateway/pull/92), [install check #93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93), [provider setup #95](https://github.com/ITPD-Almo/modular-llm-gateway/pull/95), TODO: the deployment and Sprint Review pull request for [#99](https://github.com/ITPD-Almo/modular-llm-gateway/issues/99), the VM deploy and the v0.5.0 release. |
| Mohammed-Nour | [Plan, testing plan, features and sprint close #101](https://github.com/ITPD-Almo/modular-llm-gateway/pull/101), the Week 5 split and issues [#96](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96) to [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100), and reviews of #92, #93 and #95. |
| atkond2point0 | TODO: the CI checks and quality requirement tests pull request for [#98](https://github.com/ITPD-Almo/modular-llm-gateway/issues/98). |

## Repository evidence

TODO: one merged pull request that closed its task issue, and the latest green link-check, Markdown-check, `actionlint` and product-code CI runs on main.
GitHub issue and project links and the course Git submodule are handled by the existing link-check exclusions.

## Deviations

- Issues [#96](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96) to [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100) were created through the GitHub CLI with the form's sections rather than through the issue forms; the organization issue fields were set afterwards by Ali12hamdan.
- SPRINT-05 was planned on its due date, 2026-10-31, not at the sprint's start; the planned velocity is a same-day baseline.
- [#94](https://github.com/ITPD-Almo/modular-llm-gateway/issues/94) moved to SPRINT-06 with its story [US-10](https://github.com/ITPD-Almo/modular-llm-gateway/issues/97); its pull request [#95](https://github.com/ITPD-Almo/modular-llm-gateway/pull/95) merged in SPRINT-05 as work done ahead of the story's sprint.
- `docs/features.md` has no entry for the one-command install: no functional requirement owns installation yet, and the course allows no feature without one.
- TODO: any fallback (a `scripted` or `CI` test instead of `deployed`), rework deferred to SPRINT-06, or other deviation from the day.

## Privacy

No private-only material was committed to this repository.
