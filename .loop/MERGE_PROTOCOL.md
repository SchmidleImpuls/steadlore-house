# Merge Protocol

## Consent rule

Merge when every blocking objection is resolved, withdrawn, converted into tracked follow-up, or ruled invalid by the protocol.

Consent is not consensus. Reviewers do not need to prefer the change; they must lack a valid blocking objection within their jurisdiction.

## Valid blocking objection

A blocking objection must be all of the following:

1. Domain-specific to the reviewer's jurisdiction.
2. Evidence-grounded in repository state, product artifacts, tests, threat model, or explicit user intent.
3. Material to user value, product coherence, safety, correctness, security, maintainability, reversibility, or identity.
4. Actionable, or it must explain why no safe action exists.

Invalid objections include taste without consequence, jurisdiction drift, speculative discomfort without evidence, and requests for unrelated scope expansion.

## Bias rules

- Reversible product changes bias toward shipping.
- Irreversible, strategic, legal, security-sensitive, privacy-sensitive, brand/identity-defining, or lockout-risk changes bias toward restraint and escalation.
- Non-trivial behavior changes should use TDD or test-first thinking.
- Interfaces deserve deliberate design before implementation is delegated behind them.

## Consent compiler decisions

- **Merge**: no valid blocking objections remain.
- **Revise**: valid objections remain and a bounded revision is available.
- **Reject**: the proposal conflicts with charter, non-goals, security baseline, or no longer has a coherent purpose.
- **Escalate**: human decision required because scope is strategic, irreversible, legal, security-sensitive, brand-sensitive, or beyond current artifacts.

The Consent Compiler does not debate merits. It quotes objections, checks them against the protocol, and records the decision.
