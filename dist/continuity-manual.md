# Example Household Continuity Manual

Generated: 2026-05-02T14:21:53.860265Z
Audience: trusted people and operators

> This manual is a latest-known snapshot. It may be stale if Steadlore House could not detect recent breaking changes or failed generating or publishing a newer manual.

## Start Here

If something is not working, choose the closest symptom below. Do the safe checks only. Do not reset or unplug infrastructure unless this manual specifically says to, or a trusted technical helper asks you to.

Common symptoms:
- Lights or automations are not working

## Safety Rules

Steadlore House uses deterministic policy rules for guidance. Safe checks are allowed for stressed household members; anything riskier requires escalation.

- **Safe:** Read-only or low-risk observations a Stress User may perform without special approval.
- **Privileged:** Changes to services, containers, hosts, software, or configuration requiring explicit approval.
- **High Friction:** Privileged changes to core infrastructure, identity, secrets, backups, or access that could cause lockout.
- **Forbidden:** Actions that expose secrets, delete critical data, or create unacceptable safety or lockout risk.

## Common Problems

### Lights or automations are not working

What this usually means:
- The household smart-home control system may be unavailable. This can affect app controls, dashboards, automations, and sensors. Physical wall switches may still work.

What is probably still okay:
- Internet and Wi-Fi are not necessarily affected.
- Physical wall switches may still control many lights.
- This is usually inconvenient, not dangerous.

Household impact: Some convenience automations and dashboards may be unavailable. Treat this as a smart-home problem first, not as a whole-house infrastructure failure.

What you can do meanwhile:
- Use physical wall switches for lights until smart-home controls are restored.
- Keep using normal internet and Wi-Fi if they are working.
- Do not change automations or smart-home settings while waiting for help.

Useful links to try:
- Home Assistant dashboard: `http://homeassistant.local:8123` (last checked 12 days ago)

Safe checks:
- Try the physical wall switch for the affected light.
- Check whether ordinary internet browsing works on a device already connected to the household Wi-Fi.
- Try opening the Home Assistant dashboard link in this section.

What not to touch:
- Do not reset the gateway, switches, or Wi-Fi access points while investigating this symptom.
- Do not delete containers, volumes, backups, or configuration files.
- Do not change firewall, DNS, VLAN, identity-provider, or password-manager settings.

Who to contact or what to do next:
- If physical switches work and only automations are unavailable, wait for the operator if that is realistic. If the operator is unavailable, contact the trusted helper listed in this manual.
- If internet or Wi-Fi also appear unavailable, use the separate internet or Wi-Fi runbook when one exists. Do not assume this smart-home symptom is the cause.
- Secret references identify where access information is kept; this manual does not contain passwords or recovery keys.

## Who Can Help

- **Primary Operator** (Operator) — Use normal family contact methods.
- **Trusted Helper** (Trusted Person) — Contact if the primary operator is unavailable.

## Where Access Information Is Stored

No passwords or recovery keys are stored in this manual. These entries only say where the household expects access information to be kept.

- **Home Assistant admin access** (system: 1Password; vault: Household Shared; item: Home Assistant; responsible person: Primary Operator)
- **House server console access** (system: 1Password; vault: Household Shared; item: House Server 01; responsible person: Primary Operator)

## Household Systems

### Home Assistant

Home Assistant is the household smart-home control system. It helps with lights, automations, sensors, and dashboards.

Importance: High
If unavailable: Some lights, automations, sensors, and dashboards may not work. Internet and Wi-Fi are not necessarily affected.

Open here:
- Home Assistant dashboard: `http://homeassistant.local:8123` (last checked 12 days ago)

## For Helper Persons

This section is for someone contacted by the stressed household member. It may use technical terms, but it still must not bypass safety guidance or expose secrets.

### Symptom Notes

- **Lights or automations are not working:** Home Assistant may not have returned correctly after container maintenance. Check container status and logs before any restart or rollback. A restart is not a first check for a stressed household member.

### Service Evidence

#### Home Assistant

Facts:
- Home Assistant is managed as a container named homeassistant. [current; source: manual inventory; status: manually_confirmed; confidence: medium; last verified: 2026-04-20T12:00:00Z; age: 12 days; freshness window: 14 days]
- Home Assistant provides convenience automations, not the primary internet connection. [current; source: operator note; status: manually_confirmed; confidence: high; last verified: 2026-04-15T12:00:00Z; age: 17 days; freshness window: 90 days]

### Devices

#### House Server 01

Type: Host
Location: Utility cabinet shelf
Household Impact: Runs household services. If unavailable, some local services may stop, but internet and Wi-Fi are not automatically affected. Do not unplug or reset this device unless a trusted technical helper asks you to.

Facts:
- Home Assistant is expected to run on this host as a container. [STALE; source: manual inventory; status: manually_confirmed; confidence: high; last verified: 2026-01-15T10:00:00Z; age: 107 days; freshness window: 30 days]
