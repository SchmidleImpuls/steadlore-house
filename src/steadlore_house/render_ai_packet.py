from __future__ import annotations

from datetime import UTC, datetime

from .models import Evidence, Inventory, Runbook
from .staleness import age_in_days, is_stale


def render_ai_packet(inventory: Inventory, runbooks: list[Runbook], *, now: datetime | None = None) -> str:
    """Render a redacted Markdown packet for a chatbot assisting a Stress User."""
    current = now or datetime.now(UTC)
    lines: list[str] = []
    lines.append(f"# {inventory.household_name} AI Assistance Packet")
    lines.append("")
    lines.append(f"Generated: {current.astimezone(UTC).isoformat().replace('+00:00', 'Z')}")
    lines.append("")
    lines.append("## Instructions for the chatbot")
    lines.append("")
    lines.extend(
        [
            "- You are helping a stressed household member understand this packet and perform safe checks only.",
            "- Use a calm tone. The emotional posture is: We have prepared for this.",
            "- Use only the facts in this packet. Do not invent missing facts.",
            "- Treat stale facts as possibly outdated and say so clearly.",
            "- Prefer 'consistent with' or 'the latest-known information suggests' over certainty about root causes.",
            "- Always surface temporary workarounds before escalation.",
            "- Do not imply the Primary Operator is available. If the Primary Operator is unavailable, direct the household member to a Helper Person.",
            "- Do not ask for passwords, tokens, recovery keys, private keys, TOTP seeds, backup codes, or credential exports.",
            "- Do not suggest resetting gateways, switches, Wi-Fi access points, firewall rules, DNS, VLANs, identity providers, password-manager access, backups, containers, volumes, or configuration files.",
            "- Do not suggest privileged or high-friction actions as first checks.",
            "- If privileged action seems necessary, tell the household member to contact a Helper Person listed in this packet.",
            "- Start from the user-visible symptom, not from a guessed root cause.",
        ]
    )
    lines.append("")
    lines.extend(_render_suggested_first_response(runbooks))
    lines.extend(_render_safety_policy(runbooks))
    lines.extend(_render_symptoms(runbooks, inventory, current))
    lines.extend(_render_people(inventory))
    lines.extend(_render_access_references(inventory))
    lines.extend(_render_facts(inventory, current))
    lines.extend(_render_unknowns())
    return "\n".join(lines).rstrip() + "\n"


def _render_suggested_first_response(runbooks: list[Runbook]) -> list[str]:
    lines = ["## Suggested first response", ""]
    symptoms = ", ".join(sorted(runbook.symptom for runbook in runbooks))
    lines.append(
        "Tell the household member: I can help you use the Steadlore House continuity information. "
        "Choose the closest symptom, then I will walk you through safe checks only."
    )
    if symptoms:
        lines.append(f"Known symptoms in this packet: {symptoms}.")
    lines.append("")
    return lines


def _render_safety_policy(runbooks: list[Runbook]) -> list[str]:
    lines = ["## Safety policy", ""]
    lines.append("Safe checks allowed:")
    for check in sorted({check.text for runbook in runbooks for check in runbook.first_checks}):
        lines.append(f"- {check}")
    lines.append("")
    lines.append("Do not suggest these actions:")
    for item in sorted({item for runbook in runbooks for item in runbook.do_not_touch}):
        lines.append(f"- {item}")
    lines.append("")
    return lines


def _render_symptoms(runbooks: list[Runbook], inventory: Inventory, now: datetime) -> list[str]:
    lines = ["## Symptom runbooks", ""]
    service_by_id = {service.id: service for service in inventory.services}
    for runbook in sorted(runbooks, key=lambda item: item.symptom):
        lines.append(f"### Symptom: {runbook.symptom}")
        lines.append("")
        lines.append(f"Plain summary: {runbook.plain_summary}")
        lines.append(f"Household impact: {runbook.household_impact}")
        if runbook.probably_still_ok:
            lines.append("Probably still okay:")
            for item in runbook.probably_still_ok:
                lines.append(f"- {item}")
        if runbook.temporary_workarounds:
            lines.append("Temporary workarounds to surface before escalation:")
            for item in runbook.temporary_workarounds:
                lines.append(f"- {item}")
        endpoints = []
        for service_id in runbook.applies_to:
            service = service_by_id.get(service_id)
            if service:
                endpoints.extend(service.access_endpoints)
        if endpoints:
            lines.append("Useful endpoints:")
            for endpoint in sorted(endpoints, key=lambda item: item.label):
                lines.append(f"- {endpoint.label}: {endpoint.url} {_render_evidence(endpoint.evidence, now)}")
        lines.append("Escalate if safe checks do not resolve the situation or if privileged action seems necessary.")
        if runbook.helper_note:
            lines.append(f"Helper context: {runbook.helper_note}")
        lines.append("")
    return lines


def _render_people(inventory: Inventory) -> list[str]:
    lines = ["## People", ""]
    for person in sorted(inventory.people, key=lambda item: item.name):
        contact = f"; contact hint: {person.contact_hint}" if person.contact_hint else ""
        lines.append(f"- {person.name}; role: {person.role}{contact}")
    lines.append("")
    return lines


def _render_access_references(inventory: Inventory) -> list[str]:
    lines = ["## Secret references", ""]
    lines.append("No secrets are included. These entries only describe where access information is expected to be stored.")
    for reference in sorted(inventory.secret_references, key=lambda item: item.label):
        parts = [f"label: {reference.label}", f"system: {reference.system}"]
        if reference.vault:
            parts.append(f"vault: {reference.vault}")
        if reference.item:
            parts.append(f"item: {reference.item}")
        if reference.physical_hint:
            parts.append(f"physical hint: {reference.physical_hint}")
        if reference.responsible_person:
            parts.append(f"responsible person: {reference.responsible_person}")
        lines.append(f"- {'; '.join(parts)}")
    lines.append("")
    return lines


def _render_facts(inventory: Inventory, now: datetime) -> list[str]:
    lines = ["## Facts with evidence", ""]
    for service in sorted(inventory.services, key=lambda item: item.name):
        lines.append(f"### Service: {service.name}")
        lines.append(f"Description: {service.plain_description}")
        lines.append(f"Household impact if unavailable: {service.household_impact}")
        for fact in sorted(service.facts, key=lambda item: item.text):
            lines.append(f"- Fact: {fact.text} {_render_evidence(fact.evidence, now)}")
        lines.append("")
    for device in sorted(inventory.devices, key=lambda item: item.name):
        lines.append(f"### Device: {device.name}")
        lines.append(f"Type: {device.device_type}")
        lines.append(f"Location: {device.location}")
        lines.append(f"Household impact: {device.household_impact}")
        for fact in sorted(device.facts, key=lambda item: item.text):
            lines.append(f"- Fact: {fact.text} {_render_evidence(fact.evidence, now)}")
        lines.append("")
    return lines


def _render_unknowns() -> list[str]:
    return [
        "## Unknowns the chatbot must not invent",
        "",
        "- Whether any service is currently running.",
        "- Whether recent maintenance or a breaking change occurred.",
        "- Whether internet or Wi-Fi are currently working.",
        "- Any password, token, recovery key, private key, TOTP seed, or backup code.",
        "",
    ]


def _render_evidence(evidence: Evidence, now: datetime) -> str:
    stale = is_stale(evidence.last_verified, evidence.freshness_days, now=now)
    return (
        f"[stale: {str(stale).lower()}; source: {evidence.source}; status: {evidence.status}; "
        f"confidence: {evidence.confidence}; last_verified: {evidence.last_verified}; "
        f"age_days: {age_in_days(evidence.last_verified, now=now)}; freshness_days: {evidence.freshness_days}]"
    )
