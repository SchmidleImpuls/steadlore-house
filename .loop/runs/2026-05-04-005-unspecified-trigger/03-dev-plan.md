# Development Plan

## Codebase facts
- Discovery data lives in `src/steadlore_house/network_discovery.py` as immutable dataclasses: `NetworkSnapshot`, `NetworkNeighbor`, and `ActiveScanHost` currently carry `connector_hints` populated from local MAC vendor enrichment.
- Vendor-to-hint mapping lives in `src/steadlore_house/mac_vendors.py` via `VENDOR_CONNECTOR_HINTS`, `MacVendorLookup.connector_hints_for()`, and `connector_hints_for_vendor()`.
- User-facing Network Discovery Snapshot rendering is in `src/steadlore_house/render_network_snapshot.py`.
  - `render_network_snapshot()` calls `_render_connector_candidates(candidates)`.
  - `_render_candidates()`, `_render_neighbors()`, and `_render_active_scan()` render connector-candidate wording.
  - `core_infrastructure_candidates()` includes devices when they have `vendor` or `connector_hints`; entries with hints only can become user-facing candidates.
- User-facing Manual Inventory Draft YAML rendering is in `src/steadlore_house/render_inventory_draft.py`.
  - `_review_metadata()` emits `connector_hints`.
  - `_facts_from_candidate()` emits “Possible connector candidate…” facts.
  - `_suggest_device_type()` uses `connector_hints` as a device-type signal.
- The interactive draft review path in `src/steadlore_house/review_inventory_draft.py` can print `Connector hints` if an existing draft contains them.
- CLI help in `src/steadlore_house/cli.py` says “Vendor names are connector hints only”, which is also user-facing connector-hint language.
- Tests currently assert the old behavior:
  - `tests/test_network_discovery.py` expects vendor enrichment to produce connector hints and expects rendered snapshots to contain connector-candidate text.
  - `tests/test_render_inventory_draft.py` expects `_review.connector_hints` and a connector-candidate fact.
  - `tests/test_cli_help.py` covers discovery help but not the exact connector-hint sentence.
- `README.md` already states there is no Home Assistant connector, Portainer connector, Telegram bot, or automated recovery workflow yet.
- Documentation debt exists in `docs/data-model.md`, which still describes possible connector candidates and `connector_hints` in drafts; engineering docs and ubiquitous language already say unavailable connector suggestions should not be user-facing.

## Proposed implementation
Smallest coherent change: remove unavailable connector-candidate language from rendered outputs and generated drafts while preserving neutral discovery observations such as IP address, MAC address, vendor, route, DNS, interface, active-scan state, evidence, warnings, and candidate confidence.

Implementation shape:
1. Update failing tests first to assert absence of “Possible Connector Candidates”, “connector candidates”, `connector_hints`, and “Possible connector candidate…” in generated snapshot/draft outputs.
2. In `render_network_snapshot.py`:
   - Stop calling `_render_connector_candidates()` and remove or leave unused only if immediately deleted.
   - Stop rendering connector-hint lines in core candidates, observed neighbors, and active scan hosts.
   - Change candidate inclusion so a host/neighbor is not promoted to a user-facing candidate solely because it has `connector_hints`; neutral `vendor` remains a valid vendor-enrichment signal.
   - Keep existing candidate language for gateway, DNS, and vendor-enriched observed devices.
3. In `render_inventory_draft.py`:
   - Stop emitting `_review.connector_hints`.
   - Stop generating connector-candidate facts.
   - Avoid deriving suggested device type from `connector_hints`; use neutral vendor names and route/DNS reasons only.
4. In `cli.py`, replace the discovery help sentence about vendor names being connector hints with neutral vendor-enrichment language.
5. Consider removing connector-hint display from `review_inventory_draft.py` so old drafts do not re-surface unavailable connector suggestions during review. This is small and keeps the user-facing cleanup coherent.
6. Update `docs/data-model.md` to retire statements that Discovery Snapshots and Manual Inventory Drafts include possible connector candidates or `connector_hints`, replacing them with neutral vendor-enrichment wording.

This deliberately does not remove the internal `connector_hints` fields or `mac_vendors.py` mapping in the same slice unless tests reveal that keeping them causes user-facing leakage. Keeping internal fields minimizes schema churn and preserves reversibility for a future Available Connector design.

## Module/interface impact
- Protected boundary: Connector/Discovery Context remains observational and does not advertise unavailable connectors.
- Touched deep module/interface: `render_network_snapshot.py` as the Markdown Renderer for Discovery Snapshots.
- Touched renderer: `render_inventory_draft.py` as the YAML Renderer for review-required Manual Inventory Drafts.
- Touched CLI boundary: `cli.py` help text only, to keep user-facing language aligned.
- Optional touched review boundary: `review_inventory_draft.py` display text only, to avoid resurfacing stale connector-hint metadata from older drafts.
- No new module should be created; this is a renderer/output cleanup, not connector architecture.
- No canonical Manual Inventory schema change is intended. Generated draft `_review` metadata changes, but `_review` is explicitly draft-only and removed during promotion.

## Test-first plan
First failing verification should be renderer-level:
- Update `tests/test_network_discovery.py::test_renders_network_snapshot_with_map_and_limits` to build a snapshot containing `connector_hints` but assert rendered Markdown does not contain:
  - `Possible Connector Candidates`
  - `connector candidates`
  - `example connector candidate`
- Add or adjust a network snapshot test proving useful neutral facts still render:
  - vendor name remains present
  - gateway/DNS candidates remain present
  - Mermaid map remains present and deterministic
- Update `tests/test_render_inventory_draft.py::test_render_inventory_draft_from_network_candidates_is_review_required_and_valid_inventory` to assert:
  - `_review` has no `connector_hints`
  - rendered YAML text has no `connector_hints`
  - generated facts have no “Possible connector candidate” text
  - vendor fact remains present
  - draft still validates as Inventory and keeps discovered, low-confidence Evidence
- Add a CLI help assertion that `discover-network --help` does not contain “connector hints”.
- Run `pytest` after implementation.

## Files likely touched
- `tests/test_network_discovery.py` — update expectations and add absence checks for discovery snapshot Markdown.
- `tests/test_render_inventory_draft.py` — update draft YAML expectations and add absence checks for connector-candidate facts/fields.
- `tests/test_cli_help.py` — add/adjust help-text coverage for neutral vendor-enrichment wording.
- `src/steadlore_house/render_network_snapshot.py` — remove user-facing connector-candidate rendering and prevent hint-only candidate promotion.
- `src/steadlore_house/render_inventory_draft.py` — stop emitting `connector_hints`, connector-candidate facts, and hint-derived type suggestions.
- `src/steadlore_house/cli.py` — replace connector-hint wording in discovery help.
- `src/steadlore_house/review_inventory_draft.py` — likely remove display of legacy `connector_hints` during interactive review.
- `docs/data-model.md` — align documentation with the accepted decision that unavailable connector suggestions are not user-facing.

## Security considerations
- Risk is low because this slice removes suggestions rather than adding access, authentication, polling, cloud calls, or remediation.
- Mitigation: do not implement any connector and do not add connector configuration or credentials.
- Preserve local-first behavior: MAC vendor enrichment remains offline and optional/auto-discovered locally.
- Preserve the separation between Discovery Snapshot observations and Manual Inventory household meaning.
- Do not add secrets to tests, docs, generated output, or fixtures.
- Avoid lockout/remediation paths entirely; this is rendering and draft-generation only.

## Debt considerations
- Retires the current watchlist item “Connector hint language before connectors exist” for user-facing Discovery Snapshot and Manual Inventory Draft outputs.
- Avoids ad hoc post-render string filtering by changing renderer behavior and draft construction directly.
- Leaves internal `connector_hints` fields/mapping as accepted short-term debt if not user-facing; future Available Connector work should revisit or rename this model deliberately.
- Reduces risk that upcoming Infrastructure Map work inherits misleading connector wording.
- Introduces no new module sprawl.

## Refused scope
- No Home Assistant, Portainer, Telegram, UniFi, Tailscale, Docker, or other connector implementation.
- No connector configuration, authentication, polling, health checks, cloud access, or package metadata.
- No Infrastructure Map, GUI, lifecycle, role visibility, dependency graph expansion, or roadmap reshuffle.
- No canonical Manual Inventory schema redesign beyond generated draft metadata cleanup.
- No AI/LLM behavior and no shell execution/remediation path.
- No broad MAC vendor enrichment redesign except where needed to prevent user-facing connector suggestions.

## Open questions
None block safe implementation. The selected slice and existing architecture/security docs are sufficient: before a Connector exists, user-facing outputs should not advertise connector suggestions.
