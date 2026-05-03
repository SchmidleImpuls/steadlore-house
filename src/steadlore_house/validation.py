from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any
from urllib.parse import urlparse

from .policy import classify_action, is_stricter_or_equal
from .staleness import parse_utc

SECRET_FIELD_NAMES = {
    "password",
    "passphrase",
    "token",
    "api_key",
    "apikey",
    "secret",
    "private_key",
    "recovery_key",
    "totp_seed",
    "backup_code",
}

VALID_EVIDENCE_STATUSES = {"known", "unknown", "inferred", "manually_confirmed", "discovered"}
VALID_ACTION_CLASSES = {"safe", "privileged", "high_friction", "forbidden"}
ROOT_CAUSE_TITLE_TERMS = {
    "container",
    "redeploy",
    "deployment",
    "maintenance",
    "docker",
    "portainer",
    "host reboot",
    "service restart",
    "after update",
    "after upgrade",
    "unavailable after",
}

class ValidationError(ValueError):
    """Raised when input data is unsafe or invalid."""


def reject_secret_fields(value: Any, *, path: str = "root") -> None:
    """Reject raw secret-looking fields in structured input.

    Secret References are allowed as explicit objects, but raw secret fields are
    not allowed in inventory, runbooks, examples, tests, or generated output.
    """
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key)
            normalized = key_text.lower().replace("-", "_")
            child_path = f"{path}.{key_text}"
            if normalized in SECRET_FIELD_NAMES:
                raise ValidationError(f"Raw secret field is not allowed: {child_path}")
            reject_secret_fields(child, path=child_path)
        return

    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        for index, child in enumerate(value):
            reject_secret_fields(child, path=f"{path}[{index}]")


def validate_inventory_data(data: Mapping[str, Any], *, path: str) -> None:
    errors: list[str] = []
    _require(data, ["household_name"], path, errors)
    _require_list(data, "people", path, errors)
    _require_list(data, "devices", path, errors)
    _require_list(data, "services", path, errors)
    _require_list(data, "secret_references", path, errors)

    _validate_unique_ids(data.get("people", []), f"{path}.people", errors)
    _validate_unique_ids(data.get("devices", []), f"{path}.devices", errors)
    _validate_unique_ids(data.get("services", []), f"{path}.services", errors)

    for index, person in enumerate(_as_list(data.get("people"))):
        item_path = f"{path}.people[{index}]"
        _require_mapping(person, item_path, errors)
        if isinstance(person, Mapping):
            _require(person, ["id", "name", "role"], item_path, errors)

    for index, device in enumerate(_as_list(data.get("devices"))):
        item_path = f"{path}.devices[{index}]"
        _require_mapping(device, item_path, errors)
        if isinstance(device, Mapping):
            _require(device, ["id", "name", "device_type", "location", "household_impact"], item_path, errors)
            if "core" in device:
                errors.append(f"{item_path}.core is not supported; use core_infrastructure")
            _validate_facts(device.get("facts", []), f"{item_path}.facts", errors)

    for index, service in enumerate(_as_list(data.get("services"))):
        item_path = f"{path}.services[{index}]"
        _require_mapping(service, item_path, errors)
        if isinstance(service, Mapping):
            _require(service, ["id", "name", "household_impact"], item_path, errors)
            _validate_facts(service.get("facts", []), f"{item_path}.facts", errors)
            for endpoint_index, endpoint in enumerate(_as_list(service.get("access_endpoints", []))):
                endpoint_path = f"{item_path}.access_endpoints[{endpoint_index}]"
                _validate_access_endpoint(endpoint, endpoint_path, errors)

    for index, reference in enumerate(_as_list(data.get("secret_references"))):
        item_path = f"{path}.secret_references[{index}]"
        _require_mapping(reference, item_path, errors)
        if isinstance(reference, Mapping):
            _require(reference, ["label", "system"], item_path, errors)

    _raise_if_errors(errors)


def validate_runbook_data(data: Mapping[str, Any], *, path: str) -> None:
    errors: list[str] = []
    _require(
        data,
        ["id", "symptom", "applies_to", "plain_summary", "household_impact", "first_checks", "escalation_path", "do_not_touch"],
        path,
        errors,
    )
    _require_list(data, "applies_to", path, errors)
    _require_list(data, "first_checks", path, errors)
    _require_list(data, "escalation_path", path, errors)
    _require_list(data, "do_not_touch", path, errors)
    if "temporary_workarounds" in data and not isinstance(data["temporary_workarounds"], list):
        errors.append(f"{path}.temporary_workarounds must be a list")

    symptom = str(data.get("symptom", ""))
    _validate_symptom_title(symptom, f"{path}.symptom", errors)

    for index, check in enumerate(_as_list(data.get("first_checks"))):
        item_path = f"{path}.first_checks[{index}]"
        _require_mapping(check, item_path, errors)
        if not isinstance(check, Mapping):
            continue
        _require(check, ["text", "action_class"], item_path, errors)
        action_class = check.get("action_class")
        text = str(check.get("text", ""))
        decision = classify_action(text)
        if action_class not in VALID_ACTION_CLASSES:
            errors.append(f"{item_path}.action_class must be one of {sorted(VALID_ACTION_CLASSES)}")
        else:
            if not is_stricter_or_equal(action_class, decision.action_class):
                errors.append(
                    f"{item_path}.action_class {action_class!r} is less strict than policy classification "
                    f"{decision.action_class!r} for term {decision.matched_term!r}"
                )
            if action_class != "safe":
                errors.append(f"{item_path} must be a Safe Action because first checks are for Stress Users")
        if decision.action_class != "safe":
            errors.append(
                f"{item_path}.text is classified as {decision.action_class!r}; "
                "first checks must be safe observations"
            )

    _raise_if_errors(errors)


def validate_relationships(inventory: Any, runbooks: Sequence[Any]) -> None:
    """Validate cross-file references after model creation."""
    errors: list[str] = []
    device_ids = {device.id for device in inventory.devices}
    service_ids = {service.id for service in inventory.services}
    known_infrastructure_ids = device_ids | service_ids

    for service in inventory.services:
        for dependency in service.depends_on:
            if dependency not in known_infrastructure_ids:
                errors.append(f"service {service.id!r} depends on unknown device or service {dependency!r}")

    for runbook in runbooks:
        for service_id in runbook.applies_to:
            if service_id not in service_ids:
                errors.append(f"runbook {runbook.id!r} applies to unknown service {service_id!r}")

    _raise_if_errors(errors)


def _validate_facts(value: Any, path: str, errors: list[str]) -> None:
    for index, fact in enumerate(_as_list(value)):
        item_path = f"{path}[{index}]"
        _require_mapping(fact, item_path, errors)
        if isinstance(fact, Mapping):
            _require(fact, ["text", "evidence"], item_path, errors)
            _validate_evidence(fact.get("evidence"), f"{item_path}.evidence", errors)


def _validate_access_endpoint(value: Any, path: str, errors: list[str]) -> None:
    _require_mapping(value, path, errors)
    if not isinstance(value, Mapping):
        return
    _require(value, ["label", "url", "evidence"], path, errors)
    url = str(value.get("url", ""))
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        errors.append(f"{path}.url must be an http or https URL")
    _validate_evidence(value.get("evidence"), f"{path}.evidence", errors)


def _validate_evidence(value: Any, path: str, errors: list[str]) -> None:
    _require_mapping(value, path, errors)
    if not isinstance(value, Mapping):
        return
    _require(value, ["source", "last_verified", "freshness_days"], path, errors)
    status = value.get("status", "known")
    if status not in VALID_EVIDENCE_STATUSES:
        errors.append(f"{path}.status must be one of {sorted(VALID_EVIDENCE_STATUSES)}")
    try:
        parse_utc(str(value.get("last_verified", "")))
    except ValueError:
        errors.append(f"{path}.last_verified must be an ISO-8601 timestamp")
    try:
        freshness_days = int(value.get("freshness_days", ""))
    except ValueError:
        errors.append(f"{path}.freshness_days must be a positive integer")
    else:
        if freshness_days <= 0:
            errors.append(f"{path}.freshness_days must be a positive integer")


def _validate_symptom_title(value: str, path: str, errors: list[str]) -> None:
    if not value.strip():
        errors.append(f"{path} must not be empty")
        return
    lowered = value.lower()
    for term in sorted(ROOT_CAUSE_TITLE_TERMS):
        if term in lowered:
            errors.append(
                f"{path} should describe a Stress User symptom, not a possible root cause; avoid {term!r}"
            )
            return


def _validate_unique_ids(items: Any, path: str, errors: list[str]) -> None:
    seen: set[str] = set()
    for index, item in enumerate(_as_list(items)):
        if not isinstance(item, Mapping):
            continue
        item_id = item.get("id")
        if not item_id:
            continue
        if str(item_id) in seen:
            errors.append(f"{path}[{index}].id duplicates {item_id!r}")
        seen.add(str(item_id))


def _require(data: Mapping[str, Any], keys: Sequence[str], path: str, errors: list[str]) -> None:
    for key in keys:
        if key not in data or data[key] is None or data[key] == "":
            errors.append(f"{path}.{key} is required")


def _require_list(data: Mapping[str, Any], key: str, path: str, errors: list[str]) -> None:
    if key not in data:
        errors.append(f"{path}.{key} is required")
    elif not isinstance(data[key], list):
        errors.append(f"{path}.{key} must be a list")


def _require_mapping(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, Mapping):
        errors.append(f"{path} must be a mapping")


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _raise_if_errors(errors: Sequence[str]) -> None:
    if errors:
        message = "Validation failed:\n- " + "\n- ".join(errors)
        raise ValidationError(message)
