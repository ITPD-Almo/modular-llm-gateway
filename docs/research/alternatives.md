# Alternatives

**Problem space (draft, pending team agreement):** Corporate IT teams need to give employees and internal applications access to several LLM providers while enforcing their own company-specific rules for authentication, sensitive-data filtering, routing, and usage logging on every request and response.

**Evidence board:** <https://miro.com/app/board/uXjVEeQDS7A=/> (view-only Miro board, one frame per alternative; screenshots captured 2026-10-05).

**Comparison properties (draft, pending team agreement):**

| ID  | Property                        | What we look for                                                                                |
| --- | ------------------------------- | ----------------------------------------------------------------------------------------------- |
| P1  | Custom request/response policies | Can a company add its own logic before the request reaches the provider and after the response returns, and can that logic change the content? |
| P2  | Access and credential controls  | How provider keys are stored and handed out, and what per-user or per-team limits exist.         |
| P3  | Routing flexibility             | What a request can be routed on, and what fallback and load-balancing options exist.             |
| P4  | Sensitive-data handling         | Whether personal or confidential data can be detected and removed before it reaches a provider, and whether logs keep it. |
| P5  | Audit and usage evidence        | What is recorded per request and per admin action, and for how long.                            |
| P6  | Operational effort              | What the company has to run itself, and which capabilities depend on the hosting model or plan.  |

## ALT-01: Portkey AI Gateway

**Kind:** Direct competitor. Commercial AI gateway offered as SaaS, with an MIT-licensed open-source gateway core and an enterprise hybrid deployment.
**Link:** <https://portkey.ai/docs/product/ai-gateway>
**Version looked at:** documentation and pricing page as of 2026-10-05; open-source gateway release [v1.15.2](https://github.com/Portkey-AI/gateway/releases/tag/v1.15.2) (published 2026-01-12).
**Depth of evaluation:** read the product documentation, the pricing page, and the open-source repository's plugin folder. Did not create an account or send traffic through the hosted gateway, so dashboard behaviour is taken from the documentation.

**Screenshots on the board:** `ALT-01 Portkey — webhook guardrail response (P1)` and `ALT-01 Portkey — plan feature comparison (P2, P5, P6)`.

**Problem it solves:** gives engineering and platform teams one OpenAI-compatible endpoint in front of many LLM providers, with routing, guardrails, credential management, and request logs, so that applications do not call providers directly.

**Observations by property**

| Property | Observation | Source |
| -------- | ----------- | ------ |
| P1 Custom request/response policies | Guardrails run as input hooks (`beforeRequestHook`) or output hooks (`afterRequestHook`); each guardrail checks only one of the two. A failed check can deny the request (HTTP 446) or let it pass with a flag (HTTP 246). Companies can plug in their own logic through a webhook guardrail, which returns a `verdict` and may return `transformedData` that replaces the request or response. The webhook times out after 3000 ms by default and then passes with `verdict: true` unless `failOnError` is set. In the open-source repository, plugins are TypeScript handlers with a `manifest.json` inside the `plugins/` folder of the gateway source; the plugins README says to enable them in `conf.json` and compile them with `npm run build-plugins` before starting the gateway. | [Guardrails](https://portkey.ai/docs/product/guardrails), [Bring your own guardrails](https://portkey.ai/docs/integrations/guardrails/bring-your-own-guardrails), [plugins folder](https://github.com/Portkey-AI/gateway/tree/main/plugins) |
| P2 Access and credential controls | Provider credentials are stored once as an "Integration" and exposed to code as AI Providers with slugs such as `@openai-prod`; org admins can share one integration across workspaces. Budgets (USD or tokens, weekly or monthly), rate limits, and model allow/deny lists are described for the Model Catalog. The earlier Virtual Keys feature has been migrated to the Model Catalog. The pricing page lists RBAC from the Production plan, and SSO and "Granular Budget & Rate Limits" only on Enterprise. | [Model Catalog](https://portkey.ai/docs/product/model-catalog), [Virtual Keys](https://portkey.ai/docs/product/ai-gateway/virtual-keys), [Pricing](https://portkey.ai/pricing) |
| P3 Routing flexibility | Conditional routing chooses a target from `metadata.<key>`, `params.<key>` (for example model or temperature), or `url.pathname`, with operators such as `$eq`, `$in`, `$regex`, `$gt`, `$and`, `$or`. Targets can be nested load balancers, fallback chains, or further conditional routers. The documentation states it is available on all plans. | [Conditional routing](https://portkey.ai/docs/product/ai-gateway/conditional-routing) |
| P4 Sensitive-data handling | PII redaction replaces detected values with standardised identifiers before the request is forwarded. Portkey's own detector covers phone numbers, emails, locations, IP addresses, SSNs, names, and credit cards. The documentation states that pre-built redaction patterns are not customisable (custom patterns go through the Regex Match guardrail) and that the transformation is non-reversible. The open-source README lists PII redaction among hosted/enterprise features. The Logs page describes an `x-portkey-debug: false` request header that omits request and response content from logs while still recording tokens, cost, and latency; the page does not mention an organisation-wide setting for this. | [PII redaction](https://portkey.ai/docs/product/guardrails/pii-redaction), [OSS README](https://github.com/Portkey-AI/gateway), [Logs](https://portkey.ai/docs/product/observability/logs) |
| P5 Audit and usage evidence | Each request log records timestamp, request type, model, tokens, cost, and the raw request and response. Log retention is 3 days on Developer (10k logs/month), 30 days on Production (100k logs/month), and custom on Enterprise. Audit logs of admin actions (user, workspace, action, resource, client IP, country) are "a Portkey Enterprise plan feature". | [Logs](https://portkey.ai/docs/product/observability/logs), [Audit logs](https://portkey.ai/docs/product/enterprise-offering/audit-logs), [Pricing](https://portkey.ai/pricing) |
| P6 Operational effort | Hosted SaaS needs no infrastructure. The open-source gateway runs with `npx @portkey-ai/gateway` and has a local log console. The enterprise hybrid model keeps the data plane (gateway, cache, log store) in the customer's VPC while the control plane stays with Portkey. Private cloud and VPC hosting are listed only on Enterprise. | [OSS README](https://github.com/Portkey-AI/gateway), [Private cloud deployments](https://portkey.ai/docs/product/enterprise-offering/private-cloud-deployments), [Pricing](https://portkey.ai/pricing) |

**Strengths**

- Covers all six properties in one product. Guardrails, routing, credential management, and logs share one config model (P1–P5), so a company does not stitch separate tools together.
- Custom logic can change content, not only block it. Webhook guardrails return `transformedData` (P1), which is the closest of the observed features to our plugin idea.
- Routing is expressive and available on every plan (P3). Conditions on metadata and parameters can be nested with fallbacks and load balancing.

**Weaknesses**

- Governance features are gated by plan. SSO, granular budgets, admin audit logs, custom retention, and VPC hosting appear only on Enterprise (P2, P5, P6). The open-source gateway lacks PII redaction and RBAC. A company that self-hosts for data-control reasons loses most of the governance.
- Custom policies on the hosted product run as external webhooks. Each one adds a network hop with a 3000 ms default timeout that fails open unless `failOnError` is set (P1). In the open-source gateway, an in-process plugin is added to the gateway source and compiled with `npm run build-plugins`; the README describes no way to load one without that build step. Inference: in-process custom logic means working with the gateway's source and build.
- Keeping prompts out of logs is documented only per request. Observation: the Logs page describes omitting request and response content through the `x-portkey-debug: false` header and does not mention an organisation-wide setting. Inference, to verify with a trial account: if no such setting exists, keeping sensitive data out of logs depends on every calling application (P4, P5).
- Pre-built PII patterns cannot be customised for company-specific identifiers such as internal project codes or employee numbers. These require hand-written regex guardrails (P4).
