# Risks

|ID|Status|Impact|Likelihood|Risk|
|---|---|---|---|---|
|[RISK-01](#risk-01)|Open|High|Medium|The candidate was not shown running at the Week 3 meeting, so the Customer's verdict on the stories may not arrive before the release, which would leave the MUP unaccepted.|
|[RISK-02](#risk-02)|Open|High|Medium|The plugin interface was designed before the Customer saw it run, so the Customer may reject its inputs or outputs, which would force us to rewrite the plugins and their documentation.|
|[RISK-03](#risk-03)|Open|High|Low|The team already lost one of four members, so another member may become unavailable for a sprint, which would leave that sprint's release unfinished.|
|[RISK-04](#risk-04)|Open|Medium|Medium|The gateway's deployment target and pipeline are untested, so deploying it may take longer than one sprint, which would miss TOS-04 in Week 5.|
|[RISK-05](#risk-05)|Open|High|Medium|The team may recruit too few eligible participants or a session may not be valid, leaving the QR-09 denominator below the required three.|
|[RISK-06](#risk-06)|Open|High|Medium|A participant may not understand the recording, sanitized-results or private-access terms, invalidating the session.|
|[RISK-07](#risk-07)|Open|High|Low|Raw notes, recordings or telemetry may be inaccessible to instructors or may expose identity.|
|[RISK-08](#risk-08)|Open|High|Medium|The staging bring-up or event link may fail during a counted session, confounding usability with instrumentation failure.|
|[RISK-09](#risk-09)|Open|Medium|Medium|Recruiting and arranging in-person campus sessions may slip beyond the SPRINT-08 analysis window.|

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

## RISK-05

Recruitment may produce fewer than three eligible, valid sessions.

- **Status:** Open
- **Impact:** High
- **Likelihood:** Medium
- **Mitigation:** recruit five people against the observable UT-01 profile and pre-screen eligibility without collecting identity in the public record.
- **Contingency:** schedule replacements under the next unused participant code and do not claim a QR-09 result until three valid sessions exist.

## RISK-06

A participant may not understand or accept the recording, sanitized-results or private-access terms.

- **Status:** Open
- **Impact:** High
- **Likelihood:** Medium
- **Mitigation:** read the consent summary, answer questions before recording and obtain durable consent before every counted session.
- **Contingency:** stop and exclude the session; offer a fresh session only after consent is complete.

## RISK-07

Private raw notes, recordings or telemetry may be inaccessible to instructors or expose identity.

- **Status:** Open
- **Impact:** High
- **Likelihood:** Low
- **Mitigation:** keep text in the private usability-data repository and recordings in the team-owned folder, test instructor access before sessions, and publish only sanitized evidence.
- **Contingency:** preserve a private Moodle archive and record the access deviation before submission.

## RISK-08

The staging bring-up or event link may fail during a counted session.

- **Status:** Open
- **Impact:** High
- **Likelihood:** Medium
- **Mitigation:** reset the seed, use the reviewed image and verify the named events, source and session link in a teammate run before the first counted session.
- **Contingency:** stop the technical run, mark it invalid rather than failed usability evidence, repair instrumentation and reschedule.

## RISK-09

Recruiting and arranging in-person campus sessions may slip beyond the SPRINT-08 analysis window.

- **Status:** Open
- **Impact:** Medium
- **Likelihood:** Medium
- **Mitigation:** arrange sessions in a shared schedule immediately after design approval and hold multiple campus slots.
- **Contingency:** move the run and analysis to the next planned sprint and declare the schedule deviation.
