---
description: Turn a selected product slice into a test-first implementation path
argument-hint: "<run-id>"
---

Create a test-first path for run:

$1

Read:

- `.loop/runs/$1/02-product-selection.md`
- `.loop/runs/$1/03-dev-plan.md`
- `docs/engineering/TESTING_STRATEGY.md`
- `docs/engineering/MODULE_MAP.md`

Write or update:

`.loop/runs/$1/04-tdd-plan.md`

Use this structure:

# TDD Plan

## Behavior under test
What user-visible or module-visible behavior must change?

## Smallest failing test
The first failing test to write.

## Test level
Unit / integration / e2e / snapshot / type-level / manual check. Explain why.

## What not to mock
Real dependencies needed for confidence.

## What to mock or fake
Dependencies that would make the test slow, flaky, or irrelevant.

## Red-green-refactor path
1. Red:
2. Green:
3. Refactor:

## Feedback cadence
How often to run tests/checks during implementation.

## Risks
Flakiness, over-mocking, brittle assertions, missing behavior.

Rules:

- The rate of feedback is the speed limit.
- Prefer small deliberate steps.
- Do not implement broad code before creating a feedback loop.
