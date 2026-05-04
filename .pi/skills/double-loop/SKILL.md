---
name: double-loop
description: Manual Product Loop and Meta Loop workflow for shipping small software increments through consent-oriented review. Use when starting, reviewing, compiling, or improving loop runs in this repository.
---

# Double Loop Skill

Use this skill to run the repository-local double-loop development system manually through Pi slash commands.

## Read first

- `.loop/LOOP_CHARTER.md`
- `.loop/MERGE_PROTOCOL.md`
- `.loop/ROLE_JURISDICTIONS.md`
- `AGENTS.md`
- `docs/product/UBIQUITOUS_LANGUAGE.md`

## Product Loop sequence

1. `/product-loop-start <goal, friction, issue, or idea>` creates `.loop/runs/<YYYY-MM-DD-NNN-slug>/00-context.md`.
2. `/user-pass <run-id>` writes `01-user-observations.md`.
3. `/steward-pass <run-id>` selects exactly one slice in `02-product-selection.md`.
4. `/dev-pass <run-id>` writes `03-dev-plan.md` without implementing.
5. Optional: `/tdd-pass <run-id>` writes `04-tdd-plan.md`.
6. Implement only after the user explicitly asks for implementation.
7. `/user-review <run-id>` writes `05-user-review.md`.
8. `/steward-review <run-id>` writes `06-steward-review.md`.
9. `/technical-review <run-id>` writes `07-technical-review.md`.
10. `/consent-compile <run-id>` writes `08-gate-decision.md`.

Use `/architecture-pass [focus area]` outside or alongside a run when module boundaries, deep modules, shallow sprawl, or interface quality need inspection.

Every Product Loop run stores artifacts in `.loop/runs/<run-id>/`.

## Meta Loop sequence

Use `/meta-retro [run ids or 'recent']` only when `.loop/META_LOOP.md` entry criteria are met. It writes retrospectives under `.loop/retros/`.

The Meta Loop changes process, not product. It is slower, stricter, versioned, reversible, and resistant to bureaucracy.

## Rules to preserve

- Consent, not consensus.
- Valid objections are jurisdiction-specific, evidence-grounded, material, and actionable unless no safe action exists.
- Reversible product changes bias toward shipping.
- Strategic, irreversible, legal, security-sensitive, privacy-sensitive, or identity-defining changes bias toward restraint and escalation.
- The Developer Agent must not be the sole judge of developer work.
- The Consent Compiler applies the protocol; it does not debate.
- Avoid rule accretion: every new process rule must replace an old rule, retire a recurring failure, or be time-boxed as an experiment.
- Maintain the ubiquitous language across product artifacts, prompts, tests, code names, modules, and docs.

## Implementation caution

This skill is scaffolding. It must not implement Steadlore House product features by itself. When a Product Loop reaches implementation, follow repository safety rules: no secrets, no autonomous remediation, no AI free-form shell execution, local-first defaults, deterministic tools for actions, and tests for meaningful behavior.
