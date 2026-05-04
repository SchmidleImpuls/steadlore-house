---
description: Build or update the shared product/code vocabulary from docs and code
argument-hint: "[focus area]"
---

Build or update the ubiquitous language.

Focus:

$ARGUMENTS

Read product docs, engineering docs, tests, public APIs, domain model files, module names, and user-facing copy.

Update:

`docs/product/UBIQUITOUS_LANGUAGE.md`

Use this structure:

# Ubiquitous Language

| Term | Meaning | Used by users? | Used in code? | Related terms | Avoid/confusion |
|---|---|---:|---:|---|---|

Also include:

## Naming mismatches
Where code, docs, tests, or product language use different names for the same concept.

## Terms to retire
Terms that should be removed or replaced.

## Terms needing decision
Important concepts that lack stable names.

Rules:

- Prefer precise domain terms over generic software terms.
- If two terms overlap, distinguish or merge them.
- If a code identifier conflicts with the product language, flag it.
- Do not rename code yet. Produce the language map first.
