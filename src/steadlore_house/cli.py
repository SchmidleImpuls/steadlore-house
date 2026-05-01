from __future__ import annotations

import argparse
from pathlib import Path

from .io import load_inventory, load_runbooks
from .render_manual import render_manual
from .validation import validate_relationships


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="steadlore-house")
    subcommands = parser.add_subparsers(dest="command", required=True)

    generate = subcommands.add_parser("generate-manual", help="Generate a Markdown Continuity Manual.")
    generate.add_argument("--inventory", required=True, type=Path, help="Path to household inventory YAML.")
    generate.add_argument("--runbooks", required=True, type=Path, help="Path to a runbook YAML file or directory.")
    generate.add_argument("--output", required=True, type=Path, help="Path for generated Markdown output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate-manual":
        inventory = load_inventory(args.inventory)
        runbooks = load_runbooks(args.runbooks)
        validate_relationships(inventory, runbooks)
        manual = render_manual(inventory, runbooks)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(manual, encoding="utf-8")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
