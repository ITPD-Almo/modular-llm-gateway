# Week 02 report

## Project

Modular LLM Gateway, course team 9. Week 2 covers Assignment 2: issue tracking, the decisions and assumptions logs, the research restructure, the product vision, the first prototype, and our first meeting with our own Customer.

Read the [meeting report](meeting-report.md) first. It records what the Customer changed.

## Summary

We moved the Week 1 decisions and assumptions into their own logs, restructured the research around its identifiers, and wrote a product vision with a system context diagram. On October 9 we showed the Customer a text concept of a masking flow and a policy-version record, in a joint meeting with two other teams.

We were wrong about what mattered first. We had centred the first version on masking and finding the policy revision behind a decision. The Customer said the missing part was how plugins connect to the gateway: their inputs, outputs, execution order, and loading. The Customer also defined the first usable workflow as starting the system, adding two simple plugins, sending a request, and seeing the result. The meeting did not establish policy-version tracking as our advantage, and our three draft stories need revision after the feedback.

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
| Meeting script | [reports/week-02/meeting-script.md](meeting-script.md), unchanged from the original draft; the [dated preparation status](meeting-preparation-status.md) links the available artifacts and records what was missing. |
| Customer validation | [reports/week-02/meeting-report.md](meeting-report.md). The transcript is not public, because publication permission is unconfirmed; see Deviations. |
| AI usage | [reports/week-02/ai-usage.md](ai-usage.md) |

## Minimum Usable Product Candidate

**Core task:** a DevOps operator starts the gateway, adds two simple plugins, sends a request, and sees the plugins' effect on the request and the result.

**Stories:** none yet. The candidate we took to the meeting was three draft `Must Have` stories: reaching the provider without holding its key, masking company identifiers, and finding which policy revision decided a request. They were not opened as issues before the meeting.

**Verdict:** not given. The Customer clarified the core task above, per [DEC-005](../../docs/decisions.md#dec-005), so the three stories need revision after the feedback. They were not explicitly rejected. The revised `Must Have` stories and the Customer's verdict on them are unfinished and due in Week 3.

## What changed after the prototype

[CON-01](../../docs/product-vision.md#con-01) now requires the next design to show plugin inputs, outputs, execution order, and loading, because the Customer said our text concept did not explain how plugins connect, per [DEC-006](../../docs/decisions.md#dec-006).

## Contribution

| GitHub username | Work |
| --- | --- |
| Ali12hamdan | Decisions log in [PR #14](https://github.com/ITPD-Almo/modular-llm-gateway/pull/14), assumptions log in [PR #16](https://github.com/ITPD-Almo/modular-llm-gateway/pull/16), meeting script in [PR #26](https://github.com/ITPD-Almo/modular-llm-gateway/pull/26), meeting report and DEC-003 to DEC-006 in [PR #28](https://github.com/ITPD-Almo/modular-llm-gateway/pull/28). Presented and asked our questions in the meeting. Approved [PR #8](https://github.com/ITPD-Almo/modular-llm-gateway/pull/8#pullrequestreview-5445684123), [PR #11](https://github.com/ITPD-Almo/modular-llm-gateway/pull/11#pullrequestreview-5445810373), and [PR #12](https://github.com/ITPD-Almo/modular-llm-gateway/pull/12#pullrequestreview-5445863178). Requested changes on [PR #20](https://github.com/ITPD-Almo/modular-llm-gateway/pull/20#pullrequestreview-5471788745), [PR #21](https://github.com/ITPD-Almo/modular-llm-gateway/pull/21#pullrequestreview-5471790064), and [PR #24](https://github.com/ITPD-Almo/modular-llm-gateway/pull/24#pullrequestreview-5472673165). |
| Mohammed-Nour | Issue forms and labels in [PR #8](https://github.com/ITPD-Almo/modular-llm-gateway/pull/8), pull request template in [PR #11](https://github.com/ITPD-Almo/modular-llm-gateway/pull/11), course materials skill in [PR #12](https://github.com/ITPD-Almo/modular-llm-gateway/pull/12), research restructure in [PR #24](https://github.com/ITPD-Almo/modular-llm-gateway/pull/24), product vision and context diagram in [PR #25](https://github.com/ITPD-Almo/modular-llm-gateway/pull/25), and this report. Approved [PR #14](https://github.com/ITPD-Almo/modular-llm-gateway/pull/14#pullrequestreview-5447017406) and [PR #16](https://github.com/ITPD-Almo/modular-llm-gateway/pull/16#pullrequestreview-5447025468). |
| atkond2point0 | Markdown formatting in [PR #20](https://github.com/ITPD-Almo/modular-llm-gateway/pull/20), the Markdown CI workflow in [PR #21](https://github.com/ITPD-Almo/modular-llm-gateway/pull/21), and policy-decision spike evidence in [PR #37](https://github.com/ITPD-Almo/modular-llm-gateway/pull/37). Attended the meeting. Disposable spike code stayed off main. |
| spaghetti-n-spaghetti | Former member. Ali12hamdan and Mohammed-Nour took over their tasks. |

## Repository evidence

- Merged pull request that closed its task issue: [PR #16](https://github.com/ITPD-Almo/modular-llm-gateway/pull/16), which closed [#15](https://github.com/ITPD-Almo/modular-llm-gateway/issues/15).
- Green link check on `main` after PR #28 merged: [run 38083765574](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/38083765574).
- Green Markdown check on the same `main` revision: [run 38083765699](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/38083765699). The workflow from [PR #21](https://github.com/ITPD-Almo/modular-llm-gateway/pull/21) is merged.

These runs checked main at `1af654a`. Check both workflows again on the final merged revision before submitting.

The link check excludes `.claude/skills/itpd`, the course materials submodule. The course repository checks its own links, and its files are not our artifacts. Nothing else is excluded.

## Deviations

- **No kickoff.** We had no Week 1 kickoff, so `## Previous action points` and `## Previous open questions` in the meeting report say `None`.
- **Joint meeting.** The October 9 meeting was shared with two other teams. Our part took about 12 of its 37 minutes. Of our team, Ali12hamdan and atkond2point0 attended.
- **Late script.** The meeting script was prepared before the meeting but uploaded afterwards in [PR #26](https://github.com/ITPD-Almo/modular-llm-gateway/pull/26). It is now merged, with the original missing artifact and story links preserved. A separate [October 10 status note](meeting-preparation-status.md) links the available work. This does not complete the preparation that was missing before the meeting.
- **No story issues yet.** The stories were drafts, not issues, at the meeting. Since the Customer clarified the core task, the stories need revision after the feedback. We will open the revised story issues and ask for a verdict in Week 3. This is unfinished.
- **Text prototype.** We showed a static text concept, not running code. It tested our proposed first version with the Customer, and the answer changed the vision. The [prototype record](prototypes.md) also includes Sergey's later runnable spike; that spike was not shown in the meeting and did not implement the requested two-plugin interaction.
- **Transcript.** The host announced recording, but recording and transcript-publication permission are unconfirmed. Private sharing is also unconfirmed. We kept the transcript out of the repository, and will upload it to Moodle only if the Customer permits private sharing.
- **Roles and authors.** The planned note-taker and observer roles are not confirmed in the meeting record. Ali12hamdan wrote the meeting report and Mohammed-Nour wrote this report.
- **Team change.** spaghetti-n-spaghetti left the team, and Ali12hamdan and Mohammed-Nour took over their tasks. The team now has three active members, so [CON-02](../../docs/product-vision.md#con-02) and [ASM-06](../../docs/assumptions.md#asm-06) now say three.
- **Tasks created through the API.** Tasks [#27](https://github.com/ITPD-Almo/modular-llm-gateway/issues/27) and [#38](https://github.com/ITPD-Almo/modular-llm-gateway/issues/38) were created through the GitHub API with the Task form's fields while carrying out Ali12hamdan's requests from the terminal. The web form was not submitted.
- **Markdown CI order.** The first report draft was written while [PR #20](https://github.com/ITPD-Almo/modular-llm-gateway/pull/20) and [PR #21](https://github.com/ITPD-Almo/modular-llm-gateway/pull/21) were under review. Both are now merged and main passes both checks.
- **Checklist review.** PRs #26 and #28 were merged while their task checklists were unchecked. The preparation links and specific candidate verdict were still missing. We are recording those gaps rather than marking them as passed.
- **Report publication.** [PR #32](https://github.com/ITPD-Almo/modular-llm-gateway/pull/32) and [PR #33](https://github.com/ITPD-Almo/modular-llm-gateway/pull/33) were merged into the meeting-report branch after PR #28 merged, so their files did not reach main. Task #38 brings that work to main through a follow-up PR, preserving the original commits.

## Privacy

No private-only material was committed to this repository.
