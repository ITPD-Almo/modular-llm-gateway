# Week 7 meeting script

## Context

The SPRINT-07 Sprint Review and `UT-01` design review is on Saturday 2026-11-14, at a time still to be confirmed with the Customer, and is planned for 50 minutes.
We are working from the problem that a DevOps operator who adds checks to LLM traffic ends up maintaining a growing list of functions around each call.
We believe a configured plugin gateway lets the operator add, order and diagnose those checks without editing the request path.
Since the last review, the Customer has asked for a Docker Compose deployment ([DEC-012](../../docs/decisions.md#dec-012)) and asked why this gateway is better than a list of functions.
The usability test is the first evidence from people outside the team.
Target: get a verdict on each SPRINT-07 story and the Customer's agreement that the `UT-01` design, its participants, its pass bar and the Week 8 session plan will answer the Customer's questions.

## Agenda

1. **Permissions** (2 min). Nothing is shown. Ask questions 1, 2 and 3 one at a time, and start recording only if question 1 is answered yes.
2. **Production and the Compose workflow** (6 min). Ali12hamdan shows the production gateway on the university route from the campus network. He then brings up a versioned image with `docker compose up` per the [Compose instructions](https://github.com/ITPD-Almo/modular-llm-gateway/blob/a8752ecb5434338670554dde47f3b678432dc9c3/docs/deployment.md#versioned-compose-deployment) of the [#129](https://github.com/ITPD-Almo/modular-llm-gateway/pull/129) candidate at `a8752ec`, sends a chat through two plugins and shows the named 504 from the slow plugin. This is the live demo of the unreleased candidate. Question 4.
3. **Dashboards and quality-test results** (4 min). Ali12hamdan shows the four [Week 6 dashboards](../week-06/README.md), then the recorded result of each checked quality test, with the version or date it was tested on. These are release evidence, not part of Saturday's live demo:
   - [QR-02 QRT-01](../../docs/quality-requirements/qr/QR-02.md#qrt-01): Passes on the [campus staging run of 2026-10-31](https://github.com/ITPD-Almo/modular-llm-gateway/blob/c7dce8ff876d31a57ee0ca93d9428d8444473f6c/reports/week-05/deployment-evidence.md#deployed-qr-02-rerun-through-the-https-gate), `REL-05` (`v0.5.0`);
   - [QR-01 QRT-01](../../docs/quality-requirements/qr/QR-01.md#qrt-01): Passes in [the `REL-06` CI run, 95 tests](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/42514546746), `v0.6.0`;
   - [QR-08 QRT-01](../../docs/quality-requirements/qr/QR-08.md#qrt-01): Passes on the [campus staging run of 2026-11-08](https://github.com/ITPD-Almo/modular-llm-gateway/blob/0073150f73e3b755f0f8a29b21cddb1685b7731d/reports/week-06/README.md#qr-08-qrt-01-campus-run), `v0.6.0`, reading the [`SLI-01`](../../docs/observability.md#sli-01) timeout-series P95.

   Question 5.
4. **Stories AC by AC** (14 min). Ali12hamdan runs [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), [US-04](https://github.com/ITPD-Almo/modular-llm-gateway/issues/52), [US-09](https://github.com/ITPD-Almo/modular-llm-gateway/issues/96), [US-11](https://github.com/ITPD-Almo/modular-llm-gateway/issues/110) and [US-12](https://github.com/ITPD-Almo/modular-llm-gateway/issues/111) on the screen, one `AC-nn` at a time: 24 criteria, about 25 seconds each with the verdicts. A criterion already shown live in parts 2 and 3, such as US-04's named 504 or US-11's dashboards, is pointed back to rather than run again. Question 6 is asked after each story. A story whose criteria or verdict could not be covered stays open and is named in the read-back. The rehearsal times this part on its own.
5. **Why this gateway** (4 min). Mohammed-Nour presents the [comparison](../../docs/research/comparison.md) and the [LiteLLM Proxy spike](../week-04/prototypes.md#two-plugin-workflow-on-litellm-proxy), and what the gateway adds over a list of functions. Questions 7 and 8.
6. **`UT-01` design on staging** (10 min). atkond2point0 walks through the [`UT-01` record](https://github.com/ITPD-Almo/modular-llm-gateway/blob/a6fedaf03981b79b06c06ce18c0c82383ac71db8/docs/usability-tests/ut-01/README.md) from [#140](https://github.com/ITPD-Almo/modular-llm-gateway/pull/140), pinned to its reviewed head before the rehearsal:
   - the goal and research questions, the participant profile, and the target of five sessions with three as the minimum;
   - the three fixed tasks, the surveys and the consent;
   - the private repository and the recordings folder, by name only;
   - the session plan and `QR-09 QRT-01`.

   Ali12hamdan then shows the staging seed reset, the `source=usability-test` events in their UTC session window and the custom-plugin marker probe, following the [staging runbook](https://github.com/ITPD-Almo/modular-llm-gateway/blob/a8752ecb5434338670554dde47f3b678432dc9c3/docs/ut01-staging.md) at `a8752ec`. He states what has actually been verified and when the pre-session check runs ([#132](https://github.com/ITPD-Almo/modular-llm-gateway/issues/132)). No participant data or private access details are on the shared screen. Questions 9 to 13.
7. **Open questions from Week 6** (4 min). Mohammed-Nour reads each [open question](../week-06/meeting-report.md#open-questions). If one was already answered in the asynchronous channel, he reads the reply back for confirmation. Questions 14 to 17.
8. **Week 8 plan and threshold** (5 min). Mohammed-Nour shows the [SPRINT-08 tasks](https://github.com/ITPD-Almo/modular-llm-gateway/milestone/6) and the [threshold](../../docs/threshold-of-success.md) for TOS-02 and TOS-03. Both are due 2026-11-13, before any counted session. Questions 18, 19 and 20.
9. **Read-back** (1 min). Nothing new is shown. Mohammed-Nour reads back each decision and action point, with its owner and date. No questions.

The timeboxes add up to 50 minutes: 2 + 6 + 4 + 14 + 4 + 10 + 4 + 5 + 1.
Questions 6, 9 and 12 are the three that would change the project most; ask them even if time runs short.

## Questions

1. (closed) May we record this meeting?
2. (closed) May we publish a sanitized transcript of this meeting in the repository, naming you `Customer`?
3. (closed) If not, may we share the transcript privately with the course instructors?
4. (open) When you last upgraded a service with Compose, what did you check before you trusted the new version, and what is missing from what you just saw?
5. (open) Which of these signals would you look at first after a failed request, and what would you still have to ask the team?
6. (closed) Does this story pass each of its acceptance criteria? If not, which `AC-nn` fails, and why?
7. (open) When you last added a check to LLM traffic, how did you wire it in, and what went wrong as more checks were added?
8. (open) What would the gateway have to do that a list of functions or a LiteLLM callback cannot, for you to choose it?
9. (open) Which of your questions about whether an operator can adopt the gateway would this test leave unanswered?
10. (closed) Are developers or DevOps operators with basic terminal and Python skills, new to this gateway, the right participants? Is five sessions with a minimum of three enough?
11. (open) What would you change in the three tasks, their order or their time limits, so they reflect what an operator does in the first hour?
12. (closed) Is "at least two thirds of at least three valid participants complete the main task unaided" the right bar for `QR-09`? If not, what bar would convince you?
13. (open) What must the Week 8 results show you, beyond the pass or fail, for you to act on them?
14. (closed) Are the 250 ms hook deadline, the 504 result for a slow plugin and the current capacity behaviour acceptable for the trial?
15. (open) What request or response content, if any, may the gateway keep, and do you need to know which policy version handled a request?
16. (closed) Are static caller credentials and the current provider limits enough for the trial?
17. (open) Which made-up company-data cases, with their expected output, should a masking plugin handle?
18. (open) How should we find and book the participants on campus for the week of 2026-11-16, and is there anyone you can introduce us to?
19. (closed) Can we deliver the results, findings and `QR-09` verdict by 2026-11-21?
20. (closed) TOS-02 and TOS-03 cannot be observed by 2026-11-13, because the counted sessions run in Week 8. Should we record them as missed, or move their date to the `UT-01` results on 2026-11-21 by a decision?

## Roles

- **Moderator:** Mohammed-Nour, who also presents the comparison, the open questions and the Week 8 plan.
- **Note taker:** atkond2point0, except during the `UT-01` walkthrough, where Mohammed-Nour takes notes.
- **Observer and timekeeper:** Ali12hamdan outside his demonstrations. During his demonstrations, atkond2point0 keeps time.
- **Demonstrations:** Ali12hamdan shows production, Compose, the dashboards, the stories and staging. atkond2point0 shows the `UT-01` design.
- **Rehearsal:** the whole agenda is run on the presentation machine by 2026-11-13, from the pinned `#129` and `#140` refs above, with part 4 timed on its own.

## Key improvements

| Before | After | Principle |
| --- | --- | --- |
| "Do you like our usability test design?" | Question 9: "Which of your questions about whether an operator can adopt the gateway would this test leave unanswered?" | Ask about the Customer's own unanswered need rather than for approval, which invites a polite yes. |
| "Is a 250 ms plugin deadline OK?" | Question 14 keeps the closed form, and question 4 asks what the Customer checked when they last upgraded a service. | Ask about what the Customer actually did last time before asking for a yes or no on our number. |
| "Why would you not use LiteLLM?" | Question 8: "What would the gateway have to do that a list of functions or a LiteLLM callback cannot, for you to choose it?" | Ask for the deciding condition, not for a defence of the status quo. |
