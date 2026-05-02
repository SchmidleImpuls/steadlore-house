from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from .io import load_inventory, load_runbooks
from .network_discovery import NetworkDiscoveryError, discover_network
from .render_ai_packet import render_ai_packet
from .render_manual import render_manual
from .render_network_snapshot import render_network_snapshot
from .validation import validate_relationships


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="steadlore-house",
        description="Local-first household continuity tooling. Generates manuals and observational discovery snapshots without storing secrets or executing remediation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  steadlore-house discover-network --output dist/network-snapshot.md
  steadlore-house generate-manual --inventory examples/household.yaml --runbooks examples/runbooks --output dist/continuity-manual.md
  steadlore-house generate-ai-packet --inventory examples/household.yaml --runbooks examples/runbooks --output dist/ai-assistance-packet.md
""",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    generate = subcommands.add_parser(
        "generate-manual",
        help="Generate a Markdown Continuity Manual.",
        description="Generate a deterministic Markdown Continuity Manual from reviewed Manual Inventory and Runbooks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Example:
  steadlore-house generate-manual \\
    --inventory examples/household.yaml \\
    --runbooks examples/runbooks \\
    --output dist/continuity-manual.md
""",
    )
    generate.add_argument("--inventory", required=True, type=Path, help="Path to household inventory YAML.")
    generate.add_argument("--runbooks", required=True, type=Path, help="Path to a runbook YAML file or directory.")
    generate.add_argument("--output", required=True, type=Path, help="Path for generated Markdown output. If this is an existing directory, continuity-manual.md is written inside it.")

    ai_packet = subcommands.add_parser(
        "generate-ai-packet",
        help="Generate a Markdown AI Assistance Packet.",
        description="Generate a redacted Markdown packet for a chatbot helping a Stress User perform safe checks only.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Safety boundary:
  The packet must not contain secrets, must not invent facts, and must not authorize privileged actions.

Example:
  steadlore-house generate-ai-packet \\
    --inventory examples/household.yaml \\
    --runbooks examples/runbooks \\
    --output dist/ai-assistance-packet.md
""",
    )
    ai_packet.add_argument("--inventory", required=True, type=Path, help="Path to household inventory YAML.")
    ai_packet.add_argument("--runbooks", required=True, type=Path, help="Path to a runbook YAML file or directory.")
    ai_packet.add_argument("--output", required=True, type=Path, help="Path for generated Markdown output. If this is an existing directory, ai-assistance-packet.md is written inside it.")

    discover = subcommands.add_parser(
        "discover-network",
        help="Generate a local network discovery snapshot.",
        description="Generate an observational Network Discovery Snapshot from local OS network state. The output is not trusted Manual Inventory until reviewed.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Default behavior:
  Passive only. Reads local interfaces, routes, DNS resolver configuration, and neighbor cache.
  Does not perform port scans, login attempts, cloud lookups, or inventory mutation.

Optional active scan:
  --active-scan uses an existing nmap binary for a ping scan only: nmap -sn -oX - <subnet>
  If --subnet is omitted, Steadlore scans IPv4 subnets discovered from local interfaces.
  Use --subnet to override or repeat --subnet to scan multiple explicit targets.

MAC vendor enrichment:
  By default, Steadlore tries to find a local nmap-mac-prefixes file and uses it offline.
  --mac-vendors overrides auto-discovery with a local nmap-mac-prefixes or IEEE OUI file.
  Vendor names are connector hints only; they do not confirm device role or Household Impact.

Examples:
  steadlore-house discover-network --output dist/network-snapshot.md
  steadlore-house discover-network --active-scan --output dist/network-snapshot.md
  steadlore-house discover-network --active-scan --subnet 192.0.2.0/24 --output dist/network-snapshot.md
""",
    )
    discover.add_argument("--output", required=True, type=Path, help="Path for generated Markdown output. If this is an existing directory, network-snapshot.md is written inside it.")
    discover.add_argument("--active-scan", action="store_true", help="Also run an explicit nmap ping scan. Requires nmap on PATH.")
    discover.add_argument("--subnet", action="append", default=[], help="Subnet to scan when --active-scan is used, such as 192.0.2.0/24. Can be repeated. If omitted, local IPv4 subnets are discovered from interfaces.")
    discover.add_argument("--mac-vendors", type=Path, help="Optional local nmap-mac-prefixes or IEEE OUI file for offline MAC vendor enrichment. Overrides automatic local nmap-mac-prefixes discovery.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate-manual":
        _print_status(f"Generating Continuity Manual from {args.inventory} and {args.runbooks}...")
        inventory = load_inventory(args.inventory)
        runbooks = load_runbooks(args.runbooks)
        validate_relationships(inventory, runbooks)
        manual = render_manual(inventory, runbooks)
        output_path = _write_markdown(args.output, manual, default_filename="continuity-manual.md", parser=parser)
        _print_status(f"Wrote Continuity Manual to {output_path}")
        return 0

    if args.command == "generate-ai-packet":
        _print_status(f"Generating AI Assistance Packet from {args.inventory} and {args.runbooks}...")
        inventory = load_inventory(args.inventory)
        runbooks = load_runbooks(args.runbooks)
        validate_relationships(inventory, runbooks)
        packet = render_ai_packet(inventory, runbooks)
        output_path = _write_markdown(args.output, packet, default_filename="ai-assistance-packet.md", parser=parser)
        _print_status(f"Wrote AI Assistance Packet to {output_path}")
        return 0

    if args.command == "discover-network":
        if args.active_scan and not shutil.which("nmap"):
            parser.error("--active-scan requires nmap on PATH. Install nmap or omit --active-scan for passive discovery.")
        if args.mac_vendors and not args.mac_vendors.is_file():
            parser.error(f"--mac-vendors must point to an existing local vendor file: {args.mac_vendors}")
        mode = "passive local snapshot plus explicit nmap ping scan" if args.active_scan else "passive local snapshot"
        _print_status(f"Discovering network ({mode})...")
        try:
            snapshot = discover_network(active_scan=args.active_scan, subnets=tuple(args.subnet), mac_vendor_path=args.mac_vendors)
        except NetworkDiscoveryError as error:
            parser.error(str(error))
        rendered = render_network_snapshot(snapshot)
        output_path = _write_markdown(args.output, rendered, default_filename="network-snapshot.md", parser=parser)
        _print_status(f"Wrote Network Discovery Snapshot to {output_path}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


def _print_status(message: str) -> None:
    print(message)


def _resolve_output_path(path: Path, *, default_filename: str) -> Path:
    if path.exists() and path.is_dir():
        return path / default_filename
    return path


def _write_markdown(path: Path, content: str, *, default_filename: str, parser: argparse.ArgumentParser) -> Path:
    output_path = _resolve_output_path(path, default_filename=default_filename)
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
    except OSError as error:
        parser.error(f"could not write output to {output_path}: {error}")
    return output_path


if __name__ == "__main__":
    raise SystemExit(main())
