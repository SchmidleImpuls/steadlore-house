---
description: Review implemented changes from the product strategy perspective
argument-hint: "<run-id>"
---

Act as Product Steward Reviewer for run:

$1

Read:

- `.loop/runs/$1/02-product-selection.md`
- `docs/product/VISION.md`
- `docs/product/TARGET_USERS.md`
- `docs/product/NON_GOALS.md`
- `docs/product/ROADMAP.md`
- `docs/product/DECISION_LOG.md`

Inspect the diff and relevant artifacts.

Write:

`.loop/runs/$1/06-steward-review.md`

Use this structure:

# Steward Review

## Verdict
Pass / Concern / Block

## Vision alignment
Does this move toward the intended product?

## Scope discipline
Did the implementation stay inside the selected slice?

## Non-goal check
Any violation?

## Strategic risk
Any drift, premature complexity, wrong-user optimization, or positioning confusion?

## Domain-valid blocking objections
Only product-strategy blockers.

## Non-blocking concerns
Concerns that should not block merge.

## Suggested follow-ups
Backlog or decision-log candidates.
