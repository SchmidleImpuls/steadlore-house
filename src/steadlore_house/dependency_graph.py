from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import re

from .models import Evidence, Inventory
from .staleness import is_stale


@dataclass(frozen=True)
class DependencyNode:
    id: str
    mermaid_id: str
    label: str
    kind: str
    trust_label: str


@dataclass(frozen=True)
class DependencyEdge:
    source_id: str
    target_id: str


@dataclass(frozen=True)
class DependencyGraph:
    nodes: tuple[DependencyNode, ...]
    edges: tuple[DependencyEdge, ...]


def build_dependency_graph(inventory: Inventory, *, now: datetime | None = None) -> DependencyGraph:
    """Build a dependency graph from reviewed Manual Inventory relationships."""
    current = now or datetime.now(UTC)
    device_by_id = {device.id: device for device in inventory.devices}
    service_by_id = {service.id: service for service in inventory.services}
    nodes_by_id: dict[str, DependencyNode] = {}
    edges: list[DependencyEdge] = []
    used_mermaid_ids: set[str] = set()

    def new_mermaid_id(value: str) -> str:
        base = _mermaid_id(value)
        candidate = base
        suffix = 2
        while candidate in used_mermaid_ids:
            candidate = f"{base}_{suffix}"
            suffix += 1
        used_mermaid_ids.add(candidate)
        return candidate

    def add_known_node(entity_id: str) -> None:
        if entity_id in nodes_by_id:
            return
        if entity_id in service_by_id:
            service = service_by_id[entity_id]
            evidence = [fact.evidence for fact in service.facts] + [endpoint.evidence for endpoint in service.access_endpoints]
            nodes_by_id[entity_id] = DependencyNode(
                id=entity_id,
                mermaid_id=new_mermaid_id(entity_id),
                label=service.name,
                kind="Service",
                trust_label=_trust_label(evidence, current),
            )
            return
        if entity_id in device_by_id:
            device = device_by_id[entity_id]
            evidence = [fact.evidence for fact in device.facts]
            nodes_by_id[entity_id] = DependencyNode(
                id=entity_id,
                mermaid_id=new_mermaid_id(entity_id),
                label=device.name,
                kind="Device",
                trust_label=_trust_label(evidence, current),
            )
            return
        unresolved_id = f"unresolved:{entity_id}"
        nodes_by_id[unresolved_id] = DependencyNode(
            id=unresolved_id,
            mermaid_id=new_mermaid_id(f"unresolved-{entity_id}"),
            label=f"Unresolved dependency: {entity_id}",
            kind="Unknown",
            trust_label="unresolved",
        )

    for service in sorted(inventory.services, key=lambda item: (item.name, item.id)):
        for target_id in sorted(service.depends_on):
            add_known_node(service.id)
            if target_id in device_by_id or target_id in service_by_id:
                add_known_node(target_id)
                edge_target_id = target_id
            else:
                add_known_node(target_id)
                edge_target_id = f"unresolved:{target_id}"
            edges.append(DependencyEdge(source_id=service.id, target_id=edge_target_id))

    return DependencyGraph(
        nodes=tuple(sorted(nodes_by_id.values(), key=lambda node: (node.label, node.id))),
        edges=tuple(sorted(edges, key=lambda edge: (edge.source_id, edge.target_id))),
    )


def render_dependency_graph_mermaid(graph: DependencyGraph) -> str:
    if not graph.edges:
        return ""

    node_by_id = {node.id: node for node in graph.nodes}
    lines = ["```mermaid", "flowchart TD"]
    for node in graph.nodes:
        label = _escape_mermaid_label(f"{node.kind}: {node.label}<br/>{node.trust_label}")
        lines.append(f'  {node.mermaid_id}["{label}"]')
    for edge in graph.edges:
        source = node_by_id[edge.source_id]
        target = node_by_id[edge.target_id]
        lines.append(f"  {source.mermaid_id} -->|depends on| {target.mermaid_id}")
    lines.append("```")
    return "\n".join(lines)


def _trust_label(evidence_items: list[Evidence], now: datetime) -> str:
    if not evidence_items:
        return "no evidence"
    stale = any(is_stale(evidence.last_verified, evidence.freshness_days, now=now) for evidence in evidence_items)
    freshness = "STALE" if stale else "current"
    statuses = sorted({evidence.status for evidence in evidence_items})
    return f"{freshness}; {', '.join(statuses)}"


def _mermaid_id(value: str) -> str:
    normalized = re.sub(r"[^0-9A-Za-z_]+", "_", value).strip("_").lower()
    if not normalized:
        return "node"
    if normalized[0].isdigit():
        return f"node_{normalized}"
    return normalized


def _escape_mermaid_label(value: str) -> str:
    break_token = "__STEADLORE_LINE_BREAK__"
    return (
        value.replace("<br/>", break_token)
        .replace("&", "and")
        .replace("<", "(")
        .replace(">", ")")
        .replace("[", "(")
        .replace("]", ")")
        .replace("{", "(")
        .replace("}", ")")
        .replace('"', "'")
        .replace("|", "/")
        .replace(break_token, "<br/>")
    )
