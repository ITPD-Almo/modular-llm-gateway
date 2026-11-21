# Configuration plan

**Reviewed:** 2026-11-21

This inventory records how the gateway is built, checked, delivered and understood.
Each `CFG-nn` names an existing configuration item and the connections a maintainer must follow when changing it.
Private settings are described by their purpose and location in words.
The Week 8 evaluation at `reports/week-08/cm-evaluation.md` judges a frozen baseline and carries the proposed improvements.

## Source control and release

### CFG-01

The protected `main` branch.

- **Status:** Active
- **Type:** setting
- **Purpose:** require independent review and the named required check before changes enter the shared baseline. Without this gate, the release could include changes the accountable member has never checked.
- **Owner:** Ali12hamdan, as repository administrator.
- **Where:** the repository's branch-protection settings for `main`, named here without an authenticated settings link.
- **Connections:**
  - `enforces` [CFG-02](#cfg-02). One approving review is required, stale approvals are dismissed and the rule applies to administrators. A review left valid after a substantive push would approve different content.
  - `reads` the `links` result from [CFG-06](#cfg-06), with the branch required to be current. Renaming the job without the setting would leave the merge waiting for a result that never arrives.
- **What good looks like:** changes arrive through reviewed PRs, the required check reports on the current change, and force pushes and deletions remain disabled, per [Branch Protection](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#branch-protection).

### CFG-02

The task-to-PR workflow and its issue and PR forms.

- **Status:** Active
- **Type:** process
- **Purpose:** connect an implementable task, its owner, acceptance checks and one reviewed change. Without that route, a passing build would give no account of whose requested outcome it completes.
- **Owner:** the task's Responsible member, with its Accountable member verifying.
- **Where:** `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` and the Issues section of `CONTRIBUTING.md`.
- **Connections:**
  - `reads` [CFG-18](#cfg-18) for branch names, assignees, public issue fields and the one-task/one-PR rule. A form that omits requirements would hide which specification a change serves.
  - `produces` the reviewed commits consumed by [CFG-03](#cfg-03). Closing a task before its criteria hold would turn the release's task links into inaccurate evidence.
- **What good looks like:** each PR closes exactly one Task, a different Accountable member verifies and ticks its criteria, and the issue has matching roles, assignees and sprint, per [Closing A Task](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/task-issues-requirements.md#closing-a-task).

### CFG-03

The protected release tags and the release-recording process.

- **Status:** Active
- **Type:** process and setting
- **Purpose:** identify the reviewed source and explain the upgrade. Without a stable tag and a dated record, an operator cannot reproduce the version or know which evidence belongs to it.
- **Owner:** the current release task's Responsible member, with Ali12hamdan maintaining tag protection.
- **Where:** `CHANGELOG.md`, the release blocks in `docs/project-plan.md`, GitHub Releases and the repository ruleset named Protect release tags.
- **Connections:**
  - `reads` the reviewed main commit from [CFG-02](#cfg-02) and its [CFG-04](#cfg-04) checks. A tag on an unreviewed candidate would detach the release from its verification.
  - `produces` the immutable source reference used by [CFG-10](#cfg-10) and the report process [CFG-21](#cfg-21). Moving a published tag would make earlier deployment receipts and submitted permalinks disagree.
- **What good looks like:** `v*` tags on main are protected from update and deletion, the user-facing release ends with its dated changelog link, and the plan records Released and Checked QRs, per [Cutting A Release](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/releases-requirements.md#cutting-a-release).

## Checks

### CFG-04

The product CI pipeline.

- **Status:** Active
- **Type:** CI pipeline
- **Purpose:** check lint, formatting, types, wheel construction and the synthetic test suite before a change is used. Without it, a documentation-only review could miss a packaging or runtime regression.
- **Owner:** the member changing product or build code, reviewed by the task's Accountable member.
- **Where:** `.github/workflows/tests.yml`.
- **Connections:**
  - `reads` the test extras and tool settings in [CFG-13](#cfg-13). A local environment using different dependency resolution can produce a result CI cannot repeat.
  - `produces` test evidence consumed by [CFG-03](#cfg-03) and the quality-requirement testing plan. Treating a previous commit's run as the current run would verify the wrong source.
- **What good looks like:** the documented checks run on PRs and main using synthetic providers and no provider key, per [Continuous Integration](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#continuous-integration).

### CFG-05

The Markdown check.

- **Status:** Active
- **Type:** workflow
- **Purpose:** catch malformed prose and tables before readers encounter them. Without the check, a report can carry its facts in a table that renders incorrectly.
- **Owner:** the author of the changed documentation.
- **Where:** `.github/workflows/markdown.yml` and its `.markdownlint-cli2.jsonc` configuration.
- **Connections:**
  - `reads` the maintained paths described by [CFG-20](#cfg-20). A broad exclusion would allow unreadable documentation into the release.
  - `reads` the upstream-submodule exclusion associated with [CFG-19](#cfg-19). Removing the exclusion would mix the team's prose findings with the upstream course's own checks.
- **What good looks like:** the same configuration checks PR and main Markdown, and each exclusion has a reason, per [Continuous Integration](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#continuous-integration).

### CFG-06

The link check and its private-repository exclusion.

- **Status:** Active
- **Type:** workflow
- **Purpose:** ensure a reader can follow public evidence and document links. Without it, a renamed artifact can leave a report pointing at an unavailable path.
- **Owner:** the author changing links, with Ali12hamdan maintaining the corresponding branch-protection context.
- **Where:** `.github/workflows/lychee.yml`, its automatically loaded root `lychee.toml` and `.lycheeignore`.
- **Connections:**
  - `produces` the `links` result consumed by [CFG-01](#cfg-01). Changing that name without the protected-branch setting would stop the merge route.
  - `reads` the bounded concurrency, retry and immutable-evidence remapping settings in `lychee.toml`. SHA-pinned commit links are checked against their GitHub source archives and SHA-pinned files against their raw content. This avoids an unauthenticated REST API request for each commit. A remap that loses the original SHA or file path could validate a different artifact.
  - `reads` the evidence locations in [CFG-20](#cfg-20) and [CFG-21](#cfg-21). The authenticated usability-data repository is excluded with its reason, so a green link run cannot establish instructors' private access.
- **What good looks like:** public links are checked on PRs and main, and an authentication exclusion remains explicit and narrow, per [Link Checking](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#link-checking).

### CFG-07

The workflow syntax and expression check.

- **Status:** Active
- **Type:** workflow
- **Purpose:** detect a malformed GitHub Actions change before a release depends on it. Without this check, a broken workflow could stop reporting a signal the team expects.
- **Owner:** the member changing `.github/workflows/`.
- **Where:** `.github/workflows/actionlint.yml`.
- **Connections:**
  - `reads` the workflow definitions belonging to [CFG-04](#cfg-04) through [CFG-09](#cfg-09). A workflow edit outside its review would change the checks that provide release evidence.
  - `reads` a commit-pinned actionlint tool and the Go setup action maintained through [CFG-16](#cfg-16). An unreviewed tool update would change what accepts the workflow.
- **What good looks like:** workflow syntax is checked on PRs and main using identified third-party action revisions, per [Pinning Third-Party Actions](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#pinning-third-party-actions).

### CFG-08

The documentation build and Pages publication.

- **Status:** Active
- **Type:** workflow
- **Purpose:** turn the maintained documentation into a browsable site. Without it, repository changes and the site a newcomer reads can describe different workflows.
- **Owner:** the member changing documentation or its build configuration.
- **Where:** `.github/workflows/pages.yml`, `mkdocs.yml` and `requirements-docs.txt`.
- **Connections:**
  - `reads` the entry point in [CFG-20](#cfg-20). A new guide without a discoverable link can build successfully and still be missed.
  - `produces` the Pages site from main, with deploy after build. Publishing a PR candidate would present unmerged advice as the team's current workflow.
- **What good looks like:** PRs build the site and main publishes the checked documentation, with strict local validation before review, per [Continuous Integration](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#continuous-integration).

### CFG-09

The Linux and macOS terminal-installation matrix.

- **Status:** Active
- **Type:** workflow
- **Purpose:** exercise installation, the packaged demo, an external plugin and repeat installation outside the source checkout. Without it, tests in an editable checkout could hide missing wheel data or an installer regression.
- **Owner:** the member changing the installer, CLI or package layout.
- **Where:** `.github/workflows/terminal-install.yml`.
- **Connections:**
  - `reads` `install.sh`, [CFG-13](#cfg-13) and [CFG-14](#cfg-14). Missing package data would make the installed CLI behave differently from a source checkout.
  - `produces` separate runner results used by [CFG-03](#cfg-03). A skipped platform result cannot substantiate that platform's installation path.
- **What good looks like:** Ubuntu and macOS on both supported architectures exercise the reviewed SHA with synthetic setup credentials, per [Continuous Integration](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#continuous-integration).

## Environments and secrets

### CFG-10

The four-environment deployment runbook and operator helpers.

- **Status:** Active
- **Type:** document and process
- **Purpose:** let an operator verify staging, promote the same source to production and recover the previous version. Without it, continuity depends on the last operator's shell history.
- **Owner:** Ali12hamdan, as deployment operator.
- **Where:** `docs/deployment.md`, with its linked operator tools. Shared-host settings and real access instructions are kept privately by the team.
- **Connections:**
  - `reads` the source identity from [CFG-03](#cfg-03) and per-environment shape from [CFG-11](#cfg-11). A different production SHA or settings scope would invalidate staging's verification for that promotion.
  - `produces` deployment receipts consumed by [CFG-21](#cfg-21). A manually patched VM without a new receipt would make the report's version claim stale.
- **What good looks like:** development, CI, staging and production have distinct purposes, staging and production have separate private settings, and promotion and rollback use identified source, per [Environments And Deployment](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#environments-and-deployment).

### CFG-11

The public configuration shape and the private runtime profiles.

- **Status:** Active
- **Type:** configuration and secret-handling process
- **Purpose:** document the needed settings while keeping provider and ingestion credentials in their environment's private storage. Without the shape, setup becomes guesswork. Exposed values would give other people the same access.
- **Owner:** Ali12hamdan for shared deployment profiles, and each local user for their provider profile.
- **Where:** `.env.example` and `.gitignore`. Actual runtime files, provider profiles, access-code stores and telemetry credentials are private settings outside the product checkout.
- **Connections:**
  - `reads` the variable and profile names handled by `gateway/config.py`, `gateway/cli.py` and `gateway/credentials.py`, which [CFG-10](#cfg-10) and [CFG-12](#cfg-12) use. An example with the wrong name would silently select the default or fail startup.
  - `enforces` the private/public split followed by [CFG-21](#cfg-21). A real credential copied into an example would make the public snapshot a credential disclosure.
- **What good looks like:** examples have placeholders, secret values stay outside Git, and a disclosure follows the incident procedure, per [Configuration And Sensitive Information](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#configuration-and-sensitive-information).

### CFG-12

The isolated UT-01 fixture, reset and export procedure.

- **Status:** Active
- **Type:** process and configuration
- **Purpose:** provide a repeatable synthetic starting state and separate usability telemetry. Without isolation, rehearsals can alter usage metrics or a technical break can be mistaken for participant difficulty.
- **Owner:** the UT-01 facilitator and environment operator, as named in the current test record.
- **Where:** `docs/ut01-staging.md`, which owns the Compose override and `ut01-check.py` procedures. Session credentials and exports remain private.
- **Connections:**
  - `reads` the image from [CFG-15](#cfg-15) and private ingestion settings from [CFG-11](#cfg-11). A wrong organization or missing exporter setting would make the session window incomplete.
  - `produces` the private export and local marker observation used by the test family at [CFG-20](#cfg-20). HTTP events alone cannot establish assistance, reasoning or documentation discovery.
- **What good looks like:** reset and instrumentation are verified before counted sessions, test events stay in their staging scope, and observations cover the known blind spots, per [The Instrumentation](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/usability-testing-requirements.md#the-instrumentation).

## Dependencies and builds

### CFG-13

The Python package and tool manifest.

- **Status:** Active
- **Type:** manifest
- **Purpose:** declare Python support, runtime dependencies, the CLI entry point, package data and development tools. Without it, a wheel or clean environment cannot reconstruct the application's required components.
- **Owner:** the member changing the package or its dependency requirements.
- **Where:** `pyproject.toml`.
- **Connections:**
  - `produces` the input to [CFG-14](#cfg-14). Changing the declared dependency range without regenerating the runtime pins can leave the installer using a different accepted set.
  - `reads` the package layout documented by [CFG-17](#cfg-17). Leaving default JSON out of package data would break installation outside a checkout.
- **What good looks like:** a clean supported environment can build and run the documented entry point, and setup instructions identify its dependencies, per [Setup And Run Instructions](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#setup-and-run-instructions).

### CFG-14

The compiled runtime dependency pins.

- **Status:** Active
- **Type:** dependency set
- **Purpose:** give the installer and image the same selected runtime versions. Without these pins, two installs of one source commit can resolve different transitive packages.
- **Owner:** the member reviewing runtime dependency updates.
- **Where:** `requirements-runtime.txt`, generated from `pyproject.toml` by the command in its header.
- **Connections:**
  - `reads` [CFG-13](#cfg-13). A pin set generated from an older manifest can omit a newly required package.
  - `produces` the dependencies installed by `install.sh` and [CFG-15](#cfg-15). An update that changes only the manifest would leave these delivery paths on older packages.
- **What good looks like:** runtime versions are explicit, the generation command is reproducible, and a dependency update reviews the compiled result and exercises installed delivery, per [Setup And Run Instructions](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#setup-and-run-instructions).

### CFG-15

The image build and Compose launch configuration.

- **Status:** Active
- **Type:** build configuration
- **Purpose:** package one identified source revision and run that selected local image with a health check and isolated settings. Without a source receipt, staging and production can accidentally launch different builds with the same name.
- **Owner:** Ali12hamdan, as image and deployment maintainer.
- **Where:** `Dockerfile` and the root `compose.yaml` entry point.
- **Connections:**
  - `reads` the digest-pinned Python base, [CFG-13](#cfg-13) and [CFG-14](#cfg-14). A changed build input can change the image even when application source is identical.
  - `produces` the image ID and source-revision label consumed by [CFG-10](#cfg-10) and [CFG-12](#cfg-12). Rebuilding separately for production would lose the same-image promotion evidence.
- **What good looks like:** build from identified source, record the platform and image identity, and promote the verified image with matching configuration, per [Environments And Deployment](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#environments-and-deployment).

### CFG-16

The dependency-update configuration and action pins.

- **Status:** Active
- **Type:** dependency update process
- **Purpose:** turn dependency updates into reviewable changes. Without an update path, a working pin can become a version the team can no longer maintain.
- **Owner:** the Accountable member reviewing each dependency PR.
- **Where:** `.github/dependabot.yml` and the full commit references in workflow `uses` entries.
- **Connections:**
  - `triggers` weekly pip and GitHub Actions PRs through [CFG-02](#cfg-02). A changed ecosystem path could stop updates reaching the package it is meant to watch.
  - `reads` the pin families in [CFG-04](#cfg-04) through [CFG-09](#cfg-09) and [CFG-13](#cfg-13). A digest-pinned container base has no Docker ecosystem entry here, so its review remains an operator responsibility.
- **What good looks like:** third-party actions use full commits, updates are independently reviewed and the runtime pin file is reconciled when affected, per [Pinning Third-Party Actions](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#pinning-third-party-actions).

## Agent context and artifacts

### CFG-17

The root agent instructions.

- **Status:** Active
- **Type:** document
- **Purpose:** give a new editing session the repository map, runnable checks, conventions and restricted paths. Without this entry point, each session can invent a different location or workflow.
- **Owner:** the member changing the repository layout or conventions.
- **Where:** `AGENTS.md`.
- **Connections:**
  - `cites` the upstream router in [CFG-19](#cfg-19) and member conventions in [CFG-18](#cfg-18). Duplicated rule text can diverge from its owning source.
  - `cites` this configuration plan and [CFG-20](#cfg-20). A new maintained guide left out of those entry points can be absent from the next agent's context window.
- **What good looks like:** the four required sections are concise, paths are current, the upstream router is linked once, and this plan is discoverable, per [What It States](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/agent-instructions-requirements.md#what-it-states).

### CFG-18

The member contribution guide.

- **Status:** Active
- **Type:** document
- **Purpose:** make issue ownership, review, commands and history rules available to a team member without relying on an agent session. Without it, work can reach a PR in a form the accountable reviewer cannot finish.
- **Owner:** the member changing the contribution workflow.
- **Where:** `CONTRIBUTING.md`.
- **Connections:**
  - `cites` the Definition of Done and [CFG-02](#cfg-02). A duplicated completion rule can close a task even though its owner has not verified it.
  - `cites` the submodule initialization procedure for [CFG-19](#cfg-19). A clone without that step contains an empty course-materials directory.
- **What good looks like:** a new member can find setup, issue and review instructions and the required checks, per [Contributing](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#contributing).

### CFG-19

The upstream course-materials skill and its pinned submodule.

- **Status:** Active
- **Type:** upstream skill
- **Purpose:** route each deliverable to the rules it is assessed against. Without the identified rules, an editing session can satisfy an older assignment while missing this week's additions.
- **Owner:** the team member adopting a course revision. The course authors maintain its contents.
- **Where:** `.gitmodules` and `.claude/skills/itpd`, whose entry point is the upstream `SKILL.md`.
- **Connections:**
  - `reads` the installed upstream revision recorded by Git. The reviewed baseline pins `0173b82dfb82e515457a1074970c116760490c79`, so the Week 8 assignment supplied at `753d81e9c8b7b78261674c8d4836ef4e4b01d583` must be read explicitly until the team adopts it in the submodule.
  - `produces` the rule routing read by [CFG-17](#cfg-17). An uninitialized or older copy would omit the current configuration and results requirements.
- **What good looks like:** the team installs and identifies the course skill, follows the supplied current assignment, and treats upstream files as read-only, per [The Course Materials As An Agent Skill](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#the-course-materials-as-an-agent-skill).

### CFG-20

The maintained documentation map and artifact families.

- **Status:** Active
- **Type:** documentation index
- **Purpose:** let an operator or editor find the artifact that owns a fact. Without this map, a weekly summary can be mistaken for the maintained specification.
- **Owner:** the member introducing or moving maintained documentation.
- **Where:** `docs/index.md`, which links the requirement, architecture, operations, analytics and usability-test entry points.
- **Connections:**
  - `cites` the maintained families and this plan. A moved requirement without an updated entry point leaves a reader with an obsolete specification path.
  - `produces` the navigation read by [CFG-08](#cfg-08) and [CFG-17](#cfg-17). A guide present only under a week's evidence directory will not have the maintained home those readers expect.
- **What good looks like:** reusable artifacts have one final home under `docs/`, and indexes point there, per [Where Artifacts Live In The Repository](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/general-requirements.md#where-artifacts-live-in-the-repository).

### CFG-21

The weekly public-report and private-submission process.

- **Status:** Active
- **Type:** process
- **Purpose:** give graders a stable map of the week's evidence and private access details with a matching source snapshot. Without one selected main SHA, the report permalink and ZIP can describe different states.
- **Owner:** the week's release and report task's Responsible member.
- **Where:** the `reports/week-NN/` convention and the release/report instructions in `CONTRIBUTING.md`. The PDF builder, private input files and submission receipts are team-local artifacts outside the product repository.
- **Connections:**
  - `reads` [CFG-03](#cfg-03) and the maintained artifacts linked through [CFG-20](#cfg-20). Copying their content into the weekly report would create an additional version to maintain.
  - `produces` a PDF permalink and ZIP from one full main SHA. Including private raw files in that ZIP would disclose the data that the private usability repository and recordings folder are meant to protect.
- **What good looks like:** the public report links the evidence, historical weeks retain their original records, and the private wrapper and snapshot identify the same main commit, per [Permalinks And Snapshots](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#permalinks-and-snapshots).

### CFG-22

The repository's user-facing entry point.

- **Status:** Active
- **Type:** document
- **Purpose:** route a newcomer to the current product, installation and evidence. Without a current entry point, the first instruction can name an older release as the newest one.
- **Owner:** the member changing the public installation or release entry points.
- **Where:** root `README.md`.
- **Connections:**
  - `cites` [CFG-03](#cfg-03) through a version-specific release link and [CFG-21](#cfg-21) through a current-report sentence. A release published without refreshing that sentence leaves the entry point behind the evidence.
  - `cites` [CFG-20](#cfg-20) and the terminal setup guide. A broken setup link would stop a newcomer before the configured plugin flow.
- **What good looks like:** introductory claims identify their version and route readers to working setup and maintained documentation, per [Repository Setup](https://github.com/inno-itpd/itpd/blob/753d81e9c8b7b78261674c8d4836ef4e4b01d583/requirements/repository-requirements.md#repository-setup).
