# Module Map

Keep this lightweight and update when module boundaries change.

## Current bounded contexts

- Inventory Context: `src/steadlore_house/models.py`, inventory loading, validation.
- Evidence and Staleness Context: `staleness.py`, evidence fields in models.
- Continuity Manual Context: `render_manual.py`, `render_ai_packet.py`.
- Runbook Context: runbook models and examples under `examples/runbooks/`.
- Policy Context: `policy.py`.
- Connector/Discovery Context: `network_discovery.py` and snapshot renderers.
- CLI Boundary: `cli.py`.

## Current deep modules

- `validation.py`: deterministic schema, relationship, secret, symptom-title, and policy validation checks.
- `policy.py`: conservative deterministic action classification.
- `network_discovery.py`: local passive discovery and opt-in nmap ping-scan parsing behind explicit functions.
- Renderers: deterministic Markdown output from structured models.

## Shallow-module sprawl watch

No urgent module sprawl was identified during discovery, but upcoming graph, lifecycle, Infrastructure Map, and web UI work could create shallow fragments if each renderer or workflow invents its own model.

## Important interfaces to design deliberately

- Dependency graph model and builder.
- Infrastructure Map renderer.
- Lifecycle/decommission/recommission validation.
- Role visibility filtering.
- Shared application service layer for CLI and future web UI.

## Testable boundaries

- Graph builder from Inventory, Runbooks, Discovery Snapshot, and evidence inputs.
- Mermaid renderer from graph model.
- Infrastructure Map renderer from reviewed inventory plus rediscovery results.
- Lifecycle validator for decommissioned references and conflicts.
- Application services invoked by CLI and future web UI.

## Boundary problems to avoid

- Web UI shelling out to CLI as its normal backend.
- Connector code assigning household meaning.
- Renderers duplicating dependency inference logic.
- Graph output hiding evidence, freshness, or inferred status.
- GUI editing YAML without running the same validation path as CLI.

## Recommended architecture improvements

1. Add a graph model/builder module before adding GUI graph views.
2. Add Infrastructure Map rendering as Markdown before web UI implementation.
3. Add lifecycle and visibility as schema-backed concepts with validation.
4. Extract shared application service functions before a local web UI calls product behavior.

When adding modules, explain the boundary and why existing modules were not sufficient.
