# Week 6 meeting script

## Context

The SPRINT-06 Sprint Review took place on Saturday 2026-11-07 with Ali12hamdan and the Customer.
No written script was prepared before that meeting, and none is preserved in the repository or the team's notes.
This page was written on 2026-11-08, after the meeting, and contains two things:

- the [reconstructed agenda](#reconstructed-agenda-of-the-2026-11-07-meeting) of what was actually covered, rebuilt from the Customer's automatic transcript of the call; it is not a plan made beforehand;
- the [follow-up agenda](#agenda) for the next review on Saturday 2026-11-14, which the Customer asked to keep on Saturdays. It is used only if that meeting is held; otherwise its items carry into the Week 7 script.

## Reconstructed agenda of the 2026-11-07 meeting

| Order | Item | What happened | About |
| --- | --- | --- | --- |
| 1 | The Customer's framing | The Customer asked the team to formalise how it works with a customer and to go through the features. | 1 min |
| 2 | Changes since the last review | Ali12hamdan summarised the one-line install for Linux and macOS, the safe plugin lifecycle events, the guided DeepSeek key setup, CI and the university VM deployment. | 3 min |
| 3 | Live install and real-provider demo | Ali12hamdan set up the install and the DeepSeek key in a terminal; the demo request was hard to locate and took most of the time. | 8 min |
| 4 | Customer feedback on the demo | The Customer asked for a demonstration aimed at a DevOps operator's pain points: running plugins, handling bad plugins, deployment. | 8 min |
| 5 | Deployment | The Customer asked for the gateway wrapped in a Docker container brought up with Docker Compose. | 3 min |
| 6 | Plugin interface and loader | The Customer asked to see the code that loads and runs a plugin, and why the design is better than a list of functions called from a main function. | 15 min |
| 7 | Next week and meeting cadence | Ali12hamdan outlined the next week's plan; the Customer kept the meetings on Saturdays and offered asynchronous questions in the channel. | 5 min |

Not covered: the analytics and observability dashboards, the observability test, an AC-by-AC story verdict, the carried open questions and a threshold proposal.

## Agenda

Follow-up review, Saturday 2026-11-14, 30 minutes, held only if it is arranged with the Customer.

| Order | Item | Shown by | Minutes |
| --- | --- | --- | --- |
| 1 | Goal of the review: the telemetry, the diagnosability test and what the threshold should measure next. | Ali12hamdan | 1 |
| 2 | The deployed product on the university VM: `docker compose up` of a released version, then a request through two plugins and a deliberately failing plugin. | Ali12hamdan | 5 |
| 3 | Analytics staging dashboard: the focus-metric chart, the staging `source=smoke` event in the event list and its exclusion from the chart. | atkond2point0 | 3 |
| 4 | Analytics production dashboard: the same chart and query, and no test traffic. | atkond2point0 | 2 |
| 5 | Observability staging dashboard: the `SLI-01` chart and its failure series. | Ali12hamdan | 3 |
| 6 | Observability production dashboard: the same chart and query, unexercised. | Ali12hamdan | 2 |
| 7 | QR-08 QRT-01 result: the failed request's log point with its `request_id`, route and failure labels, the `SLI-01` five-minute P95 query result and the dashboard screenshot. | Mohammed-Nour | 3 |
| 8 | The optional runtime test re-run, if one was run, and the `SLI` it read. | Mohammed-Nour | 1 |
| 9 | US-01 to US-04, US-09, US-11 and US-12, criterion by criterion: ask for a verdict on each story. | Ali12hamdan | 5 |
| 10 | The carried open questions below. | Ali12hamdan | 3 |
| 11 | The threshold proposal from the [Week 6 threshold review](README.md#threshold-review), and the Customer's decision on it. | Mohammed-Nour | 2 |

## Questions

1. Does each story shown pass its criteria? Which criterion fails, if any?
2. Do the analytics and observability dashboards answer questions you recognise as a DevOps operator?
3. Does the diagnosability requirement hold in staging as shown?
4. Should the threshold keep its current measures for TOS-02 and TOS-03, or measure something the telemetry can now count?
5. Is a 250 ms hook deadline with a 504 result for the request acceptable for the next trial?
6. Is policy-version tracking needed, and what request or response content may be kept?
7. Are static caller credentials and the provider limits enough for the trial?
8. Which made-up company-data cases and expected outputs should masking support?
9. Given that LiteLLM ran the same two-plugin workflow, what would make you choose this gateway over writing your own functions or extending an existing gateway?

## Roles

- **Moderator and presenter:** Ali12hamdan.
- **Note taker:** Mohammed-Nour.
- **Demo driver for the dashboards:** atkond2point0.

## Permission questions

Asked at the start, before recording:

1. May we record this meeting?
2. May we publish a de-identified transcript, naming you `Customer`, in the repository?
3. May we share the recording with the instructors?
