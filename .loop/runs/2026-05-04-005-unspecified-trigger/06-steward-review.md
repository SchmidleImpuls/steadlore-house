# Steward Review

## Verdict
Pass

## Vision alignment
The change moves Steadlore House toward the intended product by making discovery and draft outputs more honest and less hype-prone. It supports the calm, trustworthy Operator setup path and protects the future Continuity Manual and Infrastructure Map from implying integrations that do not exist.

## Scope discipline
The implementation stays inside the selected slice. It removes connector-candidate wording from generated discovery snapshot Markdown, Manual Inventory Draft YAML, review prompts, CLI help wording, and data-model documentation without implementing connectors, GUI work, lifecycle support, role visibility, or Infrastructure Map output.

## Non-goal check
No product non-goal violation found. The diff does not add autonomous remediation, chatbot behavior, monitoring, password-management behavior, cloud dependency, connector access, authentication, polling, or any replacement-product posture. It also reinforces the explicit connector boundary that unavailable connector suggestions should not be surfaced.

## Strategic risk
Strategic risk is low. The change slightly reduces visible “future capability” language, but that is desirable because false connector promises undermine trust. The retained internal `connector_hints` fields and tests may create some future cleanup pressure, but from a product strategy perspective that is acceptable because the slice deliberately avoided a broader discovery-model redesign.

## Domain-valid blocking objections
None.

## Non-blocking concerns
- Internal names such as `connector_hints` and test fixtures still exist. This is not user-facing in the changed outputs reviewed here, but it may confuse future contributors unless later renamed or isolated behind real Available Connector support.
- The product still has a broader Operator workflow friction around discovery snapshot → Manual Inventory Draft → reviewed Manual Inventory → Continuity Manual, but that was intentionally outside this slice.

## Suggested follow-ups
- Backlog: rename or retire internal connector-hint machinery when the connector architecture is designed, or convert it to Available Connector metadata only after a connector exists.
- Backlog: add an Operator workflow guide connecting discovery, draft review, and manual generation.
- Decision-log candidate only if needed later: clarify whether vendor recognition may remain an internal discovery heuristic while connector suggestions stay hidden until a real Available Connector exists.
