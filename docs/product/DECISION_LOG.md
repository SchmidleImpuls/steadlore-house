# Product Decision Log

Record consented product decisions that shape future work.

```markdown
## YYYY-MM-DD — <decision>

- Status: proposed | accepted | superseded
- Context:
- Decision:
- Consequences:
- Related loop run:
```

## 2026-05-04 — Infrastructure Map becomes the Operator setup surface

- Status: accepted
- Context: Product discovery clarified that first value occurs after setup, before an outage.
- Decision: Use **Infrastructure Map** for the recurring Operator-facing discovery/review/sense-making surface. The Continuity Manual remains the Stress User-first household continuity artifact.
- Consequences: Roadmap should prioritize dependency graph and Infrastructure Map rendering before GUI implementation.
- Related loop run: product discovery / grill-me materialization

## 2026-05-04 — YAML remains canonical source of truth

- Status: accepted
- Context: The future GUI should reduce CLI burden without hiding inspectable local data.
- Decision: YAML remains canonical. The GUI may edit YAML; advanced Operators may edit YAML directly. Git/file history is enough for now.
- Consequences: Future web UI should share Python application modules and preserve readable file formats.
- Related loop run: product discovery / grill-me materialization

## 2026-05-04 — Meaningful Infrastructure Change is Household Impact based

- Status: accepted
- Context: Operators should maintain Steadlore after meaningful changes, but not every tiny device addition.
- Decision: A Meaningful Infrastructure Change is a change to a Device, Service, Access Path, dependency, Secret Reference, responsible person, or Location that could change Household Impact, safe guidance, escalation, or the Operator's ability to recover the household.
- Consequences: Future reminders and rediscovery mismatch review should use Household Impact, not topology alone.
- Related loop run: product discovery / grill-me materialization

## 2026-05-04 — Connector suggestions require existing connectors

- Status: accepted
- Context: Discovery can identify vendors, but user-facing suggestions for unavailable connectors create false product promises.
- Decision: Before connectors exist, show no connector suggestions. Once a connector exists, call it an **Available Connector**.
- Consequences: Future discovery output should avoid promising future connectors.
- Related loop run: product discovery / grill-me materialization

## 2026-05-04 — Local web UI direction

- Status: accepted
- Context: Infrequent maintenance makes CLI-only operation insufficient for many Operators.
- Decision: Long-term packaging should include a CLI and a Docker image with CLI plus local web app. Initial web UI binds to localhost. CLI and web app should share Python application modules rather than relying on shelling out to CLI commands.
- Consequences: Future architecture should isolate application services behind deterministic interfaces.
- Related loop run: product discovery / grill-me materialization
