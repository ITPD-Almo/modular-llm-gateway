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
The new resilience outcome and its numerical targets are team proposals pending specification review and the Customer's verdict.
The [planning task](https://github.com/ITPD-Almo/modular-llm-gateway/issues/51) links the reviewable Week 4 delivery gates; issue fields and the milestone remain the source of assignments and schedule.

#### REL-04

### SPRINT-05

Provisional: an operator can use a shared gateway deployed from a tested, identifiable build and verify or recover that deployment without relying on a presenter's laptop.

- **Due:** 2026-10-31

#### REL-05

### SPRINT-06

Provisional: an operator can compare latency, errors and timeouts across a controlled run, then identify a failing plugin from safe events without retaining request or response bodies.

- **Due:** 2026-11-07

#### REL-06

### SPRINT-07

Provisional: the usability protocol is ready and has been rehearsed, and an outside participant can attempt setup and plugin authoring from the documentation with observable success measures.

- **Due:** 2026-11-14

#### REL-07

### SPRINT-08

Provisional: an operator can rebuild a tagged release with its recorded configuration and plugin versions and rehearse a controlled upgrade and rollback.

- **Due:** 2026-11-21

#### REL-08

### SPRINT-09

Provisional: the final release incorporates the selected usability findings, has reproducible evidence and a complete handover, and is frozen for the final demonstration.

- **Due:** 2026-11-28

#### REL-09

## Progress Monitoring

- **Review:** proposed weekly review, Wednesdays at 19:00 Europe/Moscow, before the weekly customer meeting, with the time still to be confirmed by the team; it reads [threshold-of-success.md](threshold-of-success.md) and [risks.md](risks.md) and settles what changed.
- **Checked by:** the `Accountable` member of each scheduled issue reports its state, and the team walks the sprint's GitHub milestone against the sprint's goal.
- **Visible at:** the [GitHub project's Sprint table](https://github.com/orgs/ITPD-Almo/projects/1/views/2), grouped by milestone, and the [sprints' GitHub milestones](https://github.com/ITPD-Almo/modular-llm-gateway/milestones).
- **Continuation:** the [development workflow](development-workflow.md) records the next-assignment intake, file ownership, review and demonstration routine; each new assignment replaces provisional detail at planning rather than rewriting earlier reports. The Customer asked for progress beyond one iteration and welcomed asynchronous clarification in [DEC-011](decisions.md#dec-011).
- **Threshold dates:** unchanged by this replan: TOS-01 remains due October 23, TOS-04 October 30, and TOS-02 and TOS-03 November 13. The Saturday release dates do not move these goal dates; actual outcomes or agreed changes are recorded in the threshold document.
