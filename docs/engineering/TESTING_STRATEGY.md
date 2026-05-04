# Testing Strategy

Prefer TDD or test-first thinking for non-trivial behavior changes. The rate of feedback is the speed limit.

## Current baseline

Tests should continue to cover:

- schema validation
- secret-field rejection
- relationship validation
- deterministic Markdown rendering
- stale-data classification
- policy classification and forbidden-action enforcement
- network discovery parsing and timeout behavior
- CLI behavior and user-visible errors

## New strategy from product discovery

### Dependency graph tests

When graph support is added, test:

- Service → Service dependencies
- Service → Device dependencies
- Runtime Service → Host dependencies
- Access Path dependencies where relevant
- inferred vs confirmed relationships
- stale or unknown evidence rendering
- Mermaid output determinism
- graph inclusion in both Infrastructure Map and Continuity Manual

### Infrastructure Map tests

Test that the Infrastructure Map distinguishes:

- reviewed Manual Inventory
- rediscovered known infrastructure
- promotion candidates
- decommission candidates
- unknowns/gaps
- lifecycle conflicts
- available connectors only when connectors actually exist

### Lifecycle tests

When lifecycle support is added, test:

- decommissioned entities are preserved
- recommissioning requires review and proposes old data as defaults
- active references to decommissioned entities warn with disclaimers
- rediscovered decommissioned entities produce lifecycle conflicts

### Visibility tests

When visibility support is added, test role filtering:

- Stress User-visible content appears for all roles
- Helper Person-visible content appears for Helper Persons and Operators but not Stress Users
- Operator-visible content appears only for Operators
- safety-critical uncertainty is not hidden inappropriately

### Web UI tests

When web UI work begins, test shared application services separately from HTTP/UI boundaries. Do not rely on broad end-to-end tests alone.

## Documentation/scaffolding exception

Documentation-only and process-scaffolding changes may state that no product behavior tests are needed, but should still be reviewed for vocabulary and safety implications.
