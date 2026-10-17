# Week 3 written validation script

## Context

Prepared on October 17 for a written follow-up after the October 16 joint meeting. This is not the preparation for that earlier call.

DevOps operators need to load company plugins, run requests through them, and understand the result. Our candidate is [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), following [DEC-005](../../docs/decisions.md#dec-005) and [DEC-006](../../docs/decisions.md#dec-006).

Target: obtain an accept or reject verdict on each story's actual behaviour and settle whether the candidate needs a third example plugin.

Do not send the demo until task [#43](https://github.com/ITPD-Almo/modular-llm-gateway/issues/43) is merged and checked from a clean checkout. Use the real commands and results from that revision, one acceptance criterion at a time. Keep expected behaviour separate from observed results.

## Agenda

1. Permissions, questions 1-3. Show nothing; explain that the review is in writing.
2. US-01, questions 4-7. Show the configuration, clean-start command, actual plugin order, and the result after changing the configuration and restarting. Link the merged setup page and the evidence for all three criteria before sending.
3. US-02, questions 8-10. Show the merged plugin documentation and both example plugins, then demonstrate that each uses the documented interface.
4. US-03, questions 11-14. Show the documented request command, actual response and ordered plugin trace, and a repeat run using the fake provider without a real key.
5. Candidate scope, questions 15-16. Show the three linked stories and their Must Have priorities. Ask about the joint meeting's three-plugin example rather than assuming our two-plugin candidate was accepted or rejected.
6. Next work, question 17. Show any failure observed during the demo and the proposed follow-up for identifying failed or stuck plugins.
7. Read-back, question 18. Send a short list of the verdicts, failed criteria, scope changes, and proposed actions with their owners and Week 4 dates.

## Questions

1. (closed) May we keep this written exchange as the record of this review? No audio or video recording is planned.
2. (closed) May we publish a sanitized version of the exchange in our public repository?
3. (closed) If public publication is refused, may we share it privately with the course instructors?
4. (closed) For US-01 AC-01, does the clean-checkout demonstration start the gateway with two configured plugins as required?
5. (closed) For US-01 AC-02, does the observed execution order match the configuration?
6. (open) For US-01 AC-03, what changed in the result after changing the configuration and restarting?
7. (closed) Do you accept or reject US-01? If rejected, name the failed AC-nn and what you expected instead.
8. (closed) For US-02 AC-01, does the documentation explain the inputs, outputs, ordering, loading, and failure behaviour clearly enough?
9. (closed) For US-02 AC-02, do both examples use only that documented interface?
10. (closed) Do you accept or reject US-02? If rejected, name the failed AC-nn and what is missing.
11. (closed) For US-03 AC-01, does the documented request reach the fake provider and return a response?
12. (closed) For US-03 AC-02, does the response or log show each plugin's request and response changes in order?
13. (closed) For US-03 AC-03, does the repeat run demonstrate deterministic behaviour without a real provider key?
14. (closed) Do you accept or reject US-03? If rejected, name the failed AC-nn and what you expected instead.
15. (closed) You mentioned three plugins in the joint meeting. Are two example plugins enough for this sprint, or must a third be included before you accept the candidate?
16. (open) Which story, if any, must be added or removed before this set completes a useful task for you?
17. (open) From the behaviour shown, what information is missing to identify a plugin that failed or stopped responding?
18. (closed) Does our read-back correctly record your verdicts and the next actions? Please correct any owner, date, or conclusion we misunderstood.

## Key improvements

Before: "Does the gateway look good?"

After: "For US-01 AC-03, what changed in the result after changing the configuration and restarting?"

Principle: ask about observed behaviour against one criterion, so the answer can expose a failed requirement.
