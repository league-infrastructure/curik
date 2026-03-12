from __future__ import annotations

import argparse
import json
from importlib.metadata import version
from pathlib import Path

from .project import (
    CurikError,
    advance_phase,
    get_phase,
    get_spec,
    init_course,
    update_spec,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="curik")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version('curik')}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Initialize Curik files in a repo")
    init_parser.add_argument("--path", default=".", help="Repository path")

    get_phase_parser = sub.add_parser("get-phase", help="Read current course phase")
    get_phase_parser.add_argument("--path", default=".", help="Repository path")

    get_spec_parser = sub.add_parser("get-spec", help="Read the current spec")
    get_spec_parser.add_argument("--path", default=".", help="Repository path")

    update_spec_parser = sub.add_parser("update-spec", help="Update a spec section")
    update_spec_parser.add_argument("section")
    update_spec_parser.add_argument("content")
    update_spec_parser.add_argument("--path", default=".", help="Repository path")

    advance_phase_parser = sub.add_parser("advance-phase", help="Advance to target phase")
    advance_phase_parser.add_argument("target")
    advance_phase_parser.add_argument("--path", default=".", help="Repository path")

    mcp_parser = sub.add_parser("mcp", help="Run Curik MCP server placeholder")
    mcp_parser.add_argument("--path", default=".", help="Repository path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    root = Path(args.path).resolve()
    try:
        if args.command == "init":
            result = init_course(root)
            created = result.get("created", [])
            print(f"Curik initialized. Created {len(created)} files/directories.")
            print()
            print("Curik is ready. Open Claude Code in this directory and say:")
            print()
            print('  "Start Curik"')
            return 0
        if args.command == "get-phase":
            print(json.dumps(get_phase(root), indent=2))
            return 0
        if args.command == "get-spec":
            print(get_spec(root))
            return 0
        if args.command == "update-spec":
            update_spec(root, args.section, args.content)
            return 0
        if args.command == "advance-phase":
            advance_phase(root, args.target)
            return 0
        if args.command == "mcp":
            from .server import run_server

            run_server(root)
            return 0
    except CurikError as error:
        parser.exit(status=1, message=f"{error}\n")
    return 0
