# Security Baseline

Use `docs/threat-model.md` and `AGENTS.md` as canonical safety inputs. This file materializes additional security decisions from product discovery.

## Accepted baseline

- No secrets in repository examples, tests, generated output, docs, prompts, or YAML data.
- Use Secret References only.
- Do not add AI-driven arbitrary command execution.
- Do not add autonomous remediation.
- Core infrastructure, identity, backups, secrets, and lockout-risk areas require high-friction review.
- Surface stale, unknown, inferred, discovered, manually confirmed, and decommissioned/lifecycle-conflict states honestly.
- Discovery observations must remain separate from household meaning.

## Web UI baseline

Future local web UI should initially bind only to localhost.

If an Operator exposes Steadlore House through a reverse proxy, VPN, mesh network, or wider network binding, access control becomes the Operator's responsibility unless and until Steadlore House implements its own authentication model.

The web UI should use shared deterministic Python modules rather than shelling out to CLI commands as its normal backend design.

## Connector baseline

Before a connector exists, do not surface user-facing connector suggestions.

Once connectors exist, each connector package should explain:

- what it verifies
- what access it needs
- what data it reads
- privacy/security implications
- whether it mutates anything

Connectors discover. They do not define household meaning.

## Lifecycle baseline

Rediscovering a decommissioned entity is a lifecycle conflict. It should be shown for Operator review, not silently restored or ignored.

Active dependencies on decommissioned entities should warn and render disclaimers rather than fail hard by default.

## Hard-to-reverse risks

- Web UI exposure without authentication.
- Password-manager metadata connectors.
- Any action path that can change infrastructure state.
- Any feature that could cause lockout.
