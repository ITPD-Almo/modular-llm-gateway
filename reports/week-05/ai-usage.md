# AI usage - Week 5

## Tools

- **Ali12hamdan:** Codex (OpenAI); the automation below is distinguished from personal manual checks and Customer evidence.
- **Mohammed-Nour:** Claude Code (Claude Opus).
- **atkond2point0:** no statement was received at this closeout, so none is recorded here; atkond2point0's task was taken over, as the [report's deviations](README.md#deviations) say.

## What we used them for

- **Ali12hamdan:** Codex implemented the installer/CLI, platform workflow and hidden-input provider setup in [#92](https://github.com/ITPD-Almo/modular-llm-gateway/pull/92), [#93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93) and [#95](https://github.com/ITPD-Almo/modular-llm-gateway/pull/95); prepared the runbook/version alignment in [#102](https://github.com/ITPD-Almo/modular-llm-gateway/pull/102), issue fields and closeout corrections; and independently reviewed #103. It operated the owner-authorized deployment, private HTTPS/code gate and live-provider verification documented in the [evidence](deployment-evidence.md).

- **Mohammed-Nour:** reading Assignment 5 against the repository state and proposing the three-way split of the week; drafting the bodies of [US-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96), [US-10](https://github.com/ITPD-Almo/modular-llm-gateway/issues/97) and the tasks [#98](https://github.com/ITPD-Almo/modular-llm-gateway/issues/98) to [#100](https://github.com/ITPD-Almo/modular-llm-gateway/issues/100); reviewing [#92](https://github.com/ITPD-Almo/modular-llm-gateway/pull/92), [#93](https://github.com/ITPD-Almo/modular-llm-gateway/pull/93) and [#95](https://github.com/ITPD-Almo/modular-llm-gateway/pull/95); drafting the SPRINT-05 plan, the testing plan, `docs/features.md`, the `CONTRIBUTING.md` rule, this report and the [retrospective](sprint-retrospective.md); and finishing [#103](https://github.com/ITPD-Almo/modular-llm-gateway/pull/103) after taking over [#98](https://github.com/ITPD-Almo/modular-llm-gateway/issues/98): merging `main` into the stale branch, adding the ruff and mypy settings, fixing the type errors, writing the validation tests and the two `QRT-01` sections, and updating the Definition of Done.

- **atkond2point0:** not stated; see [Tools](#tools).

## What we did with the output

- **Ali12hamdan:** Codex checked the pinned Assignment 5, ran 81 local product tests plus lint/format/types/wheel build, and checked an installed wheel outside the checkout. Main CI passed 81 tests in 20.90 seconds. Mohammed-Nour independently approved #93/#95/#102; Codex merged approved work and independently reviewed/merged #103. After Ali confirmed campus Wi-Fi presence, Codex performed the deployed QRT and core checks from his workstation with the VPN left running, using route/socket evidence rather than inferring campus location. The separate Nginx configuration passed 25 isolated checks and 29 campus access checks, plus a final anonymous-denial audit. These are agent-run checks for Ali, not a claim he manually replayed them.

- **Mohammed-Nour:** I checked the split and the drafts against the Assignment 5 text and the course requirements before pushing. I read the planned velocity from the stories' `Story Points` fields (2 + 3 + 3 + 5 + 5) rather than taking an estimate. The reviews of #92 and #95 were based on reading the installer, CLI and credential code and on their green CI runs; I did not rerun the installers myself. I rejected a draft feature entry for the one-command install, because no functional requirement owns installation yet and the course does not allow a feature without one. markdownlint and the strict MkDocs build passed on every push. For #103 I ran ruff, mypy, the 81 tests, the wheel build and the strict docs build locally before pushing, and I rehearsed the QR-02 QRT-01 commands against a local gateway; that rehearsal is not counted as the deployed result. Ali12hamdan reviewed #103 instead of me, because I wrote most of it.

- **atkond2point0:** not stated; see [Tools](#tools).

## What was not used

- **Ali12hamdan:** Generated output and passing tests were not counted as Customer acceptance. Ali entered his key himself at the hidden setup prompt and authorized copying its profile through SSH stdin. Agent processes handled the private credential, but its value was not pasted into chat, printed, placed in arguments/.env or committed. Three paid synthetic live calls passed (local, staging and production); the inspected application/proxy logs contained no key/code values. Separate private profiles contain the same account key and are permission-protected plaintext. No personal retrospective feedback or Customer verdict was invented.
- **Mohammed-Nour:** passing CI and agent checks were not counted as Customer acceptance; story verdicts come only from the Sprint Review, recorded as `DEC-nnn` entries.
