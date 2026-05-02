from datetime import UTC, datetime
from pathlib import Path

from steadlore_house.mac_vendors import MacVendorLookup, load_mac_vendor_lookup, parse_vendor_file
from steadlore_house.network_discovery import (
    NetworkInterface,
    NetworkNeighbor,
    NetworkRoute,
    NetworkSnapshot,
    discover_scan_targets,
    parse_linux_ip_addr_json,
    parse_linux_ip_neigh_json,
    parse_linux_ip_route_json,
    parse_nmap_ping_xml,
    enrich_neighbor,
    parse_resolv_conf,
)
from steadlore_house.render_network_snapshot import core_infrastructure_candidates, render_network_snapshot


def test_parses_linux_interface_json() -> None:
    interfaces = parse_linux_ip_addr_json(
        '[{"ifname":"eth0","operstate":"UP","addr_info":[{"family":"inet","local":"192.0.2.10","prefixlen":24}]}]'
    )

    assert interfaces == [NetworkInterface(name="eth0", state="UP", addresses=("192.0.2.10/24",))]


def test_parses_linux_routes_json() -> None:
    routes = parse_linux_ip_route_json('[{"dst":"default","gateway":"192.0.2.1","dev":"eth0","prefsrc":"192.0.2.10"}]')

    assert routes == [NetworkRoute(destination="default", gateway="192.0.2.1", interface="eth0", preferred_source="192.0.2.10")]


def test_parses_linux_neighbors_json() -> None:
    neighbors = parse_linux_ip_neigh_json('[{"dst":"192.0.2.1","dev":"eth0","lladdr":"00:11:22:33:44:55","state":"REACHABLE"}]')

    assert neighbors == [NetworkNeighbor(ip_address="192.0.2.1", interface="eth0", mac_address="00:11:22:33:44:55", state="REACHABLE")]


def test_discovers_scan_targets_from_interface_addresses() -> None:
    snapshot = NetworkSnapshot(
        observed_at=datetime(2026, 5, 1, tzinfo=UTC),
        method="passive local OS snapshot",
        interfaces=(
            NetworkInterface(name="eth0", addresses=("192.0.2.10/24", "fe80::1/64")),
            NetworkInterface(name="loopback", addresses=("127.0.0.1/8",)),
        ),
    )

    assert discover_scan_targets(snapshot) == ("192.0.2.0/24",)


def test_parses_resolv_conf_nameservers() -> None:
    assert parse_resolv_conf("# comment\nnameserver 192.0.2.53\nnameserver 192.0.2.53\nnameserver 2001:db8::53\n") == [
        "192.0.2.53",
        "2001:db8::53",
    ]


def test_parses_nmap_ping_xml() -> None:
    hosts = parse_nmap_ping_xml(
        """
        <nmaprun>
          <host>
            <status state="up" />
            <address addr="192.0.2.20" addrtype="ipv4" />
            <address addr="00:11:22:33:44:66" addrtype="mac" vendor="Ubiquiti Inc." />
            <hostnames><hostname name="example-device.local" /></hostnames>
          </host>
        </nmaprun>
        """
    )

    assert hosts[0].ip_address == "192.0.2.20"
    assert hosts[0].mac_address == "00:11:22:33:44:66"
    assert hosts[0].hostname == "example-device.local"
    assert hosts[0].state == "up"
    assert hosts[0].vendor == "Ubiquiti Inc."
    assert hosts[0].connector_hints == ("UniFi connector candidate",)


def test_loads_explicit_mac_vendor_file(tmp_path: Path) -> None:
    vendor_file = tmp_path / "nmap-mac-prefixes"
    vendor_file.write_text("942A6F Ubiquiti Inc.\n", encoding="utf-8")

    lookup = load_mac_vendor_lookup(vendor_file)

    assert lookup.vendor_for("94-2A-6F-F0-BB-80") == "Ubiquiti Inc."
    assert lookup.source == str(vendor_file)


def test_parses_mac_vendor_files_and_enriches_neighbors() -> None:
    vendors = parse_vendor_file("942A6F Ubiquiti Inc.\n00-11-22   (hex)        Raspberry Pi Trading Ltd\n")
    lookup = MacVendorLookup(vendors)
    neighbor = enrich_neighbor(NetworkNeighbor(ip_address="192.0.2.2", mac_address="94-2A-6F-F0-BB-80"), lookup)

    assert neighbor.vendor == "Ubiquiti Inc."
    assert neighbor.connector_hints == ("UniFi connector candidate",)


def test_core_infrastructure_candidates_include_gateway_dns_and_vendor_hints() -> None:
    lookup = MacVendorLookup(parse_vendor_file("942A6F Ubiquiti Inc.\n"))
    gateway = enrich_neighbor(
        NetworkNeighbor(ip_address="192.0.2.1", interface="eth0", mac_address="94-2A-6F-F0-BB-80", state="reachable"),
        lookup,
    )
    snapshot = NetworkSnapshot(
        observed_at=datetime(2026, 5, 1, tzinfo=UTC),
        method="passive local OS snapshot",
        routes=(NetworkRoute(destination="default", gateway="192.0.2.1", interface="eth0"),),
        dns_servers=("192.0.2.53",),
        neighbors=(gateway, NetworkNeighbor(ip_address="224.0.0.251", mac_address="01-00-5E-00-00-FB")),
    )

    candidates = core_infrastructure_candidates(snapshot)

    assert [candidate.ip_address for candidate in candidates] == ["192.0.2.1", "192.0.2.53"]
    assert candidates[0].vendor == "Ubiquiti Inc."
    assert candidates[0].connector_hints == ("UniFi connector candidate",)


def test_renders_network_snapshot_with_map_and_limits() -> None:
    snapshot = NetworkSnapshot(
        observed_at=datetime(2026, 5, 1, tzinfo=UTC),
        method="passive local OS snapshot",
        interfaces=(NetworkInterface(name="eth0", state="UP", addresses=("192.0.2.10/24",)),),
        routes=(NetworkRoute(destination="default", gateway="192.0.2.1", interface="eth0"),),
        dns_servers=("192.0.2.53",),
        neighbors=(
            NetworkNeighbor(ip_address="192.0.2.1", interface="eth0", mac_address="00:11:22:33:44:55", state="REACHABLE", vendor="Example Networks", connector_hints=("example connector candidate",)),
            NetworkNeighbor(ip_address="192.0.2.2", interface="eth0", mac_address="00-00-00-00-00-00", state="unreachable"),
        ),
        evidence=("ip -j addr", "ip -j route", "ip -j neigh", "/etc/resolv.conf"),
    )

    rendered = render_network_snapshot(snapshot)

    assert "# Network Discovery Snapshot" in rendered
    assert "observational snapshot, not trusted household inventory" in rendered
    assert "## Core Infrastructure Candidates" in rendered
    assert "Example Networks" in rendered
    assert "example connector candidate" in rendered
    assert "```mermaid" in rendered
    assert "192.0.2.1" in rendered
    assert "192.0.2.53" in rendered
    assert "## Unknowns and Limits" in rendered
    assert "Passive discovery does not perform port scans" in rendered
    assert "ip -j neigh" in rendered
    assert "192.0.2.2; MAC: 00-00-00-00-00-00" not in rendered
    assert "Ignored neighbor entries with placeholder MAC addresses: 1" in rendered
