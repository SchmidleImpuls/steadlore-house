from __future__ import annotations

import json
import platform
import shutil
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .mac_vendors import MacVendorLookup, connector_hints_for_vendor, load_mac_vendor_lookup


@dataclass(frozen=True)
class NetworkInterface:
    name: str
    state: str | None = None
    addresses: tuple[str, ...] = ()


@dataclass(frozen=True)
class NetworkRoute:
    destination: str
    gateway: str | None = None
    interface: str | None = None
    preferred_source: str | None = None


@dataclass(frozen=True)
class NetworkNeighbor:
    ip_address: str
    interface: str | None = None
    mac_address: str | None = None
    state: str | None = None
    hostname: str | None = None
    vendor: str | None = None
    connector_hints: tuple[str, ...] = ()


@dataclass(frozen=True)
class ActiveScanHost:
    ip_address: str
    mac_address: str | None = None
    hostname: str | None = None
    state: str | None = None
    vendor: str | None = None
    connector_hints: tuple[str, ...] = ()


class NetworkDiscoveryError(RuntimeError):
    """Raised when explicitly requested discovery cannot be completed."""


@dataclass(frozen=True)
class NetworkSnapshot:
    observed_at: datetime
    method: str
    interfaces: tuple[NetworkInterface, ...] = ()
    routes: tuple[NetworkRoute, ...] = ()
    dns_servers: tuple[str, ...] = ()
    neighbors: tuple[NetworkNeighbor, ...] = ()
    active_scan_hosts: tuple[ActiveScanHost, ...] = ()
    warnings: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()


def discover_network(
    *,
    active_scan: bool = False,
    subnets: tuple[str, ...] = (),
    mac_vendor_path: Path | None = None,
    now: datetime | None = None,
) -> NetworkSnapshot:
    """Create a local-first network snapshot.

    Passive discovery reads local OS network state only. Active discovery is
    opt-in and uses an existing nmap binary when requested.
    """
    observed_at = now or datetime.now(UTC)
    if observed_at.tzinfo is None:
        observed_at = observed_at.replace(tzinfo=UTC)
    observed_at = observed_at.astimezone(UTC)

    vendor_lookup = _load_vendor_lookup(mac_vendor_path)

    system = platform.system().lower()
    if system == "windows":
        snapshot = _discover_windows(observed_at)
    else:
        snapshot = _discover_linux_like(observed_at)

    snapshot = enrich_snapshot(snapshot, vendor_lookup)

    if active_scan:
        scan_targets = tuple(subnets) or discover_scan_targets(snapshot)
        if not scan_targets:
            raise NetworkDiscoveryError("active scan requested but no scan subnet was provided or discovered from local interfaces")
        hosts = []
        scan_warnings = []
        scan_evidence = []
        for target in scan_targets:
            target_hosts, target_warnings, target_evidence = run_nmap_ping_scan(target)
            hosts.extend(target_hosts)
            scan_warnings.extend(target_warnings)
            scan_evidence.extend(target_evidence)
        hosts = [enrich_active_scan_host(host, vendor_lookup) for host in hosts]
        return NetworkSnapshot(
            observed_at=snapshot.observed_at,
            method="passive local OS snapshot plus explicit nmap ping scan",
            interfaces=snapshot.interfaces,
            routes=snapshot.routes,
            dns_servers=snapshot.dns_servers,
            neighbors=snapshot.neighbors,
            active_scan_hosts=tuple(hosts),
            warnings=tuple([*snapshot.warnings, *scan_warnings]),
            evidence=tuple(dict.fromkeys([*snapshot.evidence, *scan_evidence])),
        )

    return snapshot


def enrich_snapshot(snapshot: NetworkSnapshot, vendor_lookup: MacVendorLookup) -> NetworkSnapshot:
    evidence = list(snapshot.evidence)
    if vendor_lookup.source:
        evidence.append(f"MAC vendor enrichment: {vendor_lookup.source}")
    return NetworkSnapshot(
        observed_at=snapshot.observed_at,
        method=snapshot.method,
        interfaces=snapshot.interfaces,
        routes=snapshot.routes,
        dns_servers=snapshot.dns_servers,
        neighbors=tuple(enrich_neighbor(neighbor, vendor_lookup) for neighbor in snapshot.neighbors),
        active_scan_hosts=tuple(enrich_active_scan_host(host, vendor_lookup) for host in snapshot.active_scan_hosts),
        warnings=snapshot.warnings,
        evidence=tuple(dict.fromkeys(evidence)),
    )


def enrich_neighbor(neighbor: NetworkNeighbor, vendor_lookup: MacVendorLookup) -> NetworkNeighbor:
    return NetworkNeighbor(
        ip_address=neighbor.ip_address,
        interface=neighbor.interface,
        mac_address=neighbor.mac_address,
        state=neighbor.state,
        hostname=neighbor.hostname,
        vendor=vendor_lookup.vendor_for(neighbor.mac_address),
        connector_hints=vendor_lookup.connector_hints_for(neighbor.mac_address),
    )


def enrich_active_scan_host(host: ActiveScanHost, vendor_lookup: MacVendorLookup) -> ActiveScanHost:
    vendor = vendor_lookup.vendor_for(host.mac_address) or host.vendor
    return ActiveScanHost(
        ip_address=host.ip_address,
        mac_address=host.mac_address,
        hostname=host.hostname,
        state=host.state,
        vendor=vendor,
        connector_hints=tuple(dict.fromkeys([*host.connector_hints, *vendor_lookup.connector_hints_for(host.mac_address), *connector_hints_for_vendor(vendor)])),
    )


def _load_vendor_lookup(path: Path | None) -> MacVendorLookup:
    return load_mac_vendor_lookup(path)


def run_nmap_ping_scan(subnet: str) -> tuple[list[ActiveScanHost], list[str], list[str]]:
    if not shutil.which("nmap"):
        raise NetworkDiscoveryError("active scan requested but nmap was not found on PATH")

    command = ["nmap", "-sn", "-oX", "-", subnet]
    result = _run(command, timeout=120)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown nmap error"
        raise NetworkDiscoveryError(f"nmap ping scan failed for {subnet}: {detail}")
    try:
        return parse_nmap_ping_xml(result.stdout), [], ["nmap -sn -oX - <subnet>"]
    except ET.ParseError as error:
        raise NetworkDiscoveryError(f"could not parse nmap XML output for {subnet}: {error}") from error


def parse_linux_ip_addr_json(text: str) -> list[NetworkInterface]:
    items = json.loads(text or "[]")
    interfaces: list[NetworkInterface] = []
    for item in items:
        addresses = []
        for address in item.get("addr_info", []):
            local = address.get("local")
            prefix = address.get("prefixlen")
            family = address.get("family")
            if local and family in {"inet", "inet6"}:
                addresses.append(f"{local}/{prefix}" if prefix is not None else str(local))
        interfaces.append(
            NetworkInterface(
                name=str(item.get("ifname", "unknown")),
                state=item.get("operstate"),
                addresses=tuple(sorted(addresses)),
            )
        )
    return interfaces


def parse_linux_ip_route_json(text: str) -> list[NetworkRoute]:
    items = json.loads(text or "[]")
    routes: list[NetworkRoute] = []
    for item in items:
        routes.append(
            NetworkRoute(
                destination=str(item.get("dst", "default")),
                gateway=item.get("gateway"),
                interface=item.get("dev"),
                preferred_source=item.get("prefsrc"),
            )
        )
    return routes


def parse_linux_ip_neigh_json(text: str) -> list[NetworkNeighbor]:
    items = json.loads(text or "[]")
    neighbors: list[NetworkNeighbor] = []
    for item in items:
        destination = item.get("dst")
        if not destination:
            continue
        neighbors.append(
            NetworkNeighbor(
                ip_address=str(destination),
                interface=item.get("dev"),
                mac_address=item.get("lladdr"),
                state=item.get("state"),
            )
        )
    return neighbors


def discover_scan_targets(snapshot: NetworkSnapshot) -> tuple[str, ...]:
    import ipaddress

    targets: set[str] = set()
    for interface in snapshot.interfaces:
        for address_text in interface.addresses:
            try:
                interface_address = ipaddress.ip_interface(address_text)
            except ValueError:
                continue
            address = interface_address.ip
            network = interface_address.network
            if address.version != 4:
                continue
            if address.is_loopback or address.is_link_local or address.is_multicast or address.is_unspecified:
                continue
            targets.add(str(network))
    return tuple(sorted(targets))



def parse_resolv_conf(text: str) -> list[str]:
    servers: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        if len(parts) >= 2 and parts[0] == "nameserver":
            servers.append(parts[1])
    return sorted(set(servers))


def parse_nmap_ping_xml(text: str) -> list[ActiveScanHost]:
    root = ET.fromstring(text)
    hosts: list[ActiveScanHost] = []
    for host in root.findall("host"):
        status = host.find("status")
        state = status.attrib.get("state") if status is not None else None
        addresses = host.findall("address")
        ip_address = None
        mac_address = None
        vendor = None
        for address in addresses:
            addr_type = address.attrib.get("addrtype")
            if addr_type in {"ipv4", "ipv6"} and ip_address is None:
                ip_address = address.attrib.get("addr")
            if addr_type == "mac":
                mac_address = address.attrib.get("addr")
                vendor = address.attrib.get("vendor")
        hostname = None
        hostnames = host.find("hostnames")
        if hostnames is not None:
            first = hostnames.find("hostname")
            if first is not None:
                hostname = first.attrib.get("name")
        if ip_address:
            hosts.append(
                ActiveScanHost(
                    ip_address=ip_address,
                    mac_address=mac_address,
                    hostname=hostname,
                    state=state,
                    vendor=vendor,
                    connector_hints=connector_hints_for_vendor(vendor),
                )
            )
    return sorted(hosts, key=lambda item: item.ip_address)


def _discover_linux_like(observed_at: datetime) -> NetworkSnapshot:
    warnings: list[str] = []
    evidence: list[str] = []
    interfaces: list[NetworkInterface] = []
    routes: list[NetworkRoute] = []
    neighbors: list[NetworkNeighbor] = []
    dns_servers: list[str] = []

    if shutil.which("ip"):
        addr = _run(["ip", "-j", "addr"])
        evidence.append("ip -j addr")
        if addr.returncode == 0:
            interfaces = parse_linux_ip_addr_json(addr.stdout)
        else:
            warnings.append(f"Could not read network interfaces: {addr.stderr.strip()}")

        route = _run(["ip", "-j", "route"])
        evidence.append("ip -j route")
        if route.returncode == 0:
            routes = parse_linux_ip_route_json(route.stdout)
        else:
            warnings.append(f"Could not read route table: {route.stderr.strip()}")

        neigh = _run(["ip", "-j", "neigh"])
        evidence.append("ip -j neigh")
        if neigh.returncode == 0:
            neighbors = parse_linux_ip_neigh_json(neigh.stdout)
        else:
            warnings.append(f"Could not read neighbor table: {neigh.stderr.strip()}")
    else:
        warnings.append("The 'ip' command was not found; interface, route, and neighbor discovery are unavailable.")

    resolv_conf = Path("/etc/resolv.conf")
    if resolv_conf.exists():
        evidence.append("/etc/resolv.conf")
        dns_servers = parse_resolv_conf(resolv_conf.read_text(encoding="utf-8", errors="replace"))
    else:
        warnings.append("/etc/resolv.conf was not found; DNS server discovery is unavailable.")

    return NetworkSnapshot(
        observed_at=observed_at,
        method="passive local OS snapshot",
        interfaces=tuple(sorted(interfaces, key=lambda item: item.name)),
        routes=tuple(sorted(routes, key=lambda item: (item.destination, item.interface or ""))),
        dns_servers=tuple(dns_servers),
        neighbors=tuple(sorted(neighbors, key=lambda item: item.ip_address)),
        warnings=tuple(warnings),
        evidence=tuple(evidence),
    )


def _discover_windows(observed_at: datetime) -> NetworkSnapshot:
    warnings: list[str] = []
    evidence: list[str] = []
    interfaces: list[NetworkInterface] = []
    routes: list[NetworkRoute] = []
    neighbors: list[NetworkNeighbor] = []
    dns_servers: set[str] = set()

    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-NetIPConfiguration | ForEach-Object { [pscustomobject]@{ InterfaceAlias=$_.InterfaceAlias; Status=$_.NetAdapter.Status; IPv4Address=@($_.IPv4Address | ForEach-Object { [pscustomobject]@{ IPAddress=$_.IPAddress; PrefixLength=$_.PrefixLength } }); IPv6Address=@($_.IPv6Address | ForEach-Object { [pscustomobject]@{ IPAddress=$_.IPAddress; PrefixLength=$_.PrefixLength } }); DNSServerAddresses=@($_.DNSServer | ForEach-Object { $_.ServerAddresses }) } } | ConvertTo-Json -Depth 5",
    ]
    result = _run(command)
    evidence.append("Get-NetIPConfiguration")
    if result.returncode == 0 and result.stdout.strip():
        parsed = json.loads(result.stdout)
        for item in _ensure_list(parsed):
            addresses = []
            for address in _ensure_list(item.get("IPv4Address")) + _ensure_list(item.get("IPv6Address")):
                ip = address.get("IPAddress")
                prefix = address.get("PrefixLength")
                if ip:
                    addresses.append(f"{ip}/{prefix}" if prefix is not None else ip)
            status = item.get("Status")
            interfaces.append(NetworkInterface(name=str(item.get("InterfaceAlias", "unknown")), state=str(status) if status is not None else None, addresses=tuple(sorted(addresses))))
            for server in _flatten(_ensure_list(item.get("DNSServerAddresses"))):
                if server:
                    dns_servers.add(str(server))
    else:
        warnings.append("Could not read Windows IP configuration with PowerShell.")

    route_result = _run(["powershell", "-NoProfile", "-Command", "Get-NetRoute -DestinationPrefix '0.0.0.0/0' | ForEach-Object { [pscustomobject]@{ DestinationPrefix=$_.DestinationPrefix; NextHop=$_.NextHop; InterfaceAlias=$_.InterfaceAlias } } | ConvertTo-Json -Depth 3"])
    evidence.append("Get-NetRoute")
    if route_result.returncode == 0 and route_result.stdout.strip():
        for item in _ensure_list(json.loads(route_result.stdout)):
            next_hop = item.get("NextHop")
            interface = item.get("InterfaceAlias")
            routes.append(NetworkRoute(destination=str(item.get("DestinationPrefix", "default")), gateway=str(next_hop) if next_hop is not None else None, interface=str(interface) if interface is not None else None))
    else:
        warnings.append("Could not read Windows default routes with PowerShell.")

    neighbor_result = _run(["powershell", "-NoProfile", "-Command", "Get-NetNeighbor | ForEach-Object { [pscustomobject]@{ IPAddress=$_.IPAddress; InterfaceAlias=$_.InterfaceAlias; LinkLayerAddress=$_.LinkLayerAddress; State=$_.State } } | ConvertTo-Json -Depth 3"])
    evidence.append("Get-NetNeighbor")
    if neighbor_result.returncode == 0 and neighbor_result.stdout.strip():
        for item in _ensure_list(json.loads(neighbor_result.stdout)):
            ip = item.get("IPAddress")
            if ip:
                interface = item.get("InterfaceAlias")
                mac_address = item.get("LinkLayerAddress")
                state = item.get("State")
                neighbors.append(NetworkNeighbor(ip_address=str(ip), interface=str(interface) if interface is not None else None, mac_address=str(mac_address) if mac_address is not None else None, state=_windows_neighbor_state(state)))
    else:
        warnings.append("Could not read Windows neighbor table with PowerShell.")

    return NetworkSnapshot(
        observed_at=observed_at,
        method="passive local OS snapshot",
        interfaces=tuple(sorted(interfaces, key=lambda item: item.name)),
        routes=tuple(sorted(routes, key=lambda item: (item.destination, item.interface or ""))),
        dns_servers=tuple(sorted(dns_servers)),
        neighbors=tuple(sorted(neighbors, key=lambda item: item.ip_address)),
        warnings=tuple(warnings),
        evidence=tuple(evidence),
    )


def _windows_neighbor_state(value: object) -> str | None:
    if value is None:
        return None
    states = {
        0: "unreachable",
        1: "incomplete",
        2: "probe",
        3: "delay",
        4: "stale",
        5: "reachable",
        6: "permanent",
    }
    try:
        return states.get(int(value), str(value))
    except (TypeError, ValueError):
        return str(value)



def _flatten(values: list) -> list:
    flattened: list = []
    for value in values:
        if isinstance(value, list):
            flattened.extend(_flatten(value))
        else:
            flattened.append(value)
    return flattened


def _ensure_list(value: object) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _run(command: list[str], *, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as error:
        return subprocess.CompletedProcess(
            args=command,
            returncode=124,
            stdout=error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or ""),
            stderr=f"Command timed out after {timeout} seconds.",
        )
