from __future__ import annotations

from datetime import UTC, datetime

from .dependency_graph import build_dependency_graph, render_dependency_graph_mermaid
from .models import Evidence, Fact, Inventory, Runbook
from .policy import POLICY_DEFINITIONS
from .staleness import age_in_days, is_stale


def render_manual(inventory: Inventory, runbooks: list[Runbook], *, now: datetime | None = None) -> str:
    current = now or datetime.now(UTC)
    sections: list[list[str]] = [
        [
            f"# {inventory.household_name} Continuity Manual",
            "",
            f"Generated: {current.astimezone(UTC).isoformat().replace('+00:00', 'Z')}",
            f"Audience: {inventory.generated_for}",
            "",
            "> This manual is a latest-known snapshot. It may be stale if Steadlore House could not detect recent breaking changes or failed generating or publishing a newer manual.",
        ],
        _render_start_here(runbooks),
        _render_safety_rules(),
        _render_runbooks(runbooks, inventory, current),
        _render_people(inventory),
        _render_secret_references(inventory),
        _render_services(inventory, current),
        _render_helper_section(runbooks, inventory, current),
    ]
    return _join_sections(sections)


def _join_sections(sections: list[list[str]]) -> str:
    chunks = ["\n".join(section).strip() for section in sections if section]
    return "\n\n".join(chunk for chunk in chunks if chunk).rstrip() + "\n"


def _render_people(inventory: Inventory) -> list[str]:
    lines = ["## Who Can Help", ""]
    if not inventory.people:
        lines.append("No people have been added yet. Add at least one Trusted Person so the manual can show escalation contacts if the primary operator is unavailable.")
    for person in sorted(inventory.people, key=lambda item: item.name):
        suffix = f" — {person.contact_hint}" if person.contact_hint else ""
        lines.append(f"- **{person.name}** ({person.role}){suffix}")
    lines.append("")
    return lines


def _render_start_here(runbooks: list[Runbook]) -> list[str]:
    lines = ["## Start Here", ""]
    lines.append("If something is not working, choose the closest symptom below. Do the safe checks only. Do not reset or unplug infrastructure unless this manual specifically says to, or a trusted technical helper asks you to.")
    lines.append("")
    if not runbooks:
        lines.append("No runbooks have been added yet. The manual can still describe reviewed household systems, but symptom-specific recovery guidance is not available.")
    else:
        lines.append("Common symptoms:")
        for runbook in sorted(runbooks, key=lambda item: item.symptom):
            lines.append(f"- {runbook.symptom}")
    lines.append("")
    return lines


def _render_safety_rules() -> list[str]:
    lines = ["## Safety Rules", ""]
    lines.append("Steadlore House uses deterministic policy rules for guidance. Safe checks are allowed for stressed household members; anything riskier requires escalation.")
    lines.append("")
    for action_class, description in POLICY_DEFINITIONS:
        label = action_class.replace("_", " ").title()
        lines.append(f"- **{label}:** {description}")
    lines.append("")
    return lines


def _render_services(inventory: Inventory, now: datetime) -> list[str]:
    lines = ["## Household Systems", ""]
    if not inventory.services:
        lines.append("No services have been added yet. Reviewed devices can still appear in the helper section, but household-facing service explanations are not available.")
        lines.append("")
        return lines
    for service in sorted(inventory.services, key=lambda item: item.name):
        importance = "High" if service.critical else "Normal"
        lines.append(f"### {service.name}")
        lines.append("")
        lines.append(service.plain_description)
        lines.append("")
        lines.append(f"Importance: {importance}")
        lines.append(f"If unavailable: {service.household_impact}")
        if service.access_endpoints:
            lines.append("")
            lines.append("Open here:")
            for endpoint in sorted(service.access_endpoints, key=lambda item: item.label):
                lines.append(f"- {endpoint.label}: `{endpoint.url}` {_render_evidence_plain(endpoint.evidence, now)}")
        lines.append("")
    return lines


def _render_devices(inventory: Inventory, now: datetime) -> list[str]:
    lines = ["### Devices", ""]
    if not inventory.devices:
        lines.append("No devices have been added yet.")
        lines.append("")
        return lines
    for device in sorted(inventory.devices, key=lambda item: item.name):
        lines.append(f"#### {device.name}")
        lines.append("")
        lines.append(f"Type: {device.device_type}")
        lines.append(f"Core infrastructure: {'Yes' if device.core_infrastructure else 'No'}")
        lines.append(f"Location: {device.location}")
        lines.append(f"Household Impact: {device.household_impact}")
        lines.extend(_render_facts(device.facts, now))
        lines.append("")
    return lines


def _render_facts(facts: list[Fact], now: datetime) -> list[str]:
    if not facts:
        return []
    lines = ["", "Facts:"]
    for fact in sorted(facts, key=lambda item: item.text):
        lines.append(f"- {fact.text} {_render_evidence(fact.evidence, now)}")
    return lines


def _render_evidence_plain(evidence: Evidence, now: datetime) -> str:
    age = age_in_days(evidence.last_verified, now=now)
    if is_stale(evidence.last_verified, evidence.freshness_days, now=now):
        return f"(last checked {age} days ago; this may be outdated)"
    return f"(last checked {age} days ago)"


def _render_evidence(evidence: Evidence, now: datetime) -> str:
    age = age_in_days(evidence.last_verified, now=now)
    stale_label = "STALE" if is_stale(evidence.last_verified, evidence.freshness_days, now=now) else "current"
    return (
        f"[{stale_label}; source: {evidence.source}; status: {evidence.status}; "
        f"confidence: {evidence.confidence}; last verified: {evidence.last_verified}; age: {age} days; "
        f"freshness window: {evidence.freshness_days} days]"
    )


def _render_secret_references(inventory: Inventory) -> list[str]:
    lines = ["## Where Access Information Is Stored", ""]
    lines.append("No passwords or recovery keys are stored in this manual. These entries only say where the household expects access information to be kept.")
    lines.append("")
    for reference in sorted(inventory.secret_references, key=lambda item: item.label):
        parts = [f"system: {reference.system}"]
        if reference.vault:
            parts.append(f"vault: {reference.vault}")
        if reference.item:
            parts.append(f"item: {reference.item}")
        if reference.physical_hint:
            parts.append(f"physical hint: {reference.physical_hint}")
        if reference.responsible_person:
            parts.append(f"responsible person: {reference.responsible_person}")
        lines.append(f"- **{reference.label}** ({'; '.join(parts)})")
    lines.append("")
    return lines


def _render_runbooks(runbooks: list[Runbook], inventory: Inventory, now: datetime) -> list[str]:
    lines = ["## Common Problems", ""]
    if not runbooks:
        lines.append("No symptom runbooks have been added yet.")
        lines.append("")
        return lines
    service_by_id = {service.id: service for service in inventory.services}
    for runbook in sorted(runbooks, key=lambda item: item.symptom):
        lines.append(f"### {runbook.symptom}")
        lines.append("")
        lines.append("What this usually means:")
        lines.append(f"- {runbook.plain_summary}")
        lines.append("")
        if runbook.probably_still_ok:
            lines.append("What is probably still okay:")
            for item in runbook.probably_still_ok:
                lines.append(f"- {item}")
            lines.append("")
        lines.append(f"Household impact: {runbook.household_impact}")
        lines.append("")
        if runbook.temporary_workarounds:
            lines.append("What you can do meanwhile:")
            for item in runbook.temporary_workarounds:
                lines.append(f"- {item}")
            lines.append("")
        endpoints = []
        for service_id in runbook.applies_to:
            service = service_by_id.get(service_id)
            if service:
                endpoints.extend(service.access_endpoints)
        if endpoints:
            lines.append("Useful links to try:")
            for endpoint in sorted(endpoints, key=lambda item: item.label):
                lines.append(f"- {endpoint.label}: `{endpoint.url}` {_render_evidence_plain(endpoint.evidence, now)}")
            lines.append("")
        lines.append("Safe checks:")
        for check in runbook.first_checks:
            lines.append(f"- {check.text}")
        lines.append("")
        lines.append("What not to touch:")
        for item in runbook.do_not_touch:
            lines.append(f"- {item}")
        lines.append("")
        lines.append("Who to contact or what to do next:")
        for item in runbook.escalation_path:
            lines.append(f"- {item}")
        lines.append("")
    return lines


def _render_helper_section(runbooks: list[Runbook], inventory: Inventory, now: datetime) -> list[str]:
    lines = ["## For Helper Persons", ""]
    lines.append("This section is for someone contacted by the stressed household member. It may use technical terms, but it still must not bypass safety guidance or expose secrets.")
    lines.append("")

    helper_notes = [runbook for runbook in sorted(runbooks, key=lambda item: item.symptom) if runbook.helper_note]
    if helper_notes:
        lines.append("### Symptom Notes")
        lines.append("")
        for runbook in helper_notes:
            lines.append(f"- **{runbook.symptom}:** {runbook.helper_note}")
        lines.append("")

    lines.extend(_render_dependency_graph(inventory, now))
    lines.extend(_render_service_facts(inventory, now))
    lines.extend(_render_devices(inventory, now))
    return lines


def _render_dependency_graph(inventory: Inventory, now: datetime) -> list[str]:
    mermaid = render_dependency_graph_mermaid(build_dependency_graph(inventory, now=now))
    if not mermaid:
        return []
    return [
        "### Dependency Graph",
        "",
        "This graph shows reviewed Manual Inventory dependencies. It is latest-known structure, not live monitoring or remediation guidance.",
        "",
        mermaid,
        "",
    ]


def _render_service_facts(inventory: Inventory, now: datetime) -> list[str]:
    services_with_facts = [service for service in sorted(inventory.services, key=lambda item: item.name) if service.facts]
    if not services_with_facts:
        return []
    lines = ["### Service Evidence", ""]
    for service in services_with_facts:
        lines.append(f"#### {service.name}")
        lines.extend(_render_facts(service.facts, now))
        lines.append("")
    return lines
