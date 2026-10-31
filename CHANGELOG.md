# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- A [features page](docs/features.md) that lists what the gateway lets you do, in plain words, with links to the stories and requirements behind each capability.
- Guided `llmgw setup` with hidden API-key entry, read-only DeepSeek model discovery, private local persistence, provider status and logout; no `.env` editing is needed.
- An opt-in DeepSeek adapter using the saved model, a 128-output-token cap, no automatic retries and a separate supervised provider deadline, while `llmgw demo` remains offline.
- An installed `llmgw` terminal command for serving, chat, health checks, plugin inspection, workspace creation and a self-contained five-scenario demo.
- A Linux/macOS installer that provisions an isolated Python runtime without requiring Git, system Python, Docker, sudo or a provider key; runtime dependencies are pinned for the installer.

### Fixed

- Ship the default plugin configuration and demo plugins inside the Python package, so an installed wheel works outside a repository checkout.

## [0.2.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.2.0) - 2026-10-25

### Added

- Content-free plugin lifecycle events and gateway-generated `X-Request-ID` correlation for chat results and handled failures; see the [operating guide](docs/operations.md).
- Supervised request workers with configurable hook deadlines, bounded admission, worker termination/reaping and safe malformed-output errors.
- A third-party A/B example plugin loaded by configuration, a slow-plugin demo example, a step-by-step [demo](docs/demo.md), and a fuller [plugin guide](docs/plugins.md) and [setup guide](docs/setup.md) with a reset procedure.

### Changed

- Invalid chat bodies return a fixed HTTP 422 detail and a gateway-generated request ID without echoing input values.
- Default admission is four concurrent request workers per application process; even healthy traffic above capacity can receive HTTP 503 rather than waiting in a queue.
- Plugin instances are shared between the hooks of one request and reset for each new request, isolating failure recovery from later requests.

## [0.1.0](https://github.com/ITPD-Almo/modular-llm-gateway/releases/tag/v0.1.0) - 2026-10-17

### Added

- A FastAPI gateway with JSON-configured request and response plugins.
- Metadata and uppercase example plugins, with request and response audit entries.
- A deterministic fake provider, setup documentation, a plugin contract, and five automated tests.
- A public documentation site with the project plan, risks, and workflow documents.

Customer validation was not completed for this release. The three candidate stories remain open for a later verdict.

<!-- markdownlint-disable-file MD024 -->
