# Features

The capabilities the gateway offers, in the order a user meets them.
The words the gateway uses in its own sense are in the [glossary](glossary.md).

## Run my plugins in the order I set

An operator lists [plugins](glossary.md#plugin) in one configuration file, and the gateway runs them on every request in that [plugin order](glossary.md#plugin-order).

- **Stories:** [`US-01`](https://github.com/ITPD-Almo/modular-llm-gateway/issues/40)
- **Behavior:** [`FR-001`](functional-requirements/fr/FR-001.md), [`FR-002`](functional-requirements/fr/FR-002.md)
- **Decisions:** [`ADR-002`](architecture/adr/ADR-002.md)

## Write a plugin against the documented contract

A developer writes a new [plugin](glossary.md#plugin) by implementing its [hooks](glossary.md#hook) and adds it to the gateway without changing the gateway's own code.

- **Stories:** [`US-02`](https://github.com/ITPD-Almo/modular-llm-gateway/issues/41)
- **Behavior:** [`FR-003`](functional-requirements/fr/FR-003.md)
- **Decisions:** [`ADR-002`](architecture/adr/ADR-002.md)

## See what each plugin changed

An operator sends a request through the [fake provider](glossary.md#fake-provider) and sees every [plugin change](glossary.md#plugin-change) made to the request and to the reply.

- **Stories:** [`US-03`](https://github.com/ITPD-Almo/modular-llm-gateway/issues/42)
- **Behavior:** [`FR-005`](functional-requirements/fr/FR-005.md)

## Keep the gateway usable when a plugin hangs

An operator keeps using the gateway when a [plugin](glossary.md#plugin) stops answering, because only the request it was handling fails, and the operator can see which plugin failed it.

- **Stories:** [`US-04`](https://github.com/ITPD-Almo/modular-llm-gateway/issues/52)
- **Behavior:** [`FR-006`](functional-requirements/fr/FR-006.md), [`FR-007`](functional-requirements/fr/FR-007.md)
- **Decisions:** [`ADR-003`](architecture/adr/ADR-003.md)
