# Roadmap

This roadmap sequences small, reversible increments. It is not a release promise.

## Accepted sequencing

### Current foundation

- Structured Manual Inventory
- Structured Runbooks
- Evidence and staleness handling
- Deterministic Continuity Manual rendering
- Deterministic AI Assistance Packet rendering
- Local Network Discovery Snapshot
- Review-required Manual Inventory Draft
- Policy validation for Safe Actions and forbidden/privileged guidance

### Next strategic milestone

**Dependency graph model and rendering.**

Reason: the dependency graph is the most valuable pre-GUI milestone because it supports the Infrastructure Map, improves Operator setup value, and strengthens the Continuity Manual and Helper Person appendix.

## Near-term candidate increments

### 1. Dependency graph model

- User value: makes load-bearing relationships visible.
- Strategic value: bridges discovery, inventory, manual, and future GUI.
- Technical shape: start with generic `depends_on` relationships.
- Risks: schema churn if relationship types are over-designed too early.
- Tests: relationship validation and graph builder tests.
- Reversibility: moderate.

### 2. Mermaid dependency graph rendering

- User value: readable graph in Markdown outputs.
- Strategic value: validates graph semantics before GUI.
- Technical shape: deterministic Mermaid renderer.
- Risks: graph can become noisy if visibility and uncertainty are not rendered clearly.
- Tests: deterministic snapshot/string tests.
- Reversibility: easy.

### 3. Infrastructure Map Markdown output

- User value: recurring Operator review surface.
- Strategic value: first setup value before outage use.
- Technical shape: separate `dist/infrastructure-map.md` plus graph appendix in Continuity Manual.
- Risks: confusing raw discovery with household meaning.
- Tests: promotion/decommission candidate rendering, unknown/gap rendering.
- Reversibility: easy to moderate.

### 4. Lifecycle support

- User value: decommission without losing recommissioning context.
- Strategic value: supports long-lived household knowledge.
- Technical shape: `active` / `decommissioned` state, optional decommission metadata, stale-reference warnings.
- Risks: schema migration and validation complexity.
- Tests: lifecycle conflicts, active references to decommissioned entities, recommission review defaults.
- Reversibility: moderate.

### 5. Role visibility support

- User value: Stress Users see calm guidance; Helper Persons and Operators can see more technical context.
- Strategic value: makes family mode first-class without hiding technical reality.
- Technical shape: Stress User / Helper Person / Operator visibility ladder.
- Risks: accidentally hiding safety-critical uncertainty.
- Tests: renderer filtering by role.
- Reversibility: moderate.

### 6. Local web UI design and thin first implementation

- User value: Operators do not need to remember infrequent CLI workflows.
- Strategic value: makes maintenance realistic.
- Technical shape: Docker image containing CLI and local web app, sharing Python application modules.
- Risks: security, authentication, architecture debt if implemented as CLI shell wrapper.
- Tests: application service tests plus focused web boundary tests.
- Reversibility: moderate to hard.

## Later candidate connectors

Connector priority from the initial household use case:

1. UniFi
2. Reolink
3. Synology

Do not implement connectors until the manual, Infrastructure Map, data model, and safety boundaries are coherent.

## Maintenance direction

Steadlore House should eventually support configurable periodic rediscovery and Operator reminders:

- rerun discovery on a configurable schedule
- invite Operator review when meaningful mismatches appear
- remind Operators about undetectable meaningful changes
- allow enabling/disabling and frequency configuration
