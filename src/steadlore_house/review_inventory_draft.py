from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

from .validation import reject_secret_fields, validate_inventory_data

Prompt = Callable[[str], str]
Output = Callable[[str], None]


class InventoryDraftReviewError(ValueError):
    """Raised when an inventory draft cannot be reviewed safely."""


def load_inventory_draft(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise InventoryDraftReviewError(f"Expected a mapping in {path}")
    reject_secret_fields(data, path=str(path))
    validate_inventory_data(data, path=str(path))
    return data


def render_reviewed_inventory(data: dict[str, Any]) -> str:
    cleaned = _clean_review_metadata(data)
    validate_inventory_data(cleaned, path="reviewed inventory")
    return yaml.safe_dump(cleaned, sort_keys=False, allow_unicode=True, width=120).rstrip() + "\n"


def review_inventory_draft_interactive(
    data: dict[str, Any],
    *,
    prompt: Prompt = input,
    output: Output = print,
) -> dict[str, Any]:
    """Interactively promote or skip candidate devices from an inventory draft."""
    reviewed: dict[str, Any] = {
        "household_name": _ask_required(prompt, "Household name", str(data.get("household_name") or "Draft Household")),
        "generated_for": str(data.get("generated_for") or "household members and trusted persons"),
        "people": _review_people(data.get("people", []), prompt=prompt, output=output),
        "devices": [],
        "services": data.get("services", []),
        "secret_references": data.get("secret_references", []),
    }

    for device in data.get("devices", []):
        if not isinstance(device, dict):
            continue
        review = device.get("_review") if isinstance(device.get("_review"), dict) else {}
        _print_candidate(device, review, output)
        promote_default = bool(device.get("core_infrastructure", False))
        if not _ask_yes_no(prompt, "Promote this candidate to Manual Inventory?", default=promote_default):
            output("Skipped candidate.\n")
            continue
        promoted = _promote_device(device, prompt=prompt)
        reviewed["devices"].append(promoted)
        output(f"Promoted {promoted['id']}.\n")

    validate_inventory_data(reviewed, path="reviewed inventory")
    return reviewed


def _promote_device(device: dict[str, Any], *, prompt: Prompt) -> dict[str, Any]:
    default_id = _stable_id(str(device.get("id") or "device"))
    promoted = {
        "id": _ask_id(prompt, "Device ID", default_id),
        "name": _ask_required(prompt, "Name", str(device.get("name") or "Unnamed device")),
        "device_type": _ask_required(prompt, "Device type", str(device.get("device_type") or "Unknown")),
        "core_infrastructure": _ask_yes_no(prompt, "Core infrastructure?", default=bool(device.get("core_infrastructure", False))),
        "location": _ask_reviewed(prompt, "Location", str(device.get("location") or "Unknown")),
        "household_impact": _ask_reviewed(prompt, "Household impact", str(device.get("household_impact") or "Unknown")),
        "facts": device.get("facts", []),
    }
    return promoted


def _clean_review_metadata(data: dict[str, Any]) -> dict[str, Any]:
    cleaned = {key: value for key, value in data.items() if not key.startswith("_draft")}
    cleaned_devices = []
    for device in cleaned.get("devices", []):
        if isinstance(device, dict):
            cleaned_devices.append({key: value for key, value in device.items() if key != "_review"})
    cleaned["devices"] = cleaned_devices
    return cleaned


def _print_candidate(device: dict[str, Any], review: dict[str, Any], output: Output) -> None:
    output("Candidate device")
    output(f"  Current ID: {device.get('id', 'unknown')}")
    output(f"  Name: {device.get('name', 'unknown')}")
    if review.get("ip_address"):
        output(f"  IP address: {review['ip_address']}")
    if review.get("vendor"):
        output(f"  Vendor: {review['vendor']}")
    if review.get("reasons"):
        output(f"  Reasons: {', '.join(str(item) for item in review['reasons'])}")
    if review.get("connector_hints"):
        output(f"  Connector hints: {', '.join(str(item) for item in review['connector_hints'])}")
    output(f"  Suggested type: {device.get('device_type', 'Unknown')}")
    output(f"  Suggested core infrastructure: {bool(device.get('core_infrastructure', False))}")
    output(f"  Suggested household impact: {device.get('household_impact', 'Unknown')}")


def _review_people(people: Any, *, prompt: Prompt, output: Output) -> list[dict[str, Any]]:
    reviewed = [person for person in people if isinstance(person, dict)] if isinstance(people, list) else []
    if reviewed:
        output(f"People already in draft: {len(reviewed)}")
    output("People are used later in the Continuity Manual as trusted people and escalation contacts. Add people who should be contacted if the primary operator is unavailable.")
    while _ask_yes_no(prompt, "Add a person now?", default=not reviewed):
        default_id = f"person-{len(reviewed) + 1}"
        name = _ask_required(prompt, "Person name", "Trusted Helper" if not reviewed else f"Trusted Helper {len(reviewed) + 1}")
        reviewed.append(
            {
                "id": _ask_id(prompt, "Person ID", _stable_id(name) or default_id),
                "name": name,
                "role": _ask_required(prompt, "Role", "Trusted Person"),
                "contact_hint": _ask_required(prompt, "Contact hint", "Use normal family contact methods."),
            }
        )
    return reviewed



def _ask_yes_no(prompt: Prompt, label: str, *, default: bool) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        answer = prompt(f"{label} {suffix}: ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer yes or no.")


def _ask_required(prompt: Prompt, label: str, default: str) -> str:
    while True:
        answer = prompt(f"{label} [{default}]: ").strip()
        value = answer or default
        if value:
            return value
        print(f"{label} is required.")


def _ask_reviewed(prompt: Prompt, label: str, default: str) -> str:
    while True:
        value = _ask_required(prompt, label, default)
        if value.strip().lower().startswith("unknown"):
            print(f"{label} must be reviewed; do not leave it as Unknown.")
            continue
        if "review required" in value.lower():
            print(f"{label} must be reviewed; remove review-required placeholder text.")
            continue
        return value


def _ask_id(prompt: Prompt, label: str, default: str) -> str:
    while True:
        value = _ask_required(prompt, label, default)
        stable = _stable_id(value)
        if value != stable:
            print(f"Use lowercase letters, numbers, and hyphens. Suggested: {stable}")
            default = stable
            continue
        return value


def _stable_id(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return normalized or "device"
