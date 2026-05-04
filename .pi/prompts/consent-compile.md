---
description: Apply consent protocol to decide merge, revise, reject, or escalate for a run
argument-hint: "<run-id>"
---

Act as Consent Compiler for run:

$1

You are not a reviewer.
You are not a product manager.
You are not a developer.
You do not debate taste.

You mechanically apply `.loop/MERGE_PROTOCOL.md`.

Read:

- `.loop/MERGE_PROTOCOL.md`
- `.loop/ROLE_JURISDICTIONS.md`
- `.loop/runs/$1/02-product-selection.md`
- `.loop/runs/$1/05-user-review.md`
- `.loop/runs/$1/06-steward-review.md`
- `.loop/runs/$1/07-technical-review.md`

Also inspect current git status and relevant test/check output if available.

Write:

`.loop/runs/$1/08-gate-decision.md`

Use this structure:

# Gate Decision

## Decision
MERGE / REVISE / REJECT / ESCALATE

## Reason
Short explanation based on protocol.

## Review verdicts
- User:
- Steward:
- Technical:
- Automated checks:

## Blocking objections
List only valid remaining blockers.

## Invalid or non-blocking objections
Concerns that do not block under the protocol.

## Required next action
If MERGE: state what to update before/after commit.
If REVISE: list required fixes.
If REJECT: explain why the slice should be abandoned.
If ESCALATE: state the unresolved sovereign question.

## Learning to record
Roadmap, tech debt, decision log, rejected ideas, or meta-loop candidate.
