# Week 04 report

## Project

Modular LLM Gateway, team 9, Assignment 4: quality, requirements, architecture and REL-04.

## Summary

The team specified the plugin workflow, wrote the quality scenarios and architecture, and delivered the reviewed runtime and developer workflow. The matched LiteLLM comparison ran the same small interaction with comparable effort, so competitive differentiation remains unestablished and the Customer has not selected a core from that comparison.
The Customer emphasized a plugin-management system another developer/DevOps operator can understand and support, a concrete A-input/B-output example, identifiable failing or sleeping plugins, and progress against a multiweek plan.
The October 23 setup attempt did not establish a complete working demonstration or individual story verdicts; the source-based account is in [reports/week-04/meeting-report.md](meeting-report.md).

The supervised runtime and developer demo are integrated into main through independently reviewed [PR #81](https://github.com/ITPD-Almo/modular-llm-gateway/pull/81), with safe failure correlation and recovery.
The default four-worker limit deliberately rejects excess concurrent healthy requests with 503, and instances reset between requests; the accepted architecture records those costs.
These are technical results and team design choices, not Customer acceptance.

REL-04 is published as [v0.2.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.2.0) from verified main commit `960616128ca88159a003aa772dd198c4c0f515ea`; the exact-commit clean replay passed 40 tests and timed out the slow hook in 0.297 seconds with subsequent recovery.
The dated [CHANGELOG.md](../../CHANGELOG.md#020---2026-10-25) merged in #86 before the [docs/project-plan.md#rel-04](../../docs/project-plan.md#rel-04) line in #87; this report follows both.
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
| Sprint plan and estimates | [docs/project-plan.md#sprint-04](../../docs/project-plan.md#sprint-04); late planned baseline 13 and Actual Velocity 0; 13 points carried to SPRINT-05, with the close record reviewed in #87. |
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
| Documentation site | [Published documentation](https://itpd-almo.github.io/modular-llm-gateway/): the QR/FR/architecture/glossary/operating links and main documentation deployment are verified; final post-report checks are recorded with the report review before packaging. |
| Week 3 action points | [reports/week-04/meeting-report.md#previous-action-points](meeting-report.md#previous-action-points). |
| Week 3 open questions | [reports/week-04/meeting-report.md#previous-open-questions](meeting-report.md#previous-open-questions). |
| Meeting script | [reports/week-04/meeting-script.md](meeting-script.md), with separately dated future preparation in [reports/week-04/meeting-script-2.md](meeting-script-2.md). |
| Customer validation | [reports/week-04/meeting-report.md](meeting-report.md) and permitted public [reports/week-04/meeting-transcript.md](meeting-transcript.md); individual story verdicts remain unreceived. |
| REL-04 | [v0.2.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.2.0), [CHANGELOG.md#020---2026-10-25](../../CHANGELOG.md#020---2026-10-25) and [docs/project-plan.md#rel-04](../../docs/project-plan.md#rel-04), merged in the required tag/changelog/plan/report sequence. |
| Sprint retrospective | [reports/week-04/sprint-retrospective.md](sprint-retrospective.md), written with Actual Velocity set and reviewed in #85, closing #61. |
| AI usage | [reports/week-04/ai-usage.md](ai-usage.md); contributor statements and agent-run/personal checks are distinguished, and the missing third-member statement is explicit. |
| Existing-gateway comparison | [reports/week-04/prototypes.md](prototypes.md); the matched result informs ASM-02 without inventing Customer selection or broader untested claims. |
| Reproducible developer demo | [docs/demo.md](../../docs/demo.md), [docs/setup.md](../../docs/setup.md), [docs/plugins.md](../../docs/plugins.md), [docs/operations.md](../../docs/operations.md) and [reports/week-04/gateway-check.md](gateway-check.md). |

## Contribution

| Member | Evidenced work |
| --- | --- |
| Ali12hamdan | [Planning #69](https://github.com/ITPD-Almo/modular-llm-gateway/pull/69), [diagnostics #71](https://github.com/ITPD-Almo/modular-llm-gateway/pull/71), [runtime #72](https://github.com/ITPD-Almo/modular-llm-gateway/pull/72), [architecture #77](https://github.com/ITPD-Almo/modular-llm-gateway/pull/77), [integration #81](https://github.com/ITPD-Almo/modular-llm-gateway/pull/81), [tracker #79](https://github.com/ITPD-Almo/modular-llm-gateway/pull/79), [meeting account #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80), [future contracts #83](https://github.com/ITPD-Almo/modular-llm-gateway/pull/83), [release/changelog #86](https://github.com/ITPD-Almo/modular-llm-gateway/pull/86), and independent specification/comparison/guide reviews. |
| Mohammed-Nour | [Requirements/glossary #73](https://github.com/ITPD-Almo/modular-llm-gateway/pull/73), [matched comparison #75](https://github.com/ITPD-Almo/modular-llm-gateway/pull/75), [guide/examples #76](https://github.com/ITPD-Almo/modular-llm-gateway/pull/76), [agent guidance/navigation #78](https://github.com/ITPD-Almo/modular-llm-gateway/pull/78), [retrospective/AI-use/velocity #85](https://github.com/ITPD-Almo/modular-llm-gateway/pull/85), [release-plan line #87](https://github.com/ITPD-Almo/modular-llm-gateway/pull/87), preserved original script history, and independent diagnostics/runtime/architecture reviews. |
| atkond2point0 | Participation in the October 23 review, recorded in the source-based [meeting account #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80). |

## Repository evidence

[PR #73](https://github.com/ITPD-Almo/modular-llm-gateway/pull/73) merged after independent review and closed requirements task #54.
Before this report merge, main revision `9ab947028b7c6376b00551551176661561fe110f` has green [link checks](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40216250262), [Markdown checks](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40216250231), [tests](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40216250221) and [documentation build/deployment](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40216250237).
Post-merge main checks are recorded in [the final report review](https://github.com/ITPD-Almo/modular-llm-gateway/pull/84) before packaging, without making a cosmetic commit that would change the submitted snapshot.
GitHub issue/project UI links and the course Git submodule are handled by the existing link-check exclusions; authenticated dynamic views are checked separately and upstream course content is not linted as team content.

## Deviations

- The owner confirmed an operational extension to October 25, 23:59 Europe/Moscow; the formal SPRINT-04 field/milestone remains October 24 as the supplied Assignment 4 requires.
- Planning, estimation and the coordinated issue catch-up were completed late, after the October 23 meeting. The 13-point baseline was computed on October 25, not reconstructed as an earlier sprint-start estimate.
- Setup/sharing problems prevented the required complete AC-by-AC demonstration, story verdicts and validation of the full quality/architecture set. The later tests and scope clarifications do not substitute for those missing results.
- Original script commits have October 22 author/commit metadata and were transferred/inspected on October 25; actual use and role execution remain unestablished. Its agenda totals 42 minutes instead of the required 30-minute plan. The separately dated follow-up is future preparation.
- Separate recording/publication/private-sharing answers are not captured in the call. The owner confirmed sharing on October 25; this later confirmation is not backdated. The public transcript uses explicitly coarse elapsed-minute markers, keeping exact recording timecodes and access details private.
- The original planning issues were created through the API with the form's required sections when the browser initially showed sign-in; the later diagnostics issue reused that workflow. The remaining specification task #82 was created through the repository form. The browser was not blocked for every creation.
- Runtime/demo dependency PRs merged into feature branches, and some approval/checkbox gates were not finalized before those branch merges. Original branches and review evidence are retained; the complete main integration received its own independent review. Some reviewer checkboxes were not recorded before those merges; their late or outstanding record remains visible rather than being invented by the author.
- The retrospective is a written record based on the sprint artifacts and contributor inputs; no separate retrospective meeting was held. Its actions are proposals for the next sprint.
- The product has no frontend or payment module. [QR-01](../../docs/quality-requirements/qr/QR-01.md) names the real gateway entry point, loader, hook contract, configuration and worker modules as its critical testability artifacts rather than inventing the assignment’s sample components.
- Future deployment/recovery and metrics are targets, not capabilities delivered by this increment. Their contracts and final issue refinements are merged; future assignments may change those targets at weekly intake.

## Privacy

No private-only material was committed to this repository.
The recording access details and team contact mapping remain in local private submission inputs.
