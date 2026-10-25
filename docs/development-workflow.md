# Development workflow

The [project plan](project-plan.md) owns sprint goals, dates and releases; the [public project](https://github.com/orgs/ITPD-Almo/projects/1/views/2) shows the live backlog, assignments and progress.
This workflow explains how a member resumes work and how the team prepares a working increment for the next Customer meeting.
It adds no second story registry or task-status list.

## Product direction

Prioritize a plugin system that another DevOps operator can install, extend, debug and maintain.
The starting product is a Python FastAPI gateway with configured request/response hooks and a deterministic fake provider.
The immediate gap is bounded execution and recovery when a plugin is slow or broken, alongside reproducible setup and a concrete extension example.
The exact failure policy and measured targets are specified and reviewed before implementation is accepted; a proposed design is not a Customer verdict.

An automatic plugin discovery system, hot reload, a web administration interface, multiple real providers and additional example plugins are candidate upgrades, not prerequisites for every release.
Add one only when a Customer need, evidence and a small story justify it.
Use an existing gateway if the matched extension exercise shows it delivers the intended workflow with less work.

## Stewardship and review

Stewardship gives each member a place to start and a backup; it does not replace the two role values on a scheduled issue.
The owner updated the October 25 execution capacity to two active A4 contributors, Ali12hamdan and Mohammed-Nour.
This allocation applies to A4; future sprint capacity is confirmed at its planning.

| Member | Main stewardship | Independent review and backup |
| --- | --- | --- |
| Ali12hamdan | Core timeout/recovery and diagnostics code, architecture/ADRs, Customer evidence, tracker/admin work, release and submission | Verify Mohammed's requirements, developer guide, contributor guidance, comparison, retrospective and sprint-close record |
| Mohammed-Nour | Functional/quality requirements, glossary, setup/plugin guide, contributor guidance/navigation, matched comparison, retrospective and sprint-close record | Verify Ali's planning, architecture, runtime/diagnostic code, tracker changes, release and final report |

`Responsible` implements a scheduled issue; `Accountable` is a different member who verifies it and reviews the PR.
The two assignees exactly match those values.
An unscheduled product-backlog item has no milestone, role values or assignees; it may have a value priority and estimate from refinement.
Do not assign the entire future backlog to a sprint just to show ownership.

## Resume an issue

1. Read the root contributor instructions when present, the issue, its dependencies and the current published assignment through the [course router](https://github.com/inno-itpd/itpd/blob/main/SKILL.md).
2. Fetch `main` and inspect local changes before switching branches; preserve another member's work and local experiments.
3. Check that the task's story and requirement links resolve on `main`, its acceptance criteria are runnable, and its roles and milestone are set.
   Resolve a pending specification dependency before approving implementation.
4. Create the task branch as `<issue-number>-<short-description>` from current `main`; one PR closes exactly that task.
   A story is never the PR's closing issue.
5. Keep edits inside the agreed file scope, implement the observable criteria and collect synthetic evidence.
6. Describe the final behavior, decisions, checks and remaining limitations in the PR; update the Unreleased changelog for a user-visible change.
7. Request the Accountable member's review.
   The reviewer reproduces the important checks, ticks verified task criteria, and merges only after required CI and independent approval.

Keep files with one active editor during an integration window.
Ali12hamdan edits the architecture tree and its vision link and implements the gateway timeout and diagnostics code and tests; Mohammed-Nour edits the requirement trees, glossary, developer guide and contributor guidance/navigation.
Ali is Responsible for the coding tasks and Mohammed is Accountable for their independent verification; both appear as assignees because those roles are different.
The guide owner edits setup/plugin instructions and the synthetic demo recipe; the evidence owner edits the decision log and meeting account.
Coordinate changes to `docs/project-plan.md`, `CHANGELOG.md`, navigation and shared templates before rebasing or merging another branch.
Never force-push a teammate's branch or bypass protection to settle a deadline.

## Weekly continuation

The detailed Assignment 5 and later assignment files were not published when this plan was written on October 25.
The roadmap follows the [published syllabus](https://github.com/inno-itpd/itpd/blob/35c9294415d31c81a8598042b8b7419ea4481a46/course/syllabus.md); future deliverable details remain provisional until their assignment is read.

| Sprint | Product increment to prepare | Evidence to obtain before the weekly release |
| --- | --- | --- |
| 05, due October 31 | Shared deployment, repeatable test environment and verified recovery | Identified build, deployment/smoke results, setup handover and the syllabus's short pitch preparation |
| 06, due November 7 | Useful aggregate metrics and safe plugin lifecycle events | A controlled normal/slow/error workload, explainable counts and latency, and proof that fixture secrets do not leak |
| 07, due November 14 | Usability protocol and independent setup/plugin-authoring exercise | Runnable tasks, success/failure measures and rehearsal; participant identities and consent stay private |
| 08, due November 21 | Rebuildable configuration and plugin/dependency versions | Tagged reproduction, compatibility checks and a rehearsed upgrade/rollback |
| 09, due November 28 | Findings-driven fixes and final handover | Final validated scenarios, repository freeze, presentation and reflection evidence required by the published assignment |

After REL-09, use the review week to rehearse the final demonstration and architectural explanation.
The syllabus places the group final presentation on December 4 and the individual reflection on December 10; each member keeps their own contribution evidence.
No extra sprint or promised release is invented for those weeks.

At each weekly planning:

1. Read the new assignment and its linked rules; compare them with this provisional roadmap and adjust the plan through a reviewed task.
2. Review prior action points, open Customer questions, retrospective actions, the current threshold and risks.
3. Refine the next two sprints' worth of stories while leaving them unscheduled; split anything over 13 points.
   Complete or update specifications before claiming a candidate is ready.
4. Select only what the team can finish, set roles/assignees/milestone and task priorities, and manually sum selected story points into Planned Velocity before the new work starts.
5. Reserve independent review and integration time, assign a demonstrator and backup, and establish a small observable release goal.
6. At close, record Actual Velocity and carry-forward destinations honestly, publish the release, complete the retrospective and prepare the final submission from one main revision.

If the five-point resilience story carries into SPRINT-05, prioritize it before further deployment expansion.
Select the next work within capacity and leave the rest unscheduled; do not count all refined candidates as a commitment.

The October 25 estimates are an explicit late replanning baseline.
They must not become invented evidence that Week 4 was estimated at its original start.
Use actual accepted work and measured capacity to improve later planning; a story-point estimate is not a number of hours.

## Demonstration readiness

Prepare the next weekly Customer demonstration by October 29, with the existing meeting arrangement confirmed separately.
The readiness date is a team target, not a claim that a new appointment has been booked.

- By October 27, resolve remaining failure-policy questions and any runtime carry-forward that prevented the October 25 resilience increment.
- By October 28, the shared deployment candidate or a clean local release is runnable by a second member, with no presenter-specific configuration.
- By October 29, rehearse on the machine/environment that will be used, capture expected synthetic outputs, and test the reset/recovery steps.
- Before the meeting, prepare the script, roles, permission questions and a short mapping from each story's criteria to the demonstration.

The core demonstration follows one request through configured plugins, changes their order, adds an A-input/B-output example without core edits, and shows a slow or broken hook followed by a healthy request.
Identify the running version and explain what the gateway supplies beyond a manual list of functions.
Bring the relevant measurable quality requirement and ADR to explain the timeout and failure policy.
Ask for a verdict on each story one criterion at a time; record the actual decision before closing it.

The demonstrator handles the live run, a second member can take over, and the evidence owner records decisions and actions.
Use Customer-approved asynchronous review when needed; Ali prepares/sends the actual request, and no response is inferred from silence.
A prerecorded clip or saved output can explain a failure during a meeting, but does not replace the Customer's actual verdict.

## End-of-session handoff

Leave a short handoff in the task or PR describing the current branch/head, files changed, checks and results, unresolved decisions, dependency PRs, and the exact next action.
Keep public handoffs free of recording links, exact recording timecodes, credentials, raw prompts and personal details.
Recordings, private submission inputs and any unpublishable transcript remain outside the repository.
Each member supplies their own AI-use statement and contribution evidence; no teammate statement is generated as testimony.

Keep the issue's current body and fields accurate.
Keep historical meeting reports and retrospectives as records; later outcomes belong in the later report and maintained artifacts.
When a task is technically complete but awaits review or Customer acceptance, say exactly which gate remains.
