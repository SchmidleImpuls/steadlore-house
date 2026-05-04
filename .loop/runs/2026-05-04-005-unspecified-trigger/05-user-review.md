# User Acceptance Review

## Verdict
Pass

## Acceptance criteria check
- Generated discovery snapshot Markdown does not include “Possible Connector Candidates”, “connector candidates”, or similar future-connector suggestions when no Available Connector exists: Pass. `dist/network-snapshot.md` no longer shows a connector-candidate section or connector-candidate line items.
- Generated Manual Inventory Draft YAML does not include `connector_hints` or connector-candidate facts when no Available Connector exists: Pass. `dist/inventory-draft.yaml` keeps vendor and observed-network facts, but no longer emits `connector_hints` or “Possible connector candidate” facts.
- Existing discovery observations that are useful as neutral device/service facts remain available without connector-specific recommendation language: Pass. The snapshot and draft still show IP address, MAC address, vendor, interface, neighbor state, DNS/gateway candidate reasons, and low-confidence discovery Evidence.
- README or product documentation continues to state that no Home Assistant, Portainer, Telegram, or other connector exists yet, if that statement is already present: Pass. The README remains clear that those connectors do not exist yet. `docs/data-model.md` now describes vendor enrichment as a discovery observation rather than a connector hint.
- Tests or snapshots cover the absence of unavailable connector suggestions in discovery snapshot and draft outputs: Pass. Tests assert absence from rendered network snapshots, inventory drafts, and legacy interactive draft review display. `python -m pytest -q` passed with 68 tests.
- The term “Available Connector” is reserved for connectors that actually exist: Pass from a user-facing perspective. The changed outputs do not introduce Available Connector language or future connector promises.

## User value delivered
Operators now see discovery and draft outputs that are more honest about current product capability. A discovered vendor is presented as an observation, not as a suggestion that an integration exists. This reduces false affordances during the setup/review path and better preserves trust in Steadlore House as a continuity tool rather than a premature connector platform.

## New friction introduced
Very little. Removing connector hints slightly reduces speculative clues about what ecosystem a device might belong to, but vendor names and candidate reasons remain visible, so the useful review context is still present.

## Domain-valid blocking objections
None.

## Non-blocking concerns
- Some internal source and tests still use `connector_hints` naming. I do not see this leaking into current user-facing outputs, so it is not a user acceptance blocker for this slice.
- “vendor-enriched observed neighbor” is accurate but somewhat technical for an Operator review surface. It is still less misleading than connector-candidate language.

## Suggested follow-ups
- Later, rename or isolate internal connector-hint concepts if they continue to exist before real Available Connectors are implemented.
- Consider friendlier Operator-facing phrasing for candidate reasons, such as “observed device with known vendor,” while preserving deterministic evidence.
- Continue with the next Operator setup improvement: a clearer workflow from discovery snapshot to reviewed Manual Inventory to generated Continuity Manual.
