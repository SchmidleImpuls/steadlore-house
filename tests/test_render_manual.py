from datetime import UTC, datetime
from pathlib import Path

from steadlore_house.io import load_inventory, load_runbooks
from steadlore_house.render_manual import render_manual


def test_render_manual_includes_staleness_and_modes() -> None:
    inventory = load_inventory(Path("examples/household.yaml"))
    runbooks = load_runbooks(Path("examples/runbooks"))

    manual = render_manual(inventory, runbooks, now=datetime(2026, 5, 1, tzinfo=UTC))

    assert "# Example Household Continuity Manual" in manual
    assert "STALE" in manual
    assert "## Start Here" in manual
    assert "## Safety Rules" in manual
    assert "High Friction" in manual
    assert "## Common Problems" in manual
    assert "### Lights or automations are not working" in manual
    assert "## Who Can Help" in manual
    assert "## For Helper Persons" in manual
    assert "### Symptom Notes" in manual
    assert "What you can do meanwhile:" in manual
    assert "Use physical wall switches for lights until smart-home controls are restored." in manual
    assert "What not to touch:" in manual
    assert "No passwords or recovery keys are stored in this manual" in manual
    assert "could not detect recent breaking changes or failed generating or publishing a newer manual" in manual
    assert "Internet and Wi-Fi are not necessarily affected" in manual
    assert "http://homeassistant.local:8123" in manual
    assert "container redeploy" not in manual
    assert "fallback human" not in manual.lower()
    assert "Failure Scenario" not in manual

    common_problem_index = manual.index("## Common Problems")
    helper_index = manual.index("## For Helper Persons")
    container_index = manual.index("container maintenance")
    facts_index = manual.index("Facts:")
    assert common_problem_index < helper_index < container_index
    assert helper_index < facts_index


def test_render_manual_is_deterministic_for_same_inputs() -> None:
    inventory = load_inventory(Path("examples/household.yaml"))
    runbooks = load_runbooks(Path("examples/runbooks"))
    now = datetime(2026, 5, 1, tzinfo=UTC)

    assert render_manual(inventory, runbooks, now=now) == render_manual(inventory, runbooks, now=now)
