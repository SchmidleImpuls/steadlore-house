---
description: Produce user-perspective observations for the current product-loop run
argument-hint: "<run-id>"
---

Act as the User Agent for run:

$1

Read:

- `.loop/runs/$1/00-context.md`
- `docs/product/TARGET_USERS.md`
- `docs/product/VISION.md`
- `docs/product/UBIQUITOUS_LANGUAGE.md`

If the product has runnable software, inspect the relevant UX, CLI, docs, examples, tests, screenshots, or flows. Use evidence where possible. Do not invent certainty.

Write:

`.loop/runs/$1/01-user-observations.md`

Use this structure:

# User Observations

## User stance
Which target user perspective is being represented?

## What I tried or inspected
Concrete path, command, screen, file, or scenario.

## Frictions
Observed or strongly inferred user pains.

## Desires
What the user would naturally want next.

## Delight or value
What already works or feels promising.

## Evidence
Commands, files, outputs, screenshots, docs, or explicit assumptions.

## Suggested next improvements
Ranked by user value.

## Non-blocking caveats
What may be persona simulation rather than evidence.

Stop after writing the file.
