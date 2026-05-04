# Product Selection

## Selected slice
Add the smallest deterministic dependency graph rendering to the generated Continuity Manual for reviewed Manual Inventory dependencies in the existing Home Assistant scenario.

## Why this, why now
This is the smallest slice that directly advances the vision that “the house still knows how it works” while serving the Operator’s desire to be less of a single point of failure and the Helper Person’s need for technical context. The roadmap names dependency graph model and rendering as the next strategic milestone before GUI, connectors, chat, or remediation. User observations show the current manual already works as calm Stress User guidance, but the existing `depends_on` relationship is not visible enough. Choosing manual graph rendering now preserves the Continuity Manual as the first useful artifact and avoids the opportunity cost of starting a broader Infrastructure Map, web UI, connector, or review workflow before dependency meaning is visible in the core output.

## User value
The Operator and Helper Person can see the load-bearing relationship behind the first concrete symptom: Home Assistant depends on House Server 01. The Stress User path remains symptom-first and calm, while the manual gains a concise technical appendix that reduces guessing during escalation.

## Strategic value
This validates dependency graph value inside the current local-first, deterministic Markdown product before introducing a separate Infrastructure Map or GUI. It strengthens the bridge between Manual Inventory, Evidence, Stale status, Runbooks, and future Infrastructure Map rendering without expanding into discovery trust, connectors, monitoring, or remediation.

## Acceptance criteria
- The generated Continuity Manual includes a dependency graph section or appendix when reviewed Manual Inventory contains dependencies.
- The example Home Assistant dependency renders visibly as Home Assistant depending on House Server 01.
- The rendering is deterministic and suitable for Markdown, using Mermaid as the first graph format.
- Graph nodes or adjacent labels expose evidence age/trust state at least enough to show stale facts where the underlying inventory facts are stale.
- Unknown or unresolved dependency targets are rendered honestly as unknown or unresolved, not invented.
- Stress User runbook guidance remains symptom-first and is not replaced by technical graph content.
- Existing secret protections remain unchanged; no Secret values appear in generated output.
- Tests cover deterministic rendering, the Home Assistant example dependency, stale/unknown labeling behavior, and absence of graph output when no dependencies exist.

## Non-goals
- Do not build the full Infrastructure Map output in this slice.
- Do not add a GUI, Docker packaging changes, publication destinations, chat interface, or LLM-based Q&A.
- Do not implement connectors or advertise unavailable future connectors.
- Do not add autonomous remediation, privileged action execution, or free-form shell execution.
- Do not introduce typed dependency edges, Runtime Service modeling, Access Path modeling, lifecycle support, or role Visibility unless the existing generic `depends_on` rendering cannot work without a tiny supporting adjustment.
- Do not make Discovery Snapshot observations trusted Manual Inventory.

## Reversibility
Easy to moderate to reverse. A Markdown/Mermaid rendering section can be removed or changed with limited product impact if the presentation is wrong. It becomes moderately reversible only if schema changes are introduced, so the slice should prefer existing generic `depends_on` semantics.

## Risks
- Product risk: the graph could become a technical ornament instead of improving continuity understanding.
- UX risk: exposing technical structure too early in the manual could distract or stress the Stress User if not placed as an appendix or Helper Person-oriented section.
- Strategic risk: over-designing graph semantics now could delay the intended small milestone and create schema churn.
- Security risk: graph labels might accidentally surface sensitive locations, names, or Secret Reference details if renderer boundaries are careless.
- Reputational risk: a noisy or misleading graph could undermine trust in the manual’s calm, honest posture.

## Rejected alternatives
- Full Markdown Infrastructure Map: tempting because it is the Operator-facing surface, but it combines reviewed inventory, discovery candidates, stale facts, gaps, and dependencies; that is too much for the first minimal slice.
- First-run documentation improvement: useful and low-risk, but it does not advance the accepted next strategic milestone or make the existing Home Assistant dependency visible.
- Manual Inventory draft review rehearsal: useful for setup friction, but it focuses on promotion workflow rather than the core continuity model.
- Explicit unknowns/gaps in the Continuity Manual: valuable, but less directly tied to the accepted dependency graph milestone and the observed missing Home Assistant relationship.
- Local web UI: aligned with long-term Operator needs, but premature before the manual, dependency graph, and Infrastructure Map semantics are coherent.
