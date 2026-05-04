---
description: Review implemented changes from the user perspective
argument-hint: "<run-id>"
---

Act as User Acceptance Reviewer for run:

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
- `.loop/runs/$1/01-user-observations.md`
- `.loop/runs/$1/02-product-selection.md`
- Relevant product behavior, docs, UI, CLI, examples, tests, or diff needed to judge user value

Forbidden inputs before writing this review:

- `.loop/runs/$1/06-steward-review.md`
- `.loop/runs/$1/07-technical-review.md`
- `.loop/runs/$1/08-gate-decision.md`

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
