---
description: Review implemented changes for correctness, tests, security, maintainability, and debt
argument-hint: "<run-id>"
---

Act as Technical Reviewer for run:

$1

Read:

- `.loop/runs/$1/02-product-selection.md`
- `.loop/runs/$1/03-dev-plan.md`
- `docs/engineering/ARCHITECTURE.md`
- `docs/engineering/SECURITY_BASELINE.md`
- `docs/engineering/TESTING_STRATEGY.md`
- `docs/engineering/TECH_DEBT.md`
- `docs/engineering/MODULE_MAP.md`

Inspect the diff and run relevant checks if possible.

Write:

`.loop/runs/$1/07-technical-review.md`

Use this structure:

# Technical Review

## Verdict
Pass / Concern / Block

## Correctness
Bugs, edge cases, logic errors.

## Tests and feedback loops
What was tested? What is missing?

## Security
Security posture changes, sensitive data, auth, permissions, injection, dependency risk.

## Maintainability
Complexity, coupling, naming, module boundaries, readability.

## Architecture
Dee
