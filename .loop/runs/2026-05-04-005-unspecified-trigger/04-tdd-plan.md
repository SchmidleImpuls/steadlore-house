# TDD Plan

## Behavior under test
User-facing discovery and draft outputs must stop advertising unavailable connector suggestions while preserving neutral discovery observations.

Concretely:

- Network Discovery Snapshot Markdown must not render “Possible Connector Candidates”, “connector candidates”, connector-hint lines, or similar future-connector recommendation language when no Available Connector exists.
- Manual Inventory Draft YAML must not emit `_review.connector_hints` or “Possible connector candidate…” facts.
- Existing neutral observations must remain visible: vendor names, IP/MAC addresses, gateway/DNS candidates, active-scan observations, evidence, confidence, review-required status, and deterministic map output.
- CLI help for network discovery must use neutral vendor-enrichment wording, not connector-hint wording.
- Interactive draft review must not re-surface legacy `connector_hints` as user-facing guidance.

## Smallest failing test
Start with a renderer-level test in `tests/test_network_discovery.py` that builds or reuses a snapshot containing `connector_hints`, renders it with `render_network_snapshot()`, and asserts the Markdown does not contain:

- `Possible Connector Candidates`
- `connector candidates`
- `connector hints`
- an example connector-candidate label from the fixture

In the same test, assert one or two confidence-preserving neutral facts still render, such as the vendor name and gateway/DNS candidate text. This fails before implementation because the current renderer explicitly renders connector-candidate sections and hint text.

## Test level
Unit / snapshot-style renderer tests first.

Reason: the behavior change is primarily deterministic rendering and draft generation at module boundaries. Renderer-level tests give the fastest useful feedback and avoid broad end-to-end setup.

Add small integration-style CLI help coverage in `tests/test_cli_help.py` because CLI help is a user-visible boundary. Existing inventory draft rendering tests should remain validation-backed so the generated YAML still parses and validates as Inventory.

## What not to mock
Do not mock:

- `render_network_snapshot()` output construction.
- `render_inventory_draft()` YAML generation.
- Inventory validation used by the draft test.
- Real fixture/dataclass objects such as `NetworkSnapshot`, `NetworkNeighbor`, and `ActiveScanHost`.
- Click/Typer/CLI help rendering path already used by CLI help tests.

These are the boundaries where confidence is needed.

## What to mock or fake
Fake only slow or irrelevant inputs:

- Do not run real network discovery, ARP commands, nmap, DNS lookups, or MAC vendor downloads.
- Construct in-memory `NetworkSnapshot` objects with representative `connector_hints`.
- Use existing test fixtures or small inline fake discovery candidates for draft rendering.
- Avoid filesystem or Docker dependencies unless an existing test helper already provides them cheaply.

## Red-green-refactor path
1. Red:
   - Update `tests/test_network_discovery.py` to assert absence of connector-candidate language while preserving vendor/gateway/DNS/map output.
   - Update `tests/test_render_inventory_draft.py` to assert no `_review.connector_hints`, no raw `connector_hints` in YAML, no connector-candidate facts, and continued valid Inventory with discovered low-confidence Evidence.
   - Add or extend `tests/test_cli_help.py` so `discover-network --help` does not contain “connector hints”.
   - Run the narrow tests and confirm they fail for the current user-facing leakage.
2. Green:
   - Change `render_network_snapshot.py` to stop rendering connector-candidate sections and hint lines, and avoid promoting entries solely because of `connector_hints`.
   - Change `render_inventory_draft.py` to stop emitting draft `_review.connector_hints`, connector-candidate facts, and hint-derived type suggestions.
   - Change `cli.py` help text to neutral vendor-enrichment language.
   - Remove connector-hint display from `review_inventory_draft.py` if tests or grep show legacy drafts would still surface it.
   - Run the narrow tests after each small file change.
3. Refactor:
   - Delete dead renderer helper code only after green tests prove behavior.
   - Prefer model-level rendering decisions over post-render string filtering.
   - Keep internal `connector_hints` data/mapping only if it no longer leaks to user-facing outputs.
   - Update `docs/data-model.md` after behavior tests pass.
   - Run the full test suite before handoff.

## Feedback cadence
Run tests at the speed of the slice:

- After writing the first failing network snapshot test: run that single test.
- After each renderer change: run the affected test file.
- After draft changes: run `tests/test_render_inventory_draft.py`.
- After CLI wording changes: run `tests/test_cli_help.py`.
- Before final review: run the full `pytest` suite.

Use `rg -n "connector_hints|connector hints|connector candidates|Possible Connector Candidates|Possible connector candidate"` as a quick text check between test runs, but do not substitute grep for behavior tests.

## Risks
- Over-mocking could miss leakage in real renderer output; use real renderers and validation.
- Brittle assertions could overfit exact Markdown structure; assert important forbidden phrases and preserved neutral facts rather than every line.
- Removing too much could hide useful neutral observations; tests must prove vendor/gateway/DNS facts still render.
- Leaving legacy review display untouched could reintroduce unavailable connector suggestions outside generated draft output.
- Internal `connector_hints` fields may remain as short-term debt; acceptable only if no user-facing output advertises unavailable connectors.
