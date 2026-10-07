# Alternatives

**Problem space (draft, pending team agreement):** Corporate IT teams need to give employees and internal applications access to several LLM providers while enforcing their own company-specific rules for authentication, sensitive-data filtering, routing, and usage logging on every request and response.

**Evidence board:** <https://miro.com/app/board/uXjVEeQDS7A=/> (one frame per alternative; screenshots captured 2026-10-05; anonymous view-only access still needs checking).

The three alternatives were selected for detailed research per [DEC-001](../decisions.md#dec-001).

**Comparison properties (draft, pending team agreement):**

|ID|Property|What we look for|
|---|---|---|
|P1|Custom request/response policies|Can a company add its own logic before the request reaches the provider and after the response returns, and can that logic change the content?|
|P2|Access and credential controls|How provider keys are stored and handed out, and what per-user or per-team limits exist.|
|P3|Routing flexibility|What a request can be routed on, and what fallback and load-balancing options exist.|
|P4|Sensitive-data handling|Whether personal or confidential data can be detected and removed before it reaches a provider, and whether logs keep it.|
|P5|Audit and usage evidence|What is recorded per request and per admin action, and for how long.|
|P6|Operational effort|What the company has to run itself, and which capabilities depend on the hosting model or plan.|

## ALT-01

Portkey AI Gateway

- **Status:** Active
- **Kind:** Direct competitor. Commercial AI gateway offered as SaaS, with an MIT-licensed open-source gateway core and an enterprise hybrid deployment.
- **Link:** <https://portkey.ai/docs/product/ai-gateway>
- **Version looked at:** documentation and pricing page as of 2026-10-05; open-source gateway release [v1.15.2](https://github.com/Portkey-AI/gateway/releases/tag/v1.15.2) (published 2026-01-12).
- **Depth of evaluation:** read the product documentation, the pricing page, and the open-source repository's plugin folder. Did not create an account or send traffic through the hosted gateway, so dashboard behaviour is taken from the documentation.
- **Problem it solves:** gives engineering and platform teams one OpenAI-compatible endpoint in front of many LLM providers, with routing, guardrails, credential management, and request logs, so that applications do not call providers directly.

**Screenshots on the board**

`ALT-01 Portkey — webhook guardrail response (P1)` and `ALT-01 Portkey — plan feature comparison (P2, P5, P6)`.

**Observations by property**

| Property | Observation | Source |
| -------- | ----------- | ------ |
| P1 Custom request/response policies | Guardrails run as input hooks (`beforeRequestHook`) or output hooks (`afterRequestHook`); each guardrail checks only one of the two. A failed check can deny the request (HTTP 446) or let it pass with a flag (HTTP 246). Companies can plug in their own logic through a webhook guardrail, which returns a `verdict` and may return `transformedData` that replaces the request or response. The webhook times out after 3000 ms by default and then passes with `verdict: true` unless `failOnError` is set. In the open-source repository, plugins are TypeScript handlers with a `manifest.json` inside the `plugins/` folder of the gateway source; the plugins README says to enable them in `conf.json` and compile them with `npm run build-plugins` before starting the gateway. | [Guardrails](https://portkey.ai/docs/product/guardrails), [Bring your own guardrails](https://portkey.ai/docs/integrations/guardrails/bring-your-own-guardrails), [plugins folder](https://github.com/Portkey-AI/gateway/tree/main/plugins) |
| P2 Access and credential controls | Provider credentials are stored once as an "Integration" and exposed to code as AI Providers with slugs such as `@openai-prod`; org admins can share one integration across workspaces. Budgets (USD or tokens, weekly or monthly), rate limits, and model allow/deny lists are described for the Model Catalog. The earlier Virtual Keys feature has been migrated to the Model Catalog. The pricing page lists RBAC from the Production plan, and SSO and "Granular Budget & Rate Limits" only on Enterprise. | [Model Catalog](https://portkey.ai/docs/product/model-catalog), [Virtual Keys](https://portkey.ai/docs/product/ai-gateway/virtual-keys), [Pricing](https://portkey.ai/pricing) |
| P3 Routing flexibility | Conditional routing chooses a target from `metadata.<key>`, `params.<key>` (for example model or temperature), or `url.pathname`, with operators such as `$eq`, `$in`, `$regex`, `$gt`, `$and`, `$or`. Targets can be nested load balancers, fallback chains, or further conditional routers. The documentation states it is available on all plans. | [Conditional routing](https://portkey.ai/docs/product/ai-gateway/conditional-routing) |
| P4 Sensitive-data handling | PII redaction replaces detected values with standardised identifiers before the request is forwarded. Portkey's own detector covers phone numbers, emails, locations, IP addresses, SSNs, names, and credit cards. The documentation states that pre-built redaction patterns are not customisable and that the transformation is non-reversible. For other identifiers, the same page describes configuring the Regex Match guardrail with a custom pattern, replacement text (for example `[REDACTED]`), and the Redact option turned on. The open-source README lists PII redaction among hosted/enterprise features. The Logs page describes an `x-portkey-debug: false` request header that omits request and response content from logs while still recording tokens, cost, and latency; the page does not mention an organisation-wide setting for this. | [PII redaction](https://portkey.ai/docs/product/guardrails/pii-redaction), [OSS README](https://github.com/Portkey-AI/gateway), [Logs](https://portkey.ai/docs/product/observability/logs) |
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
- Company-specific identifiers depend on patterns the company writes itself. Observation: Portkey supports custom regex patterns with replacement text and redaction, while its pre-built PII patterns cannot be customised. Companies still need to write, test, and maintain these patterns. Inference: regex suits identifiers with a fixed format, such as employee numbers or project codes, but not confidential content without a fixed shape, such as a project described in prose (P4).

## ALT-02

Azure API Management AI gateway

- **Status:** Active
- **Kind:** Adjacent substitute. A general-purpose cloud API management service whose existing gateway gained LLM-specific policies; companies already on Azure reuse it instead of buying a dedicated AI gateway.
- **Link:** <https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities>
- **Version looked at:** Microsoft Learn documentation read on 2026-10-05. Page dates as shown in each page's metadata: AI gateway capabilities 2026-05-29, `llm-content-safety` 2026-08-18, `llm-token-limit` 2026-04-01, LLM logging 2026-06-12, policy reference index 2026-08-24, backends 2026-05-20, policy expressions 2026-01-15, self-hosted gateway 2025-09-30.
- **Depth of evaluation:** read the AI gateway overview, the reference pages of the LLM policies, the full policy index with its per-gateway support table, the policy expression rules, the backend and self-hosted gateway pages, the monitoring page (including Activity Log), and the pricing page. Did not create an Azure subscription or an API Management instance, so portal behaviour is taken from the documentation and its screenshots. The pricing page showed no numeric prices without a region and currency selection, so cost is not compared.
- **Problem it solves:** lets a company put its LLM endpoints behind the same API gateway it already uses for other APIs, so token limits, authentication, content checks, load balancing, and logging are configured as gateway policies rather than in each application.

**Screenshots on the board**

`ALT-02 Azure APIM — llm-content-safety blocks harm categories with 403, no redaction (P4)` and `ALT-02 Azure APIM — opt-in prompt/completion logging per API with byte limits (P5)`.

**Observations by property**

| Property | Observation | Source |
| -------- | ----------- | ------ |
| P1 Custom request/response policies | Behaviour is configured as an XML policy document with `inbound`, `backend`, `outbound`, and `on-error` sections, at global, workspace, product, API, or operation scope. Custom logic is written as C# 7 policy expressions limited to an allow-list of .NET types; no external assemblies are listed. The documentation says expressions get "only limited verification" when the policy is defined, and exceptions they throw at run time produce a runtime error. Content can be changed with `set-body` and `find-and-replace`, and an external service can be called mid-request with `send-request`. Reusable pieces are shared as policy fragments (`include-fragment`). | [Policy reference](https://learn.microsoft.com/en-us/azure/api-management/api-management-policies), [Policy expressions](https://learn.microsoft.com/en-us/azure/api-management/api-management-policy-expressions) |
| P2 Access and credential controls | Callers can be authenticated with subscription keys, `validate-jwt`, or `validate-azure-ad-token` (Entra ID app roles and claims). The gateway reaches Azure-hosted models with a managed identity, so no provider key is handed to applications; other providers' keys are stored as secret named values, optionally backed by Key Vault. `llm-token-limit` sets tokens per minute and/or a token quota per hour, day, week, month, or year on any counter key (subscription, IP, or a policy expression). It returns `429` when the rate is exceeded and `403` when the quota is exceeded, and counts are kept per gateway, not across the whole instance. | [Authenticate and authorize LLM APIs](https://learn.microsoft.com/en-us/azure/api-management/api-management-authenticate-authorize-ai-apis), [llm-token-limit](https://learn.microsoft.com/en-us/azure/api-management/llm-token-limit-policy) |
| P3 Routing flexibility | Backend pools of up to 30 backends support round-robin, weighted, and priority-based balancing, with optional session affinity by cookie. Lower-priority groups are used only when circuit breakers trip in higher ones. Only one circuit-breaker rule per backend is supported, and neither pools nor breakers are synchronised between gateway instances. Content-based routing is done by wrapping `set-backend-service` in a `choose` block with policy expressions. A unified OpenAI-compatible endpoint across providers is in preview. | [Backends](https://learn.microsoft.com/en-us/azure/api-management/backends), [AI gateway capabilities](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities) |
| P4 Sensitive-data handling | `llm-content-safety` sends prompts or completions to Azure AI Content Safety and blocks with `403` on the categories `Hate`, `SelfHarm`, `Sexual`, and `Violence`, on custom blocklists, or on detected prompt attacks (`shield-prompt`). It blocks; it does not redact. The policy index lists no policy for PII detection, redaction, or masking. Redaction would have to be built from `send-request` to a separate detection service plus `set-body`, or from `Regex.Replace`, which is on the list of .NET types allowed in policy expressions. | [llm-content-safety](https://learn.microsoft.com/en-us/azure/api-management/llm-content-safety-policy), [Policy reference](https://learn.microsoft.com/en-us/azure/api-management/api-management-policies) |
| P5 Audit and usage evidence | A diagnostic setting sends prompt, completion, and total token counts and the model name to the `ApiManagementGatewayLlmLog` table in Log Analytics. Logging of prompt and completion text is a separate per-API opt-in with a byte limit; messages over 32 KB are split into chunks, and messages over 2 MB are not supported. Token metrics with custom dimensions (for example a user ID header) go to Application Insights through `llm-emit-token-metric`. The documentation warns that token usage may be missing or inaccurate when a stream breaks. Separately, Azure Monitor Activity Log automatically records subscription-level events such as resource changes. This provides administrative change evidence; the monitoring page does not establish that each allow, redact, or reject decision is linked to the exact policy version used. | [Monitoring and Activity Log](https://learn.microsoft.com/en-us/azure/api-management/monitor-api-management), [LLM logging](https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-llm-logs), [AI gateway capabilities](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities) |
| P6 Operational effort | The managed gateway is an Azure service, so the company runs no servers, but needs an Azure subscription plus Log Analytics, Application Insights, Content Safety, and (for semantic caching) a Redis-compatible cache as separate resources. A self-hosted container gateway is available only on Developer and Premium; it must reach Azure on port 443 for configuration every 10 seconds and keeps running on its last configuration if the link drops. Feature support differs by gateway type: `llm-token-limit` and `llm-emit-token-metric` are not available on the Consumption tier, and the Anthropic Messages API is supported only in v2 tiers. | [Self-hosted gateway](https://learn.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview), [Policy reference](https://learn.microsoft.com/en-us/azure/api-management/api-management-policies), [AI gateway capabilities](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities) |

**Strengths**

- Custom logic runs in the gateway itself. Policy expressions and `set-body` can read and rewrite the request and response in-process (P1), without the extra network hop that Portkey's webhook guardrails add (ALT-01 P1).
- Identity and credentials reuse the company's existing Entra ID setup. Managed identity means applications never hold a provider key for Azure-hosted models, and JWT validation can enforce per-app roles (P2).
- Usage evidence lands in the company's own Log Analytics workspace, where it can be queried with Kusto next to other gateway logs, and prompt logging is off unless turned on per API (P5).

**Weaknesses**

- No built-in PII redaction. The only content policy blocks harmful categories and blocklisted terms; removing personal or confidential data before it reaches a provider has to be assembled by hand from `send-request` and `set-body` (P4).
- Policies are XML with embedded C# expressions that get only limited verification when saved (P1). Inference: writing a company-specific filter needs API Management expertise, and mistakes in expression logic that the save-time check does not catch surface as runtime errors, so filters need testing before they reach production traffic.
- The feature set depends on tier and gateway type. Token limits and token metrics are missing on Consumption, self-hosting is limited to Developer and Premium, and the Anthropic API needs a v2 tier (P2, P5, P6). Observation: no single tier is described as supporting every AI policy, self-hosting, and Anthropic together in the pages read. Inference: a company may have to change tier, and price, to get the full set.
- It ties the gateway to Azure. Even the self-hosted gateway is configured from, and reports to, an Azure instance (P6), and the smoothest setup (managed identity, Content Safety, Foundry import) applies to Azure-hosted models (P2).

## ALT-03

LiteLLM Proxy

- **Status:** Active
- **Kind:** Open-source/self-hosted option. A Python gateway that can run on the company's own infrastructure. It also competes directly with dedicated AI gateways.
- **Link:** <https://docs.litellm.ai/docs/simple_proxy>
- **Version looked at:** release [v1.104.0](https://github.com/BerriAI/litellm/releases/tag/v1.104.0), published 2026-10-03; live documentation read on 2026-10-05. Live docs may describe features newer than that release.
  License: the [release's LICENSE](https://raw.githubusercontent.com/BerriAI/litellm/v1.104.0/LICENSE) applies MIT outside `enterprise/`; enterprise content has a separate license. The whole repository should not be described as unconditionally MIT-licensed.
- **Depth of evaluation:** read the callback, custom guardrail, virtual key, routing, Presidio, logging, deployment, and OSS/Enterprise documentation. Also read the tagged `CustomLogger` source and checked that the named pre-call, response, streaming, and logging methods exist. No proxy was deployed, no paid license was used, and no requests were sent to a provider. Latency, usability, and failure behaviour are not measured.
- **Problem it solves:** gives developers and platform teams an OpenAI-compatible endpoint for multiple providers, with local routing, access keys, spend tracking, and custom policy hooks.

**Screenshot evidence**

Two screenshots of the live documentation, captured in a browser on 2026-10-05 and checked for readability:

- [Callback stages](../../reports/week-01/images/alt-03-litellm-hooks.png): request modification, response modification, and separate streaming hooks (P1).
- [OSS and Enterprise comparison](../../reports/week-01/images/alt-03-litellm-oss-enterprise.png): OSS includes custom guardrails and Presidio; management-operation logs are shown under Enterprise (P2, P4, P5, P6).

These images are in the repository. Ali12hamdan confirmed uploading both to the shared evidence board. Anonymous view-only access still needs checking. Screenshots show documentation, not a tested deployment.

**Observations by property**

| Property | Observation | Source |
| --- | --- | --- |
| P1 Custom request/response policies | Python `CustomLogger` callbacks can modify or reject requests before a provider call and modify responses afterwards. Non-streaming success and streaming response processing use different methods. A callback instance is registered by a dotted path in YAML. The tagged source defines `async_pre_call_hook`, `async_post_call_success_hook`, and `async_post_call_streaming_hook`. The separate `CustomGuardrail.apply_guardrail` interface extracts content and writes returned content back; raising an exception blocks the call. | [Callback guide](https://docs.litellm.ai/docs/proxy/call_hooks), [tagged callback source](https://raw.githubusercontent.com/BerriAI/litellm/v1.104.0/litellm/integrations/custom_logger.py), [custom guardrail guide](https://docs.litellm.ai/docs/proxy/guardrails/custom_guardrail) |
| P2 Access and credential controls | Virtual keys control model access, track spend, and support budgets. Provider credentials can be referenced through environment variables in the gateway configuration. Virtual-key management requires PostgreSQL. The Enterprise comparison includes organization/delegated admin roles and JWT-based authentication; it says Admin UI SSO is free for up to five users, with a license required beyond that. | [Virtual keys](https://docs.litellm.ai/docs/proxy/virtual_keys), [Enterprise comparison](https://docs.litellm.ai/docs/enterprise) |
| P3 Routing flexibility | The router supports random distribution (`simple-shuffle`, the default), least-busy, usage-based, latency-based, and cost-based strategies. Fallbacks move to another model group after retries fail; the guide also describes context-window and content-policy fallbacks. These documents establish routing mechanisms, not measured performance or arbitrary semantic classification of requests. | [Load balancing](https://docs.litellm.ai/docs/proxy/load_balancing), [Fallbacks](https://docs.litellm.ai/docs/proxy/reliability) |
| P4 Sensitive-data handling | The OSS/Enterprise comparison explicitly includes custom guardrails and Presidio PII masking in OSS. The Presidio guide requires separate Analyzer and Anonymizer containers and supports masking or blocking. Logging can globally omit message/response content with `turn_off_message_logging`, while retaining metadata such as spend. The logging guide describes a permission-controlled client opt-out; this behaviour was not tested against the tagged release. | [Enterprise comparison](https://docs.litellm.ai/docs/enterprise), [Presidio guide](https://docs.litellm.ai/docs/proxy/guardrails/pii_masking_v2), [Logging](https://docs.litellm.ai/docs/proxy/logging) |
| P5 Audit and usage evidence | OSS includes spend tracking, request/response logging, Prometheus metrics, and callbacks to logging providers such as OpenTelemetry or Langfuse. The Enterprise comparison lists management-operation logs and audit logs with retention policies for admin actions/key changes. Request logs and administrative audit logs are different capabilities. The read pages do not establish that OSS has no way to implement custom audit events. | [Logging](https://docs.litellm.ai/docs/proxy/logging), [Enterprise comparison](https://docs.litellm.ai/docs/enterprise) |
| P6 Operational effort | A monolithic deployment can serve gateway traffic, management APIs, and UI in one image. Production guidance requires PostgreSQL for auth/tracking and Redis once multiple instances are used. Presidio adds two services if that integration is selected. These requirements apply to those features/deployment modes, not to every minimal proxy. Configuration, database migrations, upgrades, and infrastructure remain the operator's responsibility. | [Production deployment](https://docs.litellm.ai/docs/proxy/deploy), [Virtual keys](https://docs.litellm.ai/docs/proxy/virtual_keys), [Presidio guide](https://docs.litellm.ai/docs/proxy/guardrails/pii_masking_v2) |

**Strengths**

- Compared with ALT-02's XML/C# policy expressions, it offers ordinary Python extension classes with documented configuration and examples (P1). ALT-01 also supports source-level TypeScript plugins; extensibility is not unique to LiteLLM or our proposed product.
- Custom guardrails and Presidio masking are included in OSS, unlike ALT-01's documented enterprise PII feature split and ALT-02's need to compose a redaction policy (P4). Presidio still requires deployment and configuration.
- Compared with the per-request logging control documented for ALT-01, LiteLLM documents a gateway-wide option to omit message content while keeping spend metadata (P4, P5). Whether this satisfies the Customer's privacy requirements needs a configuration test.

**Weaknesses**

- For an IT operator using virtual keys and Presidio, the gateway, PostgreSQL, Analyzer, and Anonymizer form a multi-service deployment; scaling across instances adds Redis (P2, P4, P6). Inference: this is more to operate than a narrow single-instance proxy with static access rules. No setup-time measurement has been made.
- The ready-made administrative audit and delegated-admin capabilities are listed under Enterprise (P2, P5). A team choosing only OSS would need to check whether request logs and custom callbacks cover its actual audit needs before claiming equivalence.
- Non-streaming and streaming response hooks are separate, and callback registration uses a Python instance path (P1). Inference: an extension author needs tests for each supported path; a non-streaming example alone does not demonstrate streaming coverage. This is an integration concern, not evidence that LiteLLM cannot be tested safely.

**Consequence for our project:** Python plugins, PII masking, global body-free logging, and provider fallbacks already exist. We should compare a small, explicit policy-and-audit workflow against configuring LiteLLM before committing to a new gateway.
