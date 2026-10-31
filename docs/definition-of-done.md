# Definition of done

## Story

- The issue has type `User Story`, one `MoSCoW` value and resolving FR/ADR links in `Specified by`.
- Every acceptance criterion passes on `main`.
- Every task issue that works on the story has closed with its pull request merged, so each also met the Task and Pull Request lists below.
- The story issue links the evidence for each criterion.
- The accountable member has checked that each criterion is runnable, and that every link on the issue resolves.

A story closes only on the Customer's acceptance, recorded as a `DEC-nnn` in [decisions.md](decisions.md) and in a comment on the story issue.

## Task

- The issue has type `Task`, a required `Requirements` list of FR/ADR links or an explained `None`, and numbered checkbox criteria.
- Every acceptance criterion the task carries is satisfied.
- The task closes as completed, which happens when the pull request that closes it merges into `main`.
- The task is scheduled in its sprint's GitHub milestone and carries its `Priority`, distinct `Responsible` and `Accountable` values, and exactly the two matching assignees.

We keep no task tracker in the repository: every task is a GitHub issue opened from the Task form.

## Pull Request

- A pull request closes exactly one task issue and links it with `Closes #<number>`.
- The accountable reviewer ticks every task acceptance criterion before approving.
- The approval comes from a member other than the author.
- The documentation site builds strictly; the repository checks are green: the link check, the Markdown check, `actionlint` over the workflows, and the product-code checks of the tests workflow: lint (`ruff check`), format (`ruff format --check`), type check (`mypy gateway`), build (`python -m build --wheel`) and tests (`python -m pytest`).
- A user-visible change updates the `[Unreleased]` section of `CHANGELOG.md`.
- The acceptance criteria this pull request claims pass on its branch, and on `main` after it merges.
- No secret, provider key, recording, or private-only material is committed.
- Implementation notes in the pull request description record the decisions made and how the change was checked.
