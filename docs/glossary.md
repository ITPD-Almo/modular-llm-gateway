# Glossary

The words this project uses in one way only.

## Plugin Pipeline

### Plugin

A class, loaded by its import path from the configuration file, that changes chat requests and provider replies through a request hook and a response hook.

**Defined by:** [`FR-003`](functional-requirements/fr/FR-003.md).

### Hook

One of a plugin's two methods, `process_request` or `process_response`, which receives a dictionary and returns the dictionary the next stage uses.

**Defined by:** [`FR-003`](functional-requirements/fr/FR-003.md).

### Stage

The part of a chat request in which a hook runs: `request` before the provider is called, or `response` after it replies.

**Defined by:** [`FR-001`](functional-requirements/fr/FR-001.md).

### Plugin Order

The order of the import paths in the configuration file, which is the order in which both the request hooks and the response hooks run.

**Defined by:** [`FR-001`](functional-requirements/fr/FR-001.md).

### Plugin Change

An entry a plugin adds to `plugin_changes` naming itself, the stage and what it changed, returned to the client with the reply.

**Defined by:** [`FR-005`](functional-requirements/fr/FR-005.md).

## Operation

### Configured Plugin

A plugin identity present in the selected gateway configuration for a running application.

**Defined by:** [`FR-012`](functional-requirements/fr/FR-012.md).

### Configured Chat

A chat attempt processed through one or more configured plugins.

**Defined by:** [`FR-012`](functional-requirements/fr/FR-012.md).

### Fake Provider

The built-in stand-in for an LLM provider that needs no key and replies with `fake:`, a space and the last message's content.

**Defined by:** [`FR-004`](functional-requirements/fr/FR-004.md).

### Hook Deadline

The longest time the gateway waits for one hook before it ends the request with a timeout response.

**Defined by:** [`FR-007`](functional-requirements/fr/FR-007.md).

### Lifecycle Event

A content-free record the gateway writes when a hook starts, completes, fails or times out, carrying the request identifier, plugin, stage, elapsed time and reason.

**Defined by:** [`FR-008`](functional-requirements/fr/FR-008.md).

## Product analytics

### Focus metric

The main usage measure the team uses to assess the trial's value.

### Input metric

A measurable step the team can change to help explain movement in the focus metric.

### Counter-metric

A measure that guards against raising the focus metric by making the experience worse.

### Metric tree

The focus metric, its guard and its input metrics arranged in their explanatory order.

## Observability and telemetry

### Observability

The ability to investigate the gateway's operation using the signals it emits.

### Signal

A metric, log or trace used to understand how the gateway operated.

### Service level indicator

A defined measure of a service's behavior, with a unit, time window and query. **SLI** is its abbreviation.

### SLI

See [Service level indicator](#service-level-indicator).

### Telemetry

Operating or usage data the product emits for analysis outside the request path.

### Observability backend

The service that receives and stores operating signals and provides queries and visualizations over them.

### Dashboard

A view that groups charts so an analyst or operator can read usage metrics or operating signals for one environment.

### Instrumentation

Code that measures an operation or records a product action and emits the resulting signal or event.

### Event

A structured record of a named action or outcome that occurred in the product.

### Analytics backend

The service that receives and stores product usage events and lets analysts query them and chart usage metrics.

## Usability testing

### Usability test

A structured evaluation in which representative participants attempt predefined product tasks while completion, help and
friction are recorded.

### Participant

An eligible person outside the team who attempts the UT-01 tasks.

### Usability session

One participant's complete run of the fixed UT-01 protocol.

### Consent

Durable agreement to participate, be recorded and allow sanitized results to be used, with the private-data terms understood.

### Recording

The private audio or video evidence of a usability session, kept in the team-owned recordings folder.

### Measure

A defined observation collected from a participant or session, such as task time or a SEQ response.

### Metric

A product-analytics number computed from gateway events for a stated purpose, such as the count of completed chats in a
time window.

### Statistic

A numerical summary of observed measures, such as an unaided-completion rate, median or mean, reported with its sample count.

### Usability test task

A participant scenario with a goal and start point, run in a fixed order without telling the participant how to use the interface.

### Main task

The first UT-01 task: the product's primary flow, which is the subject of QR-09.

### Secondary task

An adjacent flow run after the main task to reveal related friction; it does not determine the QR-09 verdict.

### Unaided completion

Reaching a task's predefined end state within its time limit without a hint, command, explanation or facilitator action.

### Assisted completion

Reaching a task's predefined end state after help that the observer records.

### Failed task

Not reaching a task's predefined end state within its time limit.

### Think-aloud

The instruction for a participant to say what they are trying and noticing while the observer records behavior.

### SEQ

The seven-point Single Ease Question asked after each task: higher scores mean the task was easier.

### SUS

The ten-item System Usability Scale, scored from its standard responses with `2.5 × (20 + sum(odd) - sum(even))`.

### Valid participant

An eligible participant whose consent, recording, profile match and complete, technically usable session data permit inclusion in the predeclared analysis.

## Repository configuration

### Configuration

The files, settings, dependencies and processes that build, check, deliver and explain this gateway repository.

**Defined by:** [the configuration-management requirements][configuration-rules].

### Configuration management

The team's practice of identifying, owning, reviewing and updating the configuration that produces the gateway and its evidence.

**Defined by:** [the configuration plan](configuration-plan.md).

### Configuration review

A review of the gateway's configuration at an identified baseline, judging the artifact set against the local purposes it serves.

**Defined by:** [the evaluation requirements][evaluation-rules].

### Configuration plan

The maintained inventory of the gateway's configuration items, their owners, locations and connections.

**Defined by:** [the configuration plan](configuration-plan.md).

### Configuration item

One existing maintained file, setting, process or dependency assigned a repository-wide `CFG-nn` in the configuration plan.

**Defined by:** [the configuration items][configuration-items].

### Configuration evaluation

The week's evidence of how well the gateway's artifact sets serve their local goals, including recommendations and their tradeoffs.

**Defined by:** [the evaluation requirements][evaluation-rules].

### Baseline

The identified and frozen tag or source commit whose configuration an evaluation judges.

**Defined by:** [the configuration-management requirements][configuration-rules].

### Upkeep

Work that keeps the gateway's repository, documentation, checks and delivery configuration accurate as the project changes.

### Reproducible build

A gateway build that produces the same artifact from the same identified source, dependencies, target platform and build configuration.

**Defined by:** [the image build procedure](deployment.md#versioned-compose-deployment).

### Dependency pinning

Selecting explicit package versions, action commits or image digests so a gateway installation or check uses reviewed dependencies.

**Defined by:** [the runtime pins](configuration-plan.md#cfg-14) and [the dependency update process](configuration-plan.md#cfg-16).

### Secret

A provider key, ingestion credential, private signing key or access code that grants access and is kept outside the public product repository.

**Defined by:** [the deployment's private configuration](deployment.md#configuration-and-layout).

### Context window

The finite text available to a coding agent during a gateway editing session, including the instructions and artifact excerpts it has read.

### Agent instruction

A repository rule or navigation instruction in `AGENTS.md` that guides a coding agent's edits, checks and handling of protected files.

**Defined by:** [the root agent instructions](https://github.com/ITPD-Almo/modular-llm-gateway/blob/main/AGENTS.md).

[configuration-rules]: https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/configuration-management-requirements.md#where-the-configuration-plan-and-the-review-live
[configuration-items]: https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/configuration-management-requirements.md#the-configuration-items
[evaluation-rules]: https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/configuration-management-requirements.md#the-evaluation
