# Week 01 report

## Project

Modular LLM Gateway, course team 9. Draft report, not ready for submission.

We are looking at how corporate IT teams can control access to LLM providers and apply company rules to requests and responses. We still need feedback from our own Customer to confirm which problems are worth solving.

## Summary

We researched Portkey, Azure API Management, and LiteLLM. They already offer routing, filtering, and ways to add custom logic. Having plugins or custom regex is not enough to make our project different.

We drafted two possible gaps: linking each policy decision to the policy version used, and making a small policy trial easier to set up. We also wrote two value propositions based on them. These are still ideas to check, not confirmed advantages. We have not built a gateway or prototype.

## Coverage

| Required deliverable | Artifact or evidence | Status |
| --- | --- | --- |
| Broad candidate search, 10+ candidates | [Candidate list](candidate-list.md) | 10 candidates recorded after the detailed research; explained below. |
| Three or four detailed alternatives | [Alternatives](../../docs/research/alternatives.md) | Three documented; PR #5 is approved and awaiting its required check before merge. |
| Qualitative comparison, six or more properties | [Comparison](../../docs/research/comparison.md) | Six properties compared. We have not recorded evidence that the team agreed on them before evaluation. |
| Gap analysis and rejected gaps | [Gap analysis](../../docs/research/gap-analysis.md) | Both gaps are provisional and have not passed all four tests. |
| Two or three value propositions | [Value propositions](../../docs/research/value-proposition.md) | Two draft proposals with tradeoffs and checks to do. |
| Two screenshots per alternative and external board | [Research board](https://miro.com/app/board/uXjVEeQDS7A=/), [LiteLLM hooks](images/alt-03-litellm-hooks.png), [LiteLLM OSS/enterprise](images/alt-03-litellm-oss-enterprise.png) | ALT-03 images show official documentation, not a deployed test. Upload them to the board; confirm all six images and anonymous view-only access. |
| Own customer kickoff script, report, and notes or transcript | Missing | We have not met our Customer or had a written exchange. We used another team's transcript as background; our own kickoff is still missing. |
| AI usage disclosure | [AI usage](ai-usage.md) | Draft; other members must confirm their usage. |
| Public repository and MIT license | [Repository](https://github.com/ITPD-Almo/modular-llm-gateway), [MIT license](../../LICENSE) | Present. Team number is absent from current GitHub names; resolve with course staff before renaming. |
| Reviewed merged PR and green main CI | [PR #1](https://github.com/ITPD-Almo/modular-llm-gateway/pull/1), [successful main link check](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/37362230041) | An earlier main check passed. The [latest main run](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/37364669033) could not get a GitHub runner. Its rerun is queued; latest main must pass before submission. |
| Branch protection evidence | [Review rules](images/branch-protection-reviews.png) show protection for `main`, one required approval, and stale approval dismissal. [Check rules](images/branch-protection-checks.png) show the required `links` check, up-to-date branches, and no administrator bypass. | Both screenshots inspected and included in this report. |
| Each member contributes through a PR and reviews another | Contribution table below | Incomplete for two members; their write-access invitations are still pending acceptance. |
| Private Moodle PDF and ZIP of same revision | Pending, kept outside public repository | Prepare after all required work is merged and final revision is known. |

We have not excluded any links from the link check.

## Contribution

| GitHub username | Recorded work |
| --- | --- |
| Ali12hamdan | Repository setup in [PR #1](https://github.com/ITPD-Almo/modular-llm-gateway/pull/1); LiteLLM research and draft synthesis in [PR #5](https://github.com/ITPD-Almo/modular-llm-gateway/pull/5); [approved PR #2](https://github.com/ITPD-Almo/modular-llm-gateway/pull/2#pullrequestreview-5419376762) and [PR #3](https://github.com/ITPD-Almo/modular-llm-gateway/pull/3#pullrequestreview-5419628206). |
| Mohammed-Nour | Portkey in [PR #2](https://github.com/ITPD-Almo/modular-llm-gateway/pull/2), Azure and comparison in [PR #3](https://github.com/ITPD-Almo/modular-llm-gateway/pull/3), approval of [PR #1](https://github.com/ITPD-Almo/modular-llm-gateway/pull/1). |
| spaghetti-n-spaghetti | Own contribution PR and review evidence still needed. |
| atkond2point0 | Own contribution PR and review evidence still needed. The ALT-03 draft prepared by Ali12hamdan does not count as this member's contribution. |

## Deviations and open work

We added the full candidate list after researching the first alternatives. This was different from the required order of searching widely first.

We are preparing this report after the deadline. We could not meet with our Customer and have not received written feedback. Our own kickoff is missing, so we have no Customer-approved decisions or action points.

We read another team's kickoff transcript to understand the project, including request and response handling, plugins, and a possible first proxy. We did not attend their meeting. Their decisions belong to their team and do not confirm our gaps. We have kept the raw transcript out of this repository.

GAP-01, GAP-02, VP-01, and VP-02 remain provisional. We still need to check that users need them and that existing products do not already meet those needs. Reading the other team's transcript does not replace our kickoff. Board access, the remaining member contributions, and the private submission still need finishing.

## Privacy

No private-only material was committed to this repository.
