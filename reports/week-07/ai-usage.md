# AI usage - Week 7

## Tools

- **Ali12hamdan:** OpenAI Codex.
- **Mohammed-Nour:** Claude Code (Claude Opus).
- **atkond2point0:** Codex (OpenAI). The agent-assisted drafting below is separate from participant evidence, teammate dry-run evidence and Customer acceptance.

## What we used them for

- **Ali12hamdan:** implementing and testing the Compose package, the staging event export and the offline probe, drafting the customer walkthrough and documenting the recorded checks.
- **Mohammed-Nour:**
  - Reading Assignment 7 at its pinned commit against the repository and GitHub state.
  - Drafting the SPRINT-07 and SPRINT-08 plan and the task issues [#130](https://github.com/ITPD-Almo/modular-llm-gateway/issues/130), [#131](https://github.com/ITPD-Almo/modular-llm-gateway/issues/131) and [#132](https://github.com/ITPD-Almo/modular-llm-gateway/issues/132) to [#138](https://github.com/ITPD-Almo/modular-llm-gateway/issues/138), and the [meeting script](meeting-script.md).
  - Reviewing [#129](https://github.com/ITPD-Almo/modular-llm-gateway/pull/129), [#140](https://github.com/ITPD-Almo/modular-llm-gateway/pull/140) and [#141](https://github.com/ITPD-Almo/modular-llm-gateway/pull/141) against their acceptance criteria and the course requirements, including running the link and Markdown checks.
  - Completing this report's coverage and evidence.
- **atkond2point0:**
  - Reading the pinned ITPD Assignment 7 and usability-testing requirements.
  - Inspecting issue #131 and PR #129's public bring-up contract.
  - Drafting the UT-01 record, task scenarios, surveys, consent template, session template, results stub, QR-09/QRT-01, glossary terms and risks.
  - Keeping participant identities, recordings, private links, raw notes and credentials out of the repository.

## What we did with the output

- **Ali12hamdan:**
  - **Accepted:** the pinned-image workflow, the UTC-window export and the offline marker probe, after testing them. The walkthrough uses synthetic data and shows the configured plugin, its visible result and the follow-up after a named 504.
  - **Changed:** the walkthrough uses one small custom request hook to show an operator adding behavior through the configuration. The staged telemetry implementation check and the teammate exercise have separate records.
  - **Rejected:** treating the local Compose run as a campus access result, a participant result or a customer verdict. It is product rehearsal evidence only.
- **Mohammed-Nour:**
  - **Checked:** each draft against the pinned assignment and the course requirements. I checked the planned velocity by hand against the saved `Story Points` fields.
  - **Changed:** after Ali's review, I repinned the script's demo and evidence links to the reviewed commits.
  - **Review findings:** I accepted these only after reading the files myself: the malformed results table, the missing risk fields, the QRT format and an "applied" push that contained only a merge of `main`.
  - **Not decided by the agent:** approval of #140's private access and dry-run criteria rested on my own private confirmation, not on agent output.
- **atkond2point0:**
  - **Checked:** the bar has the same meaning across the record, the analysis plan and the QRT: at least 2/3 of at least 3 valid participants completing the main task unaided.
  - **Still to do by the team:** review the wording, run the uncounted teammate dry run, apply its wording, time-limit and instrumentation changes, verify the instrumentation before the first counted session, and obtain the design-review notes.

## What was not used

- **Ali12hamdan:** Codex used the public test design, consent template, survey and synthetic fixture descriptions. It received no participant identity, consent record, raw usability note or participant recording.
- **Mohammed-Nour:**
  - **Usability material:** the agent read only the public UT-01 design files. It was given no participant identity, consent record, raw note, recording or private usability-data repository content.
  - **No invented outcomes:** no output was recorded as a Customer verdict, a meeting outcome or a test result.
  - **Private values:** addresses, credentials and recording links were kept out of every prompt that produced public text.
- **atkond2point0:** no participant material, recording, personal data, provider key or private access credential was supplied to the agent or committed. The draft is not usability evidence and claims no counted session.
