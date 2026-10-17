# Modular LLM Gateway

Status: [v0.1.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.1.0) is released, with configurable plugins and a fake provider. Customer validation was not completed for the Week 3 submission.

## Project

Corporate IT teams need to manage employee access to LLM providers while applying company-specific security, filtering, routing, and logging policies.

The proposed product is a modular gateway with a core and replaceable plugins for request and response processing. Candidate capabilities include authentication, sensitive-data masking, token usage tracking, and provider routing. Clear plugin documentation and examples should help developers and coding agents create company-specific plugins.

The first version uses Python 3.12 and FastAPI, with two example plugins and a deterministic fake provider. The plugin workflow follows our Customer decisions; acceptance of the implemented stories is still pending.

Repository: [ITPD-Almo/modular-llm-gateway](https://github.com/ITPD-Almo/modular-llm-gateway).

## Team

Organization: [ITPD-Almo](https://github.com/ITPD-Almo).

| GitHub username |
| --- |
| Ali12hamdan |
| Mohammed-Nour |
| atkond2point0 |

Course team: **9**. Real names and university emails belong only in the private Moodle submission.

## Documentation

Start with the [online documentation](https://itpd-almo.github.io/modular-llm-gateway/), [setup guide](docs/setup.md), and [documentation index](docs/index.md). See the [Week 03 report](reports/week-03/README.md) for the release and remaining gaps. Course project documentation includes the [Week 02 report](reports/week-02/README.md), [product vision](docs/product-vision.md), [decisions](docs/decisions.md), and [assumptions](docs/assumptions.md). Research includes the [Week 01 report](reports/week-01/README.md), [alternatives](docs/research/alternatives.md), [comparison](docs/research/comparison.md), [gap analysis](docs/research/gap-analysis.md), and [value propositions](docs/research/value-proposition.md).

## Contribution workflow

Create a branch, make a focused change, and open a pull request. Another team member reviews and approves it before merging to `main`.

## License

[MIT](LICENSE).
