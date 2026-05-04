# Architecture

Canonical architecture boundaries are described in `AGENTS.md` and `docs/product/UBIQUITOUS_LANGUAGE.md`. This file materializes current product discovery decisions for near-term engineering design.

## Accepted decisions

### Local-first file model

YAML remains the canonical source of truth for Manual Inventory, Runbooks, and near-term structured inputs. Advanced Operators may edit YAML directly. Future GUI workflows should edit the same local source files rather than hiding data in an opaque store.

Git/file history is sufficient for now.

### Deterministic core modules

CLI and future web app should share Python application modules. The web app should not shell out to the CLI as its normal backend design, except possibly as a temporary development shortcut.

Target architecture direction:

- parsing/loading modules
- validation modules
- discovery modules
- graph/model modules
- rendering modules
- application service functions shared by CLI and web UI
- thin CLI and thin web boundaries

### Infrastructure Map

The Infrastructure Map is a first-class product surface. It should combine:

- overlap between confirmed Manual Inventory and rediscovery
- promotion candidates discovered but not in inventory
- decommission candidates present in inventory but not rediscovered
- unknowns/gaps
- dependency graph
- stale facts and trust states
- available connectors once connectors exist

### Dependency graph

Start with generic `depends_on` relationships. Do not prematurely introduce typed edge taxonomy.

Initial graph relationship scope:

- Service depends on Service
- Service depends on Device
- Runtime Service dependencies, such as Home Assistant depending on Docker
- Runtime Service or Container depends on Host
- Device depends on household-controlled or physically present uplink devices
- Access Path dependencies, such as Tailscale, when they affect access/help

First rendering should use Mermaid in Markdown.

### Runtime Service

Docker-like infrastructure should be modeled as a **Runtime Service**: a technical Service that enables other Services or Containers to run. It is usually Helper Person or Operator facing, not Stress User facing unless its outage has household impact.

### Lifecycle

Entities should eventually support lifecycle state:

- active
- decommissioned

Decommissioned entities are preserved for archive and recommissioning. Rediscovery of a decommissioned entity is a lifecycle conflict, not merely stale data.

## Reversible bets

- Mermaid is enough to validate graph semantics before GUI work.
- Generic `depends_on` can carry initial graph value without typed edges.
- YAML editing through GUI can be safe if validation remains strict.

## Hard-to-reverse risks

- Introducing a database or opaque store too early would weaken inspectability and local-first trust.
- Building a web UI as a shell wrapper around CLI commands would create brittle architecture and security review problems.
- Adding connector-specific assumptions into inventory meaning would violate the boundary that connectors discover and inventory models household meaning.

## Unresolved questions

- Exact graph data structure and schema migration path.
- Exact entity visibility representation.
- Exact web framework, if any, for the local UI.
- How scheduled discovery is configured and executed.
