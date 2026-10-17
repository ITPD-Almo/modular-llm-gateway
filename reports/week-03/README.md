# Week 03 report

## Project

Modular LLM Gateway, course team 9. This is a draft for Assignment 3: planning and the first usable release.

## Summary

The Week 3 candidate is [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42): configure plugins, write one against a documented interface, and see their effects on a request and response.

The planning documents and documentation site merged in [PR #46](https://github.com/ITPD-Almo/modular-llm-gateway/pull/46), and the gateway merged in [PR #48](https://github.com/ITPD-Almo/modular-llm-gateway/pull/48), closing tasks #44 and #43. A [fresh-clone check](gateway-check.md) on main at `71cb6ff3eac0da2172d6563229d2a76f7d2598b2` starts the gateway, checks the eight story criteria, and passes all five tests. REL-03 is not cut, and no v0.1.0 release is claimed in this draft.

The October 16 joint meeting did not demonstrate or settle our three stories. The gateway is now merged and checked, and Ali has a written demo to forward against each criterion. No story has been moved out of the candidate, and no Customer scope change is inferred from another team's discussion.

## Customer meeting outcome

See the [joint meeting report](meeting-report.md) and the [written validation script](meeting-script.md).

| Story | Shown for our team on October 16 | Verdict |
| --- | --- | --- |
| [US-01, #40](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40) | No. | Local evidence ready; Customer demonstration and reply pending. |
| [US-02, #41](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41) | No. | Local evidence ready; Customer demonstration and reply pending. |
| [US-03, #42](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42) | No. | Local evidence ready; Customer demonstration and reply pending. |

DEC-008 onwards will record actual verdicts once received, following [DEC-007](../../docs/decisions.md#dec-007), the stack decision merged through #43. Those entries do not exist yet.

## Coverage

| Deliverable | Artifact or current status |
| --- | --- |
| Threshold of success | [threshold-of-success.md](../../docs/threshold-of-success.md), merged in #46. |
| Project plan | [project-plan.md](../../docs/project-plan.md), merged in #46. |
| Risk register | [risks.md](../../docs/risks.md), merged in #46. |
| Stack decision | [DEC-007](../../docs/decisions.md#dec-007), merged in #48. |
| Definition of Done | [definition-of-done.md](../../docs/definition-of-done.md), merged in #46. |
| Contributing guide | [CONTRIBUTING.md](../../CONTRIBUTING.md), merged in #46. |
| Sprint milestones and issue fields | [SPRINT-03](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/1). The seven sprint milestones exist. Responsible and Accountable are Public and set on #40 to #45, matching the assignees. Both fields are pinned to issues without a type; the saved setting was verified. |
| GitHub project | [Public sprint table](https://github.com/orgs/ITPD-Almo/projects/1/views/2), grouped by Milestone, with Responsible, Accountable, Assignees and Milestone. It contains #40 to #45. |
| Minimum usable product | [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), implemented in #48 and [checked locally](gateway-check.md#story-checks); Customer verdicts pending. |
| Changelog and first release | [CHANGELOG.md](../../CHANGELOG.md) has Unreleased entries from #48. The [v* tag ruleset](https://github.com/ITPD-Almo/modular-llm-gateway/rules/25307574) blocks updates and deletion. The tag, release, dated 0.1.0 section and REL-03 line are still pending. |
| Documentation site | [Documentation site](https://itpd-almo.github.io/modular-llm-gateway/), deployed through GitHub Actions. The landing page, setup page, and plugin page return HTTP 200. |
| Setup and run instructions | [Setup guide](../../docs/setup.md), merged in #48; the POSIX start and curl example work from a fresh clone. |
| Week 2 action points | [Position at the meeting](meeting-report.md#previous-action-points), followed by [October 17 implementation checks](gateway-check.md#week-2-action-points). Both technical actions are implemented; Customer validation remains open. |
| Week 2 open questions | [Position at the meeting](meeting-report.md#previous-open-questions) and [current answers](gateway-check.md#week-2-open-questions), with unresolved points carried forward. |
| Meeting script | [Written validation script](meeting-script.md), prepared after the joint meeting and before the planned written exchange. |
| Customer validation | [Joint meeting report](meeting-report.md); written validation and its transcript are pending. |
| AI usage | [AI-use report](ai-usage.md), with Ali's draft entry and the other members' statements pending. |

## Contribution

| GitHub username | Work and current evidence |
| --- | --- |
| Ali12hamdan | Task [#45](https://github.com/ITPD-Almo/modular-llm-gateway/issues/45): Pages configuration, public organization fields and project, reviews of #46, #48 and the dependency updates, fresh-clone gateway checks, meeting documents, and preparation for written validation and the release. |
| Mohammed-Nour | Task [#44](https://github.com/ITPD-Almo/modular-llm-gateway/issues/44), planning and workflow documents in [PR #46](https://github.com/ITPD-Almo/modular-llm-gateway/pull/46). |
| atkond2point0 | Task [#43](https://github.com/ITPD-Almo/modular-llm-gateway/issues/43), the gateway, plugin interface, setup instructions, and tests in merged [PR #48](https://github.com/ITPD-Almo/modular-llm-gateway/pull/48). |

## Repository evidence

- [PR #46](https://github.com/ITPD-Almo/modular-llm-gateway/pull/46) closed [#44](https://github.com/ITPD-Almo/modular-llm-gateway/issues/44); [PR #48](https://github.com/ITPD-Almo/modular-llm-gateway/pull/48) closed [#43](https://github.com/ITPD-Almo/modular-llm-gateway/issues/43).
- Latest green main checks at `71cb6ff3eac0da2172d6563229d2a76f7d2598b2`: [links](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228923), [Markdown](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228873), [tests](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228883), and [site build and deployment](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/39045228886).
- [PR #49](https://github.com/ITPD-Almo/modular-llm-gateway/pull/49) updates the pinned setup-python action; [PR #50](https://github.com/ITPD-Almo/modular-llm-gateway/pull/50) allows pytest 9. Both were reviewed and merged with passing checks.

These checks cover the current implementation. The final submission must use the main commit after this report is reviewed and merged.

## Deviations

- **Issues created through the API.** The Week 3 story and task issues were created through the API rather than submitted through the web forms. They carry the form's fields and labels, but that does not remove the workflow deviation.
- **Written validation after the meeting.** Our stories were not demonstrated at the October 16 joint meeting. The written demo is prepared from the merged implementation and local results. No verdict has been received yet, so this report does not say a written verdict was already given.
- **Meeting preparation.** No original script for the October 16 call was supplied. The script in this draft is for the later written exchange and is not backdated.
- **Attendance and permissions.** Team 9 attendance is unconfirmed by the supplied record. The separate permission answers and the permitted transcript-sharing scope are also unconfirmed. The raw transcript stays out of the public repository.
- **Task checklist at merge.** Task #43 closed when #48 merged, but its acceptance boxes were still unchecked when verified afterwards. The local checks are recorded separately, and the accountable reviewer has been asked to record the verified criteria.
- **Unfinished work.** This draft is not ready for submission. Actual story verdicts, tag, release, final AI-use entries, and the final PDF and snapshot are still pending.

## Privacy

No private-only material has been added to these public drafts.
