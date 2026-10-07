# Product vision

Modular LLM Gateway

## Goal

An IT operator in a small company can route employees' LLM requests through one self-hosted gateway that masks fixed-format company identifiers and shows, for any request, which policy revision allowed, masked, or rejected it, without storing the prompt.

**Supports:** [VP-01](research/value-proposition.md#vp-01), [VP-02](research/value-proposition.md#vp-02).

## Stakeholders

- **IT operator**: runs the gateway, writes the policy, and answers for its decisions; the primary user.
- **Employee**: sends prompts through the gateway from an internal tool, and is affected by every mask and rejection without configuring anything.
- **Plugin developer**: writes a company-specific request or response plugin against the documented plugin interface.
- **Security or compliance officer**: asks the operator to explain a decision after the fact, and never touches the gateway.
- **LLM provider**: receives the masked requests and returns the responses.
- **Customer**: the course instructor, who decides the scope.

## Constraints

### CON-01

The product is a modular core with replaceable plugins for request and response processing.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** policy logic cannot be written directly into the core, so even the first masking rule needs a plugin interface, its documentation, and an example.

### CON-02

Built and maintained by four students.

- **Status:** Active
- **Source:** Team-given
- **What it costs:** no component may need an expert the team does not have, so no general PII detector, no high-availability setup, and no identity administration.

### CON-03

Delivered within the autumn 2026 term, which ends on 10 December 2026.

- **Status:** Active
- **Source:** Environmental
- **What it costs:** one provider and one deployment mode are all the course can verify; every further provider or mode is a story we do not build.

### CON-04

No real provider keys, prompts, or personal data in the public repository or its tests.

- **Status:** Active
- **Source:** Derived
- **What it costs:** tests run against a mocked provider and synthetic identifiers, so real-provider behaviour and real employee data stay untested until the operator deploys it.

## Boundary

### BND-01

Manage employee identities, single sign-on, and group membership.

- **Status:** Active
- **Handled by:** the IT operator, who issues each internal tool a static gateway credential by hand
- **Why:** [`CON-02`](#con-02): identity administration needs expertise and time the team does not have, and every alternative we studied already sells it.

### BND-02

Detect confidential content that has no fixed format, such as a project described in prose.

- **Status:** Active
- **Handled by:** Nobody
- **Why:** team reasoning: regex cannot establish semantic confidentiality, and we have no dataset or accuracy target for it, per [the rejected directions](research/gap-analysis.md#directions-rejected-for-now).

### BND-03

Keep decision records tamper-proof and store them for the long term.

- **Status:** Active
- **Handled by:** Company log store
- **Why:** [`CON-02`](#con-02): the gateway writes the records, and durable, compliance-grade storage is a product of its own.

### BND-04

Edit policies or install plugins through a web administration interface while the gateway runs.

- **Status:** Active
- **Handled by:** the IT operator, by editing the policy file and restarting the gateway
- **Why:** [`CON-03`](#con-03): a static policy file gives every decision one revision to point at, and an administration interface would take the term on its own.

### BND-05

Run the language models.

- **Status:** Active
- **Handled by:** LLM provider
- **Why:** team reasoning: the gateway sits between the company and the provider and does not host models.

## Context

![System context diagram](architecture/context.svg)

The actors are the employee, whose internal tool sends requests through the gateway with a static credential, and the IT operator, who supplies that credential, the policy file, and the plugins, and reads the decision records.
The external systems are the LLM provider, which receives masked requests per `BND-05`, and the company log store, which keeps the decision records per `BND-03`.
The security or compliance officer is a stakeholder but exchanges nothing with the gateway, so the officer is not on the diagram, and nothing on it detects confidential prose, because `BND-02` leaves that job to nobody.

## Where The Detail Lives

- [User stories](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=label%3Auser-story)
- [Assumptions](assumptions.md) and [decisions](decisions.md)
