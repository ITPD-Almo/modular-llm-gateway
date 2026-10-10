# Week 2 validation meeting script

## Context

Corporate IT teams need to control employee access to LLM providers and apply company rules to requests and responses.

We think operators need to know which policy version handled a request, without keeping its prompt in the decision record. We also think a small trial with one provider and static caller credentials could be enough to start. These beliefs are still unverified.

Target: check whether the prototype, product boundary, and Minimum Usable Product candidate solve a useful task for the Customer.

We plan to meet in the next one or two days; the exact time is not confirmed. There was no Week 1 kickoff, so we have no previous meeting actions or questions to carry over. This draft needs the prototype, vision, assumption, and story links before review.

## Agenda

1. Permissions (2 minutes; questions 1-3).
   Show: nothing. Ask each permission separately and note the answers before starting any recording.
2. Prototype (10 minutes; questions 4-7).
   Show: the planned masking example and decision records for two policy versions from `reports/week-02/prototypes.md`. Link pending; confirm the examples are ready before the meeting.
3. Product boundary (7 minutes; questions 8-10).
   Show: the proposed boundary in `docs/product-vision.md` and who handles the jobs we leave out. Link pending.
4. Minimum Usable Product candidate (8 minutes; questions 11-13).
   Core task: an employee sends a request, a company identifier is masked before forwarding, and an operator can find the decision record naming the policy version that handled it.
   Show these three proposed stories, with their acceptance criteria:
   - US-01: reach the provider without holding its key. Issue link pending.
   - US-02: mask company identifiers before forwarding. Issue link pending.
   - US-03: find which policy revision handled a request. Issue link pending.
   Also show the [full story list](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=label%3Auser-story), so the Customer can change the candidate or priorities.
5. Read-back (3 minutes).
   Show: the note taker's list. Read back the decisions, including the verdict on the candidate, and confirm actions with owners and Week 3 due dates. Correct anything we misunderstood.

Planned length: 30 minutes. Ask for 60 if the Customer can give it. The questions marked ★ take priority if time runs short.

## Questions

1. (closed) May we record this meeting?
2. (closed) May we publish a sanitized transcript in the public repository?
3. (closed) If publication is refused, may we share the transcript privately with course instructors?
4. ★ (open) The last time someone asked why a request was blocked or changed, what did you have to look up?
5. (closed) For that case, would the record we are showing identify the policy version and rule you needed?
6. (open) What information is missing from this record before you could use it to explain the decision?
7. (closed) Is keeping prompt and response text out of the decision record acceptable for this trial? This checks ASM-01; its link is pending.
8. ★ (open) Which item on our proposed "will not do" list would prevent you from using the trial, and why?
9. (closed) Are one provider and static caller credentials acceptable for the first trial? This checks ASM-03; its link is pending.
10. (open) Give us a made-up example of a company identifier that must be masked. What should the provider receive instead? This checks ASM-05; its link is pending.
11. ★ (open) Which of these three stories could be removed while still leaving a useful task, and which could not?
12. (open) What is missing for an employee to send a masked request and for an operator to explain how it was handled?
13. (closed) Should any Should Have story join this candidate, or any proposed Must Have story leave it? If yes, name the story and the reason.

## Roles

- Moderator: Ali12hamdan. Ask the questions, keep time, and read back the results.
- Note taker: spaghetti-n-spaghetti. Record permission answers, decisions, actions, open questions, and disagreements.
- Observer: Mohammed-Nour. Record what we did not ask and which questions were not answered.
- Prototype demo: atkond2point0. Show the examples and explain what the prototype tests.

The whole team attends. Listen to objections and record what needs to change.

## Key improvements

Before: "Do you want an audit log?"

After: "The last time someone asked why a request was blocked or changed, what did you have to look up?"

Principle: ask about a real past task instead of inviting agreement with our idea.

Before: "Does this prototype look useful?"

After: "What information is missing from this record before you could use it to explain the decision?"

Principle: ask for specific missing information, so the answer can change the prototype or a requirement.
