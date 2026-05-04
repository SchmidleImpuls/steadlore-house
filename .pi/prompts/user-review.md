---
description: Review implemented changes from the user perspective
argument-hint: "<run-id>"
---

Act as User Acceptance Reviewer for run:

$1

Read:

- `.loop/runs/$1/01-user-observations.md`
- `.loop/runs/$1/02-product-selection.md`
- `.loop/runs/$1/03-dev-plan.md`

Inspect the current changed product behavior, docs, CLI, UI, examples, or tests as relevant.

Write:

`.loop/runs/$1/05-user-review.md`

Use this structure:

# User Acceptance Review

## Verdict
Pass / Concern / Block

## Acceptance criteria check
Criterion-by-criterion.

## User value delivered
What is genuinely better?

## New friction introduced
What got worse or more confusing?

## Domain-valid blocking objections
Only user-experience or user-value blockers.

## Non-blocking concerns
Concerns that should not block merge.

## Suggested follow-ups
Backlog candidates only.
