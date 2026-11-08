# AI usage - Week 6

## Tools

- **Ali12hamdan:** OpenAI Codex.
- **Mohammed-Nour:** Claude Code (Claude Opus).
- **atkond2point0:** Codex.

## What we used them for

- **Ali12hamdan:** reading the pinned assignment, planning the tasks and their handoffs, implementing the observability exporter and the QR-08 checker, preparing the analytics handoff, and running the automated checks and the loopback rehearsals on the university VM.
- **Mohammed-Nour:** reading Assignment 6 at its pinned commit against the repository and GitHub state; drafting the bodies of [US-11](https://github.com/ITPD-Almo/modular-llm-gateway/issues/110), [US-12](https://github.com/ITPD-Almo/modular-llm-gateway/issues/111), [US-13](https://github.com/ITPD-Almo/modular-llm-gateway/issues/118) and the tasks [#112](https://github.com/ITPD-Almo/modular-llm-gateway/issues/112) to [#117](https://github.com/ITPD-Almo/modular-llm-gateway/issues/117), and the refinement notes on #65, #67, #68 and #97; converting the Customer's automatic transcript into a private de-identified working copy with a small script, to write the meeting report from; drafting the [meeting script](meeting-script.md), the [meeting report](meeting-report.md), DEC-012 to DEC-014, the SPRINT-06 plan, the threshold review, the [retrospective](sprint-retrospective.md) and the [report](README.md).
- **atkond2point0:** repository inspection, implementation drafting, test drafting and documentation structure for the analytics pipeline.

## What we did with the output

- **Ali12hamdan:** the evidence keeps the VM loopback rehearsals separate from the independent campus verification, which is still to be run.
- **Mohammed-Nour:** I checked each draft against the pinned assignment and the course requirements. The private working copy of the transcript was compared line by line with the source, and it is not committed because publication was not asked for. The Customer's feedback was not recorded as story acceptance, and only statements the Customer made explicitly became `DEC-nnn` entries. TOS-04 was set to `Missed` on its date even though the deployment itself was verified a day later. The planned velocity was added by hand from the stories' `Story Points`.
- **atkond2point0:** I accepted the bounded allowlist shape and the separation between instrumentation and dashboard operations after checking it against the existing gateway parent path and the privacy constraints. I changed the generated draft to use the repository's existing FastAPI and TestClient conventions, fake providers and FR/ADR linking style.

## What was not used

- **Mohammed-Nour:** no output was counted as a Customer verdict or as a deployed test result; the recording link, access codes and addresses were kept out of every prompt that produced public text.
- **atkond2point0:** any claim of a live OpenPanel dashboard, campus access, production data or Customer acceptance was rejected, because none of them was verified.
