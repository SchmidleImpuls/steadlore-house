from datetime import UTC, datetime
from pathlib import Path

from steadlore_house.dependency_graph import build_dependency_graph, render_dependency_graph_mermaid
from steadlore_house.io import load_inventory
from steadlore_house.models import Inventory


def test_renders_home_assistant_dependency_with_stale_target_label() -> None:
    inventory = load_inventory(Path("examples/household.yaml"))

    graph = build_dependency_graph(inventory, now=datetime(2026, 5, 1, tzinfo=UTC))
    mermaid = render_dependency_graph_mermaid(graph)

    assert "flowchart TD" in mermaid
    assert "Home Assistant" in mermaid
    assert "House Server 01" in mermaid
    assert "home_assistant -->|depends on| house_server_01" in mermaid
    assert "Device: House Server 01<br/>STALE; manually_confirmed" in mermaid


def test_dependency_graph_rendering_is_deterministic() -> None:
    inventory = load_inventory(Path("examples/household.yaml"))
    now = datetime(2026, 5, 1, tzinfo=UTC)

    first = render_dependency_graph_mermaid(build_dependency_graph(inventory, now=now))
    second = render_dependency_graph_mermaid(build_dependency_graph(inventory, now=now))

    assert first == second


def test_unresolved_dependency_target_is_rendered_honestly() -> None:
    inventory = Inventory.from_dict(
        {
            "household_name": "Example",
            "people": [],
            "devices": [],
            "services": [
                {
                    "id": "home-assistant",
                    "name": "Home Assistant",
                    "critical": True,
                    "household_impact": "Automations may not work.",
                    "depends_on": ["missing-host"],
                }
            ],
            "secret_references": [],
        }
    )

    mermaid = render_dependency_graph_mermaid(
        build_dependency_graph(inventory, now=datetime(2026, 5, 1, tzinfo=UTC))
    )

    assert "Unresolved dependency: missing-host" in mermaid
    assert "Unknown: Unresolved dependency: missing-host<br/>unresolved" in mermaid
    assert "home_assistant -->|depends on| unresolved_missing_host" in mermaid


def test_unknown_evidence_status_is_visible_in_node_label() -> None:
    inventory = Inventory.from_dict(
        {
            "household_name": "Example",
            "people": [],
            "devices": [
                {
                    "id": "house-server-01",
                    "name": "House Server 01",
                    "device_type": "Host",
                    "location": "Utility cabinet",
                    "household_impact": "Runs local services.",
                    "facts": [
                        {
                            "text": "The host role needs review.",
                            "evidence": {
                                "source": "manual inventory",
                                "last_verified": "2026-04-30T00:00:00Z",
                                "freshness_days": 30,
                                "status": "unknown",
                                "confidence": "low",
                            },
                        }
                    ],
                }
            ],
            "services": [
                {
                    "id": "home-assistant",
                    "name": "Home Assistant",
                    "critical": True,
                    "household_impact": "Automations may not work.",
                    "depends_on": ["house-server-01"],
                }
            ],
            "secret_references": [],
        }
    )

    mermaid = render_dependency_graph_mermaid(
        build_dependency_graph(inventory, now=datetime(2026, 5, 1, tzinfo=UTC))
    )

    assert "Device: House Server 01<br/>current; unknown" in mermaid


def test_no_dependencies_produce_no_mermaid_output() -> None:
    inventory = Inventory.from_dict(
        {
            "household_name": "Example",
            "people": [],
            "devices": [
                {
                    "id": "house-server-01",
                    "name": "House Server 01",
                    "device_type": "Host",
                    "location": "Utility cabinet",
                    "household_impact": "Runs local services.",
                }
            ],
            "services": [
                {
                    "id": "home-assistant",
                    "name": "Home Assistant",
                    "critical": True,
                    "household_impact": "Automations may not work.",
                }
            ],
            "secret_references": [],
        }
    )

    graph = build_dependency_graph(inventory, now=datetime(2026, 5, 1, tzinfo=UTC))

    assert graph.edges == ()
    assert render_dependency_graph_mermaid(graph) == ""


def test_mermaid_labels_are_escaped() -> None:
    inventory = Inventory.from_dict(
        {
            "household_name": "Example",
            "people": [],
            "devices": [
                {
                    "id": "server-bracket",
                    "name": "Server [rack] \"A\"",
                    "device_type": "Host",
                    "location": "Utility cabinet",
                    "household_impact": "Runs local services.",
                }
            ],
            "services": [
                {
                    "id": "service-pipe",
                    "name": "Lights | Automations",
                    "critical": True,
                    "household_impact": "Automations may not work.",
                    "depends_on": ["server-bracket"],
                }
            ],
            "secret_references": [],
        }
    )

    mermaid = render_dependency_graph_mermaid(
        build_dependency_graph(inventory, now=datetime(2026, 5, 1, tzinfo=UTC))
    )

    assert "Server (rack) 'A'" in mermaid
    assert "Lights / Automations" in mermaid
    assert "[rack]" not in mermaid
    assert '"A"' not in mermaid
