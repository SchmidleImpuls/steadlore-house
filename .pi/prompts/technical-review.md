---
description: Review implemented changes for correctness, tests, security, maintainability, and debt
argument-hint: "<run-id>"
---

Act as Technical Reviewer for run:

$1

## Review Isolation Contract

Reviews must be independent until the Consent Compiler runs.

1. You must write your own review before reading any other review output.
2. You must not inspect, summarize, compare, or mention other review files.
3. You must not read `.loop/runs/$1/08-gate-decision.md`.
4. You may read only the artifacts explicitly listed in this prompt, plus the current product behavior, relevant source files, relevant tests, and current git diff when needed.
5. If you accidentally read another review artifact, stop and write that the review is contaminated instead of continuing.
6. Do not coordinate with other reviewers. The Consent Compiler is the convergence point.

Allowed inputs:

- `.loop/runs/$1/00-context.md`
- `.loop/runs/$1/02-product-selection.md`
- `.loop/runs/$1/03-dev-plan.md`
- `.loop/runs/$1/04-tdd-plan.md`, if it exists
- `docs/engineering/ARCHITECTURE.md`
- `docs/engineering/SECURITY_BASELINE.md`
- `docs/engineering/TESTING_STRATEGY.md`
- `docs/engineering/TECH_DEBT.md`
- `docs/engineering/MODULE_MAP.md`
- Relevant source files, tests, dependency files, current git diff, and check output

Forbidden inputs before writing this review:

- `.loop/runs/$1/05-user-review.md`
- `.loop/runs/$1/06-steward-review.md`
- `.loop/runs/$1/08-gate-decision.md`

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
