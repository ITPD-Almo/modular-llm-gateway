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
