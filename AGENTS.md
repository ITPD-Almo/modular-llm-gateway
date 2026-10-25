# Agent Instructions

The course requirements are routed from [`SKILL.md`](https://github.com/inno-itpd/itpd/blob/main/SKILL.md); read the rule before you change an artifact it checks.

## Layout

- `gateway/` is the product: one FastAPI application.
  - `main.py`: app factory and HTTP endpoints.
  - `config.py`: plugin loading.
  - `execution.py`: supervised request-local worker pipeline and cleanup.
  - `validation.py`: chat/plugin output shape and JSON-size validation.
  - `provider.py`: the deterministic fake provider.
  - `diagnostics.py`: lifecycle events.
  - `plugins/`: the `Plugin` protocol in `base.py` and the bundled plugins.
  - The [testability requirement](docs/quality-requirements/qr/QR-01.md) names the critical modules it covers.
- `config/plugins.json` is the default plugin list; `GATEWAY_CONFIG` selects another file.
- `examples/` holds the third-party A/B and slow-hook examples and their configuration files; they load without editing gateway core.
- `tests/` holds the pytest suite; every test uses synthetic plugins and the fake provider, never a provider key or the network.
- `docs/` holds the maintained artifacts and the documentation site:
  - the vision, the plan and the decisions
  - the assumptions and the research
  - `quality-requirements/`, `functional-requirements/` and the glossary
  - the setup, plugin, operations and demo guides
  - `architecture/`: the container view (`container.svg` source and rendered `container.png`) and the decision records in `architecture/adr/`, with `TEMPLATE.md` for a new `ADR-nnn`

  New maintained documents go here, never into `reports/` first.
- `reports/week-NN/` holds each week's evidence and report, and is not rewritten after its week.
- `.github/` holds the CI workflows, the issue forms and the pull request template.
- `.claude/skills/itpd/` is the course repository as a Git submodule.

Keep this map and the documentation entry points current in the same pull request that introduces a module, example directory or guide; do not describe an unmerged path as already present.

## Checks

| Command | What it checks | CI workflow |
| --- | --- | --- |
| `python -m pytest` | Tests | `tests.yml` |
| `npx markdownlint-cli2 "**/*.md"` | Markdown, with the rules in `.markdownlint-cli2.jsonc` | `markdown.yml` |
| `lychee --exclude-path .claude/skills/itpd './**/*.md'` | Links. It fetches external links, so it needs the network; it is the Rust lychee CLI, not the npm package | `lychee.yml` |
| `python -m mkdocs build --strict` | Documentation site; run it after `pip install -r requirements-docs.txt` | `pages.yml`, which builds and deploys from `main` |

Install the tools with `python -m pip install -e ".[test]"` in a Python 3.12 virtual environment, as [`docs/setup.md`](docs/setup.md) describes.

## Conventions

- **Branches:** `<issue-number>-<short-description>`, normally from `main`. One pull request closes exactly one task issue with `Closes #<number>`, and never a user story.
- **Dependency stacks:** a pull request may build on another's branch when it needs unmerged records. Name the base pull request in the description and keep the dependent one draft. After the base merges, merge `main` into the branch without rewriting history, retarget it to `main` and rerun the checks before review. A task closes only when its pull request merges into `main`.
- **Commit messages:** one imperative line of at most 72 characters, starting with a capital letter and ending without a full stop; add a body when the reason is not obvious.
- **Pull requests:** use `.github/pull_request_template.md`. The task's `Accountable` member reviews and merges, and the author never approves their own pull request.
- **Links:** in issues and pull requests, link a repository file by its full `https://github.com/ITPD-Almo/modular-llm-gateway/blob/main/...` URL. Inside `docs/`, use relative links. Link a file outside `docs/` by its GitHub URL.
- **Identifiers:** `FR-nnn`, `ADR-nnn` and `DEC-nnn` take three digits and `QR-nn`, `US-nn` and `ASM-nn` two; an identifier is never reused or renumbered.
- **Code:** Python 3.12 with type hints. Plugin hooks are synchronous, take one dictionary and return a new one.
- **Changelog:** a user-visible change adds its line under `[Unreleased]` in `CHANGELOG.md`.
- **Secrets:** no real provider key, prompt, recording or personal data in any file.

The same conventions are written for members in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Do Not Edit

- `.claude/skills/itpd/` is the course's material. Never edit it. A member updates the submodule pin only when the team adopts a new course revision.
- `reports/week-NN/` of a past week is historical evidence. A later correction goes into the current week's report.
- Released sections of `CHANGELOG.md` and published `REL-nn` lines in `docs/project-plan.md` describe tags that already exist. Only the release task's member changes them.
- `docs/decisions.md` is edited only by the member who owns the Customer evidence. Hand over proposed decision text instead.
- `.github/workflows/` is changed in its own pull request, so a broken gate cannot hide inside a feature change.
