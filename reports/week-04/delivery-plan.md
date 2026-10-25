# Week 4 delivery plan

This is the October 25 remaining-work plan, prepared after the October 23 Customer meeting.
The owner confirmed that all three current contributors are available and that Assignment 4 is extended to **October 25, 23:59 Europe/Moscow**.
It replaces the earlier deadline assumption; it does not backdate sprint planning, estimates or meeting preparation.
The [project plan](../../docs/project-plan.md#sprint-04) owns the goal and velocity baseline, and the [Sprint table](https://github.com/orgs/ITPD-Almo/projects/1/views/2) owns live issue assignments and state.

## Starting point and intended increment

The starting main commit is `6bd7eef96916a938bfb6e1bf11e50600426fccfd`, with published `v0.1.0`.
It contains configured request/response hooks, two example plugins, a fake provider, setup instructions, tests and the documentation site.
The carried stories have not received individual Customer acceptance.
The October 23 demonstration encountered installation problems and did not establish acceptance of every criterion.

The intended increment lets another operator install the gateway, add a plugin through documented configuration, identify a bad or slow hook and complete a later healthy request.
The quality and functional requirements, container design and ADRs must explain that behavior and its tradeoffs.
Existing raised-exception handling does not by itself provide an execution deadline or terminate a hung plugin.

Use a minimal team-proposed timeout/failure policy that is explicit and testable.
The proposed default fails the affected request rather than silently bypassing transformations; the Customer's requested resilience does not settle every fail-versus-skip case.
Numerical values in the new story are proposed verification targets, to be reconciled with the accepted QR and ADR.
Keep this question visible for genuine Customer validation.

## Parallel work and handoffs

Ali12hamdan implements core timeout/recovery and safe lifecycle diagnostics and coordinates Customer evidence, the tracker/forms and final report/submission preparation.
Mohammed-Nour leads requirements and glossary, setup/plugin guidance, the matched existing-tool comparison, and collection of retrospective/AI-use input.
atkond2point0 leads architecture/ADRs, contributor guidance/navigation and release mechanics and independently reviews Ali's coding work.
The [development workflow](../../docs/development-workflow.md#stewardship-and-review) names backup/review stewardship and file boundaries.
Each scheduled task's actual Responsible and Accountable fields remain authoritative; a different member verifies every task.

Start meeting evidence, specifications, the architecture draft, the comparison and repository guidance in parallel.
The requirements and architecture owners agree container names and the proposed failure policy early.
Merge specification and design records before implementation approval and before the one coordinated issue migration adds their main links.
The setup guide can be improved immediately, but its final timeout demonstration follows the implemented behavior.
The evidence owner owns the decision log; research and design owners hand over proposed decision text instead of editing it concurrently.

## Coverage and dependencies

The work packages are GitHub tasks with observable checkbox criteria, full main links where records exist, explicit dependencies, ownership fields and handoff times.
The table maps assignment coverage to those tasks; it is not a completion checklist or a second backlog.

| Assignment coverage | GitHub work package |
| --- | --- |
| Part 1: sprint goal, dates and late baseline; next-two-sprint refinement and fields | [Plan](https://github.com/ITPD-Almo/modular-llm-gateway/issues/51), [tracker/refinement](https://github.com/ITPD-Almo/modular-llm-gateway/issues/59) |
| Parts 2 and 4: quality/functional records and indexes; Part 8 glossary | [Requirements](https://github.com/ITPD-Almo/modular-llm-gateway/issues/54) |
| Parts 3, 5 and 6: container image/source, responsibilities, drivers and accepted ADRs | [Architecture](https://github.com/ITPD-Almo/modular-llm-gateway/issues/55) |
| Part 7: coordinated historical-issue migration after the specifications exist | [Tracker and forms](https://github.com/ITPD-Almo/modular-llm-gateway/issues/59) |
| Part 8 contributor instructions and report/site discoverability | [Repository guidance](https://github.com/ITPD-Almo/modular-llm-gateway/issues/60) |
| Parts 9 and 10: previous outcomes, genuine decisions and validation | [Meeting evidence](https://github.com/ITPD-Almo/modular-llm-gateway/issues/53), [matched comparison](https://github.com/ITPD-Almo/modular-llm-gateway/issues/58) |
| Working increment and criterion-based demo for current and future meetings | [Safe lifecycle diagnostics](https://github.com/ITPD-Almo/modular-llm-gateway/issues/70), [runtime resilience](https://github.com/ITPD-Almo/modular-llm-gateway/issues/56), [setup and demo](https://github.com/ITPD-Almo/modular-llm-gateway/issues/57) |
| Part 11: REL-04 and the release/changelog/plan sequence | [Release and changelog](https://github.com/ITPD-Almo/modular-llm-gateway/issues/62), [sprint close and release line](https://github.com/ITPD-Almo/modular-llm-gateway/issues/63) |
| Parts 12 and 13: retrospective and actual AI-use records | [Retrospective and AI usage](https://github.com/ITPD-Almo/modular-llm-gateway/issues/61) |
| Public report, private PDF and matching final-main snapshot preparation | [Report and submission](https://github.com/ITPD-Almo/modular-llm-gateway/issues/64) |

The planning issues use the authenticated API with the required form sections; the original batch was prepared while the browser initially showed sign-in, and the later diagnostics task reused that publishing workflow.
This remains a creation-method deviation from opening through the issue-form UI; the final report records it once, and new issues should use the form UI where available.
Field creation does not prove pinning: the tracker task verifies type pins, visibility and the full one-time migration.
Pending specification links in planned issues are explicit dependencies, not claims of finished refinement; replace them with resolving main links before implementation approval or declaring readiness.
Five functional requirements is the assignment minimum, rather than a limit: the specification owner must cover every active non-Won't Have story, including the future candidates, before the coordinated migration can claim their links complete.

## Customer alignment

The October 23 discussion requests an understandable plugin-management system, installation/run documentation, a documented way to add a plugin, useful diagnostics, and resilience to badly written or slow hooks.
The live extension example replaces incoming text with A characters and replaces the provider's response with B characters; a plugin returning A text on both paths does not demonstrate that example.
The Customer prioritizes the management system over a fixed count of example plugins, and wants another DevOps operator to be able to maintain it.
Automatic discovery and hot reload were not required by the discussion; exact timeouts and the fail-versus-skip policy remain team proposals for validation.
The transcript contains no individual acceptance verdicts on the carried stories and no approval of a complete A4 requirements/architecture set.
The meeting report must preserve that distinction while reporting every Week 3 action/question outcome and assigning at least two concrete Week 5 follow-ups.

## Assignment acceptance checks

The final report links the actual artifacts and evidence; this plan's coverage mapping does not itself complete a deliverable.
Before declaring A4 complete, verify the [pinned assignment checklist](https://github.com/inno-itpd/itpd/blob/35c9294415d31c81a8598042b8b7419ea4481a46/assignments/assignment-4.md#checklist) against main.
In particular, check the distinct quality characteristics and scenario headings, exact requirement/index fields, three Accepted ADRs and their quality tradeoffs, image plus editable source, and the complete historical issue migration.
The matrix must prioritize rather than rate everything High; the testability requirement names real critical gateway modules because the detailed rule uses frontend/payment paths only as examples.
Use real runtime containers; the detailed rule explicitly permits a genuinely single-container product with an explanation, so code modules or the in-process fake provider are not invented deployments.
Resolve the next two sprints' specification gaps before claiming full refinement, and keep those candidates without milestones, role values or assignees until selected at planning.
The original pre-meeting script, original sprint-start estimates and missing Customer verdicts cannot be reconstructed as earlier evidence; the actual gaps and late replanning are declared.

## Tonight's gates

All times below are Europe/Moscow on October 25 and are target handoffs, not past accomplishments.
Owners report a missed gate immediately through the task/PR handoff so integration can be replanned.

| Target | Gate and observable exit |
| --- | --- |
| 17:30 | Plan and live assignments are reviewable; everyone has a first task, a reviewer and the file boundary. |
| 18:45 | Requirements and meeting-account drafts are reviewable; design uses agreed container names and a written failure-policy proposal. |
| 19:30 | Requirements/architecture reviews settle executable criteria and ADRs; the comparison supplies an actual result or an explicit evidence gap. |
| 20:15 | Runtime change is ready for independent error/timeout/recovery checks; ordinary-path regression behavior is preserved. |
| 20:45 | The clean setup/plugin demo, tracker migration and new-documentation navigation are ready for integration. |
| 21:00 | Rehearse the integrated build; Ali has a criterion-by-criterion Customer follow-up and asks for actual verdicts and unresolved permission/policy answers. |
| 21:30 | Freeze intended product scope after review/rework; finalize retrospective and each member's actual AI-use input. |
| 22:00–22:15 | Green main and a clean demo permit the protected new tag/release, then the versioned changelog PR. |
| 22:30 | Merge the REL-04 plan line and honest actual velocity/carry-forward record after the changelog. |
| 22:50 | Merge the final public report after all linked artifacts and the release line; current main checks/site are green. |
| 23:15 | Generate and verify the private PDF and repository ZIP from exactly that final main SHA; open the report permalink and verify recording accessibility where available. |
| 23:45 | Ali uploads once for the team and checks the resulting submission, preserving a short buffer before 23:59. |

The plan is capacity-sensitive: a missed runtime gate does not permit a false acceptance or a broken release.
Report the actual shipped behavior and replan unfinished work at the checkpoint, using the maintained risk response rather than hiding it.
The published requirements and architecture can specify a target while the report explicitly states which behavior remains unimplemented.
Do not drop required A4 artifacts silently to protect an optional upgrade.

## Working-version check

Use an isolated clean checkout/configuration rather than the local private `AlwaysAAAPlugin` experiment.
The demonstrator must run the actual commands on the environment they will present from, with a second member able to repeat them.

1. Start with a Python 3.12 virtual environment and the documented install/configuration steps; run the baseline tests.
2. Send a synthetic request through the two configured plugins and fake provider; identify the result and plugin order.
3. Change the list/order, restart as documented and show the new behavior.
4. Add an A-input/B-output plugin against the documented contract without editing gateway core; show the configuration and output.
5. Run a deliberately failing hook and a slow request hook and response hook; show the documented result, safe diagnostics, health and a later healthy request.
6. Repeat the timeout exercise to show bounded resource use, then reset to the normal configuration.
7. Record technical results per criterion and ask for individual Customer verdicts separately.

For the next weekly Customer meeting, use the October 27–29 preparation targets in the [continuation workflow](../../docs/development-workflow.md#demonstration-readiness).
The demo is about an operable and maintainable system, with concrete evidence of what it adds beyond manual function calls.

## Release and submission controls

The existing `v0.1.0` tag is preserved.
Choose the next SemVer version from the delivered change after integration, rather than publishing a guessed version in this plan.
Do not move or delete a protected tag.

Merge the implementation and supporting records, finish genuine review/rework, and verify main.
Then publish the tag/release, merge the dated changelog, merge the plan's REL-04 line, and merge the weekly report in that order.
Reviewers tick only criteria they have checked and approve only other members' work.
Stories close only after the actual Customer acceptance decision; task merges alone do not close stories.

At sprint close, calculate Actual Velocity manually from completed/accepted stories and relocate unfinished product work deliberately.
Only ready, estimated work selected at planning enters SPRINT-05; unresolved candidates stay in the product backlog with no milestone, role values or assignees.
Refined future candidates are not all scheduled automatically.
Leave the release-line and final-report tasks in SPRINT-04 until their PRs merge; close the milestone only after the final report merge and after verifying that no open issue remains in it.
This cleanup follows the report merge, so it cannot block the report on a milestone that contains its own task.

The private PDF and ZIP must refer to one final main revision after the report and every linked file have merged.
Use real contributor details and an instructor-accessible recording link only in the private submission; keep exact recording timecodes and raw transcripts out of public planning records.
If a required permission, recording link, preparation record or Customer verdict is still missing, declare the actual gap instead of substituting a fabricated statement.
Do not generate another cosmetic commit after building the matching artifacts.

## Continuing backlog

The [product backlog](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=is%3Aissue%20is%3Aopen%20no%3Amilestone) carries proposed deployment/recovery and operational-observability stories for the next two sprints.
They have candidate scope, runnable checks, value priorities and relative estimates, and remain unscheduled.
Their pending specifications and future assignment changes must be resolved before calling them fully refined or selecting them at planning.
Longer-term usability, configuration/rebuild and final-handover goals live in the [project plan](../../docs/project-plan.md), with the [weekly intake routine](../../docs/development-workflow.md#weekly-continuation) keeping them current.
