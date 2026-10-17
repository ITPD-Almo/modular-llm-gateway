# Week 03 report

## Project

Modular LLM Gateway, course team 9. Assignment 3: planning and the first working release, with Customer validation declared missing.

## Summary

The Week 3 candidate is [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42): configure plugins, write one against a documented interface, and see their effects on a request and response.

The planning documents and documentation site merged in [PR #46](https://github.com/ITPD-Almo/modular-llm-gateway/pull/46), and the gateway merged in [PR #48](https://github.com/ITPD-Almo/modular-llm-gateway/pull/48), closing tasks #44 and #43. A [fresh-clone check](gateway-check.md) on main at `71cb6ff3eac0da2172d6563229d2a76f7d2598b2` starts the gateway, checks the eight story criteria, and passes all five tests. [REL-03](../../docs/project-plan.md#rel-03) is published as [v0.1.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.1.0) from that tested commit.

The October 16 joint meeting did not demonstrate or settle our three stories. The gateway is merged and checked, and a written demo was prepared against each criterion. We could not obtain Customer verdicts for this submission, so the validation requirement is missing. No story has been moved out of the candidate, and no Customer scope change is inferred from another team's discussion.

## Minimum Usable Product Candidate

The core task is for a DevOps operator to start the gateway with two configured plugins, send a request to the fake provider, and see each plugin's effect on the request and response. A plugin developer can add a plugin through the documented interface without changing the core.

The candidate is [US-01, #40](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02, #41](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), and [US-03, #42](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), all Must Have, under [MLS-03](../../docs/project-plan.md#mls-03). [DEC-005](../../docs/decisions.md#dec-005) and [DEC-006](../../docs/decisions.md#dec-006) explain the earlier workflow and interface direction; neither accepts this implementation. No verdict DEC exists for these stories. Nothing moved out of the candidate.

## Customer meeting outcome

See the [joint meeting report](meeting-report.md) and the [written validation script](meeting-script.md).

| Story | Shown for our team on October 16 | Verdict |
| --- | --- | --- |
| [US-01, #40](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40) | No. | Missing for Week 3. Implemented and checked locally; remains open in SPRINT-04 for a Customer verdict. |
| [US-02, #41](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41) | No. | Missing for Week 3. Implemented and checked locally; remains open in SPRINT-04 for a Customer verdict. |
| [US-03, #42](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42) | No. | Missing for Week 3. Implemented and checked locally; remains open in SPRINT-04 for a Customer verdict. |

No verdict decisions were added. [DEC-007](../../docs/decisions.md#dec-007) remains the latest decision. No story was removed from the candidate. [TOS-01](../../docs/threshold-of-success.md#tos-01) remains Open because its acceptance deadline is October 23, in Week 4; releasing the code does not meet that goal.

## Coverage

| Deliverable | Artifact or current status |
| --- | --- |
| Threshold of success | [docs/threshold-of-success.md](../../docs/threshold-of-success.md), merged in #46. |
| Project plan | [docs/project-plan.md](../../docs/project-plan.md), merged in #46. |
| Risk register | [docs/risks.md](../../docs/risks.md), merged in #46. |
| Stack decision | [DEC-007](../../docs/decisions.md#dec-007), merged in #48. |
| Definition of Done | [docs/definition-of-done.md](../../docs/definition-of-done.md), merged in #46. |
| Contributing guide | [CONTRIBUTING.md](../../CONTRIBUTING.md), merged in #46. |
| Sprint milestones and issue fields | [SPRINT-03](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/1). The seven sprint milestones exist. SPRINT-03 is closed after release; open stories #40 to #42 and report task #45 were moved to [SPRINT-04](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/2). Responsible and Accountable remain Public and match the assignees. Both fields are pinned to issues without a type; the saved setting was verified. |
| GitHub project | [Public sprint table](https://github.com/orgs/ITPD-Almo/projects/1/views/2), grouped by Milestone, with Responsible, Accountable, Assignees and Milestone. It contains #40 to #45. |
| Minimum usable product | [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), implemented in #48 and [checked locally](gateway-check.md#story-checks); Customer validation missing for this submission. |
| Changelog and first release | [CHANGELOG.md](../../CHANGELOG.md) has a dated 0.1.0 section linked to [v0.1.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.1.0), with a new empty Unreleased section. The [v* tag ruleset](https://github.com/ITPD-Almo/modular-llm-gateway/rules/25307574) blocks updates and deletion. [REL-03](../../docs/project-plan.md#rel-03) links the release. |
| Documentation site | [Documentation site](https://itpd-almo.github.io/modular-llm-gateway/), deployed through GitHub Actions. The landing page, setup page, and plugin page return HTTP 200. |
| Setup and run instructions | [docs/setup.md](../../docs/setup.md), merged in #48; the POSIX start and curl example work from a fresh clone. |
| Week 2 action points | [Position at the meeting](meeting-report.md#previous-action-points), followed by [October 17 implementation checks](gateway-check.md#week-2-action-points). Both technical actions are implemented; Customer validation remains open. |
| Week 2 open questions | [Position at the meeting](meeting-report.md#previous-open-questions) and [current answers](gateway-check.md#week-2-open-questions), with unresolved points carried forward. |
| Meeting script | [reports/week-03/meeting-script.md](meeting-script.md), prepared after the joint meeting and before the planned written exchange. |
| Customer validation | [reports/week-03/meeting-report.md](meeting-report.md) records the joint meeting. The later written review was not completed; there are no verdicts or written-exchange transcript. The source VTT stays private because sharing permission is unconfirmed. |
| AI usage | [reports/week-03/ai-usage.md](ai-usage.md), with Ali's entry and Mohammed-Nour's supplied statement. atkond2point0's Week 3 statement is missing. |

## Contribution

| GitHub username | Work and current evidence |
| --- | --- |
| Ali12hamdan | Task [#45](https://github.com/ITPD-Almo/modular-llm-gateway/issues/45): Pages configuration, public organization fields and project, reviews of #46, #48 and the dependency updates, fresh-clone gateway checks, meeting documents, and preparation of the written demo, the protected release, and this report. |
| Mohammed-Nour | Task [#44](https://github.com/ITPD-Almo/modular-llm-gateway/issues/44), planning and workflow documents in [PR #46](https://github.com/ITPD-Almo/modular-llm-gateway/pull/46); SPRINT-04 to SPRINT-09 milestones, story issues #41 to #42 and task issues #43 to #45; [review of #48](https://github.com/ITPD-Almo/modular-llm-gateway/pull/48#pullrequestreview-5558282327). |
| atkond2point0 | Task [#43](https://github.com/ITPD-Almo/modular-llm-gateway/issues/43), the gateway, plugin interface, setup instructions, and tests in merged [PR #48](https://github.com/ITPD-Almo/modular-llm-gateway/pull/48). |

## Repository evidence

- [PR #46](https://github.com/ITPD-Almo/modular-llm-gateway/pull/46) closed [#44](https://github.com/ITPD-Almo/modular-llm-gateway/issues/44); [PR #48](https://github.com/ITPD-Almo/modular-llm-gateway/pull/48) closed [#43](https://github.com/ITPD-Almo/modular-llm-gateway/issues/43).
- Green implementation checks on main at `71cb6ff3eac0da2172d6563229d2a76f7d2598b2`: [links](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228923), [Markdown](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228873), [tests](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228883), and [site build and deployment](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228886).
- [PR #49](https://github.com/ITPD-Almo/modular-llm-gateway/pull/49) updates the pinned setup-python action; [PR #50](https://github.com/ITPD-Almo/modular-llm-gateway/pull/50) allows pytest 9. Both were reviewed and merged with passing checks.

These checks cover the released implementation. The PDF permalink and repository snapshot must use the same final main commit after this report is reviewed and merged.

## Deviations

- **Issues created through the API.** The Week 3 story and task issues were created through the API rather than submitted through the web forms. They carry the form's fields and labels, but that does not remove the workflow deviation.
- **Customer validation missing.** Our stories were not demonstrated at the October 16 joint meeting. A written demo was prepared, but the exchange was not completed for this submission. The local checks are technical evidence, not Customer acceptance. Stories #40 to #42 stay open in SPRINT-04, and no verdict DEC was invented.
- **Meeting preparation.** No original script for the October 16 call was supplied. The supplied script was prepared for the later written exchange, which did not take place for this submission; it is not backdated.
- **Transcript sharing permissions.** This meeting report was prepared from the shared transcript. The separate permission answers and permitted sharing scope are unconfirmed, so the raw transcript stays out of the public repository.
- **Task checklist at merge.** Task #43 closed when #48 merged, but its acceptance boxes were still unchecked when verified afterwards. The local checks are recorded separately, and the accountable reviewer has been asked to record the verified criteria.
- **AI-use statement missing.** atkond2point0 did not supply a Week 3 statement. His tools or uses were not inferred from his commits. Mohammed-Nour supplied his statement in the PR review comment; it is included.
- **Release records in one PR.** The dated changelog section, REL-03 line and weekly report are combined in #47, after the tag was published, rather than merged as separate PRs. This keeps the final release records together; the tag existed before their links were added.
- **Planning confirmation.** The threshold goals and Wednesday review time are team drafts and still need confirmation; the missing Customer exchange did not settle them.
- **Recording access missing.** The October 16 joint meeting was recorded, but no instructor-accessible recording link was supplied for this submission. No Week 2 recording is used as a substitute.
- **Post-release carryover.** Task #45 moved to SPRINT-04 because it was still open when the release was cut. It remains the Week 3 report and release task; its merge is required before taking the final snapshot.

## Privacy

No private-only material was committed to this repository.
