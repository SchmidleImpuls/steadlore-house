# Loop Context

## Trigger
No product idea, issue, friction, or goal was supplied in the input. This run is therefore only initialized with repository context and should not select or implement a product slice until the human supplies intent or confirms that the loop should discover a small next increment from current strategy.

## Relevant product strategy
- Steadlore House is a local-first household continuity system whose core promise is: if something happens, the house still knows how it works.
- The Continuity Manual remains the first useful household continuity artifact; the Infrastructure Map is the first Operator setup and review value surface.
- The accepted next strategic milestone is dependency graph model and rendering, with Infrastructure Map, lifecycle, role visibility, and local web UI as later/near-term candidates.
- Current product boundaries exclude autonomous remediation, generic chatbot behavior, smart-home hub behavior, monitoring dashboard behavior, password management, estate planning, and unavailable connector suggestions.

## Relevant engineering context
- Current repository state includes a Python prototype with YAML as canonical local source of truth, deterministic renderers, validation, policy handling, passive/opt-in network discovery, review-required inventory draft flow, and dependency graph/Mermaid support.
- Current modules include `models.py`, `validation.py`, `dependency_graph.py`, renderers for the Continuity Manual and AI Assistance Packet, `network_discovery.py`, `policy.py`, and a thin CLI boundary.
- Tests already cover schema validation, secret rejection, relationship validation, deterministic rendering, stale classification, policy enforcement, network discovery behavior, CLI behavior, and dependency graph behavior.
- Technical debt to watch includes connector hint language before connectors exist, CLI-first workflows, partial dependency graph semantics, no lifecycle state, and no role visibility model.

## Relevant ubiquitous language
- Operator: primary setup and maintenance user.
- Stress User: primary Continuity Manual audience during confusion, outage, or Operator unavailability.
- Helper Person: secondary audience who may use more technical appendices.
- Continuity Manual: generated human-readable household continuity artifact.
- Infrastructure Map: Operator-facing review and sense-making surface.
- Inventory, Fact, Evidence, Last Verified, Freshness Window, Stale, Unknown, Inferred, Manually Confirmed, Discovered.
- Dependency, Runtime Service, Access Path, Household Impact.
- Safe Action, Privileged Action, High-Friction Action, Forbidden Action, Policy, Secret Reference.
- Available Connector only when a connector actually exists.

## Known constraints
- Do not implement anything during this start step.
- No secrets may be stored in docs, examples, tests, fixtures, generated output, or sample data; use Secret References only.
- Do not add AI-driven arbitrary command execution or autonomous remediation.
- Discovery observations must remain separate from household meaning.
- Core infrastructure, identity, backups, secrets, and lockout-risk areas require high-friction review.
- Keep changes small, deterministic, local-first, schema-backed, testable, and aligned with the ubiquitous language.
- Because the trigger is empty, the next Product Loop pass must avoid inventing a user problem.

## Initial uncertainty
- What user friction, issue, or goal this run is meant to address.
- Whether the human wants to continue a previously selected roadmap item or start from a newly supplied trigger.
- Whether this run should be closed as accidentally started if no trigger was intended.
