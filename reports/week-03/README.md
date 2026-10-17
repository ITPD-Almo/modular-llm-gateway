# Week 03 report

## Project

Modular LLM Gateway, course team 9. This is a draft for Assignment 3: planning and the first usable release.

## Summary

The Week 3 candidate is [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42): configure plugins, write one against a documented interface, and see their effects on a request and response.

The planning documents and documentation site are under review in [PR #46](https://github.com/ITPD-Almo/modular-llm-gateway/pull/46). The gateway is task [#43](https://github.com/ITPD-Almo/modular-llm-gateway/issues/43); no gateway PR is available yet. REL-03 is not cut, and no v0.1.0 release is claimed in this draft.

The October 16 joint meeting did not demonstrate or settle our three stories. We are preparing a written follow-up against each criterion after the code merges. No story has been moved out of the candidate, and no Customer scope change is inferred from another team's discussion.

## Customer meeting outcome

See the [joint meeting report](meeting-report.md) and the [written validation script](meeting-script.md).

| Story | Shown for our team on October 16 | Verdict |
| --- | --- | --- |
| [US-01, #40](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40) | No. | Pending written demonstration and Customer reply. |
| [US-02, #41](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41) | No. | Pending written demonstration and Customer reply. |
| [US-03, #42](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42) | No. | Pending written demonstration and Customer reply. |

DEC-008 onwards will record actual verdicts once received, following the stack decision reserved as DEC-007 in #43. Those entries do not exist yet.

## Coverage

| Deliverable | Artifact or current status |
| --- | --- |
| Threshold of success | Pending merge of `docs/threshold-of-success.md` in #46. |
| Project plan | Pending merge of `docs/project-plan.md` in #46. |
| Risk register | Pending merge of `docs/risks.md` in #46. |
| Stack decision | DEC-007 is part of #43; not yet on main. |
| Definition of Done | Pending merge of `docs/definition-of-done.md` in #46. |
| Contributing guide | Pending merge of `CONTRIBUTING.md` in #46. |
| Sprint milestones and issue fields | [SPRINT-03](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/1). The seven sprint milestones exist; the Responsible and Accountable fields still need owner setup. |
| GitHub project | Pending owner setup and the actual table-view URL. |
| Minimum usable product | [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), awaiting #43 and written validation. |
| Changelog and first release | `CHANGELOG.md` is part of #43. The dated 0.1.0 section and REL-03 line are added only after the tag and release exist. |
| Documentation site | Pages is configured for GitHub Actions. Deployment is pending #46. |
| Setup and run instructions | `docs/setup.md` is part of #43; not yet on main. |
| Week 2 action points | [Previous action points](meeting-report.md#previous-action-points). Both outcomes still need the merged gateway and written follow-up. |
| Week 2 open questions | [Previous open questions](meeting-report.md#previous-open-questions), all seven covered and unresolved points carried forward. |
| Meeting script | [Written validation script](meeting-script.md), prepared after the joint meeting and before the planned written exchange. |
| Customer validation | [Joint meeting report](meeting-report.md); written validation and its transcript are pending. |
| AI usage | [AI-use report](ai-usage.md), with Ali's draft entry and the other members' statements pending. |

## Contribution

| GitHub username | Work and current evidence |
| --- | --- |
| Ali12hamdan | Task [#45](https://github.com/ITPD-Almo/modular-llm-gateway/issues/45): Pages configuration, review of #46, meeting documents, and preparation for written validation and the release. |
| Mohammed-Nour | Task [#44](https://github.com/ITPD-Almo/modular-llm-gateway/issues/44), planning and workflow documents in [PR #46](https://github.com/ITPD-Almo/modular-llm-gateway/pull/46). |
| atkond2point0 | Task [#43](https://github.com/ITPD-Almo/modular-llm-gateway/issues/43), the gateway, plugin interface, setup instructions, and tests; PR pending. |

## Repository evidence

- A merged PR that closed its task: [#39](https://github.com/ITPD-Almo/modular-llm-gateway/pull/39), which closed [#38](https://github.com/ITPD-Almo/modular-llm-gateway/issues/38).
- Green link check on the current main revision: [run 38084580284](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/38084580284).
- Green Markdown check on the same revision: [run 38084580295](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/38084580295).

These runs checked main at b8decdc. Replace them with the final submission revision's evidence after the Week 3 work merges.

## Deviations

- **Issues created through the API.** The Week 3 story and task issues were created through the API rather than submitted through the web forms. They carry the form's fields and labels, but that does not remove the workflow deviation.
- **Written validation after the meeting.** Our stories were not demonstrated at the October 16 joint meeting. A written review is planned after #43 merges. No verdict has been received yet, so this report does not say a written verdict was already given.
- **Meeting preparation.** No original script for the October 16 call was supplied. The script in this draft is for the later written exchange and is not backdated.
- **Attendance and permissions.** Team 9 attendance is unconfirmed by the supplied record. The separate permission answers and the permitted transcript-sharing scope are also unconfirmed. The raw transcript stays out of the public repository.
- **Unfinished work.** This draft is not ready for submission. The gateway, project and fields, site deployment, actual story verdicts, tag, release, final AI-use entries, and final PDF and snapshot are still pending.

## Privacy

No private-only material has been added to these public drafts.
