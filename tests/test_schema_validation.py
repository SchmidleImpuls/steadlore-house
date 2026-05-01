import pytest

from steadlore_house.models import Inventory, Runbook
from steadlore_house.validation import (
    ValidationError,
    validate_inventory_data,
    validate_relationships,
    validate_runbook_data,
)


def test_requires_inventory_fields() -> None:
    with pytest.raises(ValidationError, match="household_name is required"):
        validate_inventory_data({"people": [], "devices": [], "services": [], "secret_references": []}, path="inventory")


def test_validates_access_endpoint_urls() -> None:
    data = {
        "household_name": "Example",
        "people": [],
        "devices": [],
        "secret_references": [],
        "services": [
            {
                "id": "home-assistant",
                "name": "Home Assistant",
                "household_impact": "Some controls may not work.",
                "access_endpoints": [
                    {
                        "label": "Dashboard",
                        "url": "homeassistant.local:8123",
                        "evidence": {
                            "source": "manual inventory",
                            "last_verified": "2026-04-20T12:00:00Z",
                            "freshness_days": 30,
                        },
                    }
                ],
            }
        ],
    }

    with pytest.raises(ValidationError, match="must be an http or https URL"):
        validate_inventory_data(data, path="inventory")


def test_rejects_root_cause_runbook_symptom_titles() -> None:
    data = _valid_runbook_data() | {"symptom": "Home Assistant is unavailable after container redeploy"}

    with pytest.raises(ValidationError, match="should describe a Stress User symptom"):
        validate_runbook_data(data, path="runbook")


def test_first_checks_must_be_safe() -> None:
    data = _valid_runbook_data()
    data["first_checks"] = [{"text": "Restart the Home Assistant container.", "action_class": "privileged"}]

    with pytest.raises(ValidationError, match="first checks are for Stress Users"):
        validate_runbook_data(data, path="runbook")


def test_runbooks_must_reference_existing_services() -> None:
    inventory = Inventory.from_dict(
        {
            "household_name": "Example",
            "people": [],
            "devices": [],
            "services": [],
            "secret_references": [],
        }
    )
    runbook = Runbook.from_dict(_valid_runbook_data())

    with pytest.raises(ValidationError, match="applies to unknown service"):
        validate_relationships(inventory, [runbook])


def _valid_runbook_data() -> dict:
    return {
        "id": "lights-not-working",
        "symptom": "Lights or automations are not working",
        "applies_to": ["home-assistant"],
        "plain_summary": "Smart-home controls may be unavailable.",
        "probably_still_ok": ["Internet and Wi-Fi are not necessarily affected."],
        "household_impact": "Some automations may not work.",
        "first_checks": [{"text": "Try the physical wall switch.", "action_class": "safe"}],
        "escalation_path": ["Contact the trusted helper."],
        "do_not_touch": ["Do not reset network equipment."],
    }
