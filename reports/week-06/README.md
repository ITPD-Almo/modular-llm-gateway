# Week 06 report

## Project

Modular LLM Gateway, team 9, Assignment 6: product analytics, observability and the Week 6 release.

## Summary

SPRINT-06 set out to make the gateway's use and operation visible: privacy-safe analytics events for a product analyst ([US-11](https://github.com/ITPD-Almo/modular-llm-gateway/issues/110)) and the operating signals an operator uses to diagnose a failed request ([US-12](https://github.com/ITPD-Almo/modular-llm-gateway/issues/111)), in four dashboards on the university network.
The sprint was planned, and its task issues opened, only on 2026-11-08, its due date; the [plan](../../docs/project-plan.md#sprint-06) records it.

The telemetry work started on the due date.
The observability pipeline ([#108](https://github.com/ITPD-Almo/modular-llm-gateway/issues/108), [PR #109](https://github.com/ITPD-Almo/modular-llm-gateway/pull/109)) adds the [observability plan](../../docs/observability.md), `SLI-01` and the diagnosability requirement QR-08, rehearsed against a local OpenObserve.
The analytics pipeline ([#112](https://github.com/ITPD-Almo/modular-llm-gateway/issues/112)) was not delivered by the deadline, so there is no `docs/analytics.md`, no focus metric and no analytics query result to show; the focus metric has no value, and it would need the analytics pipeline deployed and people outside the team using the gateway in the Week 7 usability test.
The four dashboards and the deployed QR-08 QRT-01 run are recorded below as they stood at the deadline; the tests that are not `Passes` are in the [testing plan](../../docs/project-plan.md#quality-requirement-testing-plan).

The Customer review was held on 2026-11-07, before the telemetry existed.
It showed the one-command install and a request to a real model, and it settled three decisions: a Docker Compose deployment ([DEC-012](../../docs/decisions.md#dec-012)), the terminal as the interface ([DEC-013](../../docs/decisions.md#dec-013)) and Saturday reviews with asynchronous questions ([DEC-014](../../docs/decisions.md#dec-014)).
No story was walked through its criteria and no verdict was given, so Actual Velocity is 0 and US-01 to US-04, US-09, US-11 and US-12 (24 points) move to SPRINT-07.

REL-06 is recorded in [docs/project-plan.md#rel-06](../../docs/project-plan.md#rel-06).

## Minimum usable product and Customer outcome

The candidate remains [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41) and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42).
At the [2026-11-07 review](meeting-report.md) the Customer saw the install and the guided provider setup from [US-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96) and the plugin configuration and hook code behind US-01 to US-04, but no story was shown criterion by criterion and none was accepted or rejected, so no verdict `DEC-nnn` exists.
All scheduled stories moved to SPRINT-07 rather than being dropped.

## Dashboards and the observability test

No dashboard screenshot exists at the time of writing: the analytics and observability backends were not yet deployed on the university VM, so `reports/week-06/images/` has no files and QR-08 QRT-01 has not been run against staging.
Mohammed-Nour, on the university network, checked again for the deployed pipelines before the deadline; the [deviations](#deviations) record what was missing.

## Threshold review

| Goal | Current measure | New data can settle it | Proposal |
| --- | --- | --- | --- |
| [TOS-01](../../docs/threshold-of-success.md#tos-01) | An accepted verdict, as a `DEC-nnn`, on every candidate story of MLS-03, by the end of Week 4, 2026-10-23. | No: it is settled by a Customer verdict, not by telemetry. | — |
| [TOS-02](../../docs/threshold-of-success.md#tos-02) | One usability-test session in which a participant outside the team follows `docs/setup.md`, sends a request through two plugins and sees the result without help, by the end of Week 7, 2026-11-13. | No: it is settled by an observed session; analytics events could count the steps, but no analytics pipeline is deployed. | — |
| [TOS-03](../../docs/threshold-of-success.md#tos-03) | One plugin, written by a developer outside the team against `docs/plugins.md`, that loads from the configuration file and changes a request, with no commit to the core, by the end of Week 7, 2026-11-13. | No: it is settled by an outside developer's plugin and the repository history, which no signal records. | — |
| [TOS-04](../../docs/threshold-of-success.md#tos-04) | A request to the deployed gateway passes through two plugins and returns the fake provider's response, shown in the release notes of `REL-05`, by the end of Week 5, 2026-10-30. | No: its date had passed before the review; the observability data could show such a request, but not by that date. | — |

[TOS-01](../../docs/threshold-of-success.md#tos-01) is `Missed`.
[TOS-02](../../docs/threshold-of-success.md#tos-02) stays `Open`.
[TOS-03](../../docs/threshold-of-success.md#tos-03) stays `Open`.
[TOS-04](../../docs/threshold-of-success.md#tos-04) is `Missed`.

The team proposed no measure: an analytics-measured proposal needs a metric section in `docs/analytics.md` to cite, and the analytics plan was not delivered; the two open goals already measure what the Customer cares about, outside people using the product, in Week 7. No proposal was presented at the 2026-11-07 review, so there is no Customer decision on one and no goal changed.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan and new stories | [docs/project-plan.md#sprint-06](../../docs/project-plan.md#sprint-06), and [US-11](https://github.com/ITPD-Almo/modular-llm-gateway/issues/110) and [US-12](https://github.com/ITPD-Almo/modular-llm-gateway/issues/111) in the [SPRINT-06 milestone](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/4) |
| Analytics plan | Not delivered: `docs/analytics.md` does not exist; see [Deviations](#deviations) |
| Events and instrumentation | Not delivered: no event table or instrumentation; see [Deviations](#deviations) |
| Analytics dashboards | Not delivered: no analytics backend was deployed, so there are no screenshots |
| Observability plan and `SLI`s | [docs/observability.md](../../docs/observability.md) |
| Observability dashboards | Not delivered: the observability backend was not deployed on the VM, so there are no screenshots |
| Feature documentation | [docs/features.md](../../docs/features.md) |
| Functional requirements | [docs/functional-requirements/README.md](../../docs/functional-requirements/README.md), with FR-013; FR-012 was not written |
| ADRs and container view | [docs/architecture/adr/README.md](../../docs/architecture/adr/README.md) and [docs/architecture/README.md#container-view](../../docs/architecture/README.md#container-view), with ADR-008; ADR-007 was not written |
| Observability requirement | [docs/quality-requirements/qr/QR-08.md](../../docs/quality-requirements/qr/QR-08.md) and its [QRT-01](../../docs/quality-requirements/qr/QR-08.md#qrt-01) |
| Runtime test re-run | None: no runtime test was re-run this sprint |
| Threshold review | [reports/week-06/README.md#threshold-review](#threshold-review) |
| Week 5 action points | [`## Previous action points` in reports/week-06/meeting-report.md](meeting-report.md#previous-action-points): Week 5 had no meeting report, so these are the Week 4 action points it carried |
| Week 5 open questions | [`## Previous open questions` in reports/week-06/meeting-report.md](meeting-report.md#previous-open-questions) |
| Meeting script | [reports/week-06/meeting-script.md](meeting-script.md): a reconstructed agenda and a follow-up agenda, written after the meeting |
| Meeting transcript | [reports/week-06/meeting-transcript.md](meeting-transcript.md) |
| Customer validation | [reports/week-06/meeting-report.md](meeting-report.md); no threshold proposal was presented, so there is no threshold decision |
| `REL-06` | [docs/project-plan.md#rel-06](../../docs/project-plan.md#rel-06) |
| Sprint retrospective | [reports/week-06/sprint-retrospective.md](sprint-retrospective.md) |
| AI usage | [reports/week-06/ai-usage.md](ai-usage.md) |

## Contribution

| Member | Evidenced work |
| --- | --- |
| Ali12hamdan | Presented at the [2026-11-07 Customer review](meeting-report.md); opened the observability task [#108](https://github.com/ITPD-Almo/modular-llm-gateway/issues/108) and [PR #109](https://github.com/ITPD-Almo/modular-llm-gateway/pull/109): the OTLP exporter, `SLI-01`, QR-08, FR-013, ADR-008 and the QRT checker, rehearsed locally. |
| Mohammed-Nour | Planned SPRINT-06 and refined the backlog: [US-11](https://github.com/ITPD-Almo/modular-llm-gateway/issues/110), [US-12](https://github.com/ITPD-Almo/modular-llm-gateway/issues/111), [US-13](https://github.com/ITPD-Almo/modular-llm-gateway/issues/118), tasks [#112](https://github.com/ITPD-Almo/modular-llm-gateway/issues/112) to [#117](https://github.com/ITPD-Almo/modular-llm-gateway/issues/117) and the notes on #65, #67, #68 and #97; wrote the Week 6 meeting artifacts, DEC-012 to DEC-014, the threshold review, the retrospective and this report for [#117](https://github.com/ITPD-Almo/modular-llm-gateway/issues/117). |
| atkond2point0 | Accountable for [#108](https://github.com/ITPD-Almo/modular-llm-gateway/issues/108) and [#112](https://github.com/ITPD-Almo/modular-llm-gateway/issues/112); no commit or review is recorded for this sprint at the time of writing. |

## Repository evidence

The pull request for [#117](https://github.com/ITPD-Almo/modular-llm-gateway/issues/117) closes that task after independent review.
Latest checks on `main` before this sprint's merges: [links](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/41238756989), [Markdown](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/41238756894), [actionlint](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/41238756926), [product-code CI](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/41238757054), [native installation](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/41238756896) and [docs](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/41238757179).
GitHub issue and project links and the course Git submodule are handled by the existing link-check exclusions.

## Deviations

- SPRINT-06 was planned on its due date, 2026-11-08, the day after its review; its Planned Velocity is a same-day remaining-work baseline, and the stories and tasks were created through the GitHub API with the forms' sections rather than through the issue forms. The organization's `MoSCoW`, `Story Points`, `Responsible` and `Accountable` fields are set by Ali12hamdan, because Mohammed-Nour has no organization access; the values are also in each issue's notes.
- The analytics and observability work started on the due date. The analytics pipeline and its two dashboards ([#112](https://github.com/ITPD-Almo/modular-llm-gateway/issues/112) to [#114](https://github.com/ITPD-Almo/modular-llm-gateway/issues/114)) were not delivered, and the observability backend and its two dashboards ([#115](https://github.com/ITPD-Almo/modular-llm-gateway/issues/115), [#116](https://github.com/ITPD-Almo/modular-llm-gateway/issues/116)) were not deployed on the university VM. As a result there is no `docs/analytics.md`, event table, FR-012, ADR-007, analytics feature entry, staging smoke event or computed metric, there are no dashboard screenshots, and the open tasks move to SPRINT-07.
- QR-08 QRT-01, the only test planned for SPRINT-06, was not run against staging because the observability backend was not deployed there; it moves to SPRINT-07, as the [testing plan](../../docs/project-plan.md#quality-requirement-testing-plan) records.
- Seven task issues were created for Part 1, but only three are closed by a pull request: [#108](https://github.com/ITPD-Almo/modular-llm-gateway/issues/108), [#112](https://github.com/ITPD-Almo/modular-llm-gateway/issues/112) and [#117](https://github.com/ITPD-Almo/modular-llm-gateway/issues/117). The four dashboard tasks are configured in the backends, not in the repository, so they are closed by their Accountable member when their criteria hold, which conflicts with the course rule that a pull request closes a task.
- The 2026-11-07 review was not prepared in writing, did not show the dashboards or the observability test, asked for no story verdict and presented no threshold proposal. The [meeting script](meeting-script.md) is reconstructed after the meeting and carries a follow-up agenda for 2026-11-14, which is held only if arranged.
- Week 5 has no meeting report, so the Week 6 meeting report closes the Week 4 action points and open questions that the Week 5 report carried.
- The retrospective is a written closeout from the issue, pull request and meeting records; no synchronous ceremony or complete set of personal feedback was recorded.
- The AI usage statements of Ali12hamdan and atkond2point0 had not been received when this report was written.

## Privacy

No private-only material was committed to this repository.
