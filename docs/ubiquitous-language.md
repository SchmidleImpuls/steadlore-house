# Ubiquitous Language

This document defines the shared vocabulary for Steadlore House.

Use these terms consistently in code, documentation, examples, issues, tests, and user-facing output.

If the vocabulary is wrong or incomplete, improve it here before spreading new terms elsewhere.

## Brand and product

| Term | Meaning |
|---|---|
| Steadlore | The continuity brand. |
| Steadlore House | The first Steadlore product, focused on household infrastructure continuity. |
| Securing continuity | The slogan for Steadlore. |
| We have prepared for this | The emotional line: calm readiness without panic. |

## People

| Term | Meaning |
|---|---|
| Household | The people, spaces, routines, devices, services, procedures, and responsibilities Steadlore House helps preserve. |
| Operator | The technical person who understands and maintains the household infrastructure. |
| Trusted Person | Someone allowed to use Steadlore House for guidance. May be non-technical. |
| Stress User | A trusted person using Steadlore House during an outage, absence, confusion, illness, travel, emergency, or after the operator’s death. |
| Fallback Human | A person who can help when the operator is unavailable. |
| Contributor | A human or artificial participant improving the project. |

## Household infrastructure

| Term | Meaning |
|---|---|
| Device | A physical object, such as a gateway, switch, mini-PC, DGX Spark, NVR, access point, camera, modem, or server. |
| Service | A useful household capability provided by one or more devices, such as Wi-Fi, internet access, Home Assistant, camera recording, Plex, or local AI inference. |
| Critical Service | A service whose outage creates meaningful household pain, risk, confusion, or loss of safety. |
| Location | A physical place, such as utility cabinet, studio, master bedroom, rack, shelf, or room. |
| Port | A physical or logical connection point, such as a switch port or exposed service port. Use precise qualifiers when ambiguity matters. |
| Host | A device that runs software services. |
| Container | A containerized runtime unit, usually managed by Docker, Portainer, or a similar tool. |
| Stack | A deployable group of related containers or services. |
| Dependency | A relationship where one device, service, or procedure relies on another. |
| Household Impact | The real-world consequence of a device or service being unavailable. |

## Knowledge model

| Term | Meaning |
|---|---|
| Inventory | The structured model of devices, services, locations, dependencies, people, and household meaning. |
| Fact | A claim the system can use, such as “Home Assistant runs on node1-ein.” |
| Evidence | Metadata that explains where a fact came from, when it was verified, and how reliable it is. |
| Source | The origin of a fact, such as manual inventory, Portainer, Home Assistant, Tailscale, UniFi, local scan, or user confirmation. |
| Last Verified | The time a fact was last checked, imported, or manually confirmed. |
| Freshness Window | The amount of time after which a fact should be considered stale unless verified again. |
| Stale | A fact whose last verification is older than its freshness window. |
| Unknown | A value the system does not know. Unknown values must not be invented. |
| Inferred | A fact derived from other facts rather than directly observed. Inferred facts require clear labeling. |
| Manually Confirmed | A fact explicitly confirmed by an operator or trusted person. |
| Discovered | A fact imported from a connector or scan. |
| Confidence | A qualitative or quantitative indication of how much the system should rely on a fact. Confidence must not hide evidence or age. |

## Documentation and guidance

| Term | Meaning |
|---|---|
| Continuity Manual | The generated human-readable documentation explaining what the household depends on and how to respond when something breaks. |
| Family Mode | Plain-English explanations optimized for non-technical trusted people. |
| Operator Mode | Technical explanations for the operator or technically capable fallback humans. |
| Runbook | A structured recovery guide for a known failure scenario. |
| Failure Scenario | A recognizable situation requiring guidance, such as “Home Assistant is unavailable after redeploy.” |
| Recovery Path | The recommended sequence from detection to explanation to safe checks to escalation. |
| First Checks | Low-risk observations or checks that help understand a failure. |
| Escalation Path | The point where the system tells the user who to contact or what privileged access is required. |
| Do-Not-Touch List | Devices, services, accounts, or actions that trusted people should avoid unless explicitly instructed. |
| Last-Known State | The most recent state the system knows, including when and how it was verified. |

## Safety and access

| Term | Meaning |
|---|---|
| Safe Action | A read-only or low-risk action allowed without special approval. |
| Privileged Action | An action requiring explicit approval, such as restarting a container, rebooting a host, or updating software. |
| High-Friction Action | A privileged action affecting core infrastructure, identity, secrets, backups, or access. |
| Forbidden Action | An action the system must never perform. |
| Approval | Explicit permission from an authorized person before a privileged action. |
| Policy | Rules that define which actions are safe, privileged, high-friction, or forbidden. |
| Secret | Sensitive material such as a password, token, private key, recovery key, TOTP seed, or backup code. |
| Secret Reference | A pointer to where a secret is stored, without including the secret itself. |
| Lockout | A state where the operator or trusted people lose access to systems they need. Steadlore House must not create lockout paths. |
| Remediation | An action intended to fix a problem. In v0, remediation is guidance only, not autonomous execution. |

## System architecture

| Term | Meaning |
|---|---|
| Connector | A read-only integration that imports facts from a source system. |
| Manual Inventory | Human-authored structured inventory, usually stored in YAML or another readable format. |
| Generated Manual | Markdown or other output produced from inventory, evidence, and runbooks. |
| Renderer | Code that turns structured data into human-readable output. |
| Validator | Code that checks whether structured data is complete, coherent, and safe enough to use. |
| Conversation Interface | A way to ask questions, such as Telegram, CLI, web chat, or another UI. |
| Agent | A bounded software actor that may help interpret or guide, but must not bypass policy. Use this term carefully. |
| Local-First | A design stance where core data and functionality remain available locally and do not require a cloud service. |

## Bounded contexts

### Inventory Context

Responsible for modeling:

- devices
- services
- locations
- dependencies
- people
- household impact

The Inventory Context should not perform live discovery or execute recovery actions.

### Evidence and Staleness Context

Responsible for modeling:

- source
- last verified time
- freshness windows
- stale state
- confidence
- unknowns

This context qualifies facts. It does not decide household meaning.

### Continuity Manual Context

Responsible for generating readable documentation.

The manual must be useful without live connectors, chat interfaces, or LLMs.

### Runbook Context

Responsible for failure scenarios, first checks, recovery paths, escalation, and forbidden actions.

Runbooks should explain household impact.

### Policy Context

Responsible for classifying actions as safe, privileged, high-friction, or forbidden.

Policy must prevent lockout and secret exposure.

### Connector Context

Responsible for importing facts from external systems.

Connectors discover. They do not define household meaning.

### Conversation Context

Responsible for surfacing existing knowledge through an interface.

Conversation is not the source of truth.

## Preferred term choices

Use:

- Trusted Person, not end user, family member, or customer when discussing safe access.
- Stress User when designing for outage or emergency use.
- Continuity Manual, not wiki, docs, binder, or knowledge base.
- Fact, not data point, assertion, or claim unless discussing epistemology.
- Evidence, not metadata when source and verification matter.
- Secret Reference, not secret, credential, or password pointer.
- Household Impact, not business impact.
- Forbidden Action, not dangerous thing.
- Unknown, not empty, missing, or null when discussing meaning.

## Terms to avoid or use carefully

Avoid casual use of:

- autonomous
- swarm
- copilot
- oracle
- magic
- self-healing
- bot
- AI brain
- home operating system
- estate vault
- emergency bunker
- disaster mode

These terms distort the product direction.

Use them only when explicitly discussing what the product is not.