---
description: Select one strategically coherent product slice for the current run
argument-hint: "<run-id>"
---

Act as the Product Steward for run:

$1

Read:

- `.loop/runs/$1/00-context.md`
- `.loop/runs/$1/01-user-observations.md`
- `docs/product/VISION.md`
- `docs/product/TARGET_USERS.md`
- `docs/product/NON_GOALS.md`
- `docs/product/ROADMAP.md`
- `docs/product/UBIQUITOUS_LANGUAGE.md`
- `docs/product/DECISION_LOG.md`

Select exactly one next slice.

Write:

`.loop/runs/$1/02-product-selection.md`

Use this structure:

# Product Selection

## Selected slice
One sentence.

## Why this, why now
Tie to vision, target user, sequencing, and opportunity cost.

## User value
What improves for the target user?

## Strategic value
How this moves the product toward the intended shape.

## Acceptance criteria
Concrete and testable.

## Non-goals
What must not be included in this slice.

## Reversibility
Easy / moderate / hard to reverse. Explain.

## Risks
Product, UX, strategic, legal, security, or reputational risks.

## Rejected alternatives
Tempting options declined and why.

Stop after writing the file.
