# Ubiquitous Language

This document defines the shared vocabulary for Steadlore House and for the Product Loop that governs product changes.

Use these terms consistently in code, documentation, examples, tests, issues, prompts, and user-facing output.

If the vocabulary is wrong or incomplete, improve it here before spreading new terminology elsewhere.

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
| Operator | The technical person who understands and maintains the household infrastructure. The Operator is the primary setup and maintenance user. |
| Trusted Person | Someone allowed to use Steadlore House for guidance. May be non-technical. |
| Stress User | A Trusted Person using Steadlore House during an outage, absence, confusion, illness, travel, emergency, or after the Operator’s death. The Stress User is the primary audience for the Continuity Manual. |
| Helper Person | Someone contacted by a Stress User for help. May be technical or non-technical. The Helper Person is the secondary audience for the Continuity Manual and may use technical appendices. |
| Contributor | A human or artificial participant improving the project. |

## Household infrastructure

| Term | Meaning |
|---|---|
| Device | A physical object, such as a gateway, switch, mini-PC, NVR, access point, camera, modem, or server. |
| Service | A useful household capability provided by one or more devices, such as Wi-Fi, internet access, Home Assistant, camera recording, Plex, or local AI inference. |
| Runtime Service | A technical Service that enables other Services or Containers to run, such as Docker. Usually Helper Person or Operator facing unless its outage has direct Household Impact. |
| Critical Service | A service whose outage creates meaningful household pain, risk, confusion, or loss of safety. |
| Core Infrastructure | Devices or services whose changes or outages may affect broad household connectivity, identity, secrets, backups, access, or lockout risk. Examples include gateways, DNS, switches, Wi-Fi access points, VLANs, and firewall rules. |
| Location | A physical place, such as utility cabinet, studio, master bedroom, rack, shelf, or room. |
| Port | A physical or logical connection point, such as a switch port or exposed service port. Use precise qualifiers when ambiguity matters. |
| Host | A Device that runs software services. |
| Container | A containerized runtime unit, usually managed by Docker, Portainer, or a similar tool. Containers may become first-class when a connector or dependency graph needs them. |
| Stack | A deployable group of related containers or services. |
| Dependency | A relationship where one Device, Service, Access Path, or procedure relies on another. Initial graph modeling may use generic `depends_on` relationships before introducing typed dependency edges. |
| Access Path | A route or mechanism used to reach, administer, or help with household infrastructure, such as Tailscale. |
| Household Impact | The real-world consequence of a Device or Service being unavailable. |
| Meaningful Infrastructure Change | A change to a Device, Service, Access Path, Dependency, Secret Reference, responsible person, or Location that could change Household Impact, safe guidance, escalation, or the Operator's ability to recover the household. |

## Knowledge model

| Term | Meaning |
|---|---|
| Inventory | The structured model of Devices, Services, Locations, Dependencies, people, and household meaning. |
| Fact | A claim the system can use, such as “Home Assistant runs on the house server.” |
| Evidence | Metadata that explains where a Fact came from, when it was verified, and how reliable it is. |
| Source | The origin of a Fact, such as Manual Inventory, Portainer, Home Assistant, Tailscale, UniFi, local scan, or user confirmation. |
| Last Verified | The time a Fact was last checked, imported, or manually confirmed. |
| Freshness Window | The amount of time after which a Fact should be considered stale unless verified again. |
| Stale | A Fact whose Last Verified timestamp is older than its Freshness Window. Stale does not mean false. |
| Unknown | A value the system does not know. Unknown values must not be invented. |
| Inferred | A Fact or Dependency derived from other facts rather than directly observed. Inferred information requires clear labeling. |
| Manually Confirmed | A Fact explicitly confirmed by an Operator or Trusted Person. |
| Discovered | A Fact imported from a connector or scan. |
| Confidence | A qualitative or quantitative indication of how much the system should rely on a Fact. Confidence must not hide Evidence or age. |
| Decommissioned | Intentional lifecycle state for an entity that is no longer active but whose metadata is preserved for archive, stale-reference warnings, and possible recommissioning. Decommissioned is not the same as Stale. |
| Recommission | Return a decommissioned entity to active use after review, using previous metadata as defaults rather than blindly restoring it. |
| Lifecycle Conflict | A state where Evidence contradicts lifecycle status, such as rediscovering a decommissioned Device. |

## Documentation and guidance

| Term | Meaning |
|---|---|
| Continuity Manual | The generated human-readable documentation explaining what the household depends on and how to respond when something breaks. It is the first useful household continuity artifact. |
| Infrastructure Map | A recurring Operator-facing review and sense-making surface that combines reviewed Manual Inventory, rediscovery overlap, promotion candidates, decommission candidates, unknowns/gaps, dependency graph, evidence/trust state, and Available Connectors. It may appear as a Helper Person appendix. |
| AI Assistance Packet | A generated, redacted Markdown rendering of the same household knowledge, optimized for a chatbot helping a Stress User understand the Continuity Manual and perform safe checks only. |
| Plain-English Summary | Guidance optimized for a stressed household member. |
| Helper Note | More technical context for a Helper Person, without hiding safety constraints or uncertainty from the Stress User. |
| Runbook | A structured recovery guide for a symptom a Stress User may notice. |
| Symptom | A user-visible problem requiring guidance, such as “Lights or automations are not working.” |
| Failure Scenario | A known technical situation that may explain a Symptom. Use this term carefully; Runbook titles should prefer Symptoms over possible root causes. |
| Recovery Path | The recommended sequence from detection to explanation to safe checks to escalation. |
| First Checks | Low-risk observations or checks that help understand a failure. |
| Escalation Path | The point where the system tells the user who to contact or what privileged access is required. |
| Do-Not-Touch List | Devices, services, accounts, or actions that trusted people should avoid unless explicitly instructed. |
| Last-Known State | The most recent state the system knows, including when and how it was verified. |
| Visibility | Audience level controlling whether information is shown to Stress Users, Helper Persons, or Operators. Stress User-visible content is visible to all roles; Helper Person-visible content is visible to Helper Persons and Operators; Operator-visible content is visible only to Operators. |

## Safety and access

| Term | Meaning |
|---|---|
| Safe Action | A read-only or low-risk action allowed without special approval. |
| Privileged Action | An action requiring explicit approval, such as restarting a container, rebooting a host, or updating software. |
| High-Friction Action | A privileged action affecting Core Infrastructure, identity, secrets, backups, or access. |
| Forbidden Action | An action the system must never perform. |
| Approval | Explicit permission from an authorized person before a Privileged Action. |
| Policy | Rules that define which actions are Safe, Privileged, High-Friction, or Forbidden. |
| Secret | Sensitive material such as a password, token, private key, recovery key, TOTP seed, or backup code. |
| Secret Reference | A pointer to where a Secret is stored, without including the Secret itself. |
| Lockout | A state where the Operator or trusted people lose access to systems they need. Steadlore House must not create lockout paths. |
| Remediation | An action intended to fix a problem. In v0, Remediation is guidance only, not autonomous execution. |

## System architecture

| Term | Meaning |
|---|---|
| Connector | A read-only integration that imports Facts from a source system. Connectors discover; they do not define household meaning. |
| Available Connector | A Connector that exists and is relevant to discovered or inventoried infrastructure. Do not advertise unavailable future connectors as user-facing suggestions. |
| Discovery Snapshot | A timestamped observational output from local discovery. It is not trusted Manual Inventory until reviewed. |
| Manual Inventory Draft | A review-required draft generated from Discovery Snapshot candidates to reduce blank-page work. It is not trusted Manual Inventory until edited and confirmed. |
| Manual Inventory | Human-authored structured Inventory, usually stored in YAML or another readable format. |
| Generated Manual | Markdown or other output produced from Inventory, Evidence, and Runbooks. |
| Renderer | Code that turns structured data into human-readable output. |
| Validator | Code that checks whether structured data is complete, coherent, and safe enough to use. |
| Conversation Interface | A way to ask questions, such as Telegram, CLI, web chat, or another UI. |
| Agent | A bounded software actor that may help interpret or guide, but must not bypass Policy. Use this term carefully. |
| Local-First | A design stance where core data and functionality remain available locally and do not require a cloud service. |

## Bounded contexts

### Inventory Context

Responsible for modeling Devices, Services, Locations, Dependencies, people, and Household Impact.

The Inventory Context should not perform live discovery or execute recovery actions.

### Evidence and Staleness Context

Responsible for modeling Source, Last Verified, Freshness Windows, stale state, confidence, and unknowns.

This context qualifies Facts. It does not decide household meaning.

### Infrastructure Map Context

Responsible for presenting the Operator-facing review surface that connects reviewed Inventory, rediscovery observations, promotion candidates, decommission candidates, unknowns/gaps, dependency graph, and trust state.

The Infrastructure Map must distinguish observed topology from household meaning.

### Continuity Manual Context

Responsible for generating readable documentation.

The manual must be useful without live connectors, chat interfaces, or LLMs.

### Runbook Context

Responsible for Symptoms, First Checks, Recovery Paths, escalation, and Forbidden Actions.

Runbooks should explain Household Impact.

### Policy Context

Responsible for classifying actions as Safe, Privileged, High-Friction, or Forbidden.

Policy must prevent Lockout and Secret exposure.

### Connector Context

Responsible for importing Facts from external systems.

Connectors discover. They do not define household meaning.

### Conversation Context

Responsible for surfacing existing knowledge through an interface.

Conversation is not the source of truth.

## Product Loop terms

| Term | Meaning |
|---|---|
| Product Loop | The review loop for shipping product increments. |
| Meta Loop | The slower loop for improving the development process. |
| Blocking Objection | A valid, jurisdiction-specific, evidence-grounded, material objection that prevents merge until resolved. |
| Consent Compiler | The role that mechanically applies merge/revise/reject/escalate rules. |
| Run Directory | A timestamped folder under `.loop/runs/` containing artifacts for one loop run. |

## Preferred term choices

Use:

- Stress User for the primary Continuity Manual reader under pressure.
- Helper Person for someone contacted by the Stress User.
- Trusted Person, not end user, family member, or customer when discussing safe access.
- Continuity Manual, not wiki, docs, binder, or knowledge base.
- Infrastructure Map, not First Map, when discussing the Operator-facing review/sense-making surface.
- AI Assistance Packet for chatbot-oriented renderings of the same source data.
- Fact, not data point, assertion, or claim unless discussing epistemology.
- Evidence, not metadata when Source and verification matter.
- Secret Reference, not secret, credential, or password pointer.
- Household Impact, not business impact.
- Forbidden Action, not dangerous thing.
- Unknown, not empty, missing, or null when discussing meaning.
- Available Connector only when the connector actually exists.

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
- future connector, in user-facing discovery output

These terms distort the product direction.

Use them only when explicitly discussing what the product is not.

## Naming mismatches to resolve

- First Map should be replaced by Infrastructure Map.
- Connector hints should not be user-facing unless they correspond to an existing connector. Prefer Available Connector once implemented.
- Docker-like dependencies should not be hidden as incidental Facts forever; use Runtime Service when they need to appear in dependency graphs.

## Terms needing future decisions

- Exact schema name for Visibility.
- Whether Runtime Service is represented as a service type, tag, role, or separate entity kind.
- Exact representation of Access Path.
- Exact rendering label for Lifecycle Conflicts.
