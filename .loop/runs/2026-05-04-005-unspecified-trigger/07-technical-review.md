# Technical Review

## Verdict
Pass

## Correctness
No blocking correctness issues found.

The implementation removes connector-candidate wording from the generated Network Discovery Snapshot, Manual Inventory Draft YAML, interactive draft review display, and CLI help while preserving neutral discovery observations such as IP address, MAC address, vendor, gateway/DNS reasons, interfaces, state, evidence, and review-required status.

The renderer change also avoids promoting a discovered neighbor or active-scan host solely because it has internal `connector_hints`, which matches the selected slice.

Non-blocking edge observations:

- Internal `connector_hints` fields and scoring remain in discovery/candidate structures. They do not appear to leak into current user-facing outputs, but future rendering surfaces should be careful not to re-expose them.
- `docs/engineering/TECH_DEBT.md` still lists “Connector hint language before connectors exist” as a current watchlist item. Since this slice appears to retire the user-facing part of that debt, the debt record should be updated soon to avoid stale guidance.

## Tests and feedback loops
Tested during review:

- `python -m pytest tests/test_network_discovery.py tests/test_render_inventory_draft.py tests/test_cli_help.py tests/test_review_inventory_draft.py`
- `python -m pytest`
- `git diff --check`
- `rg` check for connector-candidate leakage in `dist`, relevant `src`, `docs/data-model.md`, and `README.md`

Results:

- Focused tests passed: `26 passed`.
- Full suite passed: `68 passed`.
- `git diff --check` passed.
- Grep found only internal `connector_hints` references in source structures, not generated/user-facing output.

Coverage is adequate for this slice. Missing but non-blocking:

- A CLI help test should also assert absence of “connector hints,” not only presence of the replacement wording.
- Future tests should protect any new Infrastructure Map/discovery surface against reintroducing unavailable connector suggestions.

## Security
No security regression found.

The change removes misleading integration suggestions and does not add connector access, authentication, polling, cloud calls, network behavior, secret handling, shell execution, remediation, or privileged actions. It preserves local-first deterministic rendering and keeps Discovery Snapshot observations separate from Manual Inventory household meaning.

No secrets were introduced in changed generated outputs, docs, tests, or examples.

## Maintainability
The change is small and localized to existing renderer/output boundaries: `render_network_snapshot.py`, `render_inventory_draft.py`, `review_inventory_draft.py`, and CLI help text. It avoids post-render string filtering and instead changes renderer behavior directly, which is maintainable.

Leaving internal `connector_hints` machinery is acceptable short-term debt for reversibility, but the naming is now potentially confusing because the user-facing product has explicitly moved away from connector suggestions until real Available Connectors exist.

## Architecture
The implementation aligns with the documented Connector/Discovery boundary: discovery remains observational and does not advertise unavailable connectors. It does not implement connectors, change the canonical Manual Inventory schema, add Infrastructure Map scope, or introduce new modules.

The data-model documentation was updated to describe vendor enrichment as a neutral observation rather than a connector suggestion. The remaining architecture follow-up is to update the technical debt watchlist so future contributors know the user-facing leakage has been retired while internal connector-hint data remains temporary internal debt.

## Debt and follow-ups
Suggested follow-ups, none blocking merge:

- Update `docs/engineering/TECH_DEBT.md` to retire or narrow the connector-hint debt item to internal naming/model cleanup.
- Add explicit CLI help absence coverage for “connector hints.”
- Rename or isolate internal `connector_hints` concepts when Available Connector architecture is designed.
