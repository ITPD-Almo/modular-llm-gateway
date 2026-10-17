# Risks

| ID                  | Status | Impact | Likelihood | Risk                                                                                                                                                                                     |
| ------------------- | ------ | ------ | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [RISK-01](#risk-01) | Open   | High   | Medium     | The candidate was not shown running at the Week 3 meeting, so the Customer's verdict on the stories may not arrive before the release, which would leave the MUP unaccepted.             |
| [RISK-02](#risk-02) | Open   | High   | Medium     | The plugin interface was designed before the Customer saw it run, so the Customer may reject its inputs or outputs, which would force us to rewrite the plugins and their documentation. |
| [RISK-03](#risk-03) | Open   | High   | Low        | The team already lost one of four members, so another member may become unavailable for a sprint, which would leave that sprint's release unfinished.                                    |
| [RISK-04](#risk-04) | Open   | Medium | Medium     | The gateway's deployment target and pipeline are untested, so deploying it may take longer than one sprint, which would miss TOS-04 in Week 5.                                           |

## RISK-01

The candidate was not shown running at the Week 3 meeting, so the Customer's verdict on the stories may not arrive before the release, which would leave the MUP unaccepted.

- **Status:** Open
- **Impact:** High
  - Without a verdict, no candidate story can close, and [TOS-01](threshold-of-success.md#tos-01) has no evidence.
- **Likelihood:** Medium
  - The Week 3 meeting has passed, and the next joint meeting gives our team about ten minutes.
- **Trigger:** the gateway is merged into `main` and the Customer has not answered the written demo within one day.
- **Window:** [SPRINT-03](project-plan.md#sprint-03) and [SPRINT-04](project-plan.md#sprint-04), up to the Week 4 meeting.
- **Mitigation:** send the Customer a written demo against each story's acceptance criteria as soon as the gateway merges, and keep the written exchange as the transcript.
- **Contingency:** show the stories, one acceptance criterion at a time, as the first item of the Week 4 meeting, and leave them open in the meantime.

## RISK-02

The plugin interface was designed before the Customer saw it run, so the Customer may reject its inputs or outputs, which would force us to rewrite the plugins and their documentation.

- **Status:** Open
- **Impact:** High
  - The interface is the centre of the product, per [CON-01](product-vision.md#con-01), and a rewrite would take the sprint planned for failure handling.
- **Likelihood:** Medium
  - The Customer has asked for the interface, per [DEC-006](decisions.md#dec-006), but has not yet seen one.
- **Trigger:** the Customer rejects an acceptance criterion of the plugin story, or asks for a different plugin input or output.
- **Window:** [SPRINT-04](project-plan.md#sprint-04).
- **Mitigation:** keep the interface small, one request in and one request out, and ask the Customer about it before building more plugins on it.
- **Contingency:** keep the two example plugins on the old interface behind an adapter, and move the rewrite into SPRINT-04 in place of the failure-handling work.

## RISK-03

The team already lost one of four members, so another member may become unavailable for a sprint, which would leave that sprint's release unfinished.

- **Status:** Open
- **Impact:** High
  - Each member owns one third of a sprint, so one absence removes a whole part of the week's work.
- **Likelihood:** Low
  - The three remaining members have each delivered in every week so far.
- **Trigger:** a scheduled issue has no commit or comment from its `Responsible` member two days before the sprint's due date.
- **Window:** any sprint, [SPRINT-03](project-plan.md#sprint-03) to [SPRINT-09](project-plan.md#sprint-09).
- **Mitigation:** every issue names an `Accountable` member who knows the work well enough to finish it.
- **Contingency:** the `Accountable` member takes the issue over, and the sprint's lowest-priority issue moves to the next sprint.

## RISK-04

The gateway's deployment target and pipeline are untested, so deploying it may take longer than one sprint, which would miss TOS-04 in Week 5.

- **Status:** Open
- **Impact:** Medium
  - [TOS-04](threshold-of-success.md#tos-04) would slip, but the gateway itself would still run locally.
- **Likelihood:** Medium
  - No deployment target is chosen for this gateway yet, and no pipeline has deployed it, so the first attempt falls in the same sprint as the deadline.
- **Trigger:** the gateway does not answer a request in the deployment target by Tuesday of Week 5, 2026-10-27.
- **Window:** [SPRINT-05](project-plan.md#sprint-05).
- **Mitigation:** package the gateway as a container image in SPRINT-04, so the Week 5 work is only to run that image.
- **Contingency:** deploy the container by hand to one virtual machine, and automate the deployment in SPRINT-06.
