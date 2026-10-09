# Week 02 report

## Project

Modular LLM Gateway, course team 9. Week 2 covers Assignment 2: issue tracking, the decisions and assumptions logs, the research restructure, the product vision, the first prototype, and our first meeting with our own Customer.

Read the [meeting report](meeting-report.md) first. It records what the Customer changed.

## Summary

We moved the Week 1 decisions and assumptions into their own logs, restructured the research around its identifiers, and wrote a product vision with a system context diagram. On October 9 we showed the Customer a text concept of a masking flow and a policy-version record, in a joint meeting with two other teams.

We were wrong about what mattered first. We had centred the first version on masking and finding the policy revision behind a decision. The Customer said the missing part was how plugins connect to the gateway: their inputs, outputs, execution order, and loading. The Customer also defined the first usable workflow as starting the system, adding two simple plugins, sending a request, and seeing the result. The meeting did not establish policy-version tracking as our advantage, and the Customer did not accept our three draft stories as a complete candidate.

Still open: the revised story issues and the Customer's verdict on them, the plugin interface design, whether an existing gateway already supports this workflow, and permission to publish the transcript.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Kickoff action points | [reports/week-02/meeting-report.md#previous-action-points](meeting-report.md#previous-action-points) |
| Kickoff open questions | [reports/week-02/meeting-report.md#previous-open-questions](meeting-report.md#previous-open-questions) |
| Product vision | [docs/product-vision.md](../../docs/product-vision.md) |
| System context diagram | [docs/architecture/context.svg](../../docs/architecture/context.svg), a hand-written SVG that is its own source, embedded in [docs/product-vision.md#context](../../docs/product-vision.md#context) |
| Assumptions | [docs/assumptions.md](../../docs/assumptions.md) |
| Decisions | [docs/decisions.md](../../docs/decisions.md) |
| Story issues | [Issues with the user-story label](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=label%3Auser-story). None are open yet; see Deviations. |
| Issue forms | [.github/ISSUE_TEMPLATE/user-story.yml](../../.github/ISSUE_TEMPLATE/user-story.yml), [.github/ISSUE_TEMPLATE/task.yml](../../.github/ISSUE_TEMPLATE/task.yml), [.github/ISSUE_TEMPLATE/config.yml](../../.github/ISSUE_TEMPLATE/config.yml) |
| Labels | [Repository labels](https://github.com/ITPD-Almo/modular-llm-gateway/labels) |
| Pull request template | [.github/pull_request_template.md](../../.github/pull_request_template.md) |
| Prototypes | [reports/week-02/prototypes.md](prototypes.md) |
| Meeting script | [reports/week-02/meeting-script.md, in draft PR #26](https://github.com/ITPD-Almo/modular-llm-gateway/pull/26) |
| Customer validation | [reports/week-02/meeting-report.md](meeting-report.md). The transcript is not public, because publication permission is unconfirmed; see the Moodle submission. |
| AI usage | [reports/week-02/ai-usage.md](ai-usage.md) |

## Minimum Usable Product Candidate

**Core task:** a DevOps operator starts the gateway, adds two simple plugins, sends a request, and sees the plugins' effect on the request and the result.

**Stories:** none yet. The candidate we took to the meeting was three draft `Must Have` stories: reaching the provider without holding its key, masking company identifiers, and finding which policy revision decided a request. They were not opened as issues before the meeting.

**Verdict:** the Customer did not accept those three stories as a complete candidate, and redefined the core task above, per [DEC-005](../../docs/decisions.md#dec-005). The revised `Must Have` stories and the Customer's verdict on them are due in Week 3.

## What changed after the prototype

[CON-01](../../docs/product-vision.md#con-01) now requires the next design to show plugin inputs, outputs, execution order, and loading, because the Customer said our text concept did not explain how plugins connect, per [DEC-006](../../docs/decisions.md#dec-006).

## Contribution

| GitHub username | Work |
| --- | --- |
| Ali12hamdan | Decisions log in [PR #14](https://github.com/ITPD-Almo/modular-llm-gateway/pull/14), assumptions log in [PR #16](https://github.com/ITPD-Almo/modular-llm-gateway/pull/16), meeting script in [PR #26](https://github.com/ITPD-Almo/modular-llm-gateway/pull/26), meeting report and DEC-003 to DEC-006 in [PR #28](https://github.com/ITPD-Almo/modular-llm-gateway/pull/28). Presented and asked our questions in the meeting. Approved [PR #8](https://github.com/ITPD-Almo/modular-llm-gateway/pull/8#pullrequestreview-5445684123), [PR #11](https://github.com/ITPD-Almo/modular-llm-gateway/pull/11#pullrequestreview-5445810373), and [PR #12](https://github.com/ITPD-Almo/modular-llm-gateway/pull/12#pullrequestreview-5445863178). Requested changes on [PR #20](https://github.com/ITPD-Almo/modular-llm-gateway/pull/20#pullrequestreview-5471788745), [PR #21](https://github.com/ITPD-Almo/modular-llm-gateway/pull/21#pullrequestreview-5471790064), and [PR #24](https://github.com/ITPD-Almo/modular-llm-gateway/pull/24#pullrequestreview-5472673165). |
| Mohammed-Nour | Issue forms and labels in [PR #8](https://github.com/ITPD-Almo/modular-llm-gateway/pull/8), pull request template in [PR #11](https://github.com/ITPD-Almo/modular-llm-gateway/pull/11), course materials skill in [PR #12](https://github.com/ITPD-Almo/modular-llm-gateway/pull/12), research restructure in [PR #24](https://github.com/ITPD-Almo/modular-llm-gateway/pull/24), product vision and context diagram in [PR #25](https://github.com/ITPD-Almo/modular-llm-gateway/pull/25), and this report. Approved [PR #14](https://github.com/ITPD-Almo/modular-llm-gateway/pull/14#pullrequestreview-5447017406) and [PR #16](https://github.com/ITPD-Almo/modular-llm-gateway/pull/16#pullrequestreview-5447025468). |
| atkond2point0 | Markdown formatting in [PR #20](https://github.com/ITPD-Almo/modular-llm-gateway/pull/20) and the Markdown CI workflow in [PR #21](https://github.com/ITPD-Almo/modular-llm-gateway/pull/21). Attended the meeting. |
| spaghetti-n-spaghetti | No Week 2 contribution recorded. |

## Repository evidence

- Merged pull request that closed its task issue: [PR #16](https://github.com/ITPD-Almo/modular-llm-gateway/pull/16), which closed [#15](https://github.com/ITPD-Almo/modular-llm-gateway/issues/15).
- Latest green link check on `main`: [run 37673365517](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/37673365517).
- Latest green Markdown check on `main`: none yet, because the workflow in [PR #21](https://github.com/ITPD-Almo/modular-llm-gateway/pull/21) is not merged.

The link check excludes `.claude/skills/itpd`, the course materials submodule. The course repository checks its own links, and its files are not our artifacts. Nothing else is excluded.

## Deviations

- **No kickoff.** We had no Week 1 kickoff, so `## Previous action points` and `## Previous open questions` in the meeting report say `None`.
- **Joint meeting.** The October 9 meeting was shared with two other teams. Our part took about 12 of its 37 minutes. Of our team, Ali12hamdan and atkond2point0 attended.
- **Late script.** The meeting script was prepared before the meeting but uploaded afterwards in draft [PR #26](https://github.com/ITPD-Almo/modular-llm-gateway/pull/26). Its candidate part does not list `US-nn` issues, because none were open.
- **No story issues yet.** The stories were drafts, not issues, at the meeting. Since the Customer redefined the core task, we will open revised story issues and ask for a verdict in Week 3 rather than open stories the Customer has already rejected as a candidate.
- **Text prototype.** The prototype was a static text concept, not running code. It still tested our proposed first version with the Customer, and the answer changed the vision.
- **Transcript.** The host announced recording, but recording and transcript-publication permission are unconfirmed. We kept it out of the repository and will include it in the Moodle submission if publication is refused.
- **Roles and authors.** The planned note-taker and observer roles are not confirmed in the meeting record. Ali12hamdan wrote the meeting report and Mohammed-Nour wrote this report, in place of spaghetti-n-spaghetti, who did not take part in the Week 2 work.
- **Markdown CI order.** The formatting fixes ([PR #20](https://github.com/ITPD-Almo/modular-llm-gateway/pull/20)) and the Markdown workflow ([PR #21](https://github.com/ITPD-Almo/modular-llm-gateway/pull/21)) were still under review when this report was written.

## Privacy

No private-only material was committed to this repository.
