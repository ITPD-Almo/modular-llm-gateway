# Week 01 report

## Project

Modular LLM Gateway, course team 9. Draft report, not ready for submission.

Problem-space hypothesis: corporate IT teams need to apply company-specific rules to employee LLM requests and responses while controlling provider access. We still need our own customer evidence to identify a narrower unmet need.

## Summary

We evaluated Portkey, Azure API Management, and LiteLLM. Existing products already provide substantial routing, filtering, and extension capabilities. A plugin system or custom regex alone does not establish a market gap.

Two provisional gaps and two corresponding value propositions are drafted. They need customer validation and checks against existing extension options before we commit to building them. No implementation or prototype is included this week.

## Coverage

| Required deliverable | Artifact or evidence | Status |
| --- | --- | --- |
| Broad candidate search, 10+ candidates | [Candidate list](candidate-list.md) | Draft added after detailed research; sequence deviation below. |
| Three or four detailed alternatives | [Alternatives](../../docs/research/alternatives.md) | Three documented; ALT-03 is in draft PR #5. |
| Qualitative comparison, six or more properties | [Comparison](../../docs/research/comparison.md) | Draft; agreement before evaluation is not evidenced here. |
| Gap analysis and rejected gaps | [Gap analysis](../../docs/research/gap-analysis.md) | Provisional; four-test validation incomplete. |
| Two or three value propositions | [Value propositions](../../docs/research/value-proposition.md) | Two drafts with assumptions and follow-up checks. |
| Two screenshots per alternative and external board | [Research board](https://miro.com/app/board/uXjVEeQDS7A=/), [LiteLLM hooks](images/alt-03-litellm-hooks.png), [LiteLLM OSS/enterprise](images/alt-03-litellm-oss-enterprise.png) | ALT-03 images show official documentation, not a deployed test. Upload them to the board; confirm all six images and anonymous view-only access. |
| Own customer kickoff script, report, and notes or transcript | Pending | Skipped in this work session at the team's request; remains required. |
| AI usage disclosure | [AI usage](ai-usage.md) | Draft; other members must confirm their usage. |
| Public repository and MIT license | [Repository](https://github.com/ITPD-Almo/modular-llm-gateway), [MIT license](../../LICENSE) | Present. Team number is absent from current GitHub names; resolve with course staff before renaming. |
| Reviewed merged PR and green main CI | [PR #1](https://github.com/ITPD-Almo/modular-llm-gateway/pull/1), [successful main link check](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/37362230041) | Historical green evidence. The [latest main run](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/37364669033) failed because GitHub could not allocate a hosted runner; a rerun is being requested. Latest main must pass before submission. |
| Branch protection evidence | [Review rules](images/branch-protection-reviews.png) show protection for `main`, one required approval, and stale approval dismissal. [Check rules](images/branch-protection-checks.png) show the required `links` check, up-to-date branches, and no administrator bypass. | Both screenshots inspected and included in this report. |
| Each member contributes through a PR and reviews another | Contribution table below | Incomplete for two members; their write-access invitations are still pending acceptance. |
| Private Moodle PDF and ZIP of same revision | Pending, kept outside public repository | Prepare after all required work is merged and final revision is known. |

No links are excluded from the link check: `.lycheeignore` contains only a comment. There are no exclusion justifications to provide.

## Contribution

| GitHub username | Recorded work |
| --- | --- |
| Ali12hamdan | Repository setup in [PR #1](https://github.com/ITPD-Almo/modular-llm-gateway/pull/1); LiteLLM research and draft synthesis in [PR #5](https://github.com/ITPD-Almo/modular-llm-gateway/pull/5); [approved PR #2](https://github.com/ITPD-Almo/modular-llm-gateway/pull/2#pullrequestreview-5419376762) and [PR #3](https://github.com/ITPD-Almo/modular-llm-gateway/pull/3#pullrequestreview-5419628206). |
| Mohammed-Nour | Portkey in [PR #2](https://github.com/ITPD-Almo/modular-llm-gateway/pull/2), Azure and comparison in [PR #3](https://github.com/ITPD-Almo/modular-llm-gateway/pull/3), approval of [PR #1](https://github.com/ITPD-Almo/modular-llm-gateway/pull/1). |
| spaghetti-n-spaghetti | Own contribution PR and review evidence still needed. |
| atkond2point0 | Own contribution PR and review evidence still needed. The ALT-03 draft prepared by Ali12hamdan does not count as this member's contribution. |

## Deviations and open work

The broader candidate list was documented after the first detailed evaluations to recover missing search evidence. This does not establish that the required broad-search-first process was followed.

The report is being prepared after the assignment deadline. The team's own kickoff is still missing; another team's meeting is background only. Gap validation, board permissions, remaining member contributions, and the final private submission are still open.

## Privacy

No private-only material is included in this report or the local draft changes; recordings, personal identity mappings, university emails, and credentials must stay out of the public repository.
