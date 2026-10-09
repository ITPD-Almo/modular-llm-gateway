# Week 2 prototypes

## Text concept of the gateway flow

- **What it is:** a short text presentation of our research, an employee request being masked before forwarding, a policy-version decision record, and a proposed first-version scope. It was a static concept, not a running gateway.
- **View:** the [proposed flow](images/gateway-flow-concept.png) and the [first-version proposal](images/gateway-scope-concept.png). The screenshots were captured after the meeting from the original prepared slides; they are not screenshots of the live call.
- **Tested:** the proposed workflow behind [GAP-01](../../docs/research/gap-analysis.md#gap-01) and [ASM-01](../../docs/assumptions.md#asm-01). No story issue's AC-nn was demonstrated, and ASM-01 remains Open.
- **Question:** does the proposed masking and request-record flow show a useful first version, and what is missing?
- **What the customer said:** the high-level flow looked fine, but it did not explain the interface between the gateway and its plugins. The Customer asked to see plugin inputs, outputs, ordering, and loading. A first usable interaction can use two simple plugins, a restart, and a fake provider.
- **What changed:** [DEC-006](../../docs/decisions.md#dec-006), listed in the [meeting report](meeting-report.md#decisions), now informs the [plugin-interface requirement](../../docs/product-vision.md#con-01). The [goal](../../docs/product-vision.md#goal) focuses on DevOps users composing plugins, per [DEC-003](../../docs/decisions.md#dec-003), and states the small usable interaction from [DEC-005](../../docs/decisions.md#dec-005). [BND-04](../../docs/product-vision.md#bnd-04) records the allowed restart. The revised story candidate and weekly summary still need to carry these changes.
