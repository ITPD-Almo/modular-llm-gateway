# Modular LLM Gateway

The Modular LLM Gateway sits between a company's employees and an LLM provider.
A DevOps operator starts it, lists the company's plugins in a configuration file, and every request and response passes through those plugins in order before it reaches the provider or the employee.
A plugin can mask data, reject a request, add information, or route it, and a plugin developer writes one against a documented interface rather than against the gateway's core.

This is a course project of team 9 in the autumn 2026 term, and it is a work in progress.

## Start here

- [Product vision](product-vision.md): the goal, the stakeholders, the constraints, and what the gateway does not do.
- [Threshold of success](threshold-of-success.md): the goals the project must reach to count as a success.
- [Project plan](project-plan.md): the milestones, the sprints, and their releases.
- [Setup](setup.md): install and run the gateway.
- [Plugin contract](plugins.md): plugin inputs, outputs, order, loading, and failures.
- [Developer demo](demo.md): normal and changed plugin order, a third-party A/B plugin, timeout recovery and reset.
- [Operating guide](operations.md): request correlation, lifecycle events, limits and recovery.

- [Terminal installation and supervisor demo](terminal.md): install on Linux/macOS without preinstalled Python, Git or Docker.

## Requirements

- [Quality requirements](quality-requirements/README.md): the quality bars the gateway is checked against, sorted by business importance and technical risk.
- [Functional requirements](functional-requirements/README.md): what the gateway shall do, one checkable behavior per record.
- [Architecture](architecture/README.md): the container view and the architectural decision records.
- [Glossary](glossary.md): the words this project uses in one way only.

## How we work

- [Definition of done](definition-of-done.md): when a story, a task, and a pull request are done.
- [Risks](risks.md): what could take the plan away, and the fallback for each.
- [Decisions](decisions.md) and [assumptions](assumptions.md): what we agreed with the Customer, and what we still need to check.
- Contributing guide: `CONTRIBUTING.md` in the repository root says how a change gets into the repository.
- Agent instructions: `AGENTS.md` in the repository root gives the layout, checks, conventions and off-limits files to whoever edits the repository next.

## Research

- [Alternatives](research/alternatives.md): the existing gateways we studied.
- [Comparison](research/comparison.md): how they compare on the properties that matter here.
- [Gap analysis](research/gap-analysis.md): what they leave open.
- [Value propositions](research/value-proposition.md): what this gateway offers in those gaps.

## Around the project

- [Source code and issues](https://github.com/ITPD-Almo/modular-llm-gateway)
- [User stories](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=is%3Aissue%20type%3A%22User%20Story%22)
- [Sprints](https://github.com/ITPD-Almo/modular-llm-gateway/milestones)
- [Releases](https://github.com/ITPD-Almo/modular-llm-gateway/releases)
