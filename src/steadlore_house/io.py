from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import Inventory, Runbook
from .validation import reject_secret_fields, validate_inventory_data, validate_runbook_data


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    reject_secret_fields(data, path=str(path))
    return data


def load_inventory(path: Path) -> Inventory:
    data = load_yaml(path)
    validate_inventory_data(data, path=str(path))
    return Inventory.from_dict(data)


def load_runbooks(path: Path) -> list[Runbook]:
    if path.is_file():
        data = load_yaml(path)
        validate_runbook_data(data, path=str(path))
        return [Runbook.from_dict(data)]

    runbooks: list[Runbook] = []
    for child in sorted(path.glob("*.yaml")):
        data = load_yaml(child)
        validate_runbook_data(data, path=str(child))
        runbooks.append(Runbook.from_dict(data))
    return runbooks
