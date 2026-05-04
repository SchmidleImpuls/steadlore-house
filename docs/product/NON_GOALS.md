# Non-Goals

Canonical non-goals are defined in `AGENTS.md` and reinforced by `README.md`. This file records product-loop strategy boundaries.

## Explicit non-goals

Steadlore House is not:

- a generic chatbot
- a smart-home hub
- a password manager
- a monitoring dashboard
- a replacement for Home Assistant, Portainer, Tailscale, UniFi, Synology, Reolink, or NetBox
- an estate-planning app
- an autonomous infrastructure remediation platform
- an AI agent with free-form shell access
- a product about death as its primary emotional frame
- Steadlore Life or any other future Steadlore product

## Connector boundaries

Before a connector exists, Steadlore House should not surface future connector suggestions to users.

When a connector exists and is relevant, the product language should be:

> Available connector

Connector-specific details about access needs, verification behavior, and privacy/security implications belong with the connector package.

## GUI boundaries

A local web UI is in near-term product direction, but it must not compromise local-first behavior, YAML inspectability, or the manual-first safety model.

## Strategic escalation triggers

Escalate before changing boundaries around:

- autonomous remediation
- secret handling
- cloud dependencies
- web UI exposure/authentication
- brand architecture beyond Steadlore House
- legal/financial/estate continuity domains
