# Decisions

## DEC-001

Research Portkey, Azure API Management, and LiteLLM in detail, and keep the other seven candidates at overview level.

- **Status:** Active
- **Date:** 2026-10-05
- **Made by:** Team
- **Source:** the Week 1 research selection, recorded in the [candidate list](../reports/week-01/candidate-list.md) and [PR #5](https://github.com/ITPD-Almo/modular-llm-gateway/pull/5).
- **Why:** this gives us a direct product, an enterprise API platform, and a self-hosted option to compare. We can return to the other candidates later.

## DEC-002

Explore linking each policy decision to its policy version and a small private policy trial as possible gaps, without treating plugins alone as an advantage.

- **Status:** Active
- **Date:** 2026-10-05
- **Made by:** Team
- **Source:** the Week 1 research and team review in [PR #5](https://github.com/ITPD-Almo/modular-llm-gateway/pull/5).
- **Why:** existing products already offer custom logic, masking options, logs, and routing. We still need to check whether users need these two narrower jobs and whether existing extensions can handle them. Both gaps remain provisional; we have not decided to build a new gateway core.
