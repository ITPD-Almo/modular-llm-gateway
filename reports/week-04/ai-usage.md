# AI usage - Week 4

## Tools

- **Ali12hamdan:** OpenAI Codex.
- **Mohammed-Nour:** Claude Code (Claude Opus).
- **atkond2point0:** Week 4 statement not provided for this submission.

## What we used them for

- **Ali12hamdan:** inspecting repository and session history and the supplied meeting source; A4 planning and the two-person issue allocation; the diagnostics and timeout implementation; requirements and pull request review; architecture, ADR and capacity requirement drafts; tracker forms and workflow; the sanitized meeting account and a private follow-up draft. Source: Ali12hamdan's statement on [#61](https://github.com/ITPD-Almo/modular-llm-gateway/issues/61).

- **Mohammed-Nour:** building the disposable LiteLLM Proxy spike ([#74](https://github.com/ITPD-Almo/modular-llm-gateway/pull/74)) and writing the matched comparison ([#75](https://github.com/ITPD-Almo/modular-llm-gateway/pull/75)); drafting the original October 22 meeting script; drafting the quality and functional requirements ([#73](https://github.com/ITPD-Almo/modular-llm-gateway/pull/73)), the setup and plugin guides with the A/B example and demo ([#76](https://github.com/ITPD-Almo/modular-llm-gateway/pull/76)), and `AGENTS.md` ([#78](https://github.com/ITPD-Almo/modular-llm-gateway/pull/78)); running reviews of [#69](https://github.com/ITPD-Almo/modular-llm-gateway/pull/69), [#71](https://github.com/ITPD-Almo/modular-llm-gateway/pull/71), [#72](https://github.com/ITPD-Almo/modular-llm-gateway/pull/72), [#77](https://github.com/ITPD-Almo/modular-llm-gateway/pull/77), [#80](https://github.com/ITPD-Almo/modular-llm-gateway/pull/80), [#81](https://github.com/ITPD-Almo/modular-llm-gateway/pull/81) and [#83](https://github.com/ITPD-Almo/modular-llm-gateway/pull/83); and drafting this report and the [retrospective](sprint-retrospective.md).

## What we did with the output

- **Ali12hamdan:** the agent ran local pytest suites, real HTTP request and response timeouts with twenty-timeout recovery, process and thread counts, 4/8/20 healthy-load bursts, a fresh-clone replay of the guide, Markdown and strict builds, and live GitHub field readbacks. These are agent-run checks, not a claim that Ali12hamdan ran every command personally. Drafts were revised after review, Customer requests were kept separate from team-proposed numbers, and private access inputs stayed outside Git. A first issue-field script replaced instead of merging the field values; the readback caught it, the saved values were restored, and the script was fixed to submit the full set.

- **Mohammed-Nour:** runtime-related reviews used agent-run pytest, strict documentation builds and real HTTP checks with throwaway plugins outside the repository: exceptions, malformed output, both timeout stages, repeated timeouts with child-process counts, and synthetic secrets in prompts and exception text. The linked reviews record their particular checks; this does not claim every documentation review repeated the whole HTTP suite. The reviews requested changes where a rule or criterion was not met. I confirmed the [October 23 meeting report](meeting-report.md) against my own attendance, because the source recording was not on my machine. Drafts were edited before each push, and markdownlint and the strict build passed.

## What was not used

- **Ali12hamdan:** suggestions were not used as proof of story acceptance, of a ceremony that did not happen, or of permission answers absent from the source.

- **Mohammed-Nour:** the LiteLLM spike code was not merged; [#74](https://github.com/ITPD-Almo/modular-llm-gateway/pull/74) was closed as the prototype rules require. Passing tests and agent checks were not counted as Customer acceptance, so Actual Velocity stays 0. The retrospective's actions are team proposals, not outcomes of a held retrospective meeting.
