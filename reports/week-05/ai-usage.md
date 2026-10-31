# AI usage - Week 5

## Tools

- **Ali12hamdan:** Codex (OpenAI); the automation below is distinguished from personal manual checks and Customer evidence.
- **Mohammed-Nour:** Claude Code (Claude Opus).
- **atkond2point0:** no statement was given by the deadline, so none is recorded here; atkond2point0's task was taken over, as the [report's deviations](README.md#deviations) say.

## What we used them for

- **Ali12hamdan:** Codex implemented the terminal installer/CLI, native platform workflow and guided provider setup in [#92](https://github.com/ITPD-Almo/modular-llm-gateway/pull/92), [#93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93) and [#95](https://github.com/ITPD-Almo/modular-llm-gateway/pull/95); drafted the deployment runbook, placeholder configuration and version alignment in [#102](https://github.com/ITPD-Almo/modular-llm-gateway/pull/102); updated organization issue fields; and reviewed this draft. It also prepared local deployment/evidence helpers and a rescheduled-meeting script. Those local drafts are not published product features or evidence of a completed deployment or meeting.

- **Mohammed-Nour:** reading Assignment 5 against the repository state and proposing the three-way split of the week; drafting the bodies of [US-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96), [US-10](https://github.com/ITPD-Almo/modular-llm-gateway/issues/97) and the tasks [#98](https://github.com/ITPD-Almo/modular-llm-gateway/issues/98) to [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100); reviewing [#92](https://github.com/ITPD-Almo/modular-llm-gateway/pull/92), [#93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93) and [#95](https://github.com/ITPD-Almo/modular-llm-gateway/pull/95); drafting the SPRINT-05 plan, the testing plan, `docs/features.md`, the `CONTRIBUTING.md` rule, this report and the [retrospective](sprint-retrospective.md); and finishing [#103](https://github.com/ITPD-Almo/modular-llm-gateway/pull/103) after taking over [#98](https://github.com/ITPD-Almo/modular-llm-gateway/issues/98): merging `main` into the stale branch, adding the ruff and mypy settings, fixing the type errors, writing the validation tests and the two `QRT-01` sections, and updating the Definition of Done.

- **atkond2point0:** not stated; see [Tools](#tools).

## What we did with the output

- **Ali12hamdan:** Codex inspected the source against the pinned Assignment 5 revision, ran 69 local product tests, Markdown lint and the strict docs build, and checked an installed 0.5.0 wheel outside the checkout with the fake-provider HTTP demo. Native Linux/macOS checks are recorded in the feature PRs. Mohammed-Nour independently approved and merged #93, #95 and #102; Codex merged the already-approved #92 and preserved history while updating the dependencies. VM work so far prepared isolated private runtimes and checked SSH/status; it did not activate a gateway candidate. These are agent-run checks, not a claim that Ali personally replayed each platform or verified campus access. This draft's merge-conflict repair and agent-policy corrections were also made with Codex and need the report owner's review.

- **Mohammed-Nour:** I checked the split and the drafts against the Assignment 5 text and the course requirements before pushing. I read the planned velocity from the stories' `Story Points` fields (2 + 3 + 3 + 5 + 5) rather than taking an estimate. The reviews of #92 and #95 were based on reading the installer, CLI and credential code and on their green CI runs; I did not rerun the installers myself. I rejected a draft feature entry for the one-command install, because no functional requirement owns installation yet and the course does not allow a feature without one. markdownlint and the strict MkDocs build passed on every push. For #103 I ran ruff, mypy, the 81 tests, the wheel build and the strict docs build locally before pushing, and I rehearsed the QR-02 QRT-01 commands against a local gateway; that rehearsal is not counted as the deployed result. Ali12hamdan reviewed #103 instead of me, because I wrote most of it.

- **atkond2point0:** not stated; see [Tools](#tools).

## What was not used

- **Ali12hamdan:** passing agent checks were not used as Customer acceptance, campus verification or a real QR-02 result. No real provider key was supplied to the agent and it made no paid generation request. Personal retrospective input and the other member's AI usage remain unconfirmed rather than being invented.
- **Mohammed-Nour:** passing CI and agent checks were not counted as Customer acceptance; story verdicts come only from the Sprint Review, recorded as `DEC-nnn` entries.
