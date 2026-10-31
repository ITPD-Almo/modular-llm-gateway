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
The Week 5 Customer meeting, which is the SPRINT-05 Sprint Review, was postponed to Week 6, so no story received a verdict this week.
Actual Velocity is 0, and US-01 to US-04 and US-09 (18 points) moved to SPRINT-06 for their criterion-by-criterion verdicts.
The Week 4 action points and open questions that needed the meeting are carried to the Week 6 meeting.

## Minimum usable product and Customer outcome

The candidate remains [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41) and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42); [US-04](https://github.com/ITPD-Almo/modular-llm-gateway/issues/52) and [US-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96) were planned for the same review.

No Customer meeting was held in Week 5: the Sprint Review was postponed to Week 6 because the team and the Customer did not agree a meeting time in time; the new date is not yet confirmed.
No story was shown, accepted or rejected, so no verdict `DEC-nnn` exists for this week, and all five stories moved to SPRINT-06 rather than being dropped.
The implemented tests' results are recorded in the [testing plan](../../docs/project-plan.md#quality-requirement-testing-plan) and will be shown at their levels at the Week 6 review.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan and milestones | [docs/project-plan.md#sprint-05](../../docs/project-plan.md#sprint-05) and [docs/project-plan.md#milestones](../../docs/project-plan.md#milestones): the goal, Planned Velocity 18, Actual Velocity 0 (the review was postponed to Week 6), and MLS-05 due 2026-10-31, MLS-07 due 2026-11-14 |
| New stories | [User Story issues](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=is%3Aissue%20type%3A%22User%20Story%22): US-09 was initially scheduled in SPRINT-05 and carried to the [SPRINT-06 milestone](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/4) for the postponed review; US-10 remains refined and unscheduled |
| Quality requirement tests | [docs/quality-requirements/qr/](../../docs/quality-requirements/qr/): [QR-02 QRT-01](../../docs/quality-requirements/qr/QR-02.md#qrt-01) and [QR-01 QRT-01](../../docs/quality-requirements/qr/QR-01.md#qrt-01), the two active High business-importance requirements |
| Testing plan | [docs/project-plan.md#quality-requirement-testing-plan](../../docs/project-plan.md#quality-requirement-testing-plan) |
| Automated tests and CI | [.github/workflows/](../../.github/workflows/), with `actionlint` and the product-code checks |
| Deployment | [docs/deployment.md](../../docs/deployment.md); TODO: the staging and production instances and the core-task verification |
| Feature documentation | [docs/features.md](../../docs/features.md) |
| Week 4 action points | Not closed this week: the meeting was postponed, so the [Week 4 action points](../week-04/meeting-report.md#action-points) are carried to the Week 6 meeting report's `## Previous action points` |
| Week 4 open questions | Not closed this week: the [Week 4 open questions](../week-04/meeting-report.md#open-questions) are carried to the Week 6 meeting |
| Meeting script | None this week: the meeting was postponed to Week 6, and its script will be written for that meeting |
| Meeting transcript | None: no meeting was held in Week 5 |
| Customer validation | None this week: the Sprint Review was postponed to Week 6, as recorded [above](#minimum-usable-product-and-customer-outcome) |
| `REL-05` | TODO: the [v0.5.0 release](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.5.0), [CHANGELOG.md#050---2026-10-31](../../CHANGELOG.md#050---2026-10-31) and [docs/project-plan.md#rel-05](../../docs/project-plan.md#rel-05) |
| Sprint retrospective | [reports/week-05/sprint-retrospective.md](sprint-retrospective.md) |
| AI usage | [reports/week-05/ai-usage.md](ai-usage.md) |

## Contribution

| Member | Evidenced work |
| --- | --- |
| Ali12hamdan | [One-command installer #92](https://github.com/ITPD-Almo/modular-llm-gateway/pull/92), [install check #93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93), [provider setup #95](https://github.com/ITPD-Almo/modular-llm-gateway/pull/95), [deployment runbook #102](https://github.com/ITPD-Almo/modular-llm-gateway/pull/102) for [#99](https://github.com/ITPD-Almo/modular-llm-gateway/issues/99), the VM deploy and the v0.5.0 release. |
| Mohammed-Nour | [Plan, testing plan, features and sprint close #101](https://github.com/ITPD-Almo/modular-llm-gateway/pull/101), the Week 5 split and issues [#96](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96) to [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100), and reviews of #92, #93 and #95. |
| atkond2point0 | TODO: the CI checks and quality requirement tests pull request for [#98](https://github.com/ITPD-Almo/modular-llm-gateway/issues/98). |

## Repository evidence

[PR #92](https://github.com/ITPD-Almo/modular-llm-gateway/pull/92) merged after independent review and closed its task [#90](https://github.com/ITPD-Almo/modular-llm-gateway/issues/90).
TODO: the latest green link-check, Markdown-check, `actionlint` and product-code CI runs on main.
GitHub issue and project links and the course Git submodule are handled by the existing link-check exclusions.

## Deviations

- Issues [#96](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96) to [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100) were created through the GitHub CLI with the form's sections rather than through the issue forms; the organization issue fields were set afterwards by Ali12hamdan.
- SPRINT-05 was planned on its due date, 2026-10-31, not at the sprint's start; the planned velocity is a same-day baseline.
- [#94](https://github.com/ITPD-Almo/modular-llm-gateway/issues/94) moved to SPRINT-06 with its story [US-10](https://github.com/ITPD-Almo/modular-llm-gateway/issues/97); its pull request [#95](https://github.com/ITPD-Almo/modular-llm-gateway/pull/95) merged in SPRINT-05 as work done ahead of the story's sprint.
- `docs/features.md` has no entry for the one-command install: no functional requirement owns installation yet, and the course allows no feature without one.
- The Week 5 Customer meeting, the SPRINT-05 Sprint Review, was postponed to Week 6 because no meeting time was agreed in time; the new date is not yet confirmed. As a result:
  - no story was shown against its criteria, no verdict `DEC-nnn` was recorded, and Actual Velocity is 0, with US-01 to US-04 and US-09 moved to SPRINT-06;
  - `reports/week-05/meeting-script.md`, `meeting-report.md` and `meeting-transcript.md` do not exist; the Week 4 action points and open questions, including the matched LiteLLM comparison, are carried to the Week 6 meeting and closed in its report;
  - REL-05 is cut on the deployed and tested commit without a Customer review, so it carries no accepted story.
- The course VM from the university portal had not been supplied by 2026-10-31. The owner reports that the TA approved a temporary university VM which is directly reachable on campus, with Tailscale/Funnel providing outside access, and that the assignment VM is expected on Monday, November 2; see [docs/deployment.md](../../docs/deployment.md#vm-and-campus-access). These are owner-reported facts, not a completed campus deployment or test. TODO: record the actual staging QRT and production verification at their real access level, and the later migration.
- The deployment pull request [#102](https://github.com/ITPD-Almo/modular-llm-gateway/pull/102) says `Refs #99` instead of `Closes #99`, because it merges as the runbook before the deployment it describes. [#99](https://github.com/ITPD-Almo/modular-llm-gateway/issues/99) stays open until the real deployment, the campus verification and the tag exist, and is then closed by hand with #102 and this report's evidence linked, rather than by its pull request.
- TODO: any other fallback (a `scripted` or `CI` test instead of `deployed`), rework deferred to SPRINT-06, or other deviation from the day.

## Privacy

No private-only material was committed to this repository.
