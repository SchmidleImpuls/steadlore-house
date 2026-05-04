# Product Vision

## Core idea

Steadlore House exists for households where important operational knowledge lives in one person’s head.

It answers a quiet but serious question:

> What happens if that person is unavailable?

The answer should not be panic, dependence, or a pile of unlabeled boxes.

The answer should be:

> We have prepared for this.

## Promise

If something happens, the house still knows how it works.

## Product identity

Steadlore is the continuity brand.

Steadlore House is the first product: a local-first household continuity system for homes where household infrastructure has grown beyond a single modem/gateway/access-point and other household members depend on one Operator’s knowledge.

The first target is the maintainer’s own household. External target users are Operators who are asking:

> How will other household members understand and recover from this when I am unavailable?

Steadlore House is not about showing off a clever homelab. It is about protecting the people who depend on one.

## Why this matters

Modern homes increasingly depend on fragile, invisible systems:

- internet uplinks
- Wi-Fi
- smart-home controllers
- security cameras
- local servers
- media systems
- password managers
- vendor accounts
- automations
- cloud subscriptions
- self-hosted services
- local AI infrastructure

These systems are often maintained by one technically capable person.

That person may have everything in their head:

- what each box is for
- which cable matters
- which service controls which device
- where credentials live
- who to call
- what not to touch
- what is safe to restart
- what would make things worse

This is not resilience. It is hidden dependency.

Steadlore House turns that hidden dependency into shared, structured, stale-aware household knowledge.

## Emotional posture

Steadlore House should feel:

- calm
- competent
- reassuring
- quietly premium
- human
- non-geeky
- prepared without being paranoid

It should not feel like disaster prep, enterprise compliance, smart-home gadgetry, or AI hype.

The product should whisper:

> We’ve got this.

Steadlore House prepares for extended Operator unavailability without centering death as the product frame. Illness, travel, overwhelm, incapacity, absence, and death are all possible reasons the Operator may be unavailable.

## First product shape

Steadlore House begins with two related local-first artifacts:

- **Infrastructure Map:** the Operator-facing setup and review surface that makes discovered and reviewed household infrastructure understandable.
- **Continuity Manual:** the Stress User-first household continuity artifact that explains what to do when something breaks or the Operator is unavailable.

The Continuity Manual remains the first useful household continuity artifact.

The Infrastructure Map is the first Operator setup value surface. It helps the Operator distinguish load-bearing infrastructure from irrelevant clients, review discovered candidates, expose unknowns, and reduce single-point-of-failure risk.

The Operator should be able to feel:

> My house is finally documented in a way that I am less of a single point of failure.

The phrase **in a way** matters. Steadlore House must understand technical infrastructure while translating it into calm, non-technobabble guidance for Stress Users.

## First concrete scenario

The first scenario is:

> Lights or automations are not working.

A possible technical cause may be that Home Assistant is unavailable after maintenance, but the Stress User should not need to know that root cause to begin safely.

This scenario is intentionally specific.

It forces the project to model:

- a Service
- a Runtime Service or Container relationship
- a Host
- Household Impact
- privileged access
- Secret References
- stale information
- safe checks
- Forbidden Actions
- escalation to a Helper Person

If Steadlore House cannot handle one real scenario well, it has no business pretending to manage a household.

## Manual audience

The Continuity Manual primarily serves a Stress User: a potentially stressed Trusted Person who notices that something is wrong and needs calm, safe guidance.

The manual secondarily serves a Helper Person contacted by that Stress User. Helper-facing details may be more technical, but they must not obscure the Stress User path.

The manual explains:

- what symptom the household member may be seeing
- what the symptom usually means in household terms
- what is probably still okay
- what is safe to check
- what must not be touched
- who can help
- where Secret References point
- how old the information is
- what exists
- what matters
- where things are
- how things depend on each other

The manual may include technical appendices, such as an Infrastructure Map, for Helper Persons and Operators. Stress User guidance must remain symptom-first and calm.

The manual must be useful even when the agent, chat interface, live connectors, or network are unavailable.

## Long-term direction

Steadlore House may eventually grow from a manual and Infrastructure Map into a supervised self-maintenance layer for household infrastructure.

That future may include:

- read-only connectors
- health checks
- dependency maps
- local web UI
- Telegram or chat interfaces
- guided diagnostics
- runbook improvement loops
- approval-based remediation
- policy-checked actions
- local AI support
- fleet-aware infrastructure guidance

But the progression matters.

The system must earn autonomy through clarity, evidence, tests, policy, and trust.

## AI stance

AI is not the product.

Continuity is the product.

AI may help explain, summarize, classify, draft, or guide. It must not become a charming shortcut around truth, safety, or structure.

The system should not say “I fixed it” unless deterministic tools performed a known action and verified the result.

The system should not guess when it does not know.

The system should say:

> The latest verified data says this, but it is old.

That honesty is a feature.

## Accepted strategy decisions

- YAML remains the canonical local source of truth.
- The GUI may edit YAML, and advanced Operators may edit YAML directly.
- The dependency graph model is the next strategic milestone before GUI work.
- Mermaid is the first dependency graph rendering format.
- The dependency graph should appear in both the Continuity Manual and Infrastructure Map.
- The local web UI should initially bind to localhost.
- CLI and web app should share deterministic Python application modules.
- Connector suggestions should only appear for connectors that actually exist, using the language **Available Connector**.

## Reversible bets

- A local web UI should become near-term because infrequent maintenance makes CLI-only workflows hard to remember.
- Generic `depends_on` relationships can carry enough graph value before typed dependency edges are needed.
- A Markdown Infrastructure Map can validate product value before GUI implementation.
- Configurable periodic rediscovery and Operator reminders can reduce staleness without becoming surveillance or monitoring.

## Hard-to-reverse risks

- Turning Steadlore House into a generic smart-home, monitoring, or remediation platform would damage the product identity.
- Adding broad connector or GUI complexity before the manual, evidence, and dependency model are coherent would create lasting architecture debt.
- Exposing a future web UI beyond localhost without clear access control would create security and privacy risk.
- Expanding into Steadlore Life, estate, insurance, pension, mortgage, inheritance, or legal continuity would be a different product and is out of scope now.

## North star

Steadlore House succeeds when a technically complex home becomes understandable, recoverable, and less dependent on one person’s memory.

Not because the house became fully autonomous.

Because the household became prepared.
