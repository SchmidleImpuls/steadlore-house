from datetime import UTC, datetime

import yaml

from steadlore_house.models import Inventory
from steadlore_house.network_discovery import NetworkNeighbor, NetworkRoute, NetworkSnapshot
from steadlore_house.render_inventory_draft import render_inventory_draft
from steadlore_house.validation import validate_inventory_data


def test_render_inventory_draft_from_network_candidates_is_review_required_and_valid_inventory() -> None:
    snapshot = NetworkSnapshot(
        observed_at=datetime(2026, 5, 1, tzinfo=UTC),
        method="passive local OS snapshot",
        routes=(NetworkRoute(destination="default", gateway="192.0.2.1", interface="eth0"),),
        dns_servers=("192.0.2.53",),
        neighbors=(
            NetworkNeighbor(
                ip_address="192.0.2.1",
                interface="eth0",
                mac_address="00:00:5E:00:53:01",
                state="reachable",
                vendor="Example Networks",
                connector_hints=("example connector candidate",),
            ),
        ),
        evidence=("ip -j route", "MAC vendor enrichment: example-vendors.txt"),
    )

    rendered = render_inventory_draft(snapshot)
    data = yaml.safe_load(rendered)

    validate_inventory_data(data, path="inventory-draft")
    inventory = Inventory.from_dict(data)
    assert data["_draft_notice"].startswith("Draft only")
    assert inventory.devices[0].id == "candidate-device-192-0-2-1"
    assert inventory.devices[0].name == "Gateway candidate 192.0.2.1"
    assert inventory.devices[0].device_type == "Gateway"
    assert inventory.devices[0].core is True
    assert inventory.devices[0].location == "Unknown"
    assert "internet access and local routing may be affected" in inventory.devices[0].household_impact
    assert data["devices"][0]["_review"]["vendor"] == "Example Networks"
    assert data["devices"][0]["_review"]["connector_hints"] == ["example connector candidate"]
    assert data["devices"][0]["_review"]["fields_to_review"] == ["id", "name", "device_type", "core", "location", "household_impact"]
    fact_texts = [fact.text for fact in inventory.devices[0].facts]
    assert "Observed 192.0.2.1 as default gateway candidate, vendor-enriched observed neighbor." in fact_texts
    assert "Offline MAC vendor lookup suggests Example Networks for 192.0.2.1." in fact_texts
    assert "Possible connector candidate for 192.0.2.1: example connector candidate." in fact_texts
    assert all(fact.evidence.status == "discovered" for fact in inventory.devices[0].facts)
    assert all(fact.evidence.confidence == "low" for fact in inventory.devices[0].facts)
