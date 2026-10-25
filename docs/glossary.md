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

### Fake Provider

The built-in stand-in for an LLM provider that needs no key and replies with `fake:`, a space and the last message's content.

**Defined by:** [`FR-004`](functional-requirements/fr/FR-004.md).

### Hook Deadline

The longest time the gateway waits for one hook before it ends the request with a timeout response.

**Defined by:** [`FR-007`](functional-requirements/fr/FR-007.md).

### Lifecycle Event

A content-free record the gateway writes when a hook starts, completes, fails or times out, carrying the request identifier, plugin, stage, elapsed time and reason.

**Defined by:** [`FR-008`](functional-requirements/fr/FR-008.md).
