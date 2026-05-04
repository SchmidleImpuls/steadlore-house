# Product Selection

## Selected slice
Remove user-facing connector-candidate language from discovery snapshot and Manual Inventory Draft outputs until a real Available Connector exists.

## Why this, why now
This directly supports the vision of calm, trustworthy household continuity by avoiding false promises during the Operator setup path. The target Operator is trying to understand what exists, what matters, and what to review; suggesting connectors that cannot be used creates uncertainty and distracts from Manual Inventory review. It also honors the accepted sequencing: dependency graph and Infrastructure Map work matter next, but connector-hint cleanup is a smaller, safer prerequisite because future review surfaces should not carry misleading integration language. The opportunity cost is low: this is narrower and more reversible than starting GUI, lifecycle, role visibility, or connector work, and it addresses an explicit product decision already recorded in the Decision Log.

## User value
Operators see discovery and draft outputs that clearly separate observed facts from usable product capabilities. This reduces setup confusion and prevents an Operator from looking for Home Assistant, Portainer, Telegram, or other connector paths that do not exist yet.

## Strategic value
This reinforces the boundary that Connectors discover only when they actually exist, preserves trust in local-first deterministic outputs, and keeps the product pointed at a trustworthy Continuity Manual and Infrastructure Map rather than premature integration promises.

## Acceptance criteria
- Generated discovery snapshot Markdown does not include “Possible Connector Candidates”, “connector candidates”, or similar future-connector suggestions when no Available Connector exists.
- Generated Manual Inventory Draft YAML does not include `connector_hints` or connector-candidate facts when no Available Connector exists.
- Existing discovery observations that are useful as neutral device/service facts remain available without connector-specific recommendation language.
- README or product documentation continues to state that no Home Assistant, Portainer, Telegram, or other connector exists yet, if that statement is already present.
- Tests or snapshots cover the absence of unavailable connector suggestions in discovery snapshot and draft outputs.
- The term “Available Connector” is reserved for connectors that actually exist.

## Non-goals
- Do not implement any connector.
- Do not add connector configuration, authentication, polling, health checks, or cloud access.
- Do not redesign the discovery model beyond removing or hiding unavailable connector suggestions.
- Do not change the canonical YAML Manual Inventory model except where necessary to stop emitting connector-candidate draft fields.
- Do not start Infrastructure Map, GUI, lifecycle, or role visibility work in this slice.

## Reversibility
Easy to reverse. The slice removes or suppresses misleading output language without committing to a new architecture; connector suggestions can be reintroduced later under the accepted Available Connector vocabulary once a connector actually exists.

## Risks
- Product risk: removing hints may slightly reduce perceived future capability, but that is preferable to implying unavailable integrations.
- UX risk: Operators may lose a weak clue that a discovered device resembles a known ecosystem; neutral discovery facts should preserve useful observations without recommendation language.
- Strategic risk: if implemented as ad hoc string filtering instead of model-level behavior, future connector work could become messy.
- Reputational risk: leaving the current language in place would undermine trust by suggesting the product can do more than it can.
- Security risk: low, provided the slice does not add connector access or secret handling.

## Rejected alternatives
- Add a local web UI first: tempting because CLI friction is real, but it is larger, more security-sensitive, and should wait until core outputs are coherent.
- Add Infrastructure Map Markdown output: strategically important, but it would amplify the same connector-language problem if built on misleading discovery/draft wording.
- Add a fallback section for unlisted symptoms: valuable for Stress Users, but the current friction is less directly tied to an accepted product decision and would not improve Operator setup trust.
- Start a real connector: premature and explicitly outside current sequencing until the manual, Infrastructure Map, data model, and safety boundaries are coherent.
- Soften Stress User policy wording: useful, but role visibility and audience filtering need more deliberate sequencing than this smaller cleanup slice.
