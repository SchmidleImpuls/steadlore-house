---
description: Create a small safe implementation plan for the selected product slice
argument-hint: "<run-id>"
---

Act as the Developer Agent for run:

$1

Read:

- `.loop/runs/$1/00-context.md`
- `.loop/runs/$1/02-product-selection.md`
- `docs/engineering/ARCHITECTURE.md`
- `docs/engineering/SECURITY_BASELINE.md`
- `docs/engineering/TESTING_STRATEGY.md`
- `docs/engineering/TECH_DEBT.md`
- `docs/engineering/MODULE_MAP.md`
- `docs/product/UBIQUITOUS_LANGUAGE.md`

Inspect the codebase enough to ground the plan.

Do not implement yet.

Write:

`.loop/runs/$1/03-dev-plan.md`

Use this structure:

# Development Plan

## Codebase facts
Files, modules, patterns, tests, and interfaces relevant to this slice.

## Proposed implementation
Smallest coherent change.

## Module/interface impact
Which deep module or interface is touched, created, or protected?

## Test-first plan
What failing test or verification should come first?

## Files likely touched
List with rationale.

## Security considerations
Risks and mitigations.

## Debt considerations
Debt avoided, introduced, or retired.

## Refused scope
Things deliberately not included.

## Open questions
Only questions that block safe implementation.

Stop after writing the file.
