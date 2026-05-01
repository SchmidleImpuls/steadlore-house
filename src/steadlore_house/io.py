from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import Inventory, Runbook
from .validation import reject_secret_fields


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    reject_secret_fields(data, path=str(path))
    return data


def load_inventory(path: Path) -> Inventory:
    return Inventory.from_dict(load_yaml(path))


def load_runbooks(path: Path) -> list[Runbook]:
    if path.is_file():
        return [Runbook.from_dict(load_yaml(path))]

    runbooks: list[Runbook] = []
    for child in sorted(path.glob("*.yaml")):
        runbooks.append(Runbook.from_dict(load_yaml(child)))
    return runbooks
