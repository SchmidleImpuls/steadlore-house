---
description: Run a retrospective over recent product-loop runs and propose at most one loop improvement
argument-hint: "[run ids or 'recent']"
---

Run the Meta Loop.

Object under review: the product-development loop itself, not the product.

Input:

$ARGUMENTS

Read:

- `.loop/LOOP_CHARTER.md`
- `.loop/MERGE_PROTOCOL.md`
- `.loop/ROLE_JURISDICTIONS.md`
- `.loop/META_LOOP.md`
- `.loop/METRICS.md`
- `.loop/CHANGELOG.md`
- `.loop/ESCALATIONS.md`
- `.loop/runs/` as relevant

Look for recurring evidence, not isolated irritation.

Analyze:

- repeated blockers
- repeated escalations
- late-discovered product ambiguity
- late-discovered technical risk
- missing tests
- scope creep
- review theater
- excessive ceremony
- ignored artifacts
- confusing role boundaries
- rule accretion
- human overrides
- shipped changes later regretted

Create `.loop/retros/` if needed.

Write a new file:

`.loop/retros/<YYYY-MM-DD-retro>.md`

Use this structure:

# Meta Retrospective

## Runs reviewed
List.

## Observed patterns
Evidence across runs.

## What worked
Loop behaviors worth preserving.

## What failed
Recurring process failures.

## Candidate loop changes
List options.

## Selected loop change
At most one.

## Expected benefit
What should improve?

## Cost and risk
What ceremony or rigidity might this add?

## Trial period
How many future runs?

## Adoption criterion
How we know the change worked.

## Rollback criterion
How we know to remove it.

## Consent review
Does this change preserve the loop charter?

Do not modify loop rules directly unless explicitly asked.
