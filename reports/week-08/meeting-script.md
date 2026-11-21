# Week 8 customer results review script

Prepared locally for the scheduled November 21 review; that review was cancelled. Published during closeout and retained as the proposed rescheduled agenda, not evidence of a completed meeting.

## Context

Company operators need configurable policy processing around LLM calls with understandable failure behavior; this review tests the versioned Compose/plugin workflow and settles its acceptance and the next concrete policy trial using the available technical and usability evidence.

## Agenda

1. **2 minutes.** Ask the three permission questions separately and agree the review's scope, questions 1–3.
2. **7 minutes.** Identify the shared production deployment and available campus route; show the pinned local Compose image, default chat, configuration-only policy and relevant story criteria, questions 4–5. Clearly identify any local substitute and its limitation.
3. **4 minutes.** Show startup rejection, invalid hook output, timeout and same-container recovery, then the actual runner code, questions 6–7.
4. **4 minutes.** Show staging and production analytics and observability, SLI-01 and the dated deployed QR-08 evidence; identify missing or stale observations, question 8.
5. **4 minutes.** Show current sanitized UT-01 results, findings, task issues and QR-09 QRT-01 verdict when genuine results exist. Otherwise show the exact evidence shortfall and unchanged pass bar, questions 9–10.
6. **4 minutes.** Propose the next policy increment and discuss carried access, retention and policy-version questions, questions 11–13.
7. **3 minutes.** Read back actual story verdicts, any changed scope or threshold, and at least two action points with owners and Week 9 due dates, question 14.
8. **2 minutes.** Confirm unresolved questions and the next review arrangements, question 15.

Plan thirty minutes and request sixty if possible. Use the extra time for the seven-story, twenty-four-criterion checklist in Ali's speaker script. A criterion not actually shown has no verdict. Configuration evaluation is excluded from this customer agenda.

## Questions

1. **Closed.** May we record this meeting?
2. **Closed.** May we publish a sanitized transcript in the project repository?
3. **Closed.** If publication is declined, may we share the recording or transcript privately with the instructors?
4. **Open.** In the last LLM integration you operated, where did changing a company rule require an application change?
5. **Closed, repeated per shown story.** Having seen each named acceptance criterion for US-01, US-02, US-03, US-04, US-09, US-11 or US-12, do you accept that story, or which criterion failed?
6. **Open.** What did you expect to happen when this plugin failed that the demonstrated behavior did not provide?
7. **Closed.** Are the proposed 250 ms per-hook deadline, named HTTP 504 and bounded-worker trial behavior acceptable, or does a specific legitimate case require a change?
8. **Open.** Looking at this request ID, failure series and usage chart, what information would you still need to investigate an incident?
9. **Open.** What do the actual observed task outcomes change about the next increment? If there is no counted outcome yet, what decision must wait for that evidence?
10. **Closed.** Do you agree to keep the predeclared QR-09 bar of at least two-thirds unaided main-task completion among at least three valid participants? Historical threshold dates stay as recorded unless a new decision explicitly changes a future goal.
11. **Open.** Which one synthetic company-data rule should be implemented next, and what exact input/output cases should it pass?
12. **Open.** What content may the trial retain, and must an operating decision be linked to the active policy version?
13. **Open.** What access identities and provider limits are required for the next trial beyond the current static demo codes?
14. **Closed.** Is this readback of the actual accepted or rejected stories, changes, owners and due dates correct?
15. **Open.** What remains unanswered, and what should the next review settle?

## Roles

Proposed before the call: Ali12hamdan moderates and operates the demo; Mohammed-Nour takes notes and records story verdicts; atkond2point0 observes, keeps time and prepares the current-week report. Confirm attendance and roles before starting. The customer is not a usability participant.

## Key improvements

- Before: “Do you like our plugin gateway?” After: “In the last LLM integration you operated, where did changing a company rule require an application change?” The rewrite asks about experienced work and exposes whether the proposed runtime removes a real cost.
- Before: “Are the dashboards good?” After: “Looking at this request ID, failure series and usage chart, what information would you still need to investigate an incident?” The rewrite grounds feedback in the demonstrated operating task.
