# Target Users

Use canonical terms from [`UBIQUITOUS_LANGUAGE.md`](UBIQUITOUS_LANGUAGE.md).

## Accepted decisions

### Primary setup and maintenance user: Operator

The Operator is the only person who can realistically set up and maintain Steadlore House. The Operator has installed and maintains more household infrastructure than a single modem/gateway/access-point.

Operator pain:

- household infrastructure knowledge lives in their head
- other household members depend on them
- meaningful infrastructure changes are easy to forget to document
- CLI-only tooling is hard to retain when used infrequently

Operator desired outcome:

> My house is finally documented in a way that I am less of a single point of failure.

### Primary continuity user: Stress User

The Stress User is a Trusted Person who needs calm, safe guidance when something is confusing, broken, or the Operator is unavailable.

Stress User pain:

- does not know what infrastructure matters
- does not know what is safe to check
- may fear making things worse
- needs household impact, not raw technical state

### Secondary user: Helper Person

The Helper Person may help the Stress User or Operator. They can receive more technical context, including appendices and dependency maps, but safety constraints and uncertainty must remain visible.

## Role visibility ladder

Steadlore House should support an audience visibility ladder:

| Visibility | Visible to Stress User | Visible to Helper Person | Visible to Operator |
|---|---:|---:|---:|
| Stress User | yes | yes | yes |
| Helper Person | no | yes | yes |
| Operator | no | no | yes |

Default output should protect Stress Users from unnecessary technical burden while allowing transparency through appendices when appropriate.

## Reversible bets

- Helper Persons benefit from the Infrastructure Map as a technical appendix.
- Stress Users may see transparent appendices, but their primary path must remain symptom-first guidance.

## Unresolved questions

- Exact default visibility per entity type.
- Whether visibility is stored on entities, facts, graph nodes, graph edges, sections, or all of these.
