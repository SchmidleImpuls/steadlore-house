from datetime import UTC, datetime
from pathlib import Path

from steadlore_house.io import load_inventory, load_runbooks
from steadlore_house.render_ai_packet import render_ai_packet


def test_render_ai_packet_includes_chatbot_boundaries() -> None:
    inventory = load_inventory(Path("examples/household.yaml"))
    runbooks = load_runbooks(Path("examples/runbooks"))

    packet = render_ai_packet(inventory, runbooks, now=datetime(2026, 5, 1, tzinfo=UTC))

    assert "# Example Household AI Assistance Packet" in packet
    assert "## Instructions for the chatbot" in packet
    assert "perform safe checks only" in packet
    assert "We have prepared for this" in packet
    assert "Always surface temporary workarounds before escalation" in packet
    assert "Do not imply the Primary Operator is available" in packet
    assert "Do not invent missing facts" in packet
    assert "Do not ask for passwords" in packet
    assert "## Safety policy" in packet
    assert "high_friction: Privileged changes to core infrastructure" in packet
    assert "forbidden: Actions that expose secrets" in packet
    assert "## Symptom runbooks" in packet
    assert "### Symptom: Lights or automations are not working" in packet
    assert "http://homeassistant.local:8123" in packet
    assert "Temporary workarounds to surface before escalation:" in packet
    assert "Use physical wall switches for lights until smart-home controls are restored." in packet
    assert "[stale: true;" in packet
    assert "## Unknowns the chatbot must not invent" in packet
    assert "container redeploy" not in packet


def test_render_ai_packet_is_deterministic_for_same_inputs() -> None:
    inventory = load_inventory(Path("examples/household.yaml"))
    runbooks = load_runbooks(Path("examples/runbooks"))
    now = datetime(2026, 5, 1, tzinfo=UTC)

    assert render_ai_packet(inventory, runbooks, now=now) == render_ai_packet(inventory, runbooks, now=now)
