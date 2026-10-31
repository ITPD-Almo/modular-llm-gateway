# Contributing

This guide says how the team works on the Modular LLM Gateway.
What "done" means for a story, a task, and a pull request is in the [Definition of Done](docs/definition-of-done.md), and this guide does not repeat it.

## Issues

- Open every issue from a form: **User story** for a story, **Task** for one unit of work. Blank issues are disabled.
- The forms apply the `User Story` or `Task` issue type. Use `MoSCoW` for a story's value priority, `Story Points` for its refined estimate (1, 2, 3, 5, 8 or 13), and `Priority` (High, Medium or Low) for a task's work order. These are public organization issue fields, not project-only fields or labels.
- A story's `Specified by` lists its FR/ADR specifications; a task's required `Requirements` field lists the FR/ADR records it works on, or explains `None` for upkeep or authoring. Target files must already exist on `main`.
- Keep acceptance criteria as `- [ ] AC-nn: ...` checklists; preserve IDs and checked states. A different Accountable member verifies before ticking; technical tests do not create Customer acceptance.
- Leave unscheduled product-backlog issues without a milestone, role values or assignees. Refine a story and set its estimate before scheduling; split a story larger than 13 points.
- Schedule an issue by putting it in its sprint's milestone, `SPRINT-nn: <focus>`, and set its `Responsible` and `Accountable` fields in the same step.
  `Responsible` does the work and `Accountable` verifies it; they are two different members.
- The issue's assignees are exactly those two members.
- In an issue or a pull request description, link a repository file by its full URL on `main`, such as `https://github.com/ITPD-Almo/modular-llm-gateway/blob/main/docs/decisions.md#dec-006`.

## How a change gets in

1. Open or pick a task issue. Every change, including documentation and CI, goes through a pull request; direct pushes to `main` are blocked.
2. Normally create a branch from `main` named `<issue-number>-<short-description>`, such as `44-write-week-03-plan`.
   For a dependency stack, name the base PR in the description, keep the dependent PR draft until its required records exist on `main`, then merge current dependency changes without rewriting history, retarget to `main` and rerun the checks.
3. Keep the pull request to one change. Open it with the [pull request template](.github/pull_request_template.md), and start the description with `Closes #<issue-number>`.
   One pull request closes exactly one task issue.
4. Fill in the template: what changed and why, what you checked and how, and what the reviewer should look at. This is the change's implementation notes.
5. Request a review from the task's `Accountable` member.

### What the reviewer checks

- Every acceptance criterion of the task issue holds; the reviewer ticks each one in the issue before approving.
- The link check, the Markdown check, and, for product code, the tests workflow are green.
- A user-visible change has an `[Unreleased]` entry in `CHANGELOG.md`.
- No credentials, provider keys, recordings, or personal data are committed.

The reviewer approves and merges. The author cannot approve their own pull request.

## Commit messages

- One short line in the imperative mood, starting with a capital letter and ending without a full stop, such as `Add the plugin loader`.
- At most 72 characters.
- Add a body, separated by a blank line, when the reason for the change is not obvious from the line.
- Merge pull requests with a merge commit, so the history keeps each pull request's commits.

## GitHub project

The team's work is visible in the organization's [GitHub project](https://github.com/orgs/ITPD-Almo/projects/1/views/2), which holds every open issue.

- **Sprint table, grouped by milestone:** columns `Responsible`, `Accountable`, `MoSCoW`, `Story Points`, `Priority`, `Assignees`, `Milestone` and `Status`. We use it at the weekly review to walk each sprint's issues and see who does and who checks each one.

## Code conventions

Use Python 3.12 with type hints. Plugin hooks are synchronous and take and return dictionaries; prefer a new dictionary to preserve ownership between stages. Tests use synthetic inputs and the fake provider, with no provider key or outbound provider call. Preserve documented hook order and compatibility, and update the contract and meaningful tests when either changes.

Do not delete evidence branches or rewrite history to tidy it. Protect published tags and release records; a new release follows reviewed product changes, its tag, dated changelog, plan release line and weekly report in that order.

## Course materials

The course rules are in the `.claude/skills/itpd` submodule.
Clone with `git clone --recurse-submodules`, or run `git submodule update --init` in an existing clone.
