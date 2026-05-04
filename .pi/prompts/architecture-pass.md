---
description: Inspect the codebase for module boundaries, deep modules, shallow sprawl, and interface quality
argument-hint: "[focus area]"
---

Inspect architecture with emphasis on AI-maintainable code.

Focus:

$ARGUMENTS

Read:

- `docs/engineering/ARCHITECTURE.md`
- `docs/engineering/MODULE_MAP.md`
- `docs/engineering/TECH_DEBT.md`
- `docs/product/UBIQUITOUS_LANGUAGE.md`

Inspect the relevant code.

Update or create:

`docs/engineering/MODULE_MAP.md`

Use this structure:

# Module Map

## Current deep modules
Modules with substantial hidden functionality behind simple interfaces.

## Shallow-module sprawl
Small fragments with weak boundaries, excessive coupling, or confusing traversal.

## Important interfaces
Interfaces humans should design carefully before delegating implementation.

## Testable boundaries
Where behavior can be verified from outside the module.

## Boundary problems
Where tests are hard because boundaries are poor.

## Recommended architecture improvements
Ranked by leverage and reversibility.

Rules:

- Do not refactor yet.
- Prefer fewer, deeper modules with simple interfaces.
- Protect important interfaces.
- Flag code that makes AI-assisted changes riskier.
