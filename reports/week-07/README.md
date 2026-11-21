# Week 7 report

## Project

Modular LLM Gateway, Team 9. Scope covers `SPRINT-07` and the design handoff for `SPRINT-08`.

## Summary

The new [versioned Compose deployment](../../docs/deployment.md#versioned-compose-deployment) starts the same terminal gateway from a pinned image. The [local walkthrough](compose-demo-evidence.md) verifies a plugin added through configuration, a named request-hook timeout and a successful follow-up on the same gateway. The [production evidence from REL-06](../week-06/README.md#rel-06-release-verification) remains the latest released deployment record covered here. The customer-directed work follows [DEC-012](../../docs/decisions.md#dec-012) and [DEC-013](../../docs/decisions.md#dec-013).

The [UT-01 design](../../docs/usability-tests/ut-01/README.md) targets five adult developers or DevOps operators with basic terminal and Python skills who are new to the gateway. At least three valid sessions are needed to judge [QR-09 QRT-01](../../docs/quality-requirements/qr/QR-09.md#qrt-01). The team arranges the sessions on campus in Week 8. This design week claims no usability result. No transcript of the design review is published: the Customer's publication permission is still pending, as the [meeting report](meeting-report.md#metadata) records. See the [testing plan](../../docs/project-plan.md#quality-requirement-testing-plan) for tests still awaiting a verdict.

[Analytics](../../docs/analytics.md) measures seven-day [configured chat attempts](../../docs/analytics.md#configured-chat-attempts) as the input to the focus metric. The focus metric needs observed, eligible configured traffic in that window. Rehearsal traffic is excluded. [Observability](../../docs/observability.md) records the runtime signals separately.

## Minimum usable product and customer outcome

The working candidate shows a DevOps operator how to add a Python class through the configuration file, confirm its effect in one synthetic request, and recover from a slow hook. The [Week 7 feedback and review evidence](meeting-report.md) connects the confirmed operator, Compose and terminal guidance to the verified work. US-01 to US-04, US-09, US-11 and US-12 remain open for their verdicts.

## Usability test

1. The main task is a clean Compose start followed by a synthetic chat whose transformation and plugin trace the operator can explain.
2. The first secondary task is to identify a named 504, check health and complete a follow-up chat on the same process. The second is to add a small request plugin and see its marker without changing gateway core.
3. The [surveys](../../docs/usability-tests/ut-01/surveys.md) cover background, ease after each task, SUS and open-ended feedback. The [protocol](../../docs/usability-tests/ut-01/sessions/README.md) records time, completion, assistance and friction.
4. The [staging contract](../../docs/ut01-staging.md) connects one UTC window to the dedicated `ut01/gateway_usage` stream. The [implementation rehearsal](https://github.com/ITPD-Almo/modular-llm-gateway/pull/129#issuecomment-6854627777) checked eight filtered events, a successful chat, a timeout, a same-run recovery and a private offline marker result. The separate pre-session verification is [#132](https://github.com/ITPD-Almo/modular-llm-gateway/issues/132).
5. Use the [consent template](../../docs/usability-tests/ut-01/consent.md). The [private usability-data repository](https://github.com/ITPD-Almo/modular-llm-gateway-usability-data) holds filtered telemetry, consent and raw text. The [link check](../../.lycheeignore) excludes it, because the repository requires GitHub authentication. The UT-01 recordings folder link and sign-in instructions belong in the private Moodle wrapper.
6. The [session schedule](../../docs/usability-tests/ut-01/README.md#schedule), [empty results and triage templates](../../docs/usability-tests/ut-01/results.md) and [QR-09](../../docs/quality-requirements/qr/QR-09.md) carry the Week 8 handoff. The pass bar is at least two thirds of at least three valid participants completing the main task unaided. The [accountable design review](https://github.com/ITPD-Almo/modular-llm-gateway/pull/140#pullrequestreview-5907097681) reports the uncounted teammate dry run and states that instructor access was confirmed privately. The current private handoff still records instructor access as pending, so this report treats that part as a reviewer claim awaiting its private record. The recording details, dry-run date and resulting changes go in the private handoff.

## Threshold review

| Goal | Current measure | New data can settle it | Proposal |
| --- | --- | --- | --- |
| [TOS-02](../../docs/threshold-of-success.md#tos-02) | An outside operator follows setup without help and completes a configured chat by 2026-11-13, Week 7. | No. The telemetry records attempts and outcomes, while the facilitator records assistance. | — |
| [TOS-03](../../docs/threshold-of-success.md#tos-03) | An outside developer follows the plugin guide and changes a request without editing gateway core by 2026-11-13, Week 7. | No. The marker probe sees the result only. | — |

[TOS-02](../../docs/threshold-of-success.md#tos-02) is Missed.
[TOS-03](../../docs/threshold-of-success.md#tos-03) is Missed.

The counted UT-01 sessions are the next opportunity to observe both activities. The original measures and dates remain the basis of this review.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan | [docs/project-plan.md#sprint-07](../../docs/project-plan.md#sprint-07) |
| UT-01 test record | [docs/usability-tests/ut-01/README.md](../../docs/usability-tests/ut-01/README.md) |
| Surveys and post-test | [docs/usability-tests/ut-01/surveys.md](../../docs/usability-tests/ut-01/surveys.md) |
| Tasks and protocol | [docs/usability-tests/ut-01/README.md#the-tasks](../../docs/usability-tests/ut-01/README.md#the-tasks), [docs/usability-tests/ut-01/sessions/README.md](../../docs/usability-tests/ut-01/sessions/README.md) |
| Test instrumentation | [docs/usability-tests/ut-01/README.md#instrumentation](../../docs/usability-tests/ut-01/README.md#instrumentation), [docs/analytics.md#the-events](../../docs/analytics.md#the-events) |
| Consent | [docs/usability-tests/ut-01/consent.md](../../docs/usability-tests/ut-01/consent.md) |
| Private usability-data repository | [Private UT-01 text repository](https://github.com/ITPD-Almo/modular-llm-gateway-usability-data) |
| Recordings folder | Private access details belong in the Moodle wrapper. See [usability test](#usability-test) for the status. |
| Requirement and test | [docs/quality-requirements/qr/QR-09.md#qrt-01](../../docs/quality-requirements/qr/QR-09.md#qrt-01) |
| Recruitment target and session plan | [docs/usability-tests/ut-01/README.md#participant-profile](../../docs/usability-tests/ut-01/README.md#participant-profile), [docs/usability-tests/ut-01/README.md#schedule](../../docs/usability-tests/ut-01/README.md#schedule) |
| Week 8 handoff | [Usability test](#usability-test), [SPRINT-08](../../docs/project-plan.md#sprint-08) |
| Glossary | [docs/glossary.md](../../docs/glossary.md) |
| Risk register | [docs/risks.md](../../docs/risks.md) |
| Week 6 action points | [Previous action points](meeting-report.md#previous-action-points) |
| Week 6 open questions | [Previous open questions](meeting-report.md#previous-open-questions) |
| Sprint Review preparation | [reports/week-07/meeting-script.md](meeting-script.md) |
| Sprint Review | [reports/week-07/meeting-report.md](meeting-report.md) |
| Meeting transcript | None: the Customer's publication permission is pending. |
| Compose plugin demonstration | [reports/week-07/compose-demo-evidence.md](compose-demo-evidence.md) |
| `REL-07` | [v0.7.0 tag and release body](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.7.0), [CHANGELOG.md](../../CHANGELOG.md#070---2026-11-15), [docs/project-plan.md#rel-07](../../docs/project-plan.md#rel-07) |
| Retrospective | [reports/week-07/sprint-retrospective.md](sprint-retrospective.md) |
| AI usage | [reports/week-07/ai-usage.md](ai-usage.md). The earlier [Ali's disclosure](ai-usage-ali.md) is kept as a historical artifact. |

## Contribution

| Member | Work |
| --- | --- |
| Ali12hamdan | [Versioned image, Compose and staging instrumentation](https://github.com/ITPD-Almo/modular-llm-gateway/pull/129). |
| Mohammed-Nour | [Sprint plan and review script](https://github.com/ITPD-Almo/modular-llm-gateway/pull/139), plus the accountable reviews of [#129](https://github.com/ITPD-Almo/modular-llm-gateway/pull/129), [#140](https://github.com/ITPD-Almo/modular-llm-gateway/pull/140) and [#141](https://github.com/ITPD-Almo/modular-llm-gateway/pull/141). |
| atkond2point0 | [UT-01 design, QR-09, consent, and recruitment and analysis plans](https://github.com/ITPD-Almo/modular-llm-gateway/pull/140). |

## Repository evidence

[#140](https://github.com/ITPD-Almo/modular-llm-gateway/pull/140) merged and closed its task issue [#131](https://github.com/ITPD-Almo/modular-llm-gateway/issues/131). On `main` at [`ae808ad`](https://github.com/ITPD-Almo/modular-llm-gateway/commit/ae808ad501553d9ba67ff50b2ee0c99424fb2f48), the [link check](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/43690230293), [Markdown check](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/43690230262), [actionlint](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/43690230301) and [product tests](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/43690230267) passed.

[QR-01 QRT-01 passed on the release commit](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/43648314095) with 102 tests in 18.85 seconds. The [link-check configuration](../../.lycheeignore) excludes the private usability-data repository because it requires GitHub authentication.

On November 15 the TA's existing HTTPS staging route served Swagger, its schema and assets, and health with the staging credential. Anonymous requests and the wrong code returned HTTP 401. The routing check used the deployed `v0.6.0` service. The remote staging link and its access instructions are private.

## Deviations

- The current deployment evidence identifies production as `v0.6.0`. The Compose evidence is from the merged implementation and a separate synthetic run.
- The implementation rehearsal and the uncounted teammate dry run have separate checks. The [accountable review](https://github.com/ITPD-Almo/modular-llm-gateway/pull/140#pullrequestreview-5907097681) reports the dry run as done and states that instructor access was confirmed privately; the current private handoff still records instructor access as pending. [#134](https://github.com/ITPD-Almo/modular-llm-gateway/issues/134) keeps the dry-run notes in the private evidence location.
- The closeout uses [confirmed feedback and technical evidence](meeting-report.md). The design-review recording, transcript permissions, story verdicts and Week 8 agreement remain pending. The private wrapper records the available instructor access details.

## Privacy

No private-only material or participant identity is included in the product repository.
