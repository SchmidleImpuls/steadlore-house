# Technical Debt

Bad code is expensive because it makes future AI-assisted development worse.

Record accepted debt intentionally:

```markdown
## <debt item>

- Introduced in:
- Why accepted:
- Consequence if ignored:
- Retirement trigger:
- Owner/role:
```

Prefer deep modules with simple interfaces over shallow module sprawl.

## Current watchlist

### Connector hint language before connectors exist

- Introduced in: early network discovery/vendor enrichment work.
- Why accepted: useful internal discovery signal while exploring the domain.
- Consequence if ignored: user-facing output may imply connectors exist before they do.
- Retirement trigger: before any Infrastructure Map or public discovery output surfaces connector suggestions.
- Owner/role: Product Steward and Technical Reviewer.

### CLI-first workflows

- Introduced in: v0 prototype.
- Why accepted: boring, inspectable, testable foundation.
- Consequence if ignored: Operators may not remember infrequent CLI workflows, reducing maintenance reliability.
- Retirement trigger: local web UI Product Loop after dependency graph and Infrastructure Map are coherent.
- Owner/role: Product Steward and Developer Agent.

### Missing dependency graph model

- Introduced in: initial manual/data-model focus.
- Why accepted: manual generation and validation came first.
- Consequence if ignored: Infrastructure Map cannot deliver first Operator setup value.
- Retirement trigger: dependency graph model and Mermaid rendering increment.
- Owner/role: Developer Agent.

### No lifecycle state

- Introduced in: initial active-only inventory model.
- Why accepted: v0 data model stayed intentionally small.
- Consequence if ignored: decommissioning, recommissioning, and stale references remain ambiguous.
- Retirement trigger: lifecycle/decommission Product Loop.
- Owner/role: Developer Agent and Technical Reviewer.

### No role visibility model

- Introduced in: early renderer simplicity.
- Why accepted: Stress User-first output came before audience-specific filtering.
- Consequence if ignored: technical details may either overwhelm Stress Users or be omitted from Helper Persons.
- Retirement trigger: role visibility schema and renderer filtering increment.
- Owner/role: Product Steward and Developer Agent.
