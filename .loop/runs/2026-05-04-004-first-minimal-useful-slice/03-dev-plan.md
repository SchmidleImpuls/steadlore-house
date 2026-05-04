# Development Plan

## Codebase facts

- Manual Inventory is loaded from YAML through `src/steadlore_house/io.py`, which rejects raw secret-looking fields before schema validation.
- The in-memory model already has `Service.depends_on: list[str]` in `src/steadlore_house/models.py`; no schema change is needed for the selected slice.
- Cross-file relationship validation in `src/steadlore_house/validation.py` currently requires each `depends_on` target to match a known Device or Service ID.
- Continuity Manual rendering is deterministic and centralized in `src/steadlore_house/render_manual.py` via `render_manual(inventory, runbooks, now=...)` and small private section renderers.
- Evidence and stale labels are already rendered for Facts and access endpoints using `src/steadlore_house/staleness.py` helpers.
- The example Home Assistant service in `examples/household.yaml` already depends on `house-server-01`; `House Server 01` has a stale Fact at `now=datetime(2026, 5, 1, tzinfo=UTC)`.
- Existing tests in `tests/test_render_manual.py` assert deterministic Markdown, section ordering, staleness visibility, Stress User wording, and absence of unsafe/root-cause language.
- `docs/engineering/MODULE_MAP.md` calls out dependency graph builder and Mermaid renderer as interfaces to design deliberately and warns against renderers duplicating dependency inference logic.
- There is no source `dependency_graph.py` today, although stale `__pycache__` and pytest cache entries suggest a previous or abandoned local artifact; implementation should ignore cache files and add source/tests explicitly.

## Proposed implementation

Smallest coherent change:

1. Add a small deep module, likely `src/steadlore_house/dependency_graph.py`, that builds a reviewed Manual Inventory dependency graph from existing `Service.depends_on` relationships.
2. Keep graph semantics intentionally generic: an edge means `service depends_on target` and nothing more.
3. Represent only the data the renderer needs: deterministic node IDs, display labels, entity kind (`Service`, `Device`, or `Unknown`), trust/staleness label, and directed edges.
4. Render Mermaid Markdown from that graph, probably as `flowchart TD`, with stable sorting by display name or ID.
5. Include the rendered Mermaid block in the Continuity Manual only when at least one dependency exists, placed under `## For Helper Persons` as a technical appendix/subsection so Stress User symptom guidance remains first.
6. Derive node trust labels conservatively from existing Evidence-bearing facts/access endpoints:
   - mark `STALE` when any attached evidence on that entity is stale;
   - mark status values such as `unknown` or `inferred` when present;
   - mark `no evidence` or equivalent when no Evidence-bearing fields exist;
   - do not invent missing evidence for dependency edges because edges currently have no Evidence field.
7. If a dependency target is unresolved, render a clearly labeled unknown/unresolved node such as `Unresolved dependency: <id>` in the graph builder/renderer. Keep existing CLI relationship validation unchanged unless implementation proves that the generated manual must accept invalid inventory.
8. Do not update the AI Assistance Packet in this slice unless tests show shared graph code is needed there; the selected slice is Continuity Manual rendering.

## Module/interface impact

- Create/protect a Dependency Graph Context module with a narrow interface, for example:
  - `build_dependency_graph(inventory: Inventory, *, now: datetime | None = None) -> DependencyGraph`
  - `render_dependency_graph_mermaid(graph: DependencyGraph) -> str`
- Touch `render_manual.py` only to call this interface and place the returned Markdown section.
- Do not alter `models.py` unless a tiny dataclass for graph output belongs there; prefer keeping graph dataclasses in the new graph module to avoid making the Inventory model prematurely own rendering concerns.
- Preserve `validation.py` relationship checks. Validation remains stricter than the renderer's fallback handling for unresolved targets.
- Protect boundaries:
  - Inventory models reviewed household meaning.
  - Graph builder derives structure from reviewed Manual Inventory only.
  - Renderer explains structure; it does not discover or infer new household meaning.

## Test-first plan

Start with failing tests before implementation:

1. Add dependency graph unit tests in `tests/test_dependency_graph.py`:
   - Home Assistant depends on House Server 01 renders as a deterministic Mermaid edge.
   - node labels include enough evidence state to show stale underlying facts.
   - unresolved dependency targets render as unresolved/unknown, not as invented devices or services.
   - no Mermaid output is produced when no services declare dependencies.
2. Add/extend `tests/test_render_manual.py`:
   - generated manual includes a Helper Person dependency graph section for `examples/household.yaml`.
   - graph section appears after Stress User runbook guidance and does not replace `## Common Problems`.
   - rendering remains deterministic for the same inputs.
   - inventory with no dependencies omits the graph section.
3. Run focused tests first, then full suite:
   - `python -m pytest tests/test_dependency_graph.py tests/test_render_manual.py`
   - `python -m pytest`
4. After implementation, regenerate `dist/continuity-manual.md` only if repository practice expects checked-in generated outputs to match examples.

## Files likely touched

- `src/steadlore_house/dependency_graph.py` — new deep module for graph building and Mermaid rendering.
- `src/steadlore_house/render_manual.py` — include the dependency graph subsection in the Helper Person part of the Continuity Manual.
- `tests/test_dependency_graph.py` — new tests for graph model/rendering behavior and edge cases.
- `tests/test_render_manual.py` — integration tests for graph inclusion, ordering, determinism, and omission.
- `dist/continuity-manual.md` — likely regenerated example output if generated artifacts are intended to stay current.
- Possibly `docs/data-model.md`, `docs/engineering/MODULE_MAP.md`, and `docs/engineering/TECH_DEBT.md` after implementation to mark initial dependency graph rendering as implemented/partially retired.

## Security considerations

- Mermaid labels must use reviewed names/IDs only and must not include Secret References, URLs, contact hints, vault names, or physical secret storage hints.
- The graph must not suggest actions, remediation, connector availability, live status, or discovery confidence beyond existing Evidence labels.
- Stale must be shown as stale, not as failed or unavailable.
- Unknown/unresolved dependencies must be labeled honestly and must not be guessed from IDs.
- Mermaid output should escape or sanitize label text enough to avoid broken Markdown/Mermaid syntax from inventory names.
- No shell execution, connector access, network discovery, privileged action, or state mutation is needed.

## Debt considerations

- Retires part of the current `Missing dependency graph model` debt by introducing the first small graph builder and Mermaid renderer.
- Avoids schema churn by using existing generic `depends_on` and not adding typed edges, Runtime Service, Access Path, lifecycle, or Visibility.
- Avoids renderer coupling by putting graph construction/rendering behind a dedicated module instead of embedding dependency logic throughout `render_manual.py`.
- Introduces acceptable temporary debt: entity-level trust labels are derived from existing Fact/access endpoint Evidence because dependencies themselves do not yet carry Evidence.
- Does not retire Infrastructure Map debt; this only validates dependency graph rendering inside the Continuity Manual.

## Refused scope

- Full Infrastructure Map.
- GUI or local web UI.
- Connectors, Available Connector output, or discovery promotion changes.
- Runtime Service, Container, Access Path, lifecycle, recommissioning, or Visibility schema changes.
- Typed dependency edge taxonomy.
- AI Assistance Packet graph rendering unless explicitly selected later.
- Autonomous remediation, supervised action execution, or free-form shell execution.
- Any storage or rendering of Secrets rather than Secret References.

## Open questions

None blocking safe implementation. The only implementation choice to settle during TDD is exact Mermaid label escaping and wording for `STALE`, `unknown`, and unresolved nodes.
