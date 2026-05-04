# TDD Plan

## Behavior under test
The generated Continuity Manual must include a deterministic Helper Person-oriented dependency graph when reviewed Manual Inventory contains `depends_on` relationships. The graph must show the existing Home Assistant example dependency on House Server 01, expose stale or unknown evidence state honestly, render unresolved dependency targets as unresolved/unknown rather than invented entities, and omit the graph entirely when there are no dependencies. Stress User runbook guidance must remain symptom-first and must not be replaced by graph content.

At the module boundary, a new dependency graph module should turn Inventory services and their reviewed Manual Inventory dependencies into a small graph model and Mermaid Markdown without discovering, inferring, or executing anything.

## Smallest failing test
Create `tests/test_dependency_graph.py` with the first failing unit test:

- build/render a graph from the existing example inventory at a fixed `now`
- assert the Mermaid output contains a deterministic edge showing Home Assistant depends on House Server 01
- assert the House Server 01 node label includes stale state because its underlying example fact is stale at the chosen date

This is the smallest test because it proves the selected slice directly: the existing Home Assistant dependency becomes visible and evidence age is not hidden.

## Test level
Unit first, then integration.

- Unit: `tests/test_dependency_graph.py` should cover graph construction, Mermaid determinism, stale/unknown labeling, unresolved targets, escaping, and empty output. This protects the new deep module boundary and keeps feedback fast.
- Integration: extend `tests/test_render_manual.py` to verify the Continuity Manual includes the graph in the Helper Person area, after Stress User runbook guidance, and omits it when no dependencies exist. This confirms user-visible placement without turning the whole manual into brittle snapshot coverage.
- Snapshot-style assertions should stay narrow: assert important section headings, edge text, labels, and ordering rather than the entire generated Markdown unless an existing deterministic snapshot pattern already exists.

## What not to mock
Use real project models, real example inventory loading/parsing where practical, real staleness helpers, and the real manual renderer. These dependencies are needed for confidence that the graph reflects reviewed Manual Inventory, respects Evidence age, and fits the generated Continuity Manual.

Use a fixed `now` timestamp instead of mocking time globally. Do not mock the graph builder inside `render_manual.py`; the integration test should exercise the real call path.

## What to mock or fake
Fake only small in-memory inventories for edge cases that are awkward or noisy in the example fixture:

- no services with dependencies
- unresolved dependency target
- service-to-service dependency if not already present in examples
- labels requiring Mermaid escaping
- entity with no Evidence-bearing facts, if needed for `no evidence` or unknown labeling

Do not use connectors, network discovery, filesystem scanning beyond fixture loading, shell commands, external services, or generated Docker behavior in these tests.

## Red-green-refactor path
1. Red: Add the smallest unit test for Home Assistant → House Server 01 Mermaid rendering with stale labeling. Run only the focused test and confirm it fails because `steadlore_house.dependency_graph` or the expected behavior does not exist.
2. Green: Add the minimal `dependency_graph.py` interface and implementation needed to pass that test: build nodes from services/devices, build one `depends_on` edge, derive a conservative stale label from existing Evidence, and render stable Mermaid.
3. Refactor: Add the remaining unit tests one at a time for determinism, unresolved targets, empty graph output, unknown/no-evidence labels, and escaping. Then add manual-renderer integration tests and wire the graph section into `render_manual.py` under the Helper Person portion. Refactor duplication into small helpers only after tests make the intended behavior clear.

## Feedback cadence
Run tests at the highest useful frequency:

- after writing each failing test: `python -m pytest tests/test_dependency_graph.py -q`
- after each small green implementation step: rerun the focused graph tests
- when touching manual rendering: `python -m pytest tests/test_dependency_graph.py tests/test_render_manual.py -q`
- before considering the implementation complete: `python -m pytest`

If generated output is checked in, regenerate and inspect `dist/continuity-manual.md` only after the focused and full test suite pass.

## Risks
- Brittle Mermaid assertions if tests depend on incidental whitespace or full-block formatting.
- Over-mocking `render_manual.py` and missing section placement or Stress User guidance regressions.
- Under-testing label escaping, leading to broken Markdown/Mermaid for realistic inventory names.
- Confusing stale with unavailable or failed; tests must assert language that preserves the meaning of Stale.
- Accidentally weakening relationship validation to accommodate unresolved rendering. Validation should remain stricter unless a later slice explicitly changes it.
- Letting the renderer infer household meaning or include Secret References, URLs, vault hints, or physical secret storage hints in graph labels.
