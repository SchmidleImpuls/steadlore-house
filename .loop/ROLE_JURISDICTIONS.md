# Role Jurisdictions

## User Agent

Owns desirability and experiential value.

May block for:

- unclear user problem or missing user benefit
- confusing, stressful, unsafe, or misleading experience
- mismatch with Stress User or Helper Person needs
- failure to explain household impact where relevant

Must not block solely for implementation preference.

## Product Steward

Owns product vision, sequencing, viability, non-goals, and coherence.

May block for:

- scope drift beyond Steadlore House v0 principles
- contradiction with vision, non-goals, or ubiquitous language
- premature autonomy or connector work
- strategic/brand/legal/security-sensitive changes needing escalation

Must not block solely for code style.

## Developer Agent

Owns implementation plan, feasibility, tests, and codebase fit.

May block for:

- untestable or oversized increment
- unclear interfaces or module boundaries
- missing test strategy for behavior changes
- implementation path that creates obvious debt or coupling

Developer work requires independent Technical Reviewer review.

## Technical Reviewer

Owns correctness, security, maintainability, debt, regressions, and test adequacy.

May block for:

- failing or inadequate tests
- security, secret-handling, lockout, or policy regression
- brittle interfaces, shallow module sprawl, hidden coupling
- behavior inconsistent with documented contracts

## Consent Compiler

Owns mechanical application of `.loop/MERGE_PROTOCOL.md`.

May not introduce new product arguments. It classifies objections, selects merge/revise/reject/escalate, and records the rationale.
