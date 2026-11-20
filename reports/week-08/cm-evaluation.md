# CM Evaluation

- **Baseline:** [ae808ad501553d9ba67ff50b2ee0c99424fb2f48](https://github.com/ITPD-Almo/modular-llm-gateway/commit/ae808ad501553d9ba67ff50b2ee0c99424fb2f48), the main commit containing the REL-07 release record.
- **Reviewed:** 2026-11-20

## Method

For Ali12hamdan, Codex reviewed the identified main checkout and readable GitHub settings on November 20, then prepared this evaluation for Mohammed-Nour's independent task review.
The review wrote a local goal for each artifact family, grouped artifacts by those goals, followed their configuration connections, compared the repository's commands and entry points with its recorded release, and weighed a simpler artifact set for each goal.
It read the workflows, manifests, build files, maintained documentation and historical evidence, then checked branch protection, tag protection and the main CI run.
Live VM state, private instructor access, participant evidence and future review outcomes were outside the inspected evidence.
The [configuration plan](../../docs/configuration-plan.md) records 22 Active items across all five groups and assigns the identifiers used below.
All 22 identified items remain in use at the reviewed baseline.

## Find the product decision and its specification

A maintainer needs to find the reason for a behavior and the artifact that defines it without reading every weekly report.

- **Today:** the maintained family entry points at [CFG-20](../../docs/configuration-plan.md#cfg-20), the agent map at [CFG-17](../../docs/configuration-plan.md#cfg-17) and course routing at [CFG-19](../../docs/configuration-plan.md#cfg-19) lead to the product vision, decisions, FR index and architecture records. The [documentation index](../../docs/index.md#requirements) links those artifacts directly.
- **A more convenient way:** `Keep` those distinct maintained entry points and their identifiers. `Replace` the installed course revision with the explicitly adopted current course revision when the team updates that upstream dependency. Preserve the task-supplied assignment revision as the basis of this evaluation.
- **Why:** the requirement and ADR indexes already give direct paths to definitions, while the submodule at this baseline still pins the Assignment 5 revision. During this review the empty local submodule could not supply A8, so the supplied assignment and linked rules had to be retrieved explicitly. The [CFG-19 Connections field](../../docs/configuration-plan.md#cfg-19) names that context gap.
- **Tradeoffs:** retaining separate decision, FR and ADR records costs an additional link-following step but preserves who agreed the direction and what behavior is specified. Adopting a newer course revision requires a review of changed rules, which is preferable to silently treating the older installed copy as current.

## Tell owners what is scheduled and what is accepted

A team member needs one authoritative work schedule and an evidence trail for completion.

- **Today:** [CFG-02](../../docs/configuration-plan.md#cfg-02), [CFG-18](../../docs/configuration-plan.md#cfg-18) and [CFG-21](../../docs/configuration-plan.md#cfg-21) connect task issues, public Responsible/Accountable fields, assignees, sprint milestones and report evidence. The [project plan](../../docs/project-plan.md#sprint-08) links the sprint milestones, and [contribution instructions](../../CONTRIBUTING.md#issues) state where assignments live.
- **A more convenient way:** `Keep` GitHub issues and milestones as the schedule and the plan as the sprint's goal and release record. Keep task closure separate from a story's Customer verdict. Use links from the weekly report to those records instead of adding a second hand-maintained backlog in Markdown.
- **Why:** the same Responsible and Accountable values are readable from an issue and the project, while the [Week 7 report](../week-07/README.md#minimum-usable-product-and-customer-outcome) already distinguishes reviewed implementation from outstanding story verdicts. Another copy of issue state would require an edit every time a task changes hands.
- **Tradeoffs:** the repository ZIP cannot expose every live project field or private reviewer action. The sprint plan and report retain the selection, evidence and outcome a reader of the snapshot needs, while GitHub carries the operational schedule.

## Verify the change through the delivery paths people use

A reviewer needs distinct evidence for source behavior, installed behavior and readable documentation.

- **Today:** [product CI](../../docs/configuration-plan.md#cfg-04), [Markdown](../../docs/configuration-plan.md#cfg-05), [links](../../docs/configuration-plan.md#cfg-06), [actionlint](../../docs/configuration-plan.md#cfg-07), [site publication](../../docs/configuration-plan.md#cfg-08) and [installed-terminal checks](../../docs/configuration-plan.md#cfg-09) provide separate signals. The [baseline main Tests run](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/43690230267) and the workflow definitions identify which source they test. The branch setting in [CFG-01](../../docs/configuration-plan.md#cfg-01) consumes the named link check, while the contribution process calls for the relevant remaining checks before approval.
- **A more convenient way:** `Keep` the separate workflow signals and the installed-package matrix. `Add` one consistent local validation recipe to the member guide that names the existing configurations and the strict docs command, then let agent instructions point at that recipe while preserving their required Checks section.
- **Why:** the [product workflow](../../.github/workflows/tests.yml) checks an editable install, and the [terminal workflow](../../.github/workflows/terminal-install.yml) deliberately runs outside a checkout, exercising a failure mode the first path cannot prove. The agent instructions specify a strict MkDocs build, while [the Pages workflow](../../.github/workflows/pages.yml) runs the ordinary build. A clear local recipe would remove the need to reconstruct those validation differences each time. During validation of this review, [three link-check attempts](https://github.com/ITPD-Almo/modular-llm-gateway/actions/runs/44741681350) received HTTP 503 for existing GitHub evidence. The shared `lychee.toml` now bounds concurrency and retries and verifies this repository's SHA-pinned commit and file links against GitHub's commit API and raw-file endpoints, preserving the SHA and file path. This enacted improvement checks the underlying evidence object when GitHub's HTML renderer is unavailable.
- **Tradeoffs:** keeping six workflow entry points means more files and repeated checkout declarations, but each result has a different reviewer meaning. A shared recipe adds a maintained pointer, so it must reference the existing configurations rather than copy their rules. The immutable-link remap verifies that the source object exists and leaves public HTML rendering outside that check. GitHub API availability and its request quota remain external dependencies. Query-bearing, fragment-bearing and moving-reference links retain their original destinations.

## Recreate the selected runtime on another machine

An operator needs to identify the source and dependency set that produced the candidate before promoting it.

- **Today:** [CFG-13](../../docs/configuration-plan.md#cfg-13) declares version ranges, [CFG-14](../../docs/configuration-plan.md#cfg-14) compiles the runtime pins, [CFG-15](../../docs/configuration-plan.md#cfg-15) builds the digest-based image, and [CFG-16](../../docs/configuration-plan.md#cfg-16) proposes dependency updates. The [Dockerfile](../../Dockerfile) and [compiled runtime file](../../requirements-runtime.txt) show the image inputs. The native installer also consumes that compiled file, while editable source CI resolves the manifest.
- **A more convenient way:** `Keep` the compiled runtime set and promotion of one verified image. `Add` an explicit container-base update path when the team can maintain it. Keep the selected image ID and source SHA in the deployment receipt instead of rebuilding independently for production.
- **Why:** the [Dependabot configuration](../../.github/dependabot.yml) watches pip and GitHub Actions, while the image base is a separate digest. The [CFG-16 Connections field](../../docs/configuration-plan.md#cfg-16) identifies the uncovered update input. Keeping the runtime pins still avoids a different transitive resolution at every installer or image run.
- **Tradeoffs:** another update path produces another kind of PR and needs platform checks. Pinning the Python base and runtime versions reduces change between builds, but the evidence does not prove byte-identical wheels across platforms or fully locked source-test environments. Those limits remain explicit.

## Observe sessions without changing ordinary usage evidence

The usability observer needs a clean start and a link from the participant attempt to the records that can actually explain it.

- **Today:** the runbook at [CFG-10](../../docs/configuration-plan.md#cfg-10), the configuration shape at [CFG-11](../../docs/configuration-plan.md#cfg-11) and the isolated fixture at [CFG-12](../../docs/configuration-plan.md#cfg-12) establish separate settings and test-event scope. The [UT-01 record](../../docs/usability-tests/ut-01/README.md#instrumentation) owns the observation measures and blind spots. The [verified implementation rehearsal](https://github.com/ITPD-Almo/modular-llm-gateway/pull/129#issuecomment-6854627777) is technical evidence for the fixture.
- **A more convenient way:** `Keep` the dedicated test organization, UTC-window export, synthetic reset and offline marker probe. Keep the observation sheet and surveys beside the technical export instead of replacing assistance and reasoning with event counts.
- **Why:** the [staging procedure](../../docs/ut01-staging.md#export-and-verify-a-private-session-window) already supplies an allowlisted export route. The [CFG-12 Connections field](../../docs/configuration-plan.md#cfg-12) states why a successful HTTP reply cannot establish that the task was unaided. Reusing the technical evidence for that claim would remove the observation that gives QR-09 its denominator and numerator.
- **Tradeoffs:** a facilitator must reconcile two kinds of records and arrange private access. That work preserves the ability to tell environment failure, assisted success and unaided success apart. The mechanism remains subject to pre-session verification before its first counted use.

## Communicate the current release with fewer manual copies

A newcomer needs a current release entry point while historical evidence remains fixed.

- **Today:** [CFG-22](../../docs/configuration-plan.md#cfg-22) names the current release in root README prose, while [CFG-03](../../docs/configuration-plan.md#cfg-03) and [CFG-21](../../docs/configuration-plan.md#cfg-21) own release and report history. At the baseline, [the root README](https://github.com/ITPD-Almo/modular-llm-gateway/blob/ae808ad501553d9ba67ff50b2ee0c99424fb2f48/README.md) calls v0.5.0 the latest release and points to Week 5 for the current release, whereas [the same baseline's changelog](https://github.com/ITPD-Almo/modular-llm-gateway/blob/ae808ad501553d9ba67ff50b2ee0c99424fb2f48/CHANGELOG.md) already records v0.7.0.
- **A more convenient way:** `Replace` the manually maintained latest-release sentence with the repository's stable latest-release link. `Keep` version-specific setup examples and historical report links with their version or week named explicitly, and keep the dated changelog and release blocks as the record of what shipped.
- **Why:** the disagreement is visible within one frozen commit. The [CFG-22 Connections field](../../docs/configuration-plan.md#cfg-22) identifies the redundant current-version claim that every release must remember to update. A stable release pointer removes that repeated editorial step without removing the dated records.
- **Tradeoffs:** the latest-release destination changes over time and needs GitHub connectivity. A reader inspecting an older ZIP must use that ZIP's dated changelog and release block to identify its version. Keeping those immutable references preserves reproducibility while the online entry point can stay current.

## What We Could Not Judge

The current university VM and the actual staging/production source and image identities were not inspected in this review.
The runbook and [Week 7 evidence](../week-07/README.md#repository-evidence) describe their last checked state, which does not establish today's state.
The risk is environment drift or a failed demonstration, so the [environment-drift risk](../../docs/risks.md#risk-13) owns the recovery.

The live private ingestion scopes, recording-folder permissions and instructor access to the raw-data repository were not verified.
The risk is an unreadable evidence trail or access broader than intended, even when public link checks pass.
Their actual addresses and credentials are kept in the private submission materials.

A hash-locked complete development/build dependency set and a Docker-ecosystem update configuration are absent from this baseline.
They have no CFG identifiers because they do not exist.
Source CI uses manifest ranges, and the base-image digest has a manual update path, so fully repeatable developer dependency resolution and timely base-image updates could not be established.

## The First Change

Replace the root README's manually maintained latest-release claim with the stable GitHub latest-release pointer first, while keeping the pinned installation examples, dated changelog, release blocks and explicitly historical reports.
This removes the extra current-version claim that already disagrees with the baseline's release record.
Its main tradeoff is that the online pointer changes over time, so the snapshot's dated records remain the source for reproducing that snapshot.
The other goal sections remain recommendations and schedule no work.
