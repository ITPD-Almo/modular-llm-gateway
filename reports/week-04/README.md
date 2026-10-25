# Week 04 report

## Project

Modular LLM Gateway, team 9, Assignment 4: quality, requirements, architecture and REL-04.

## Summary

**Review draft: release and submission gates remain open.** This report must be finalized and merged after the released changelog and the plan's real REL-04 line; it is not a completed submission.

The team specified the plugin workflow, wrote the quality scenarios and architecture, and compared the same two-plugin interaction with LiteLLM.
The Customer emphasized a plugin-management system another developer/DevOps operator can understand and support, a concrete A-input/B-output example, identifiable failing or sleeping plugins, and progress against a multiweek plan.
The October 23 setup attempt did not establish a complete working demonstration or individual story verdicts; the source-based account is in [reports/week-04/meeting-report.md](meeting-report.md).

The supervised runtime and developer demo are integrated into main through independently reviewed [PR #81](https://github.com/ITPD-Almo/modular-llm-gateway/pull/81), with 40 passing tests and an independent clean-environment replay, including a named timeout in 0.303 seconds followed by healthy requests.
The default four-worker limit deliberately rejects excess concurrent healthy requests with 503, and instances reset between requests; the accepted architecture records those costs.
These are technical results and team design choices, not Customer acceptance.

REL-04 is published as [v0.2.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.2.0) from verified main commit `960616128ca88159a003aa772dd198c4c0f515ea`; the exact-commit clean replay passed 40 tests and timed out the slow hook in 0.297 seconds with subsequent recovery.
The dated changelog in [PR #86](https://github.com/ITPD-Almo/modular-llm-gateway/pull/86) and the following [#63 release-plan line](https://github.com/ITPD-Almo/modular-llm-gateway/issues/63) still need to merge before this report.
Future deployment/recovery and metrics remain refined, estimated and unscheduled product targets; their contracts merged in [PR #83](https://github.com/ITPD-Almo/modular-llm-gateway/pull/83) and their issue links/criteria were finalized in [PR #79](https://github.com/ITPD-Almo/modular-llm-gateway/pull/79). No future capability is claimed implemented.

## Minimum usable product and Customer outcome

The candidate remains [US-01/#40](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02/#41](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41) and [US-03/#42](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42): configure plugins, write one against the interface and see the request/response effects.
The selected sprint also adds [US-04/#52](https://github.com/ITPD-Almo/modular-llm-gateway/issues/52), keeping the gateway usable after a stuck hook.

| Story | October 23 evidence | Customer verdict |
| --- | --- | --- |
| US-01 | Local installation/startup was attempted; setup and sharing problems limited the demonstration. | No individual acceptance or rejection recorded; no verdict DEC exists. |
| US-02 | Configuration and plugin code were discussed; the later complete A/B recipe is technical rework. | No individual acceptance or rejection recorded; no verdict DEC exists. |
| US-03 | The intended curl/plugin-effects interaction was discussed but no complete AC-by-AC review was established. | No individual acceptance or rejection recorded; no verdict DEC exists. |
| US-04 | The reviewed timeout/recovery implementation was prepared after the meeting. | Not shown as a completed story at that meeting; no verdict DEC exists. |

No later Customer acceptance or rejection has been confirmed.
A planning assumption of acceptance does not supply a verdict, close a story or add accepted velocity.
No story was removed from the original candidate. All four current stories, totaling 13 points, have moved to SPRINT-05 for criterion-by-criterion Customer verdicts; Actual Velocity is 0 because none was accepted.
The [meeting account](meeting-report.md) records scope clarifications separately from those missing verdicts.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan and estimates | [docs/project-plan.md#sprint-04](../../docs/project-plan.md#sprint-04); late planned baseline 13 and Actual Velocity 0; #63 rechecks the close record when adding REL-04. |
| Product backlog refinement | [Sprint table grouped by milestone](https://github.com/orgs/ITPD-Almo/projects/1/views/2), no-milestone group; the four future stories carry estimates 8/5/5/3, runnable criteria and main FR/ADR links, with no milestone, role values or assignees. |
| Issue catch-up | [User Story issues](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=is%3Aissue%20type%3A%22User%20Story%22) and [Task issues](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=is%3Aissue%20type%3ATask); the coordinated migration merged in #79, closing #59; all 42 issues are typed and the six legacy labels are retired. |
| Quality requirements | [docs/quality-requirements/qr/](../../docs/quality-requirements/qr/) and [docs/quality-requirements/README.md](../../docs/quality-requirements/README.md); seven scenarios include the future recovery/resource targets without claiming they are implemented. |
| Functional requirements | [docs/functional-requirements/README.md](../../docs/functional-requirements/README.md) and [docs/functional-requirements/fr/](../../docs/functional-requirements/fr/). |
| Container view | [docs/architecture/README.md#container-view](../../docs/architecture/README.md#container-view), [docs/architecture/container.png](../../docs/architecture/container.png), [docs/architecture/container.svg](../../docs/architecture/container.svg) and [docs/architecture/README.md#container-responsibilities](../../docs/architecture/README.md#container-responsibilities). |
| Architecture and drivers | [docs/architecture/README.md](../../docs/architecture/README.md). |
| Architectural decisions | [docs/architecture/adr/](../../docs/architecture/adr/) and [docs/architecture/README.md#architectural-decisions](../../docs/architecture/README.md#architectural-decisions). |
| Glossary | [docs/glossary.md](../../docs/glossary.md). |
| Team AGENTS.md | [AGENTS.md](../../AGENTS.md), merged through independently reviewed PR #78, closing #60. |
| Issue fields in the project view | [Sprint table](https://github.com/orgs/ITPD-Almo/projects/1/views/2): Responsible, Accountable, MoSCoW, Story Points, Priority, Assignees, Milestone and Status. |
| Documentation site | [Published documentation](https://itpd-almo.github.io/modular-llm-gateway/): the QR/FR/architecture/glossary/operating links and post-#78 deployment were verified; #64 repeats the final check after all remaining integrations. |
| Week 3 action points | [reports/week-04/meeting-report.md#previous-action-points](meeting-report.md#previous-action-points). |
| Week 3 open questions | [reports/week-04/meeting-report.md#previous-open-questions](meeting-report.md#previous-open-questions). |
| Meeting script | [reports/week-04/meeting-script.md](meeting-script.md), with separately dated future preparation in [reports/week-04/meeting-script-2.md](meeting-script-2.md). |
| Customer validation | [reports/week-04/meeting-report.md](meeting-report.md) and permitted public [reports/week-04/meeting-transcript.md](meeting-transcript.md); individual story verdicts remain unreceived. |
| REL-04 | Published [v0.2.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.2.0); the dated [CHANGELOG.md](../../CHANGELOG.md) update is in #86, followed by the [docs/project-plan.md#rel-04](../../docs/project-plan.md#rel-04) update under #63. |
| Sprint retrospective | [reports/week-04/sprint-retrospective.md](sprint-retrospective.md), written with Actual Velocity set and reviewed in #85, closing #61. |
| AI usage | [reports/week-04/ai-usage.md](ai-usage.md); contributor statements and agent-run/personal checks are distinguished, and the missing third-member statement is explicit. |
| Reproducible developer demo | [docs/demo.md](../../docs/demo.md), [docs/setup.md](../../docs/setup.md), [docs/plugins.md](../../docs/plugins.md), [docs/operations.md](../../docs/operations.md) and [reports/week-04/gateway-check.md](gateway-check.md). |

## Contribution

| Member | Evidenced work |
| --- | --- |
| Ali12hamdan | [Planning #69](https://github.com/ITPD-Almo/modular-llm-gateway/pull/69), [diagnostics #71](https://github.com/ITPD-Almo/modular-llm-gateway/pull/71), [runtime #72](https://github.com/ITPD-Almo/modular-llm-gateway/pull/72), [architecture #77](https://github.com/ITPD-Almo/modular-llm-gateway/pull/77), [integration #81](https://github.com/ITPD-Almo/modular-llm-gateway/pull/81), [tracker #79](https://github.com/ITPD-Almo/modular-llm-gateway/pull/79), [meeting account #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80), [future contracts #83](https://github.com/ITPD-Almo/modular-llm-gateway/pull/83), [release/changelog #86](https://github.com/ITPD-Almo/modular-llm-gateway/pull/86), and independent specification/comparison/guide reviews. The final report remains under review. |
| Mohammed-Nour | [Requirements/glossary #73](https://github.com/ITPD-Almo/modular-llm-gateway/pull/73), [matched comparison #75](https://github.com/ITPD-Almo/modular-llm-gateway/pull/75), [guide/examples #76](https://github.com/ITPD-Almo/modular-llm-gateway/pull/76), [agent guidance/navigation #78](https://github.com/ITPD-Almo/modular-llm-gateway/pull/78), [retrospective/AI-use/velocity #85](https://github.com/ITPD-Almo/modular-llm-gateway/pull/85), preserved original script history, and independent diagnostics/runtime/architecture reviews. |
| atkond2point0 | Participation in the October 23 review, recorded in the source-based [meeting account #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80). |

## Repository evidence

[PR #73](https://github.com/ITPD-Almo/modular-llm-gateway/pull/73) merged after independent review and closed requirements task #54.
At this draft's writing, main revision `9606161` has green [link checks](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40214576371), [Markdown checks](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40214576381), [tests](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40214576399) and [documentation build/deployment](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40214576384).
Replace these with the final pre-report main evidence after the remaining integrations and release records merge.
GitHub issue/project UI links and the course Git submodule are handled by the existing link-check exclusions; authenticated dynamic views are checked separately and upstream course content is not linted as team content.

## Deviations

- The owner confirmed an operational extension to October 25, 23:59 Europe/Moscow; the formal SPRINT-04 field/milestone remains October 24 as the supplied Assignment 4 requires.
- Planning, estimation and the coordinated issue catch-up were completed late, after the October 23 meeting. The 13-point baseline was computed on October 25, not reconstructed as an earlier sprint-start estimate.
- Setup/sharing problems prevented the required complete AC-by-AC demonstration, story verdicts and validation of the full quality/architecture set. The later tests and scope clarifications do not substitute for those missing results.
- Original script commits have October 22 author/commit metadata and were transferred/inspected on October 25; actual use and role execution remain unestablished. Its agenda totals 42 minutes instead of the required 30-minute plan. The separately dated follow-up is future preparation.
- Separate recording/publication/private-sharing answers are not captured in the call. The owner confirmed sharing on October 25; this later confirmation is not backdated. The public transcript uses explicitly coarse elapsed-minute markers, keeping exact recording timecodes and access details private.
- The original planning issues were created through the API with the form's required sections when the browser initially showed sign-in; the later diagnostics issue reused that workflow. The remaining specification task #82 was created through the repository form. The browser was not blocked for every creation.
- Runtime/demo dependency PRs merged into feature branches, and some approval/checkbox gates were not finalized before those branch merges. Original branches and review evidence are retained; the complete main integration received its own independent review. Some reviewer checkboxes were not recorded before those merges; their late or outstanding record remains visible rather than being invented by the author.
- Future deployment/recovery and metrics are targets, not capabilities delivered by this increment. Their contracts and final issue refinements are merged; future assignments may change those targets at weekly intake.
- This is a review draft: the real REL-04 tag/changelog/plan line and final report evidence are pending. The draft banner and this temporary gap must be removed only after those gates are met.

## Privacy

No private-only material was committed to this repository.
The recording access details and team contact mapping remain in local private submission inputs.
