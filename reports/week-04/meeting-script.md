# Week 4 meeting script

## Context

DevOps operators need to load company plugins, run requests through them, and understand the result. Our candidate is [US-01](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40), [US-02](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41), and [US-03](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42), released as [v0.1.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.1.0). The Customer has not yet seen them demonstrated; the [Week 3 meeting report](../week-03/meeting-report.md#open-questions) carries their verdicts forward.

We believe the three stories complete the first usable workflow. We also believe the next risk is a plugin that fails or hangs without the operator knowing which one.

Target: obtain a verdict on each of US-01 to US-03 and settle which quality expectations and container split the architecture must answer next.

## Agenda

1. Permissions, 2 minutes. Questions 1-3. Nothing is shown.
2. Working software, 15 minutes. Questions 4-10. Show the running gateway from [the setup guide](../../docs/setup.md), [config/plugins.json](../../config/plugins.json), [the plugin contract](../../docs/plugins.md), and the curl response with `plugin_trace` and `plugin_changes`, one `AC-nn` at a time.
3. Candidate scope, 3 minutes. Questions 11-12. Show the three linked stories and their Must Have priorities.
4. Plugin failure, 4 minutes. Question 13. Show the named HTTP 500 returned by a failing plugin.
5. Quality requirements and architecture against the drivers, 8 minutes. Questions 14-16. Show the [threshold of success](../../docs/threshold-of-success.md), the vision's [constraints](../../docs/product-vision.md), and the proposed single gateway container with its external systems.
6. Remaining Week 3 questions, 7 minutes. Questions 17-20. Show [the same workflow on LiteLLM Proxy](prototypes.md#two-plugin-workflow-on-litellm-proxy).
7. Read-back, 3 minutes. Question 21. Show the list of verdicts, decisions, and action points with owners and Week 5 dates.

## Questions

1. (closed) May we record this meeting?
2. (closed) May we publish a sanitized transcript in our public repository?
3. (closed) If publication is refused, may we share the transcript privately with the course instructors?
4. (closed) For US-01 AC-01, does the gateway start with the two plugins listed in the configuration?
5. (closed) For US-01 AC-02, does the execution order in `plugin_trace` match the configuration?
6. (open) For US-01 AC-03, what did you expect to change after we reversed the list and removed one plugin?
7. (closed) For US-02 AC-01 and AC-02, does the documented contract cover what you need, and do both examples use only that contract?
8. (closed) For US-03 AC-01 and AC-02, does the response show each plugin's request and response changes in order?
9. (closed) For US-03 AC-03, does the repeat run show deterministic behaviour without a real provider key?
10. (closed) Do you accept or reject each of US-01, US-02, and US-03? If you reject one, which `AC-nn` failed?
11. (closed) On October 16 you mentioned three plugins. Are two example plugins enough, or must a third be added?
12. (open) Which story, if any, must be added or removed before this set completes a useful task for you?
13. (open) When a plugin fails or stops responding, what must the caller see and what must the operator see?
14. (open) Of failure isolation, added latency, and keeping secrets out of logs, which matters most to you, and what limit would you test it against?
15. (closed) Is one gateway service enough, or must the configuration or the audit records live in a separate store?
16. (open) Which of the threshold-of-success goals would you check first against this architecture?
17. (open) LiteLLM ran the same two-plugin workflow with comparable effort. What would make you choose our gateway over extending LiteLLM?
18. (open) Is policy-version tracking needed, and what request or response content may be kept?
19. (closed) Are static caller credentials and one provider enough for the first trial?
20. (open) Which made-up company-data examples, with their expected masked output, should the masking plugin handle?
21. (closed) Does our read-back record your verdicts, decisions, and next actions correctly?

## Roles

- Moderator: Ali12hamdan.
- Notes: Mohammed-Nour.
- Observer and demo driver: atkond2point0.

## Key improvements

Before: "Is the plugin failure handling OK?"

After: "When a plugin fails or stops responding, what must the caller see and what must the operator see?"

Principle: ask about the behaviour each person observes, so the answer becomes a testable requirement rather than a yes.
