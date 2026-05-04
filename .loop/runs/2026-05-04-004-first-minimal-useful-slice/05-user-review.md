# User Acceptance Review

## Verdict
Pass

## Acceptance criteria check
- Generated Continuity Manual includes a dependency graph when reviewed Manual Inventory contains dependencies: Pass. `/tmp/user-review-continuity-manual.md` includes `### Dependency Graph` under `## For Helper Persons`.
- Home Assistant dependency renders visibly as Home Assistant depending on House Server 01: Pass. The generated Mermaid block includes `home_assistant -->|depends on| house_server_01`.
- Rendering is deterministic and Markdown/Mermaid-suitable: Pass from observed Markdown output and tests. Full suite passes: `65 passed in 0.17s`.
- Graph labels expose evidence age/trust state enough to show stale facts: Pass. Both Home Assistant and House Server 01 graph nodes show `STALE; manually_confirmed`, and detailed evidence remains below.
- Unknown or unresolved dependency targets are rendered honestly: Pass at graph module/test level. `tests/test_dependency_graph.py` covers `Unresolved dependency: missing-host`; normal CLI relationship validation still prevents invalid inventory from generating a manual.
- Stress User guidance remains symptom-first: Pass. `## Common Problems` and the lights/automations runbook remain before `## For Helper Persons`; safe checks and do-not-touch guidance are unchanged.
- Secret protections remain unchanged: Pass. The graph uses reviewed service/device names only; Secret References remain in the existing Secret Reference section and no secret values appear.
- Tests cover expected behavior: Pass. New/updated tests cover dependency rendering, stale labels, unresolved targets, deterministic output, escaping, and no graph when no dependencies exist.

## User value delivered
The manual now shows the load-bearing relationship that was previously only implicit: Home Assistant depends on House Server 01. For an Operator, this makes the first scenario feel more like “the house knows how it works.” For a Helper Person, it reduces guessing during escalation without changing the calm Stress User path.

The placement is appropriate: the graph appears as Helper Person context, not as the first thing a stressed household member sees.

## New friction introduced
The aggregate node label `STALE; manually_confirmed` is useful but a little blunt. A Helper Person may wonder which fact is stale or whether the service itself is stale/unavailable. The detailed evidence below answers this, so it is not blocking.

## Domain-valid blocking objections
None.

## Non-blocking concerns
- The graph is currently an appendix-style technical artifact. It is valuable for Helper Persons, but not yet a complete Operator-facing Infrastructure Map.
- The graph’s stale/trust label is entity-level, not dependency-edge-level. That matches the selected minimal slice, but future users may expect dependency evidence specifically.
- Mermaid rendering is useful in Markdown viewers that support it; in plain text it remains readable enough, but less visually helpful.

## Suggested follow-ups
- Add edge-level dependency evidence when the data model supports it.
- Add a short legend explaining `STALE`, `current`, `no evidence`, and `unresolved` near the graph.
- Later, reuse this graph module in the Markdown Infrastructure Map rather than expanding the Continuity Manual into an Operator dashboard.
