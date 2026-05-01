# Data Model

This document describes the initial v0 data model for Steadlore House.

The model is intentionally small. It exists to generate a deterministic Continuity Manual from manual inventory and structured runbooks. It does not implement connectors, chat, live diagnostics, or remediation.

The Continuity Manual primarily serves a Stress User: a potentially stressed household member who notices a symptom and needs calm, safe guidance. It secondarily serves a Helper Person contacted by that Stress User.

## Inputs

### Manual Inventory

The Manual Inventory describes household infrastructure and meaning that cannot be safely inferred from raw discovery alone.

Initial entities:

- `Person`: an Operator, Trusted Person, Stress User, or Helper Person.
- `Device`: a physical object such as a host, gateway, switch, or access point.
- `Service`: a household capability such as Home Assistant, Wi-Fi, or internet access.
- `SecretReference`: a pointer to where access information is stored, without containing the secret.
- `Fact`: a meaningful claim used by the manual.
- `Evidence`: source, Last Verified timestamp, Freshness Window, status, and confidence for a Fact.

### Runbook

A Runbook describes one Symptom a Stress User may notice. Runbook titles should use symptom language, not possible root causes.

A Runbook includes:

- plain-English summary
- what is probably still okay
- Household Impact
- concrete access endpoints when useful
- First Checks
- Escalation Path
- Do-Not-Touch List
- optional technical note for a Helper Person

First Checks are classified with Policy language such as Safe Action, Privileged Action, High-Friction Action, or Forbidden Action.

## Evidence and staleness

Every meaningful Fact should carry Evidence.

A Fact is marked Stale when its Last Verified timestamp is older than its Freshness Window. Stale does not mean false. It means the manual must be honest that the Fact may no longer represent the household.

The generated Continuity Manual is a latest-known artifact. It may already be outdated if Steadlore House could not detect recent breaking changes or failed generating or publishing a newer manual.

## Secrets

The model must not contain Secrets.

Allowed:

- password manager name
- vault name
- item name
- physical storage hint
- responsible person

Forbidden:

- passwords
- tokens
- private keys
- recovery keys
- TOTP seeds
- backup codes
- full credential exports

## Scope note

Steadlore House models household infrastructure. External access paths that are not household infrastructure are not modeled as household dependencies.

## Current implementation

The first implementation reads YAML files and renders Markdown.

Implemented now:

- Manual Inventory parsing
- Runbook parsing
- raw secret-field rejection
- schema validation with helpful errors
- relationship validation between runbooks, services, and dependencies
- staleness calculation
- deterministic Markdown rendering

Not implemented yet:

- web interface
- connectors
- publication destinations
- PDF rendering
- policy enforcement beyond rendered action classification
- autonomous remediation
