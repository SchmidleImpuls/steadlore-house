# Contributing to Steadlore House

Thank you for helping build Steadlore House.

This project is about continuity, not cleverness. Contributions should make household-critical knowledge more understandable, verifiable, safe, and useful under stress.

## Read first

Before contributing, read:

- `README.md`
- `AGENTS.md`
- `docs/vision.md`
- `docs/ubiquitous-language.md`

If you are an AI coding agent, treat `AGENTS.md` as binding project guidance.

## Contribution mindset

Steadlore House serves two audiences at once:

1. The technical operator who understands the household infrastructure.
2. The trusted person who may need help when the operator is unavailable.

Good contributions respect both.

A feature is not done just because it is technically correct. It must also be explainable, safe, and honest about uncertainty.

## Preferred order of work

Use this sequence whenever possible:

1. Clarify the domain language.
2. Update or confirm the data model.
3. Add or update examples.
4. Add tests.
5. Implement the smallest useful behavior.
6. Update documentation.
7. Re-check safety implications.

Do not begin with UI, chat, or automation if the underlying model is unclear.

## Scope discipline

Steadlore House should not become a pile of adjacent tools.

Before adding a feature, ask:

- Does this help the household understand what matters?
- Does this help a trusted person recover safely?
- Does this improve the continuity manual?
- Does this preserve provenance and staleness?
- Does this avoid storing secrets?
- Does this avoid unsafe autonomy?

If the answer is no, the feature probably belongs elsewhere.

## Ubiquitous language

Use the terms defined in `docs/ubiquitous-language.md`.

If you introduce a new concept, add it there first or explain why the existing vocabulary is insufficient.

Avoid synonyms that blur meaning.

For example:

- Use `Device` for physical objects.
- Use `Service` for useful capabilities.
- Use `Runbook` for structured recovery guidance.
- Use `Fact` for claims the system can use.
- Use `Evidence` for source and verification metadata.
- Use `Secret Reference` for pointers to secrets stored elsewhere.

Do not casually use terms like agent, bot, automation, node, asset, or resource when a precise project term exists.

## Safety rules

Never contribute code, docs, examples, tests, fixtures, or generated output that contain:

- real passwords
- real tokens
- private keys
- recovery keys
- TOTP seeds
- backup codes
- full emergency-kit details
- sensitive household access instructions
- instructions that could lock out the operator

Secret references are allowed.

A good secret reference points to where a trusted person can find information without exposing the information directly.

## Manual-first development

The continuity manual is the primary product artifact.

Before adding an interface such as Telegram, web chat, or an LLM layer, ensure the same information can be generated into readable Markdown.

If the manual cannot explain it, the chatbot should not pretend to explain it.

## Staleness and uncertainty

Every meaningful fact should have a path toward provenance and freshness.

Prefer answers like:

- The latest verified note says this device hosts Home Assistant, but that note is 91 days old.
- I do not know which switch port this access point uses.
- This was discovered from Portainer 6 minutes ago.
- This location was manually confirmed 4 months ago.

Avoid answers that hide uncertainty.

## Tests

Tests should cover behavior that protects trust.

Prioritize tests for:

- schema validation
- Markdown rendering
- stale-data classification
- missing-data behavior
- secret redaction
- forbidden-action enforcement
- runbook rendering
- household-impact output

Avoid brittle tests that only preserve incidental formatting.

## Documentation

Documentation should be plain, precise, and grounded.

Avoid hype.

Avoid promising features that do not exist.

Use future-oriented language only in contributor docs and vision docs.

The README should describe what currently exists and what the project is aiming toward without pretending the software is already usable.

## Pull request checklist

Before opening a pull request, confirm:

- The change fits the project scope.
- The project vocabulary is used consistently.
- New concepts are documented.
- No secrets or sensitive real-world data are included.
- Generated output remains readable.
- Tests were added or updated where appropriate.
- Safety implications were considered.
- The change does not introduce autonomous remediation.
- The change does not allow free-form shell execution.
- The change does not let the system lock out the operator.

## Commit style

Use clear, boring commit messages.

Good examples:

- Add initial device schema
- Render stale facts in manual
- Add Home Assistant down runbook example
- Document secret reference rules

Weak examples:

- Update stuff
- AI improvements
- Make it smart
- Fix magic

## AI-generated contributions

AI-generated contributions are welcome if they follow the same standards as human contributions.

AI-generated code should be reviewed especially carefully for:

- invented behavior
- hidden assumptions
- scope creep
- unsafe defaults
- missing tests
- fake certainty
- accidental secret exposure
- unnecessary abstraction

The project should use AI as a tool, not as an excuse to lower standards.

## Security reports

If you find a vulnerability or a pattern that could expose secrets, enable lockout, mislead a stress user, or permit unsafe remediation, treat it as security-relevant.

Until a dedicated security policy exists, do not publish exploit details in public issues.

## Final principle

A trusted person may use Steadlore House while stressed.

Design accordingly.