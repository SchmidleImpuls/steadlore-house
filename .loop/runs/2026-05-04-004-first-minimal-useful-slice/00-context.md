# Loop Context

## Trigger

The run starts from the input: "first minimal useful slice".

The likely intent is to identify the smallest coherent product increment that makes Steadlore House more useful without prematurely expanding scope. No implementation has been requested for this run-start step.

## Relevant product strategy

- Steadlore House should make a technically complex household understandable and recoverable when the Operator is unavailable.
- The first useful household continuity artifact remains the Continuity Manual.
- The first target scenario is symptom-first: "Lights or automations are not working."
- The accepted next strategic milestone is the dependency graph model and rendering because it supports the Infrastructure Map, improves Operator setup value, and strengthens the Continuity Manual / Helper Person appendix.
- Near-term strategy favors small, reversible increments before GUI, connectors, chat interfaces, or remediation.
- The Infrastructure Map is the Operator-facing review surface, but it should not confuse discovery observations with reviewed household meaning.

## Relevant engineering context

- Current repository state is a Python prototype with YAML as the canonical local source of truth.
- Implemented foundations include Manual Inventory parsing, Runbook parsing, schema validation, relationship validation, staleness calculation, deterministic Continuity Manual rendering, deterministic AI Assistance Packet rendering, local Network Discovery Snapshot rendering, Manual Inventory Draft generation, and policy classification.
- Not implemented product behavior still includes web UI, connectors, publication destinations, PDF rendering, complete supervised-remediation policy, autonomous remediation, Infrastructure Map, lifecycle state, role Visibility, and dependency graph rendering.
- `docs/data-model.md` says dependency graph rendering, Runtime Services, Access Paths, lifecycle, recommissioning, and role Visibility are emerging model decisions not yet implemented.
- Module boundaries to preserve: Inventory models household meaning; Evidence qualifies facts; Discovery observes; Renderers explain; Policy constrains; Conversation is not a source of truth.
- Tests currently cover schema validation, secret rejection, relationship validation, deterministic rendering, stale classification, policy behavior, network discovery, CLI behavior, and inventory-draft review.

## Relevant ubiquitous language

- Operator: technical setup and maintenance user.
- Stress User: Trusted Person under pressure who needs calm, safe guidance.
- Helper Person: person contacted for help who may receive more technical context.
- Continuity Manual: Stress User-first generated household continuity artifact.
- Infrastructure Map: Operator-facing review and sense-making surface.
- Manual Inventory: reviewed human-authored structured Inventory.
- Discovery Snapshot: observational output that is not trusted Manual Inventory until reviewed.
- Dependency: relationship where one Device, Service, Access Path, or procedure relies on another.
- Runtime Service: technical Service that enables other Services or Containers to run.
- Evidence, Last Verified, Freshness Window, Stale, Unknown, Inferred, Manually Confirmed, Discovered: terms that keep facts honest.
- Safe Action, Privileged Action, High-Friction Action, Forbidden Action, Secret Reference, and Lockout: terms that should shape safety boundaries.

## Known constraints

- Do not implement anything during this run-start step.
- Keep the eventual product slice small, reversible, and testable.
- Do not add autonomous remediation, AI free-form shell execution, or broad action execution.
- Do not store secrets; use Secret References only.
- Do not add unavailable future connector suggestions as user-facing product behavior.
- Keep core behavior local-first and deterministic.
- Do not build a web UI before the manual, Infrastructure Map, data model, and safety boundaries are coherent.
- Preserve the distinction between discovered observations and reviewed household meaning.
- Any non-trivial behavior change should have a test-first or TDD plan before implementation.
- Security-sensitive, privacy-sensitive, brand-sensitive, legal, irreversible, or lockout-risk scope should be escalated.

## Initial uncertainty

- What the human means by "first minimal useful slice": first useful slice for a new user, for the existing prototype, for the next roadmap milestone, or for a specific demo?
- Whether the next slice should be dependency graph modeling, Mermaid rendering, Infrastructure Map Markdown output, improved first-run guidance, or another smaller setup/continuity improvement.
- How much product value is needed before introducing new schema fields such as `depends_on`, Runtime Service, Access Path, lifecycle, or Visibility.
- Whether the next iteration should improve Operator setup value, Stress User continuity value, or both.
- Whether prior empty run directories for the same trigger reflect abandoned starts, duplicate starts, or intended repeated exploration.
