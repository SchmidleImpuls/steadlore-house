---
description: Start one product-loop iteration from current strategy, codebase, and backlog
argument-hint: "[goal, friction, issue, or idea]"
---

Start one product-loop iteration.

Input:

$ARGUMENTS

Create a new run directory:

`.loop/runs/<YYYY-MM-DD-NNN-slug>/`

Use the next available `NNN` for today's date. Create a short slug from the input. Do not implement anything yet.

Read the relevant existing artifacts first:

- `docs/product/VISION.md`
- `docs/product/TARGET_USERS.md`
- `docs/product/NON_GOALS.md`
- `docs/product/ROADMAP.md`
- `docs/product/UBIQUITOUS_LANGUAGE.md`
- `docs/engineering/ARCHITECTURE.md`
- `docs/engineering/SECURITY_BASELINE.md`
- `docs/engineering/TESTING_STRATEGY.md`
- `docs/engineering/TECH_DEBT.md`
- `docs/engineering/MODULE_MAP.md`
- `.loop/LOOP_CHARTER.md`
- `.loop/MERGE_PROTOCOL.md`
- `.loop/ROLE_JURISDICTIONS.md`

Also inspect the codebase or backlog only enough to avoid obvious mismatch with current repository state.

Then write:

`.loop/runs/<run>/00-context.md`

Use this structure:

# Loop Context

## Trigger
The idea, issue, user friction, or goal that started the run.

## Relevant product strategy
Only what matters for this run.

## Relevant engineering context
Only what matters for this run.

## Relevant ubiquitous language
Terms that should shape this run.

## Known constraints
Product, technical, security, legal, operational, or time constraints.

## Initial uncertainty
What is not yet known.

Stop after creating this context file. Tell the human the run id and the next recommended slash command.
