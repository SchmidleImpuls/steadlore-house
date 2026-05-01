# AGENTS.md

This file guides human and artificial contributors working on Steadlore House.

## Project identity

Steadlore is the continuity brand.

Steadlore House is the first product: a local-first household continuity system.

It helps a household preserve, verify, and surface the knowledge needed to understand and recover from failures in home infrastructure, services, devices, accounts, procedures, and responsibilities.

The emotional posture is:

- I am prepared, not paranoid.
- You are safe, not dependent on me.
- We have prepared for this.

## What this project is

Steadlore House is:

- a living continuity manual
- a household infrastructure knowledge model
- a stale-aware documentation system
- a safe recovery guide
- a bridge between technical operators and non-technical trusted people

## What this project is not

Steadlore House is not:

- a generic chatbot
- a smart-home hub
- a password manager
- a monitoring dashboard
- a replacement for Home Assistant
- a replacement for Portainer
- a replacement for Tailscale
- a replacement for NetBox
- an estate-planning app
- an autonomous infrastructure remediation platform
- an AI agent with free shell access

Do not drift into those products by accident.

## Core promise

If something happens, the house still knows how it works.

## v0 scope

v0 is a Dockerized local prototype that:

- reads a structured household inventory
- reads structured runbooks
- generates a Markdown continuity manual
- tracks fact provenance and last verification time
- marks stale information clearly
- includes a concrete Home Assistant failure scenario
- stores no secrets
- performs no autonomous remediation

v0 may include placeholders for future connectors, but it should not implement Portainer, Home Assistant, Tailscale, UniFi, Telegram, or LLM-based Q&A until the manual and data model are coherent.

## Non-negotiable principles

### Continuity before autonomy

The first useful artifact is a trustworthy manual.

Do not build an agent that acts before the system can explain.

### Ubiquitous language before implementation

Use the vocabulary in `docs/ubiquitous-language.md`.

If new concepts are needed, update the vocabulary before spreading new terminology through code, docs, tests, examples, or issues.

### Local-first by default

Household infrastructure data should stay local unless the user explicitly exports it.

Avoid dependencies that require cloud services for the core product to work.

### No secrets in the manual

Never store the following in docs, examples, tests, fixtures, generated output, or sample data:

- passwords
- API tokens
- recovery keys
- TOTP seeds
- backup codes
- private keys
- 1Password Emergency Kit contents
- full credential exports

Use secret references instead.

A secret reference may say:

- password manager name
- vault name
- item name
- physical storage hint
- responsible person

It must not include the secret itself.

### Facts need evidence and age

Every meaningful claim should be able to carry:

- source
- last verified timestamp
- freshness expectation
- confidence or verification status

The system must distinguish:

- known
- unknown
- stale
- inferred
- manually confirmed
- discovered from a connector

Never invent missing facts.

### Family mode is first-class

Steadlore House must explain household impact, not just technical state.

Bad:

- `homeassistant` container is unhealthy.

Better:

- Home Assistant appears unavailable. Some lights and automations may not work. Internet and Wi-Fi are not necessarily affected.

### Operator mode may be technical

Operator-facing output may mention containers, hosts, volumes, networks, APIs, ports, and logs.

Family-facing output should explain consequences, safe checks, and escalation paths.

### LLMs reason; deterministic tools act

If LLM features are added later, they must not directly execute arbitrary commands.

Use deterministic modules for:

- discovery
- parsing
- validation
- rendering
- policy enforcement
- action execution

LLMs may summarize, explain, classify, or help draft runbooks, but only within explicit boundaries.

### No free-form shell execution

Do not add features where a model can produce and run arbitrary shell commands.

All actions must eventually be represented as explicit, typed, policy-checked operations.

### Safe by refusal is not enough

The system should not simply refuse risky actions. It should explain:

- why the action is risky
- what information is missing
- what safe checks can be done first
- who should approve or perform the action

### Core infrastructure is high-friction

The following should be read-only or require high-friction approval:

- uplink
- gateway
- switches
- Wi-Fi access points
- VLANs
- firewall rules
- DNS
- identity providers
- Tailscale ACLs
- password-manager access
- backup deletion
- admin access changes

The system must not be able to lock out the primary operator.

## Architecture boundaries

Use these boundaries unless explicitly changed by an architecture decision record.

### Connectors discover

Connectors import facts from systems such as Home Assistant, Portainer, Tailscale, UniFi, Docker, or local scans.

Connectors should not contain household meaning or recovery policy.

### Inventory models

Inventory represents devices, services, locations, dependencies, people, and household meaning.

Inventory is not a raw dump of connector data.

### Evidence qualifies

Evidence records source, age, confidence, and verification status.

Evidence must remain visible enough to support honest answers.

### Manual explains

The continuity manual turns structured knowledge into readable documentation.

The manual should survive even when chat, LLMs, connectors, or live systems are unavailable.

### Runbooks guide

Runbooks describe failure scenarios, household impact, safe checks, escalation paths, privileged actions, and forbidden actions.

### Policy constrains

Policy defines what is safe, privileged, high-friction, or forbidden.

### Conversation surfaces

Conversation interfaces, such as Telegram or a web chat, must surface known facts, uncertainty, stale data, and runbook guidance.

Conversation is not the source of truth.

## Development preferences

Prefer boring, inspectable implementation choices.

For v0:

- Python is acceptable and preferred unless changed later.
- Use type hints.
- Use small, deep modules with simple interfaces.
- Use schema validation.
- Keep generated Markdown deterministic.
- Add tests for schemas, rendering, staleness logic, and safety rules.
- Keep the app runnable in Docker.
- Avoid heavyweight frameworks until they are justified.

## Documentation expectations

When adding a feature, update relevant docs.

At minimum, consider whether the change affects:

- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `docs/ubiquitous-language.md`
- `docs/data-model.md`
- `docs/threat-model.md`
- `docs/vision.md`
- examples
- generated manual output

## Example quality bar

Examples must be realistic enough to test the product but sanitized enough to publish.

Do not include real secrets, real recovery material, real private IPs that matter, real tokens, real account identifiers, or sensitive household details.

## If uncertain

Choose the safer, more explicit path.

Prefer:

- smaller scope
- clearer vocabulary
- stronger provenance
- local data
- deterministic behavior
- visible uncertainty
- no action

Do not create charming fog.