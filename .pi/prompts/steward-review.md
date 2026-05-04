---
description: Review implemented changes from the product strategy perspective
argument-hint: "<run-id>"
---

Act as Product Steward Reviewer for run:

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
- `docs/product/VISION.md`
- `docs/product/TARGET_USERS.md`
- `docs/product/NON_GOALS.md`
- `docs/product/ROADMAP.md`
- `docs/product/UBIQUITOUS_LANGUAGE.md`
- `docs/product/DECISION_LOG.md`
- Relevant diff or changed artifacts needed to judge product coherence

Forbidden inputs before writing this review:

- `.loop/runs/$1/05-user-review.md`
- `.loop/runs/$1/07-technical-review.md`
- `.loop/runs/$1/08-gate-decision.md`

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
