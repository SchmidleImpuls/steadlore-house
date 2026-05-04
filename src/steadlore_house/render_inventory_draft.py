from __future__ import annotations

import uuid
from typing import Any

import yaml

from .network_discovery import NetworkSnapshot
from .render_network_snapshot import Candidate, core_infrastructure_candidates


def render_inventory_draft(snapshot: NetworkSnapshot) -> str:
    """Render a review-required Manual Inventory draft from discovery candidates."""
    candidates = core_infrastructure_candidates(snapshot)
    data: dict[str, Any] = {
        "_draft_notice": "Draft only. Review before using as Manual Inventory. Discovery candidates do not confirm role, location, owner, or Household Impact.",
        "household_name": "Draft Household",
        "generated_for": "household members and trusted persons",
        "people": [],
        "devices": [_device_from_candidate(candidate, snapshot) for candidate in candidates],
        "services": [],
        "secret_references": [],
    }
    rendered = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)
    return rendered.rstrip() + "\n"


def _device_from_candidate(candidate: Candidate, snapshot: NetworkSnapshot) -> dict[str, Any]:
    return {
        "id": _candidate_id(candidate.ip_address),
        "name": _suggest_name(candidate),
        "device_type": _suggest_device_type(candidate),
        "core_infrastructure": _is_core_candidate(candidate),
        "location": "Unknown",
        "household_impact": _suggest_household_impact(candidate),
        "_review": _review_metadata(candidate),
        "facts": _facts_from_candidate(candidate, snapshot),
    }


def _review_metadata(candidate: Candidate) -> dict[str, Any]:
    data: dict[str, Any] = {
        "candidate": True,
        "promotion_required": True,
        "ip_address": candidate.ip_address,
        "reasons": list(candidate.reasons),
        "suggested_device_type": _suggest_device_type(candidate),
        "suggested_core": _is_core_candidate(candidate),
        "fields_to_review": ["id", "name", "device_type", "core_infrastructure", "location", "household_impact"],
    }
    if candidate.mac_address:
        data["mac_address"] = candidate.mac_address
    if candidate.vendor:
        data["vendor"] = candidate.vendor
    return data


def _facts_from_candidate(candidate: Candidate, snapshot: NetworkSnapshot) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = [
        {
            "text": f"Observed {candidate.ip_address} as {', '.join(candidate.reasons)}.",
            "evidence": _evidence(snapshot, source="network discovery snapshot", confidence="low"),
        }
    ]
    if candidate.mac_address:
        facts.append(
            {
                "text": f"Observed MAC address {candidate.mac_address} for {candidate.ip_address}.",
                "evidence": _evidence(snapshot, source="network discovery snapshot", confidence="low"),
            }
        )
    if candidate.vendor:
        facts.append(
            {
                "text": f"Offline MAC vendor lookup suggests {candidate.vendor} for {candidate.ip_address}.",
                "evidence": _evidence(snapshot, source=_vendor_source(snapshot), confidence="low"),
            }
        )
    return facts


def _suggest_name(candidate: Candidate) -> str:
    if "default gateway candidate" in candidate.reasons:
        return f"Gateway candidate {candidate.ip_address}"
    if "DNS server candidate" in candidate.reasons:
        return f"DNS server candidate {candidate.ip_address}"
    if candidate.vendor:
        return f"{candidate.vendor} candidate {candidate.ip_address}"
    return f"Candidate device {candidate.ip_address}"


def _suggest_device_type(candidate: Candidate) -> str:
    vendor = (candidate.vendor or "").lower()
    if "default gateway candidate" in candidate.reasons:
        return "Gateway"
    if "DNS server candidate" in candidate.reasons:
        return "Network Device"
    if "synology" in vendor:
        return "NAS"
    if "qnap" in vendor:
        return "NAS"
    if "raspberry pi" in vendor:
        return "Host"
    if "sonos" in vendor:
        return "Smart Speaker"
    if "shelly" in vendor or "espressif" in vendor:
        return "Smart Home Device"
    if "ubiquiti" in vendor:
        return "Network Device"
    return "Unknown"


def _is_core_candidate(candidate: Candidate) -> bool:
    return bool({"default gateway candidate", "DNS server candidate"} & set(candidate.reasons))


def _suggest_household_impact(candidate: Candidate) -> str:
    if "default gateway candidate" in candidate.reasons and "DNS server candidate" in candidate.reasons:
        return (
            "Likely core network infrastructure. If unavailable, internet access, local routing, and local name resolution may be affected. Review required."
        )
    if "default gateway candidate" in candidate.reasons:
        return "Likely core network infrastructure. If unavailable, internet access and local routing may be affected. Review required."
    if "DNS server candidate" in candidate.reasons:
        return "Likely core network infrastructure. If unavailable, local name resolution may be affected. Review required."
    return "Unknown. Review required before this candidate is used as trusted Manual Inventory."


def _evidence(snapshot: NetworkSnapshot, *, source: str, confidence: str) -> dict[str, Any]:
    return {
        "source": source,
        "last_verified": snapshot.observed_at.isoformat().replace("+00:00", "Z"),
        "freshness_days": 7,
        "status": "discovered",
        "confidence": confidence,
    }


def _vendor_source(snapshot: NetworkSnapshot) -> str:
    for item in snapshot.evidence:
        if item.startswith("MAC vendor enrichment:"):
            return item
    return "offline MAC vendor lookup"


def _candidate_id(ip_address: str) -> str:
    return f"device-{uuid.uuid5(uuid.NAMESPACE_URL, f'steadlore-house:network-candidate:{ip_address}')!s}"
