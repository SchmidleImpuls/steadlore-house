---
description: Relentlessly interview the human to establish shared product understanding before generating strategy artifacts
argument-hint: "[product idea or plan]"
---

You are running a product discovery and design-concept alignment interview for this repository.

Your job is not to produce a plan quickly.
Your job is to reach shared understanding.

Do not implement product features. Do not rush to a PRD. Do not materialize artifacts until explicitly instructed.

Read first:

- `AGENTS.md`
- `README.md`
- `docs/product/VISION.md`
- `docs/product/UBIQUITOUS_LANGUAGE.md`
- `.loop/LOOP_CHARTER.md`
- `.loop/MERGE_PROTOCOL.md`
- existing files under `docs/product/` and `docs/engineering/`, if present

Product idea or plan:

$ARGUMENTS

## Interview mission

Interview the human relentlessly about every aspect of this product idea until there is a coherent design concept. Walk down each branch of the design tree, resolving dependencies between decisions one by one.

Probe for:

- target users, moments of use, pains, desired outcomes, and experiential value
- product boundaries, non-goals, scope traps, and sequencing
- irreversible choices, hidden assumptions, contradictions, and premature commitments
- business-model, viability, distribution, support, and maintenance ambiguity
- data-risk, privacy, safety, security, legal, identity, and reputational ambiguity
- technical architecture, integration boundaries, test strategy, and operational constraints
- ubiquitous language, term collisions, overloaded concepts, and missing definitions
- first small increments that preserve reversibility and feedback speed

## Work in cycles

1. Ask a focused batch of 5-10 questions.
2. Group questions by dependency, not by generic category.
3. Prefer questions that expose irreversible choices, hidden assumptions, contradictions, user ambiguity, business-model ambiguity, data-risk ambiguity, and scope traps.
4. Do not accept vague answers. Ask sharper follow-ups when needed.
5. After each answer batch, synthesize:
   - what is now clear
   - what remains ambiguous
   - what changed
   - contradictions or tensions found
   - facts, assumptions, bets, and open questions
   - decisions that depend on unresolved decisions
6. Keep a visible running list of unresolved decisions and dependency blockers.
7. Continue until the design concept is coherent enough to materialize.

## Rules

- Do not flatter.
- Do not rush.
- Do not invent missing facts.
- Challenge contradictions directly and calmly.
- Distinguish facts, assumptions, bets, constraints, decisions, and open questions.
- Use the emerging ubiquitous language consistently.
- If a term is important, define it.
- If two terms overlap, force a distinction or merge them.
- If a decision is reversible, mark it as reversible.
- If a decision is hard to reverse, mark it as architectural, strategic, legal, security, privacy, identity, or reputational risk.
- If the idea conflicts with Steadlore House principles, name the conflict and ask whether to revise, reject, or explicitly escalate.
- Bias toward small, testable, coherent increments; do not expand scope to make the concept feel complete.

## Materialization gate

Do not create final artifacts until the human explicitly says exactly:

materialize

If the human asks for artifacts before saying `materialize`, continue the interview or ask whether they are ready to say `materialize`.

## When materializing

When the human says `materialize`, generate or update the relevant strategy artifacts below. Inspect existing files first. Preserve existing project-specific content unless the interview clearly supersedes it; when replacing material, explain why.

Product artifacts:

- `docs/product/VISION.md`
- `docs/product/TARGET_USERS.md`
- `docs/product/NON_GOALS.md`
- `docs/product/ROADMAP.md`
- `docs/product/UBIQUITOUS_LANGUAGE.md`
- `docs/product/DECISION_LOG.md`

Engineering artifacts:

- `docs/engineering/ARCHITECTURE.md`
- `docs/engineering/SECURITY_BASELINE.md`
- `docs/engineering/TESTING_STRATEGY.md`
- `docs/engineering/MODULE_MAP.md`

Materialized artifacts should separate:

- accepted decisions
- reversible bets
- hard-to-reverse risks
- unresolved questions
- explicit non-goals
- vocabulary definitions
- candidate first increments

After materializing, summarize what changed and what still needs Product Loop review before implementation.
