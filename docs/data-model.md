# Data Model

This document describes the initial v0 data model for Steadlore House.

The model is intentionally small. It exists to generate a deterministic Continuity Manual from manual inventory and structured runbooks. It does not implement connectors, chat, live diagnostics, or remediation.

The Continuity Manual primarily serves a Stress User: a potentially stressed household member who notices a symptom and needs calm, safe guidance. It secondarily serves a Helper Person contacted by that Stress User.

## Inputs and discovery outputs

### Discovery Snapshot

A Discovery Snapshot is a timestamped observational output from local discovery. It helps an operator start mapping core infrastructure, but it is not trusted Manual Inventory until reviewed.

The initial Network Discovery Snapshot may include:

- local interfaces and addresses
- default routes and gateways
- DNS servers from local resolver configuration
- neighbor entries from the local ARP/neighbor cache
- optional active ping-scan hosts when explicitly requested with `nmap`; scan targets can be explicit or derived from local IPv4 interface subnets
- optional offline MAC vendor enrichment from an automatically discovered local `nmap-mac-prefixes` file or an explicit local OUI file
- core infrastructure candidates derived from routes, DNS servers, vendor enrichment, and optional active scan results
- possible connector candidates based on vendor hints
- evidence sources and warnings

Discovery Snapshots must not infer household meaning. For example, a default gateway may be labeled as an observed gateway, and a MAC vendor may suggest a possible connector, but role, owner, location, and Household Impact require Manual Inventory confirmation.

### Manual Inventory Draft

A Manual Inventory Draft is generated from curated Discovery Snapshot candidates to reduce blank-page work for the operator.

A draft:

- is review-required
- may include candidate Devices only
- uses opaque stable candidate Device IDs derived from discovery identifiers; operators may replace them during review
- stores structured `_review` metadata for candidate IP address, vendor, reasons, connector hints, and fields to review
- may deterministically suggest `device_type`, `core_infrastructure`, and conservative Household Impact for default gateway and DNS candidates
- uses `Unknown` for role-like fields that discovery cannot know, such as Location
- marks discovered Facts with low confidence
- must not claim confirmed Household Impact
- must not include Secrets
- must not overwrite reviewed Manual Inventory

The operator reviews and edits the draft before treating it as Manual Inventory. The `review-inventory-draft` command provides an initial interactive CLI review flow that promotes confirmed candidate Devices and removes `_review` metadata from the generated Manual Inventory.

Promotion requires operator confirmation and reviewed values for stable ID, name, device type, `core_infrastructure` status, Location, and Household Impact.

Evidence fields use these meanings:

- `freshness_days`: how many days a discovered or confirmed Fact should be treated as fresh before Steadlore marks it stale.
- `confidence`: a low/medium/high indication of how strongly to rely on the Fact. Discovery-generated Facts use low confidence until reviewed.

### Manual Inventory

The Manual Inventory describes household infrastructure and meaning that cannot be safely inferred from raw discovery alone.

Initial entities:

- `Person`: an Operator, Trusted Person, Stress User, or Helper Person.
- `Device`: a physical object such as a host, gateway, switch, or access point. Devices may be marked `core_infrastructure` when they are believed to be Core Infrastructure.
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
- temporary workarounds to surface before escalation
- First Checks
- Escalation Path
- Do-Not-Touch List
- optional technical note for a Helper Person

First Checks are classified with Policy language such as Safe Action, Privileged Action, High-Friction Action, or Forbidden Action. In v0, First Checks must be Safe Actions.

### Policy

Policy is a deterministic safety layer used by validators and renderers.

Initial action classes:

- `safe`: read-only or low-risk observations a Stress User may perform without special approval.
- `privileged`: changes to services, containers, hosts, software, or configuration requiring explicit approval.
- `high_friction`: privileged changes to core infrastructure, identity, secrets, backups, or access that could cause Lockout.
- `forbidden`: actions that expose Secrets, delete critical data, or create unacceptable safety or Lockout risk.

Runbook authors declare an action class for each guided action. Validation also classifies the action text with conservative deterministic rules. A declared class must be at least as strict as the inferred policy classification, and First Checks are rejected unless both the declared and inferred class are Safe Action.

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

## Renderings

The same source data can be rendered for different audiences:

- Continuity Manual: for a Stress User first and a Helper Person second.
- AI Assistance Packet: for a chatbot helping a Stress User understand the manual and perform safe checks only.

The AI Assistance Packet must not contain more truth than the Continuity Manual. It adds explicit chatbot instructions, safety boundaries, evidence, unknowns, and escalation rules.

## Current implementation

The first implementation reads YAML files and renders Markdown.

Implemented now:

- passive local Network Discovery Snapshot rendering
- review-required Manual Inventory Draft generation from Network Discovery Snapshot candidates
- optional explicit `nmap` ping-scan snapshot rendering
- Manual Inventory parsing
- Runbook parsing
- raw secret-field rejection
- schema validation with helpful errors
- relationship validation between runbooks, services, and dependencies
- staleness calculation
- deterministic Continuity Manual rendering
- deterministic AI Assistance Packet rendering
- deterministic v0 policy classification for action guidance

Not implemented yet:

- web interface
- connectors
- publication destinations
- PDF rendering
- complete policy model for supervised remediation
- autonomous remediation
