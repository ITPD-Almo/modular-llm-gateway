# Modular LLM Gateway

Status: [v0.2.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.2.0) is the latest release, with supervised plugin deadlines/recovery, safe correlated diagnostics and the A/B developer demo. It runs locally against the fake provider; there is no shared gateway deployment. No user story has a recorded Customer acceptance yet.

## Project

Corporate IT teams need to manage employee access to LLM providers while applying company-specific security, filtering, routing, and logging policies.

The proposed product is a modular gateway with a core and replaceable plugins for request and response processing. Candidate capabilities include authentication, sensitive-data masking, token usage tracking, and provider routing. Clear plugin documentation and examples should help developers and coding agents create company-specific plugins.

The first version uses Python 3.12 and FastAPI, with two example plugins and a deterministic fake provider. The plugin workflow follows our Customer decisions; acceptance of the implemented stories is still pending.

Repository: [ITPD-Almo/modular-llm-gateway](https://github.com/ITPD-Almo/modular-llm-gateway).

## Terminal preview for Linux and macOS

The next-version [terminal installer and supervisor walkthrough](docs/terminal.md) provide an isolated runtime and the `llmgw` command without requiring Git, Python or Docker in advance. The installed demo checks plugin order, disabling, A/B transformation and timeout recovery against the fake provider. This is an unreleased local demo; the latest published release remains v0.2.0.

## Team

Organization: [ITPD-Almo](https://github.com/ITPD-Almo).

| GitHub username |
| --- |
| Ali12hamdan |
| Mohammed-Nour |
| atkond2point0 |

Course team: **9**. Real names and university emails belong only in the private Moodle submission.

## Documentation

Start with the [online documentation](https://itpd-almo.github.io/modular-llm-gateway/), [setup guide](docs/setup.md), [plugin contract](docs/plugins.md), and [documentation index](docs/index.md). The [project plan](docs/project-plan.md) holds the sprints and releases, the [Sprint table](https://github.com/orgs/ITPD-Almo/projects/1/views/2) shows who does and who checks each scheduled issue, and the [product backlog](https://github.com/ITPD-Almo/modular-llm-gateway/issues?q=is%3Aissue%20is%3Aopen%20no%3Amilestone) holds the unscheduled stories. The [quality requirements](docs/quality-requirements/README.md), [functional requirements](docs/functional-requirements/README.md), [architecture](docs/architecture/README.md) and [glossary](docs/glossary.md) specify the product, and the [operating guide](docs/operations.md) covers diagnostics and recovery. Agents start from [`AGENTS.md`](AGENTS.md). See the [Week 03 report](reports/week-03/README.md) for the release and remaining gaps. Course project documentation includes the [Week 02 report](reports/week-02/README.md), [product vision](docs/product-vision.md), [decisions](docs/decisions.md), and [assumptions](docs/assumptions.md). Research includes the [Week 01 report](reports/week-01/README.md), [alternatives](docs/research/alternatives.md), [comparison](docs/research/comparison.md), [gap analysis](docs/research/gap-analysis.md), and [value propositions](docs/research/value-proposition.md).

## Contribution workflow

For a runnable plugin-extension and recovery walkthrough, follow the [developer demo](docs/demo.md).

Create a branch, make a focused change, and open a pull request. Another team member reviews and approves it before merging to `main`.

## License

[MIT](LICENSE).
