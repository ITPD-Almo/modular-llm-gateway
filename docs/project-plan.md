# Project plan

## Milestones

### MLS-03

- **Due:** 2026-10-17
- **Sprints:** [SPRINT-03](#sprint-03)
- **Advances:** [TOS-01](threshold-of-success.md#tos-01)

A DevOps operator starts the gateway with two plugins listed in a configuration file, sends a request to a fake provider, and sees each plugin's effect on the request and the response.
The plugin interface is documented, so a plugin can be written against it rather than against the core, per [DEC-006](decisions.md#dec-006).
Restarting after a configuration change is allowed, per [DEC-005](decisions.md#dec-005).

### MLS-05

- **Due:** 2026-10-31
- **Sprints:** [SPRINT-04](#sprint-04), [SPRINT-05](#sprint-05)
- **Advances:** [TOS-04](threshold-of-success.md#tos-04)

The gateway runs in a shared environment from a tested, identifiable build, and an operator can verify the deployment and recover the previous known-good version.

### MLS-07

- **Due:** 2026-11-14
- **Sprints:** [SPRINT-06](#sprint-06), [SPRINT-07](#sprint-07)
- **Advances:** [TOS-02](threshold-of-success.md#tos-02), [TOS-03](threshold-of-success.md#tos-03)

People outside the team run the gateway and write a plugin of their own from the documentation alone, observed in the usability test.

### MLS-09

- **Due:** 2026-11-28
- **Sprints:** [SPRINT-08](#sprint-08), [SPRINT-09](#sprint-09)
- **Advances:** [TOS-02](threshold-of-success.md#tos-02), [TOS-03](threshold-of-success.md#tos-03), [TOS-04](threshold-of-success.md#tos-04)

The team can rebuild the final gateway release, explain its configuration and plugin versions, recover an earlier release, and demonstrate the fixes supported by the usability findings.

## Sprints

### SPRINT-03

A DevOps operator starts the gateway with two plugins from a configuration file, sends a request to the fake provider, and sees each plugin's effect.

- **Due:** 2026-10-17
- **Sprint Backlog:** [the issues scheduled into SPRINT-03](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/1)

#### REL-03

Released as [v0.1.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.1.0) on 2026-10-17, from [the checked main commit](https://github.com/ITPD-Almo/modular-llm-gateway/commit/71cb6ff3eac0da2172d6563229d2a76f7d2598b2). Customer validation was not completed for this submission. Stories #40 to #42 and the remaining report task #45 were carried into SPRINT-04 before the SPRINT-03 GitHub milestone was closed.

### SPRINT-04

A DevOps operator can add a documented plugin without editing the gateway core, identify a failed or timed-out hook, and use the gateway again, with testable requirements and architecture explaining the result.

- **Due:** 2026-10-24
- **Sprint Backlog:** [the issues scheduled into SPRINT-04](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/2)
- **Planned Velocity:** 13
- **Actual Velocity:** 0; no Customer verdict on US-01 to US-04 arrived by the sprint close, so the four stories (13 points) moved to SPRINT-05 for their criterion-by-criterion verdicts.

The formal sprint date above follows Assignment 4; the team owner confirmed an operational submission extension to 2026-10-25, 23:59 Europe/Moscow.
The planned velocity was computed by hand as 2 + 3 + 3 + 5 from the selected stories' `Story Points` during late replanning on October 25.
This is a remaining-work planning baseline recorded on October 25, before the newly planned work; it is not evidence of a sprint-start estimate made earlier in the week.
The three stories carried from SPRINT-03 have implementation in v0.1.0 and still await Customer verdicts.
The resilience outcome and numerical targets have accepted specifications and reviewed implementation; the Customer's verdict remains pending.
The [planning task](https://github.com/ITPD-Almo/modular-llm-gateway/issues/51) links the reviewable Week 4 delivery gates; issue fields and the milestone remain the source of assignments and schedule.

#### REL-04

Released as [v0.2.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.2.0) on 2026-10-25, from [the checked main commit](https://github.com/ITPD-Almo/modular-llm-gateway/commit/960616128ca88159a003aa772dd198c4c0f515ea), with its [dated changelog section](https://github.com/ITPD-Almo/modular-llm-gateway/blob/main/CHANGELOG.md#020---2026-10-25). Customer validation was not completed for this submission, so the release adds no accepted velocity. Stories #40 to #42 and #52 moved to SPRINT-05 for their Customer verdicts, and the unscheduled candidates #65 to #68 stay in the product backlog. The release-line task #63 and report task #64 stay in SPRINT-04 until they merge; the SPRINT-04 milestone is closed after that, once no open issue remains in it.

### SPRINT-05

The Customer opens the gateway on the university VM from the university network, the team proves its two High business-importance quality requirements in the CI and against staging, and a newcomer can install and try the gateway with one command.

- **Due:** 2026-10-31
- **Sprint Backlog:** [the issues scheduled into SPRINT-05](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/3)
- **Planned Velocity:** 18
- **Actual Velocity:** 0; the Week 5 Customer meeting, which is the SPRINT-05 Sprint Review, was postponed to Week 6, so no story received a verdict, and US-01 to US-04 and US-09 (18 points) moved to SPRINT-06.

The planned velocity was computed by hand as 2 + 3 + 3 + 5 + 5 from the `Story Points` of [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), [US-04](https://github.com/ITPD-Almo/modular-llm-gateway/issues/52) and [US-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96).
The first four stories carried over from SPRINT-04 for their Customer verdicts; US-09 is new this sprint.
[US-10](https://github.com/ITPD-Almo/modular-llm-gateway/issues/97) is refined for SPRINT-06 and stays in the product backlog with no milestone, together with the refined candidates US-05 to US-08.
The work is split into one task per member: [#98](https://github.com/ITPD-Almo/modular-llm-gateway/issues/98) for the CI checks and the quality requirement tests, [#99](https://github.com/ITPD-Almo/modular-llm-gateway/issues/99) for the deployment and the Sprint Review, and [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100) for the plan, the features and the sprint close.

#### REL-05

- **Released:** [v0.5.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.5.0) on 2026-10-31, from [the production commit](https://github.com/ITPD-Almo/modular-llm-gateway/commit/ba6d8a050e443dc13e69e4c052f4d5b766201e75).
- **Checked QRs:**
  - [QR-02](quality-requirements/qr/QR-02.md)
  - [QR-01](quality-requirements/qr/QR-01.md)

The [testing plan](#quality-requirement-testing-plan) owns the checked results and their scope. The release has no accepted story because the Customer review moved to Week 6. The later documentation closeout does not change the deployed product code.

### SPRINT-06

An analyst sees how a trial uses the gateway from privacy-safe events, and an operator finds a failed request and its effect on latency from the gateway's signals, in four dashboards on the university network; the stories carried from SPRINT-05 are shown to the Customer for their verdicts.

- **Due:** 2026-11-08
- **Sprint Backlog:** [the issues scheduled into SPRINT-06](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/4)
- **Planned Velocity:** 24
- **Actual Velocity:** 0; the 2026-11-07 review asked for no verdict, so no story was accepted, and US-01 to US-04, US-09, US-11 and US-12 (24 points) moved to SPRINT-07 for their verdicts.

The planned velocity was computed by hand as 2 + 3 + 3 + 5 + 5 + 3 + 3 from the `Story Points` of [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), [US-04](https://github.com/ITPD-Almo/modular-llm-gateway/issues/52), [US-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96), [US-11](https://github.com/ITPD-Almo/modular-llm-gateway/issues/110) and [US-12](https://github.com/ITPD-Almo/modular-llm-gateway/issues/111).
The sprint was planned on 2026-11-08, its last day and the day after its review, so the figure is a remaining-work baseline rather than a sprint-start estimate.
No plan milestone is due in SPRINT-06, so the goal above states the telemetry increment; MLS-07 is due in SPRINT-07.
The tasks are [#112](https://github.com/ITPD-Almo/modular-llm-gateway/issues/112) for the analytics pipeline and [#108](https://github.com/ITPD-Almo/modular-llm-gateway/issues/108) for the observability pipeline, [#113](https://github.com/ITPD-Almo/modular-llm-gateway/issues/113) to [#116](https://github.com/ITPD-Almo/modular-llm-gateway/issues/116) for the four dashboards, and [#117](https://github.com/ITPD-Almo/modular-llm-gateway/issues/117) for the deployed observability test and the sprint close.
The product backlog refined for the next two sprints, with no milestone, is [US-05](https://github.com/ITPD-Almo/modular-llm-gateway/issues/65) (8 points), [US-06](https://github.com/ITPD-Almo/modular-llm-gateway/issues/66) (5), [US-07](https://github.com/ITPD-Almo/modular-llm-gateway/issues/67) (5), [US-08](https://github.com/ITPD-Almo/modular-llm-gateway/issues/68) (3), [US-10](https://github.com/ITPD-Almo/modular-llm-gateway/issues/97) (3) and [US-13](https://github.com/ITPD-Almo/modular-llm-gateway/issues/118) (5), 29 points, refined on 2026-11-08 against US-11, US-12 and the Customer's [DEC-012](decisions.md#dec-012).

#### REL-06

- **Released:** [v0.6.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.6.0) on 2026-11-08, from [the production commit](https://github.com/ITPD-Almo/modular-llm-gateway/commit/1f166129406aac490df9b9704ca2f4171b3e8a0b).
- **Checked QRs:**
  - [QR-01](quality-requirements/qr/QR-01.md)
  - [QR-08](quality-requirements/qr/QR-08.md)

The release commit passed CI and the deployed QR-08 staging test over university Wi-Fi. The same commit passed protected production health and a configured DeepSeek chat through the metadata and uppercase plugins. Staging smoke events were excluded from usage counts and production received no synthetic telemetry.

### SPRINT-07

A rehearsed, customer-reviewed and instrumented `UT-01` design, with its Week 8 execution path scheduled, and `REL-07`; the stories carried from SPRINT-06 are shown to the Customer AC by AC for their verdicts.

- **Due:** 2026-11-15
- **Sprint Backlog:** [the issues scheduled into SPRINT-07](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/5)
- **Planned Velocity:** 24

The planned velocity was computed by hand as 2 + 3 + 3 + 5 + 5 + 3 + 3 from the `Story Points` of [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), [US-04](https://github.com/ITPD-Almo/modular-llm-gateway/issues/52), [US-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96), [US-11](https://github.com/ITPD-Almo/modular-llm-gateway/issues/110) and [US-12](https://github.com/ITPD-Almo/modular-llm-gateway/issues/111), carried from SPRINT-06 for their verdicts; tasks contribute zero points.
The sprint was planned on 2026-11-12, four days into the sprint and three days before its due date.
The tasks are [#128](https://github.com/ITPD-Almo/modular-llm-gateway/issues/128) for the versioned Compose image and the `UT-01` staging instrumentation, [#131](https://github.com/ITPD-Almo/modular-llm-gateway/issues/131) for the `UT-01` design, its `QR-09` requirement, the consent, the private repository and recordings folder, the recruitment, the dry run and the analysis plan, and [#130](https://github.com/ITPD-Almo/modular-llm-gateway/issues/130) for the planning, the Sprint Review, `REL-07` and the sprint close.
The counted sessions run in SPRINT-08, so MLS-07's outside-participant observation is completed by the SPRINT-08 sessions rather than by 2026-11-14.
The product backlog refined on 2026-11-12 for the next two sprints, with no milestone, is unchanged from SPRINT-06: [US-05](https://github.com/ITPD-Almo/modular-llm-gateway/issues/65) (8 points; #128 implements its Compose criterion), [US-06](https://github.com/ITPD-Almo/modular-llm-gateway/issues/66) (5), [US-07](https://github.com/ITPD-Almo/modular-llm-gateway/issues/67) (5), [US-08](https://github.com/ITPD-Almo/modular-llm-gateway/issues/68) (3), [US-10](https://github.com/ITPD-Almo/modular-llm-gateway/issues/97) (3) and [US-13](https://github.com/ITPD-Almo/modular-llm-gateway/issues/118) (5), 29 points.

#### REL-07

### SPRINT-08

Provisional: the in-person `UT-01` sessions run on staging, their results and findings are written and triaged, `QR-09 QRT-01` gets its verdict, and `REL-08` is cut.

- **Due:** 2026-11-21
- **Sprint Backlog:** [the issues scheduled into SPRINT-08](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/6)

The execution tasks are [#132](https://github.com/ITPD-Almo/modular-llm-gateway/issues/132) for the instrumentation verification before the first counted session, [#133](https://github.com/ITPD-Almo/modular-llm-gateway/issues/133) for the counted sessions, [#134](https://github.com/ITPD-Almo/modular-llm-gateway/issues/134) for the private custody and the sanitized notes, [#135](https://github.com/ITPD-Almo/modular-llm-gateway/issues/135) for the results and findings, [#136](https://github.com/ITPD-Almo/modular-llm-gateway/issues/136) for the triage, [#137](https://github.com/ITPD-Almo/modular-llm-gateway/issues/137) for the `QR-09 QRT-01` verdict and [#138](https://github.com/ITPD-Almo/modular-llm-gateway/issues/138) for `REL-08`.

#### REL-08

Planned: `REL-08` is cut on the reviewed green `main` commit at the end of SPRINT-08, and its `**Checked QRs:**` lists `QR-09` when the `QRT-01` verdict is recorded with the results.

### SPRINT-09

Provisional: the final release incorporates the selected usability findings, has reproducible evidence and a complete handover, and is frozen for the final demonstration.

- **Due:** 2026-11-28

#### REL-09

## Quality Requirement Testing Plan

| QR | QRT | Status | Checked | Planned for sprint | Evidence |
| --- | --- | --- | --- | --- | --- |
| [QR-02](quality-requirements/qr/QR-02.md) | [QR-02 QRT-01](quality-requirements/qr/QR-02.md#qrt-01) | Passes | [SPRINT-05](#sprint-05) | [SPRINT-05](#sprint-05) | [Campus staging run on 2026-10-31](https://github.com/ITPD-Almo/modular-llm-gateway/blob/c7dce8ff876d31a57ee0ca93d9428d8444473f6c/reports/week-05/deployment-evidence.md#deployed-qr-02-rerun-through-the-https-gate) |
| [QR-01](quality-requirements/qr/QR-01.md) | [QR-01 QRT-01](quality-requirements/qr/QR-01.md#qrt-01) | Passes | [SPRINT-06](#sprint-06) | [SPRINT-06](#sprint-06) | [REL-06 CI: 95 tests](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/42514546746) |
| [QR-08](quality-requirements/qr/QR-08.md) | [QR-08 QRT-01](quality-requirements/qr/QR-08.md#qrt-01) | Passes | [SPRINT-06](#sprint-06) | [SPRINT-06](#sprint-06) | [Campus staging run on 2026-11-08](https://github.com/ITPD-Almo/modular-llm-gateway/blob/0073150f73e3b755f0f8a29b21cddb1685b7731d/reports/week-06/README.md#qr-08-qrt-01-campus-run) and [release staging re-run](#rel-06) |

## Progress Monitoring

- **Review:** proposed weekly review, Wednesdays at 19:00 Europe/Moscow, before the weekly customer meeting, with the time still to be confirmed by the team; it reads [threshold-of-success.md](threshold-of-success.md), [risks.md](risks.md) and the [testing plan](#quality-requirement-testing-plan) rows that are not `Passes`, and settles what changed.
- **Checked by:** the `Accountable` member of each scheduled issue reports its state, and the team walks the sprint's GitHub milestone against the sprint's goal.
- **Visible at:** the [GitHub project's Sprint table](https://github.com/orgs/ITPD-Almo/projects/1/views/2), grouped by milestone, and the [sprints' GitHub milestones](https://github.com/ITPD-Almo/modular-llm-gateway/milestones).
- **Continuation:** the [development workflow](development-workflow.md) records the next-assignment intake, file ownership, review and demonstration routine; each new assignment replaces provisional detail at planning rather than rewriting earlier reports. The Customer asked for progress beyond one iteration and welcomed asynchronous clarification in [DEC-011](decisions.md#dec-011).
- **Threshold dates:** unchanged by any Customer decision: TOS-01 (due October 23) and TOS-04 (due October 30) were set to `Missed` in the Week 6 threshold review, and TOS-02 and TOS-03 remain due November 13. The Saturday release dates do not move these goal dates; actual outcomes or agreed changes are recorded in the threshold document.
