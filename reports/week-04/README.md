# Week 04 report

## Project

Modular LLM Gateway, team 9, Assignment 4: quality, requirements, architecture and REL-04.

## Summary

**Review draft: release and submission gates remain open.** This report must be finalized and merged after the released changelog and the plan's real REL-04 line; it is not a completed submission.

The team specified the plugin workflow, wrote the quality scenarios and architecture, and compared the same two-plugin interaction with LiteLLM.
The Customer emphasized a plugin-management system another developer/DevOps operator can understand and support, a concrete A-input/B-output example, identifiable failing or sleeping plugins, and progress against a multiweek plan.
The October 23 setup attempt did not establish a complete working demonstration or individual story verdicts; the later source account is under review in [PR #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80).

The integrated runtime/demo branch has 40 passing tests and an independent clean-environment replay, including a named timeout in 0.303 seconds followed by healthy requests.
Its [main integration #81](https://github.com/ITPD-Almo/modular-llm-gateway/pull/81) is still awaiting independent approval; a feature-branch merge is not delivery to main.
The default four-worker limit deliberately rejects excess concurrent healthy requests with 503, and instances reset between requests; the accepted architecture records those costs.
These are technical results and team design choices, not Customer acceptance.

The latest published release remains [v0.1.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.1.0).
REL-04, its new tag/changelog and final scope relocation remain pending [#62](https://github.com/ITPD-Almo/modular-llm-gateway/issues/62) and [#63](https://github.com/ITPD-Almo/modular-llm-gateway/issues/63).
Future deployment/recovery and metrics remain unscheduled product targets; [PR #83](https://github.com/ITPD-Almo/modular-llm-gateway/pull/83) refines their contracts without claiming implementation.

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
No story was removed from the original candidate; the final sprint-close record will state the actual carry-forward destinations.
The forthcoming meeting account separates genuine scope clarifications from the still-missing verdicts.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan and estimates | [docs/project-plan.md#sprint-04](../../docs/project-plan.md#sprint-04); late planned baseline 13, final Actual Velocity pending #61/#63. |
| Product backlog refinement | [Sprint table grouped by milestone](https://github.com/orgs/ITPD-Almo/projects/1/views/2), no-milestone group; future contract refinement awaits #83 before completion is claimed. |
| Issue catch-up | [User Story issues](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=is%3Aissue%20type%3A%22User%20Story%22) and [Task issues](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=is%3Aissue%20type%3ATask); final coordinated verification is owned by #59. |
| Quality requirements | [docs/quality-requirements/qr/](../../docs/quality-requirements/qr/) and [docs/quality-requirements/README.md](../../docs/quality-requirements/README.md); additional future-target scenarios are under review in #83. |
| Functional requirements | [docs/functional-requirements/README.md](../../docs/functional-requirements/README.md) and [docs/functional-requirements/fr/](../../docs/functional-requirements/fr/). |
| Container view | [docs/architecture/README.md#container-view](../../docs/architecture/README.md#container-view), [docs/architecture/container.png](../../docs/architecture/container.png), [docs/architecture/container.svg](../../docs/architecture/container.svg) and [docs/architecture/README.md#container-responsibilities](../../docs/architecture/README.md#container-responsibilities). |
| Architecture and drivers | [docs/architecture/README.md](../../docs/architecture/README.md). |
| Architectural decisions | [docs/architecture/adr/](../../docs/architecture/adr/) and [docs/architecture/README.md#architectural-decisions](../../docs/architecture/README.md#architectural-decisions). |
| Glossary | [docs/glossary.md](../../docs/glossary.md). |
| Team AGENTS.md | Pending [PR #78](https://github.com/ITPD-Almo/modular-llm-gateway/pull/78), which adds the root instructions and site navigation. |
| Issue fields in the project view | [Sprint table](https://github.com/orgs/ITPD-Almo/projects/1/views/2): Responsible, Accountable, MoSCoW, Story Points, Priority, Assignees, Milestone and Status. |
| Documentation site | [Published documentation](https://itpd-almo.github.io/modular-llm-gateway/); final new navigation/deployment verification follows #78 and #64. |
| Week 3 action points | Pending the Previous action points section in [PR #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80). |
| Week 3 open questions | Pending the Previous open questions section in [PR #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80). |
| Meeting script | Original October 22 history preserved in [PR #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80), alongside separately dated future follow-up preparation. |
| Customer validation | Meeting account and permitted sanitized public transcript in [PR #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80); individual story verdicts remain unreceived. |
| REL-04 | Pending protected tag/release and [CHANGELOG.md](../../CHANGELOG.md), followed by [docs/project-plan.md#rel-04](../../docs/project-plan.md#rel-04). |
| Sprint retrospective | Pending [task #61](https://github.com/ITPD-Almo/modular-llm-gateway/issues/61); write it after Actual Velocity is set. |
| AI usage | Pending [task #61](https://github.com/ITPD-Almo/modular-llm-gateway/issues/61); actual contributor statements and agent-run checks must remain distinct. |
| Reproducible developer demo | Reviewed in [PR #76](https://github.com/ITPD-Almo/modular-llm-gateway/pull/76), with final main integration/evidence in [PR #81](https://github.com/ITPD-Almo/modular-llm-gateway/pull/81). |

## Contribution

| Member | Evidenced work |
| --- | --- |
| Ali12hamdan | [Planning #69](https://github.com/ITPD-Almo/modular-llm-gateway/pull/69), [diagnostics #71](https://github.com/ITPD-Almo/modular-llm-gateway/pull/71), [runtime #72](https://github.com/ITPD-Almo/modular-llm-gateway/pull/72), [architecture #77](https://github.com/ITPD-Almo/modular-llm-gateway/pull/77), [integration #81](https://github.com/ITPD-Almo/modular-llm-gateway/pull/81), [tracker #79](https://github.com/ITPD-Almo/modular-llm-gateway/pull/79), [meeting account #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80), [future contracts #83](https://github.com/ITPD-Almo/modular-llm-gateway/pull/83), and independent specification/comparison/guide reviews. Unmerged work remains marked above. |
| Mohammed-Nour | [Requirements/glossary #73](https://github.com/ITPD-Almo/modular-llm-gateway/pull/73), [matched comparison #75](https://github.com/ITPD-Almo/modular-llm-gateway/pull/75), [guide/examples #76](https://github.com/ITPD-Almo/modular-llm-gateway/pull/76), [agent guidance/navigation #78](https://github.com/ITPD-Almo/modular-llm-gateway/pull/78), preserved original script history, and independent diagnostics/runtime/architecture reviews. |
| atkond2point0 | Participation in the October 23 review, recorded in the source-based [meeting account #80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80). |

## Repository evidence

[PR #73](https://github.com/ITPD-Almo/modular-llm-gateway/pull/73) merged after independent review and closed requirements task #54.
At this draft's writing, main revision `b14f774` has green [link checks](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40210684962), [Markdown checks](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40210684969), [tests](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40210684955) and [documentation build/deployment](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/40210684947).
Replace these with the final pre-report main evidence after the remaining integrations and release records merge.
GitHub issue/project UI links and the course Git submodule are handled by the existing link-check exclusions; authenticated dynamic views are checked separately and upstream course content is not linted as team content.

## Deviations

- The owner confirmed an operational extension to October 25, 23:59 Europe/Moscow; the formal SPRINT-04 field/milestone remains October 24 as the supplied Assignment 4 requires.
- Planning, estimation and the coordinated issue catch-up were completed late, after the October 23 meeting. The 13-point baseline was computed on October 25, not reconstructed as an earlier sprint-start estimate.
- Setup/sharing problems prevented the required complete AC-by-AC demonstration, story verdicts and validation of the full quality/architecture set. The later tests and scope clarifications do not substitute for those missing results.
- Original script commits have October 22 author/commit metadata and were transferred/inspected on October 25; actual use and role execution remain unestablished. Its agenda totals 42 minutes instead of the required 30-minute plan. The separately dated follow-up is future preparation.
- Separate recording/publication/private-sharing answers are not captured in the call. The owner confirmed sharing on October 25; this later confirmation is not backdated. The public transcript uses explicitly coarse elapsed-minute markers, keeping exact recording timecodes and access details private.
- The original planning issues were created through the API with the form's required sections when the browser initially showed sign-in; the later diagnostics issue reused that workflow. The remaining specification task #82 was created through the repository form. The browser was not blocked for every creation.
- Runtime/demo dependency PRs merged into feature branches, and some approval/checkbox gates were not finalized before those branch merges. Original branches and review evidence are retained; the complete main integration receives its own independent review. Reviewer boxes must reflect actual verification, including any late recording.
- Future deployment/recovery and metrics are targets, not capabilities delivered by this increment. Their new contracts require reviewed merge and final issue-link/refinement checks before readiness is claimed; future assignments may change them at weekly intake.
- This is a review draft: REL-04, sprint-close/retrospective/AI-use records and final report evidence are pending. These draft-state gaps must be replaced with their actual outcomes before final approval.

## Privacy

No private-only material was committed to this repository.
The recording access details and team contact mapping remain in local private submission inputs.
