# Threat Model

This document records the initial v0 safety posture for Steadlore House.

## v0 trust boundary

Steadlore House v0 reads local OS network state, reads local Manual Inventory and Runbook YAML, validates structured inputs, and renders Markdown outputs. It does not connect to household management APIs, execute remediation, or store Secrets. Active ping discovery is opt-in and uses an existing `nmap` binary only when explicitly requested.

## Primary risks

- Secret exposure in inventory, runbooks, examples, tests, or generated output.
- Unsafe guidance that tells a stressed household member to change or reset infrastructure.
- Lockout caused by changes to gateways, switches, Wi-Fi access points, DNS, VLANs, identity providers, password-manager access, backups, or admin access.
- False confidence from stale or unknown facts.
- False confidence from treating observed network hosts as confirmed household inventory.
- False confidence from treating MAC vendor names as confirmed device roles.
- A future Conversation Interface inventing missing facts or escalating from guidance into action.

## v0 mitigations

- Raw secret-looking fields are rejected during validation.
- Secret References may point to where access information is stored but must not include the Secret itself.
- Network Discovery Snapshots are labeled as observational and not trusted Manual Inventory.
- MAC vendor enrichment is local-only and rendered as candidate hints, not confirmed roles.
- Facts carry Evidence and freshness information; stale facts are rendered visibly.
- Runbook titles must describe Stress User symptoms rather than guessed root causes.
- First Checks must be Safe Actions.
- Deterministic policy classification rejects First Checks that appear privileged, high-friction, or forbidden.
- The AI Assistance Packet instructs chatbots to perform safe checks only, avoid invented facts, and escalate privileged actions to Helper Persons.

## Non-goals for v0

- Autonomous remediation.
- Free-form shell execution.
- API connector-driven discovery.
- Credential storage.
- Replacing Home Assistant, Portainer, Tailscale, UniFi, NetBox, monitoring tools, or a password manager.
