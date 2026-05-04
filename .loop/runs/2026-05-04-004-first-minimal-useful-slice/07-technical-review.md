# Technical Review

## Verdict
Pass

## Correctness
No blocking correctness issues found.

The implementation makes the existing reviewed Manual Inventory dependency visible in the Continuity Manual as intended: Home Assistant renders as depending on House Server 01, and the graph is omitted when there are no dependencies. The graph builder uses existing `Service.depends_on` relationships only and does not infer missing household meaning.

Edge cases covered include deterministic output, unresolved dependency targets when constructing an in-memory inventory directly, unknown evidence status, Mermaid label escaping, and empty dependency sets.

Non-blocking observations:

- Real file-loaded inventories still reject unresolved `depends_on` targets through existing relationship validation, while the graph builder can render unresolved targets if called directly. That is acceptable for this slice, but future callers should understand this difference.
- Repeated unresolved targets may allocate an extra internal Mermaid ID before ending on the final unresolved node. This does not break rendering, but it is a small cleanup candidate if unresolved graph rendering becomes more common.

## Tests and feedback loops
Tested during review:

- `python -m pytest tests/test_dependency_graph.py tests/test_render_manual.py`
- `python -m pytest`

Result: `65 passed`.

The added tests are relevant and fast. They cover the selected behavior at both the dependency graph module boundary and the generated manual integration point.

Missing but non-blocking for this minimal slice:

- Service-to-service dependency rendering.
- Exact `no evidence` label assertion.
- Duplicate/similar IDs that normalize to the same Mermaid ID.

These can be added when the graph is reused for the Infrastructure Map or expanded beyond the Home Assistant example.

## Security
No security regression found.

The change does not add shell execution, connectors, network access, authentication surface, privileged actions, or remediation. The graph renders reviewed Service and Device names plus evidence status only; it does not render Secret References, URLs, vault hints, contact hints, or physical secret storage hints.

Mermaid labels are sanitized enough for the tested Markdown/Mermaid syntax risks. Existing raw secret-field rejection and validation paths remain unchanged.

## Maintainability
The implementation uses a focused `dependency_graph.py` module with a narrow builder/rendering interface, keeping dependency logic out of `render_manual.py`. This is maintainable and matches the planned small deep module approach.

The code is readable and deterministic. The custom Mermaid escaping is intentionally small; keep it covered by tests if label rules expand.

## Architecture
The change aligns with the documented architecture boundaries:

- Inventory remains the reviewed source of household meaning.
- The graph builder derives structure from Manual Inventory `depends_on` relationships.
- The Continuity Manual renderer presents the graph as Helper Person context, not as live monitoring or remediation.
- No connector, Infrastructure Map, GUI, Runtime Service, Access Path, lifecycle, or Visibility scope was introduced.

The TECH_DEBT and MODULE_MAP updates accurately reflect the new partial dependency graph model and avoid claiming the full Infrastructure Map is implemented.

## Debt and follow-ups
Accepted debt is bounded and documented: graph evidence is entity-level, not dependency-edge-level.

Suggested follow-ups, none blocking merge:

- Add a short graph legend for `STALE`, `current`, `no evidence`, and `unresolved`.
- Add service-to-service and duplicate Mermaid-ID tests before graph semantics broaden.
- Reuse this graph module for the future Markdown Infrastructure Map rather than duplicating dependency inference elsewhere.
