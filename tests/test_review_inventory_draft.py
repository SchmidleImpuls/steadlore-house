from pathlib import Path

import pytest
import yaml

from steadlore_house.models import Inventory
from steadlore_house.review_inventory_draft import load_inventory_draft, render_reviewed_inventory, review_inventory_draft_interactive
from steadlore_house.validation import validate_inventory_data


def test_review_inventory_draft_promotes_confirmed_candidate() -> None:
    data = load_inventory_draft(Path("dist/inventory-draft.yaml"))
    answers = iter(
        [
            "Example Household",
            "n",
            "y",
            "main-gateway",
            "Main Gateway",
            "Gateway",
            "y",
            "Utility cabinet",
            "Provides internet access and local routing for the household.",
            "n",
        ]
    )
    messages: list[str] = []

    reviewed = review_inventory_draft_interactive(data, prompt=lambda text: next(answers), output=messages.append)
    rendered = render_reviewed_inventory(reviewed)
    rendered_data = yaml.safe_load(rendered)

    validate_inventory_data(rendered_data, path="reviewed")
    inventory = Inventory.from_dict(rendered_data)
    assert inventory.household_name == "Example Household"
    assert inventory.generated_for == "household members and trusted persons"
    assert len(inventory.devices) == 1
    assert inventory.devices[0].id == "main-gateway"
    assert inventory.devices[0].name == "Main Gateway"
    assert inventory.devices[0].device_type == "Gateway"
    assert inventory.devices[0].core_infrastructure is True
    assert inventory.devices[0].location == "Utility cabinet"
    assert "_review" not in rendered
    assert "_draft_notice" not in rendered


def test_core_infrastructure_candidate_defaults_to_promote() -> None:
    data = load_inventory_draft(Path("dist/inventory-draft.yaml"))
    answers = iter(
        [
            "Example Household",
            "n",
            "",
            "main-gateway",
            "Main Gateway",
            "Gateway",
            "y",
            "Utility cabinet",
            "Provides internet access and local routing for the household.",
            "n",
        ]
    )

    reviewed = review_inventory_draft_interactive(data, prompt=lambda text: next(answers), output=lambda text: None)

    assert reviewed["devices"][0]["id"] == "main-gateway"



def test_review_inventory_draft_rejects_unknown_location() -> None:
    data = load_inventory_draft(Path("dist/inventory-draft.yaml"))
    answers = iter(
        [
            "Example Household",
            "n",
            "y",
            "main-gateway",
            "Main Gateway",
            "Gateway",
            "y",
            "Unknown",
            "Utility cabinet",
            "Provides internet access and local routing for the household.",
            "n",
        ]
    )

    reviewed = review_inventory_draft_interactive(data, prompt=lambda text: next(answers), output=lambda text: None)

    assert reviewed["devices"][0]["location"] == "Utility cabinet"


def test_load_inventory_draft_rejects_invalid_yaml_shape(tmp_path: Path) -> None:
    path = tmp_path / "draft.yaml"
    path.write_text("[]\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Validation failed"):
        load_inventory_draft(path)
