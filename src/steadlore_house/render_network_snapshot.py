from __future__ import annotations

import ipaddress
from dataclasses import dataclass

from .network_discovery import ActiveScanHost, NetworkNeighbor, NetworkSnapshot


@dataclass(frozen=True)
class Candidate:
    ip_address: str
    reasons: tuple[str, ...]
    mac_address: str | None = None
    vendor: str | None = None
    connector_hints: tuple[str, ...] = ()
    interfaces: tuple[str, ...] = ()
    state: str | None = None


def render_network_snapshot(snapshot: NetworkSnapshot) -> str:
    lines: list[str] = []
    lines.append("# Network Discovery Snapshot")
    lines.append("")
    lines.append(f"Observed: {snapshot.observed_at.isoformat().replace('+00:00', 'Z')}")
    lines.append(f"Method: {snapshot.method}")
    lines.append("")
    lines.append(
        "> This is an observational snapshot, not trusted household inventory. It may be incomplete, stale, or misleading. Review discoveries before turning them into Manual Inventory."
    )
    lines.append("")
    candidates = core_infrastructure_candidates(snapshot)
    lines.extend(_render_summary(snapshot, candidates))
    lines.extend(_render_candidates(candidates))
    lines.extend(_render_mermaid(snapshot, candidates))
    lines.extend(_render_interfaces(snapshot))
    lines.extend(_render_routes(snapshot))
    lines.extend(_render_dns(snapshot))
    lines.extend(_render_neighbors(snapshot))
    lines.extend(_render_active_scan(snapshot))
    lines.extend(_render_ignored_noise(snapshot))
    lines.extend(_render_unknowns())
    lines.extend(_render_evidence(snapshot))
    lines.extend(_render_warnings(snapshot))
    return "\n".join(lines).rstrip() + "\n"


def core_infrastructure_candidates(snapshot: NetworkSnapshot) -> list[Candidate]:
    by_ip: dict[str, Candidate] = {}
    default_gateways = {route.gateway for route in snapshot.routes if route.gateway and route.destination in {"default", "0.0.0.0/0", "::/0"}}
    dns_servers = set(snapshot.dns_servers)
    neighbor_by_ip = _deduplicated_neighbors(snapshot.neighbors)

    for ip_address in sorted(default_gateways | dns_servers):
        neighbor = neighbor_by_ip.get(ip_address)
        reasons = []
        if ip_address in default_gateways:
            reasons.append("default gateway candidate")
        if ip_address in dns_servers:
            reasons.append("DNS server candidate")
        by_ip[ip_address] = _candidate_from_neighbor(ip_address, neighbor, tuple(reasons))

    for neighbor in neighbor_by_ip.values():
        if _is_noise_address(neighbor.ip_address):
            continue
        if neighbor.vendor:
            existing = by_ip.get(neighbor.ip_address)
            reasons = tuple([*(existing.reasons if existing else ()), "vendor-enriched observed neighbor"])
            by_ip[neighbor.ip_address] = _candidate_from_neighbor(neighbor.ip_address, neighbor, reasons)

    for host in snapshot.active_scan_hosts:
        if _is_noise_address(host.ip_address):
            continue
        if host.vendor:
            existing = by_ip.get(host.ip_address)
            reasons = tuple([*(existing.reasons if existing else ()), "vendor-enriched nmap ping host"])
            by_ip[host.ip_address] = Candidate(
                ip_address=host.ip_address,
                reasons=tuple(dict.fromkeys(reasons)),
                mac_address=host.mac_address,
                vendor=host.vendor,
                connector_hints=host.connector_hints,
                state=host.state,
            )

    return sorted(by_ip.values(), key=lambda item: _ip_sort_key(item.ip_address))


def _candidate_from_neighbor(ip_address: str, neighbor: NetworkNeighbor | None, reasons: tuple[str, ...]) -> Candidate:
    if not neighbor:
        return Candidate(ip_address=ip_address, reasons=tuple(dict.fromkeys(reasons)))
    return Candidate(
        ip_address=ip_address,
        reasons=tuple(dict.fromkeys(reasons)),
        mac_address=neighbor.mac_address,
        vendor=neighbor.vendor,
        connector_hints=neighbor.connector_hints,
        interfaces=tuple(sorted({neighbor.interface} if neighbor.interface else set())),
        state=neighbor.state,
    )


def _render_summary(snapshot: NetworkSnapshot, candidates: list[Candidate]) -> list[str]:
    return [
        "## Summary",
        "",
        f"- Interfaces observed: {len(snapshot.interfaces)}",
        f"- Routes observed: {len(snapshot.routes)}",
        f"- DNS servers observed: {len(snapshot.dns_servers)}",
        f"- Neighbor entries observed: {len(snapshot.neighbors)}",
        f"- Core infrastructure candidates: {len(candidates)}",
        f"- Active scan hosts observed: {len(snapshot.active_scan_hosts)}",
        "",
    ]


def _render_candidates(candidates: list[Candidate]) -> list[str]:
    lines = ["## Core Infrastructure Candidates", ""]
    lines.append("These are candidates only. Confirm role, location, owner, and Household Impact before adding them to Manual Inventory.")
    lines.append("")
    if not candidates:
        lines.append("- None identified from routes, DNS servers, vendor enrichment, or active scan results.")
    for candidate in candidates:
        lines.append(f"- **{candidate.ip_address}**")
        lines.append(f"  - Why listed: {', '.join(candidate.reasons)}")
        if candidate.mac_address:
            lines.append(f"  - MAC: {candidate.mac_address}")
        if candidate.vendor:
            lines.append(f"  - Vendor: {candidate.vendor}")
        if candidate.interfaces:
            lines.append(f"  - Interfaces: {', '.join(candidate.interfaces)}")
        if candidate.state:
            lines.append(f"  - Last-known neighbor state: {candidate.state}")
        lines.append("  - Confidence: candidate only; confirm manually")
    lines.append("")
    return lines


def _render_mermaid(snapshot: NetworkSnapshot, candidates: list[Candidate]) -> list[str]:
    lines = ["## Network Map", "", "```mermaid", "graph TD"]
    lines.append('  this_machine["This machine"]')

    for index, candidate in enumerate(candidates[:30]):
        node_id = f"candidate_{index}"
        label_parts = [candidate.ip_address]
        if candidate.vendor:
            label_parts.append(candidate.vendor)
        if candidate.reasons:
            label_parts.append(candidate.reasons[0])
        label = "\\n".join(label_parts)
        lines.append(f'  {node_id}["{_escape_mermaid(label)}"]')
        arrow = "-->" if "default gateway candidate" in candidate.reasons or "DNS server candidate" in candidate.reasons else "-. candidate .->"
        lines.append(f"  this_machine {arrow} {node_id}")

    if not candidates:
        lines.append('  unknown["No core infrastructure candidates identified"]')
        lines.append("  this_machine -. unknown .-> unknown")

    lines.append("```")
    lines.append("")
    return lines


def _render_interfaces(snapshot: NetworkSnapshot) -> list[str]:
    lines = ["## Interfaces", ""]
    if not snapshot.interfaces:
        lines.append("- Unknown. No interface data was observed.")
    for interface in snapshot.interfaces:
        addresses = ", ".join(interface.addresses) if interface.addresses else "unknown addresses"
        state = interface.state or "unknown state"
        lines.append(f"- **{interface.name}** — {state}; {addresses}")
    lines.append("")
    return lines


def _render_routes(snapshot: NetworkSnapshot) -> list[str]:
    lines = ["## Routes", ""]
    if not snapshot.routes:
        lines.append("- Unknown. No route data was observed.")
    for route in snapshot.routes:
        parts = [f"destination: {route.destination}"]
        if route.gateway:
            parts.append(f"gateway: {route.gateway}")
        if route.interface:
            parts.append(f"interface: {route.interface}")
        if route.preferred_source:
            parts.append(f"preferred source: {route.preferred_source}")
        lines.append(f"- {'; '.join(parts)}")
    lines.append("")
    return lines


def _render_dns(snapshot: NetworkSnapshot) -> list[str]:
    lines = ["## DNS Servers", ""]
    if not snapshot.dns_servers:
        lines.append("- Unknown. No DNS server data was observed.")
    for server in snapshot.dns_servers:
        lines.append(f"- {server}")
    lines.append("")
    return lines


def _render_neighbors(snapshot: NetworkSnapshot) -> list[str]:
    lines = ["## Observed Neighbors", ""]
    neighbors = list(_deduplicated_neighbors(snapshot.neighbors).values())
    if not neighbors:
        lines.append("- None observed from the local neighbor cache.")
    for neighbor in sorted(neighbors, key=lambda item: _ip_sort_key(item.ip_address)):
        if _is_noise_address(neighbor.ip_address) or _is_placeholder_mac(neighbor.mac_address):
            continue
        parts = [neighbor.ip_address]
        if neighbor.hostname:
            parts.append(f"hostname: {neighbor.hostname}")
        if neighbor.mac_address and not _is_placeholder_mac(neighbor.mac_address):
            parts.append(f"MAC: {neighbor.mac_address}")
        if neighbor.vendor:
            parts.append(f"vendor: {neighbor.vendor}")
        if neighbor.interface:
            parts.append(f"interface: {neighbor.interface}")
        if neighbor.state:
            parts.append(f"state: {neighbor.state}")
        lines.append(f"- {'; '.join(parts)}")
    lines.append("")
    return lines


def _render_active_scan(snapshot: NetworkSnapshot) -> list[str]:
    if not snapshot.active_scan_hosts:
        return []
    lines = ["## Active Scan Hosts", ""]
    lines.append("These hosts were observed only because an explicit nmap ping scan was requested.")
    lines.append("")
    for host in snapshot.active_scan_hosts:
        parts = [host.ip_address]
        if host.hostname:
            parts.append(f"hostname: {host.hostname}")
        if host.mac_address:
            parts.append(f"MAC: {host.mac_address}")
        if host.vendor:
            parts.append(f"vendor: {host.vendor}")
        if host.state:
            parts.append(f"state: {host.state}")
        lines.append(f"- {'; '.join(parts)}")
    lines.append("")
    return lines


def _render_ignored_noise(snapshot: NetworkSnapshot) -> list[str]:
    network_noise = [neighbor for neighbor in snapshot.neighbors if _is_noise_address(neighbor.ip_address)]
    placeholder_mac = [
        neighbor
        for neighbor in snapshot.neighbors
        if not _is_noise_address(neighbor.ip_address) and _is_placeholder_mac(neighbor.mac_address)
    ]
    if not network_noise and not placeholder_mac:
        return []
    lines = ["## Ignored Network Noise", ""]
    if network_noise:
        lines.append(f"- Ignored multicast, broadcast, unspecified, loopback, and link-local neighbor entries: {len(network_noise)}")
    if placeholder_mac:
        lines.append(f"- Ignored neighbor entries with placeholder MAC addresses: {len(placeholder_mac)}")
    lines.append("")
    return lines


def _render_unknowns() -> list[str]:
    return [
        "## Unknowns and Limits",
        "",
        "- Whether an observed neighbor is important to the household.",
        "- Whether a vendor-enriched device has the role suggested by its vendor.",
        "- Whether an observed host is currently healthy.",
        "- Device roles, owners, locations, and household impact unless manually confirmed elsewhere.",
        "- Services running on observed hosts. Passive discovery does not perform port scans.",
        "- Devices that did not appear in local caches or the optional active scan.",
        "",
    ]


def _render_evidence(snapshot: NetworkSnapshot) -> list[str]:
    lines = ["## Evidence", ""]
    if not snapshot.evidence:
        lines.append("- No evidence sources were recorded.")
    for item in snapshot.evidence:
        lines.append(f"- {item}")
    lines.append("")
    return lines


def _render_warnings(snapshot: NetworkSnapshot) -> list[str]:
    if not snapshot.warnings:
        return []
    lines = ["## Warnings", ""]
    for warning in snapshot.warnings:
        lines.append(f"- {warning}")
    lines.append("")
    return lines


def _deduplicated_neighbors(neighbors: tuple[NetworkNeighbor, ...]) -> dict[str, NetworkNeighbor]:
    result: dict[str, NetworkNeighbor] = {}
    for neighbor in neighbors:
        existing = result.get(neighbor.ip_address)
        if existing is None or _neighbor_score(neighbor) > _neighbor_score(existing):
            result[neighbor.ip_address] = neighbor
    return result


def _neighbor_score(neighbor: NetworkNeighbor) -> int:
    score = 0
    if neighbor.mac_address and not _is_placeholder_mac(neighbor.mac_address):
        score += 4
    if neighbor.vendor:
        score += 3
    if neighbor.connector_hints:
        score += 2
    if neighbor.state and neighbor.state.lower() == "reachable":
        score += 1
    return score


def _is_placeholder_mac(value: str | None) -> bool:
    if not value:
        return False
    normalized = "".join(char for char in value.upper() if char in "0123456789ABCDEF")
    return normalized in {"000000000000", "FFFFFFFFFFFF"}



def _is_noise_address(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    return bool(address.is_multicast or address.is_loopback or address.is_unspecified or address.is_link_local or value.endswith(".255") or value == "255.255.255.255")


def _ip_sort_key(value: str) -> tuple[int, int | str]:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return (1, value)
    return (0, int(address))


def _escape_mermaid(value: str) -> str:
    return value.replace('"', "'")
