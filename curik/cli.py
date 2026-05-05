"""Curik CLI — argparse entry point exposing all domain functions as subcommands."""

from __future__ import annotations

import argparse
import json
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any

from .changes import (
    approve_change_plan,
    close_change_plan,
    create_change_plan,
    create_issue,
    execute_change_plan,
    list_issues,
    register_change_plan,
    review_change_plan,
)
from .hugo import (
    create_content_page,
    hugo_build,
    list_content_pages,
    update_frontmatter,
)
from .migrate import inventory_course, migrate_structure, sequester_content
from .project import (
    CurikError,
    advance_phase,
    advance_sub_phase,
    get_course_status,
    get_phase,
    get_spec,
    init_course,
    record_alignment,
    record_course_concept,
    record_pedagogical_model,
    update_course_yml,
    update_spec,
)
from .publish import check_publish_ready, get_publish_guide
from .readme import generate_readmes
from .scaffolding import (
    approve_outline,
    create_lesson_stub,
    create_outline,
    generate_change_plan,
    get_outline,
    scaffold_structure,
)
from .layout_check import check_legacy_hugo_layout
from .layout_migrate import migrate_hugo_layout
from .syllabus import validate_syllabus_consistency, write_syllabus_url
from .templates import bump_curriculum_version, hugo_setup, hugo_setup_from_course
from .validation import (
    get_validation_report,
    save_validation_report,
    validate_course,
    validate_lesson,
    validate_module,
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _add_common_args(parser: argparse.ArgumentParser, json_flag: bool = True) -> None:
    """Add --path and optionally --json to a subcommand parser."""
    parser.add_argument("--path", default=".", help="Repository path (default: .)")
    if json_flag:
        parser.add_argument(
            "--json",
            action="store_true",
            dest="json_output",
            help="Output as JSON",
        )


def _read_json_input(args: argparse.Namespace, attr: str = "content") -> Any:
    """Resolve JSON from a positional arg, --file/-f, or stdin.

    Precedence: positional arg > --file/-f > stdin (if not a TTY).
    Raises SystemExit(1) with a message if none provide valid JSON.
    """
    raw: str | None = None

    # 1. Positional arg
    value = getattr(args, attr, None)
    if value is not None:
        raw = value

    # 2. --file / -f
    if raw is None:
        file_path = getattr(args, "file", None)
        if file_path is not None:
            try:
                raw = Path(file_path).read_text(encoding="utf-8")
            except OSError as exc:
                _error(f"Cannot read file {file_path!r}: {exc}")

    # 3. stdin (only if not a TTY)
    if raw is None:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()

    if raw is None:
        _error(
            "No JSON input provided. Pass inline JSON, use -f FILE, or pipe via stdin."
        )

    try:
        return json.loads(raw)  # type: ignore[arg-type]
    except json.JSONDecodeError as exc:
        _error(f"Invalid JSON: {exc}")


def _read_text_input(args: argparse.Namespace, attr: str = "content") -> str:
    """Resolve text from a positional arg, --file/-f, or stdin.

    Precedence: positional arg > --file/-f > stdin (if not a TTY).
    Raises SystemExit(1) if no input is found.
    """
    # 1. Positional arg
    value = getattr(args, attr, None)
    if value is not None:
        return value  # type: ignore[return-value]

    # 2. --file / -f
    file_path = getattr(args, "file", None)
    if file_path is not None:
        try:
            return Path(file_path).read_text(encoding="utf-8")
        except OSError as exc:
            _error(f"Cannot read file {file_path!r}: {exc}")

    # 3. stdin
    if not sys.stdin.isatty():
        return sys.stdin.read()

    _error("No text input provided. Pass inline text, use -f FILE, or pipe via stdin.")


def _output(data: Any, args: argparse.Namespace) -> None:
    """Print data as JSON or human-readable depending on --json flag."""
    if getattr(args, "json_output", False):
        print(json.dumps(data, indent=2))
    else:
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                print(item)
        else:
            print(data)


def _error(msg: str) -> int:
    """Print an error message to stderr and exit with code 1."""
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Handler: top-level init
# ---------------------------------------------------------------------------


def _handle_init(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    course_type = getattr(args, "type", "course") or "course"
    try:
        result = init_course(root, course_type)
    except CurikError as exc:
        return _error(str(exc))

    created = result.get("created", [])
    updated = result.get("updated", [])
    existing = result.get("existing", [])

    if created:
        print("Created:")
        for p in created:
            print(f"  {p}")
    if updated:
        print("Updated:")
        for p in updated:
            print(f"  {p}")
    if existing and not created and not updated:
        print("Everything up to date.")

    print()
    print("Curik is ready. Open Claude Code in this directory and say:")
    print()
    print('  "Start Curik"')
    print()
    print("The /curik skill walks you through the curriculum development process.")
    return 0


# ---------------------------------------------------------------------------
# Handler: top-level status
# ---------------------------------------------------------------------------


def _handle_status(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    try:
        result = get_course_status(root)
    except CurikError as exc:
        return _error(str(exc))
    _output(result, args)
    return 0


# ---------------------------------------------------------------------------
# Handler: phase group
# ---------------------------------------------------------------------------


def _handle_phase(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.phase_command

    if sub == "get":
        try:
            result = get_phase(root)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "advance":
        try:
            advance_phase(root, args.target)
        except CurikError as exc:
            return _error(str(exc))
        print(f"Advanced to phase: {args.target}")

    elif sub == "advance-sub":
        try:
            result = advance_sub_phase(root)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    return 0


# ---------------------------------------------------------------------------
# Handler: spec group
# ---------------------------------------------------------------------------


def _handle_spec(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.spec_command

    if sub == "get":
        try:
            text = get_spec(root)
        except CurikError as exc:
            return _error(str(exc))
        print(text, end="")

    elif sub == "update":
        content = _read_text_input(args)
        try:
            update_spec(root, args.section, content)
        except CurikError as exc:
            return _error(str(exc))
        print(f"Updated spec section: {args.section}")

    elif sub == "record-concept":
        content = _read_text_input(args)
        try:
            record_course_concept(root, content)
        except CurikError as exc:
            return _error(str(exc))
        print("Recorded course concept.")

    elif sub == "record-model":
        content = _read_text_input(args)
        try:
            record_pedagogical_model(root, content)
        except CurikError as exc:
            return _error(str(exc))
        print("Recorded pedagogical model.")

    elif sub == "record-alignment":
        content = _read_text_input(args)
        try:
            record_alignment(root, content)
        except CurikError as exc:
            return _error(str(exc))
        print("Recorded alignment decision.")

    return 0


# ---------------------------------------------------------------------------
# Handler: config group
# ---------------------------------------------------------------------------


def _handle_config(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.config_command

    if sub == "update":
        updates = _read_json_input(args)
        if not isinstance(updates, dict):
            return _error("JSON input must be an object (key-value pairs).")
        try:
            result = update_course_yml(root, updates)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    return 0


# ---------------------------------------------------------------------------
# Handler: scaffold group
# ---------------------------------------------------------------------------


def _handle_scaffold(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.scaffold_command

    if sub == "structure":
        structure = _read_json_input(args)
        if not isinstance(structure, dict):
            return _error("JSON input must be an object with a 'modules' key.")
        try:
            result = scaffold_structure(root, structure)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "lesson":
        try:
            path = create_lesson_stub(root, args.module, args.lesson, args.tier)
        except CurikError as exc:
            return _error(str(exc))
        print(f"Created: {path}")

    elif sub == "outline":
        content = _read_text_input(args)
        try:
            path = create_outline(root, args.name, content)
        except CurikError as exc:
            return _error(str(exc))
        print(f"Created outline: {path}")

    elif sub == "approve-outline":
        try:
            path = approve_outline(root, args.name)
        except CurikError as exc:
            return _error(str(exc))
        print(f"Approved outline: {path}")

    elif sub == "get-outline":
        try:
            text = get_outline(root, args.name)
        except CurikError as exc:
            return _error(str(exc))
        print(text, end="")

    elif sub == "change-plan":
        items_raw = _read_json_input(args, attr="items_json")
        if not isinstance(items_raw, list):
            return _error("JSON input must be a list of strings.")
        try:
            path = generate_change_plan(root, args.title, items_raw)
        except CurikError as exc:
            return _error(str(exc))
        print(f"Created change plan: {path}")

    return 0


# ---------------------------------------------------------------------------
# Handler: issue group
# ---------------------------------------------------------------------------


def _handle_issue(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.issue_command

    if sub == "create":
        content = _read_text_input(args)
        try:
            result = create_issue(root, args.title, content)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "list":
        status = getattr(args, "status", "open") or "open"
        try:
            result = list_issues(root, status)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    return 0


# ---------------------------------------------------------------------------
# Handler: plan group
# ---------------------------------------------------------------------------


def _handle_plan(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.plan_command

    if sub == "create":
        issue_numbers = _read_json_input(args, attr="issue_numbers_json")
        if not isinstance(issue_numbers, list):
            return _error("JSON input must be a list of issue numbers.")
        try:
            result = create_change_plan(root, args.title, issue_numbers)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "register":
        try:
            result = register_change_plan(root, args.plan_number)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "approve":
        try:
            result = approve_change_plan(root, args.plan_number)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "execute":
        try:
            result = execute_change_plan(root, args.plan_number)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "review":
        gaps: list[str] = []
        gaps_json = getattr(args, "gaps_json", None)
        if gaps_json:
            try:
                gaps = json.loads(gaps_json)
            except json.JSONDecodeError as exc:
                return _error(f"Invalid JSON in --gaps-json: {exc}")
        try:
            result = review_change_plan(root, args.plan_number, gaps)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "close":
        try:
            result = close_change_plan(root, args.plan_number)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    return 0


# ---------------------------------------------------------------------------
# Handler: migrate group
# ---------------------------------------------------------------------------


def _handle_migrate(args: argparse.Namespace) -> int:
    sub = args.migrate_command

    if sub == "inventory":
        try:
            result = inventory_course(args.repo_path)
        except CurikError as exc:
            return _error(str(exc))
        if getattr(args, "json_output", False):
            print(json.dumps(result, indent=2))
        else:
            _output(result, args)

    elif sub == "sequester":
        root = Path(args.path).resolve()
        try:
            result = sequester_content(root)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "structure":
        root = Path(args.path).resolve()
        modules = _read_json_input(args, attr="modules_json")
        if not isinstance(modules, list):
            return _error("JSON input must be a list of module names.")
        try:
            result = migrate_structure(root, args.tier, modules)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "hugo-layout":
        root = Path(args.path).resolve()
        try:
            result = migrate_hugo_layout(
                root,
                dry_run=args.dry_run,
                force=args.force,
                verify=args.verify,
            )
        except RuntimeError as exc:
            return _error(str(exc))
        if not args.dry_run:
            _output(result, args)

    return 0


# ---------------------------------------------------------------------------
# Handler: validate group
# ---------------------------------------------------------------------------


def _handle_validate(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.validate_command

    if sub == "lesson":
        tier = getattr(args, "tier", None)
        try:
            result = validate_lesson(root, args.lesson_path, tier=tier)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "module":
        try:
            result = validate_module(root, args.module_path)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "course":
        tier = getattr(args, "tier", None)
        try:
            result = validate_course(root, tier=tier)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "get-report":
        try:
            result = get_validation_report(root)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "save-report":
        report = _read_json_input(args, attr="report_json")
        if not isinstance(report, dict):
            return _error("JSON input must be an object.")
        try:
            result = save_validation_report(root, report)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    return 0


# ---------------------------------------------------------------------------
# Handler: syllabus group
# ---------------------------------------------------------------------------


def _handle_syllabus(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.syllabus_command

    if sub == "write-url":
        try:
            result = write_syllabus_url(root, args.uid, args.url)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "validate":
        try:
            result = validate_syllabus_consistency(root)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    return 0


# ---------------------------------------------------------------------------
# Handler: hugo group
# ---------------------------------------------------------------------------


def _handle_hugo(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.hugo_command

    if sub == "pages":
        section = getattr(args, "section", None)
        try:
            result = list_content_pages(root, section=section)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "create-page":
        extra_fm: dict | None = None
        fm_json = getattr(args, "frontmatter_json", None)
        if fm_json:
            try:
                extra_fm = json.loads(fm_json)
            except json.JSONDecodeError as exc:
                return _error(f"Invalid JSON in --frontmatter-json: {exc}")
        content_text = getattr(args, "content", "") or ""
        try:
            path = create_content_page(
                root, args.page_path, args.title,
                content=content_text,
                extra_frontmatter=extra_fm,
            )
        except CurikError as exc:
            return _error(str(exc))
        print(f"Created: {path}")

    elif sub == "update-frontmatter":
        updates = _read_json_input(args, attr="updates_json")
        if not isinstance(updates, dict):
            return _error("JSON input must be an object.")
        try:
            result = update_frontmatter(root, args.page_path, updates)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    elif sub == "setup":
        title = getattr(args, "title", None)
        tier = getattr(args, "tier", None)
        if title is not None:
            # Explicit title+tier provided — call hugo_setup directly
            effective_tier = tier if tier is not None else 2
            try:
                result = hugo_setup(root, title, effective_tier)
            except Exception as exc:
                return _error(str(exc))
        else:
            # No title — read from course.yml
            try:
                result = hugo_setup_from_course(root)
            except Exception as exc:
                return _error(str(exc))
        _output(result, args)

    elif sub == "bump-version":
        try:
            new_version = bump_curriculum_version(root)
        except (FileNotFoundError, ValueError) as exc:
            return _error(str(exc))
        _output({"version": new_version}, args)

    elif sub == "build":
        try:
            result = hugo_build(root)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    return 0


# ---------------------------------------------------------------------------
# Handler: readme group
# ---------------------------------------------------------------------------


def _handle_readme(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.readme_command

    if sub == "generate":
        docs_dir = getattr(args, "docs_dir", "site/content") or "site/content"
        try:
            result = generate_readmes(root, docs_dir=docs_dir)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    return 0


# ---------------------------------------------------------------------------
# Handler: publish group
# ---------------------------------------------------------------------------


def _handle_publish(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    sub = args.publish_command

    if sub == "guide":
        try:
            text = get_publish_guide(root)
        except CurikError as exc:
            return _error(str(exc))
        print(text, end="")

    elif sub == "check":
        try:
            result = check_publish_ready(root)
        except CurikError as exc:
            return _error(str(exc))
        _output(result, args)

    return 0


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="curik",
        description="Curik curriculum development tool",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version('curik')}",
    )

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # ── init ──────────────────────────────────────────────────────────────
    init_p = sub.add_parser("init", help="Initialize Curik files in a repo")
    init_p.add_argument(
        "--type",
        choices=["course", "resource-collection"],
        default="course",
        help="Course type (default: course)",
    )
    init_p.add_argument("--path", default=".", help="Repository path (default: .)")

    # ── status ────────────────────────────────────────────────────────────
    status_p = sub.add_parser("status", help="Show course status")
    _add_common_args(status_p)

    # ── phase ─────────────────────────────────────────────────────────────
    phase_p = sub.add_parser("phase", help="Phase management commands")
    phase_sub = phase_p.add_subparsers(dest="phase_command", metavar="SUBCOMMAND")

    ph_get = phase_sub.add_parser("get", help="Get current phase info")
    _add_common_args(ph_get)

    ph_adv = phase_sub.add_parser("advance", help="Advance to a target phase")
    ph_adv.add_argument("target", help="Target phase (e.g. phase2)")
    ph_adv.add_argument("--path", default=".", help="Repository path")

    ph_advsub = phase_sub.add_parser("advance-sub", help="Advance to next sub-phase")
    _add_common_args(ph_advsub)

    # ── spec ──────────────────────────────────────────────────────────────
    spec_p = sub.add_parser("spec", help="Spec management commands")
    spec_sub = spec_p.add_subparsers(dest="spec_command", metavar="SUBCOMMAND")

    sp_get = spec_sub.add_parser("get", help="Print the course spec")
    sp_get.add_argument("--path", default=".", help="Repository path")

    sp_update = spec_sub.add_parser("update", help="Update a spec section")
    sp_update.add_argument("section", help="Spec section key")
    sp_update.add_argument("content", nargs="?", help="Content (or use -f/stdin)")
    sp_update.add_argument("-f", "--file", help="Read content from file")
    sp_update.add_argument("--path", default=".", help="Repository path")

    sp_concept = spec_sub.add_parser("record-concept", help="Record course concept")
    sp_concept.add_argument("content", nargs="?", help="Content (or use -f/stdin)")
    sp_concept.add_argument("-f", "--file", help="Read content from file")
    sp_concept.add_argument("--path", default=".", help="Repository path")

    sp_model = spec_sub.add_parser("record-model", help="Record pedagogical model")
    sp_model.add_argument("content", nargs="?", help="Content (or use -f/stdin)")
    sp_model.add_argument("-f", "--file", help="Read content from file")
    sp_model.add_argument("--path", default=".", help="Repository path")

    sp_align = spec_sub.add_parser("record-alignment", help="Record alignment decision")
    sp_align.add_argument("content", nargs="?", help="Content (or use -f/stdin)")
    sp_align.add_argument("-f", "--file", help="Read content from file")
    sp_align.add_argument("--path", default=".", help="Repository path")

    # ── config ────────────────────────────────────────────────────────────
    config_p = sub.add_parser("config", help="Config management commands")
    config_sub = config_p.add_subparsers(dest="config_command", metavar="SUBCOMMAND")

    cfg_update = config_sub.add_parser("update", help="Update course.yml fields")
    cfg_update.add_argument(
        "content", nargs="?", metavar="UPDATES_JSON",
        help="JSON object of field updates (or use -f/stdin)",
    )
    cfg_update.add_argument("-f", "--file", help="Read JSON from file")
    _add_common_args(cfg_update)

    # ── scaffold ──────────────────────────────────────────────────────────
    scaffold_p = sub.add_parser("scaffold", help="Scaffolding commands")
    scaffold_sub = scaffold_p.add_subparsers(dest="scaffold_command", metavar="SUBCOMMAND")

    sc_struct = scaffold_sub.add_parser("structure", help="Scaffold course structure")
    sc_struct.add_argument(
        "content", nargs="?", metavar="STRUCTURE_JSON",
        help="JSON structure (or use -f/stdin)",
    )
    sc_struct.add_argument("-f", "--file", help="Read JSON from file")
    _add_common_args(sc_struct)

    sc_lesson = scaffold_sub.add_parser("lesson", help="Create a lesson stub")
    sc_lesson.add_argument("module", help="Module name")
    sc_lesson.add_argument("lesson", help="Lesson filename")
    sc_lesson.add_argument(
        "--tier", type=int, required=True, choices=[1, 2, 3, 4],
        help="Tier (1-4)",
    )
    sc_lesson.add_argument("--path", default=".", help="Repository path")

    sc_outline = scaffold_sub.add_parser("outline", help="Create an outline")
    sc_outline.add_argument("name", help="Outline name")
    sc_outline.add_argument("content", nargs="?", help="Content (or use -f/stdin)")
    sc_outline.add_argument("-f", "--file", help="Read content from file")
    sc_outline.add_argument("--path", default=".", help="Repository path")

    sc_approve = scaffold_sub.add_parser("approve-outline", help="Approve an outline")
    sc_approve.add_argument("name", help="Outline name")
    sc_approve.add_argument("--path", default=".", help="Repository path")

    sc_getout = scaffold_sub.add_parser("get-outline", help="Print an outline")
    sc_getout.add_argument("name", help="Outline name")
    sc_getout.add_argument("--path", default=".", help="Repository path")

    sc_cp = scaffold_sub.add_parser("change-plan", help="Generate a change plan")
    sc_cp.add_argument("title", help="Change plan title")
    sc_cp.add_argument(
        "items_json", nargs="?", metavar="ITEMS_JSON",
        help="JSON list of items (or use -f/stdin)",
    )
    sc_cp.add_argument("-f", "--file", help="Read JSON from file")
    sc_cp.add_argument("--path", default=".", help="Repository path")

    # ── issue ─────────────────────────────────────────────────────────────
    issue_p = sub.add_parser("issue", help="Issue management commands")
    issue_sub = issue_p.add_subparsers(dest="issue_command", metavar="SUBCOMMAND")

    iss_create = issue_sub.add_parser("create", help="Create an issue")
    iss_create.add_argument("title", help="Issue title")
    iss_create.add_argument("content", nargs="?", help="Issue body (or use -f/stdin)")
    iss_create.add_argument("-f", "--file", help="Read content from file")
    _add_common_args(iss_create)

    iss_list = issue_sub.add_parser("list", help="List issues")
    iss_list.add_argument(
        "--status", choices=["open", "done"], default="open",
        help="Filter by status (default: open)",
    )
    _add_common_args(iss_list)

    # ── plan ──────────────────────────────────────────────────────────────
    plan_p = sub.add_parser("plan", help="Change plan commands")
    plan_sub = plan_p.add_subparsers(dest="plan_command", metavar="SUBCOMMAND")

    pl_create = plan_sub.add_parser("create", help="Create a change plan")
    pl_create.add_argument("title", help="Plan title")
    pl_create.add_argument(
        "issue_numbers_json", nargs="?", metavar="ISSUE_NUMBERS_JSON",
        help="JSON list of issue numbers (or use -f/stdin)",
    )
    pl_create.add_argument("-f", "--file", help="Read JSON from file")
    _add_common_args(pl_create)

    pl_register = plan_sub.add_parser("register", help="Register a change plan")
    pl_register.add_argument("plan_number", type=int, help="Plan number")
    _add_common_args(pl_register)

    pl_approve = plan_sub.add_parser("approve", help="Approve a change plan")
    pl_approve.add_argument("plan_number", type=int, help="Plan number")
    _add_common_args(pl_approve)

    pl_execute = plan_sub.add_parser("execute", help="Execute a change plan")
    pl_execute.add_argument("plan_number", type=int, help="Plan number")
    _add_common_args(pl_execute)

    pl_review = plan_sub.add_parser("review", help="Review a change plan")
    pl_review.add_argument("plan_number", type=int, help="Plan number")
    pl_review.add_argument("--gaps-json", dest="gaps_json", help="JSON list of gaps")
    _add_common_args(pl_review)

    pl_close = plan_sub.add_parser("close", help="Close a change plan")
    pl_close.add_argument("plan_number", type=int, help="Plan number")
    _add_common_args(pl_close)

    # ── migrate ───────────────────────────────────────────────────────────
    migrate_p = sub.add_parser("migrate", help="Migration commands")
    migrate_sub = migrate_p.add_subparsers(dest="migrate_command", metavar="SUBCOMMAND")

    mg_inv = migrate_sub.add_parser("inventory", help="Inventory a course repo")
    mg_inv.add_argument("repo_path", help="Path to course repository")
    mg_inv.add_argument(
        "--json", action="store_true", dest="json_output", help="JSON output",
    )

    mg_seq = migrate_sub.add_parser("sequester", help="Sequester existing content")
    _add_common_args(mg_seq)

    mg_str = migrate_sub.add_parser("structure", help="Migrate course structure")
    mg_str.add_argument("--tier", type=int, required=True, help="Tier (1-4)")
    mg_str.add_argument(
        "modules_json", nargs="?", metavar="MODULES_JSON",
        help="JSON list of module names (or use -f/stdin)",
    )
    mg_str.add_argument("-f", "--file", help="Read JSON from file")
    _add_common_args(mg_str)

    mg_hl = migrate_sub.add_parser(
        "hugo-layout",
        help="Migrate Hugo files from root to site/ subdirectory",
    )
    mg_hl.add_argument(
        "--dry-run", dest="dry_run", action="store_true",
        help="Print planned moves without making any changes",
    )
    mg_hl.add_argument(
        "--force", action="store_true",
        help="Skip dirty-tree check (proceed even with uncommitted changes)",
    )
    mg_hl.add_argument(
        "--verify", action="store_true",
        help="Run 'hugo --source site' after migration to verify the build",
    )
    mg_hl.add_argument("--path", default=".", help="Repository path (default: .)")

    # ── validate ──────────────────────────────────────────────────────────
    validate_p = sub.add_parser("validate", help="Validation commands")
    validate_sub = validate_p.add_subparsers(dest="validate_command", metavar="SUBCOMMAND")

    vl_lesson = validate_sub.add_parser("lesson", help="Validate a lesson file")
    vl_lesson.add_argument("lesson_path", help="Lesson file path (relative to repo root)")
    vl_lesson.add_argument("--tier", type=int, help="Tier (1-4)")
    _add_common_args(vl_lesson)

    vl_module = validate_sub.add_parser("module", help="Validate a module directory")
    vl_module.add_argument("module_path", help="Module directory path")
    _add_common_args(vl_module)

    vl_course = validate_sub.add_parser("course", help="Validate the entire course")
    vl_course.add_argument("--tier", type=int, help="Tier (1-4)")
    _add_common_args(vl_course)

    vl_report = validate_sub.add_parser("get-report", help="Get saved validation report")
    _add_common_args(vl_report)

    vl_save = validate_sub.add_parser("save-report", help="Save a validation report")
    vl_save.add_argument(
        "report_json", nargs="?", metavar="REPORT_JSON",
        help="JSON report object (or use -f/stdin)",
    )
    vl_save.add_argument("-f", "--file", help="Read JSON from file")
    _add_common_args(vl_save)

    # ── syllabus ──────────────────────────────────────────────────────────
    syllabus_p = sub.add_parser("syllabus", help="Syllabus commands")
    syllabus_sub = syllabus_p.add_subparsers(dest="syllabus_command", metavar="SUBCOMMAND")

    sy_write = syllabus_sub.add_parser("write-url", help="Write a syllabus URL")
    sy_write.add_argument("uid", help="Lesson UID")
    sy_write.add_argument("url", help="Lesson URL")
    _add_common_args(sy_write)

    sy_val = syllabus_sub.add_parser("validate", help="Validate syllabus consistency")
    _add_common_args(sy_val)

    # ── hugo ──────────────────────────────────────────────────────────────
    hugo_p = sub.add_parser("hugo", help="Hugo site commands")
    hugo_sub = hugo_p.add_subparsers(dest="hugo_command", metavar="SUBCOMMAND")

    hg_pages = hugo_sub.add_parser("pages", help="List content pages")
    hg_pages.add_argument("--section", help="Limit to a section of content/")
    _add_common_args(hg_pages)

    hg_create = hugo_sub.add_parser("create-page", help="Create a content page")
    hg_create.add_argument("page_path", help="Page path under content/")
    hg_create.add_argument("title", help="Page title")
    hg_create.add_argument("--content", dest="content", help="Page body content")
    hg_create.add_argument(
        "--frontmatter-json", dest="frontmatter_json",
        help="Extra frontmatter fields as JSON",
    )
    hg_create.add_argument("--path", default=".", help="Repository path")

    hg_fm = hugo_sub.add_parser("update-frontmatter", help="Update page frontmatter")
    hg_fm.add_argument("page_path", help="Page path under content/")
    hg_fm.add_argument(
        "updates_json", nargs="?", metavar="UPDATES_JSON",
        help="JSON object of frontmatter updates (or use -f/stdin)",
    )
    hg_fm.add_argument("-f", "--file", help="Read JSON from file")
    _add_common_args(hg_fm)

    hg_setup = hugo_sub.add_parser("setup", help="Set up Hugo configuration and theme")
    hg_setup.add_argument("--title", help="Course title (reads from course.yml if omitted)")
    hg_setup.add_argument("--tier", type=int, help="Tier (1-4)")
    _add_common_args(hg_setup)

    hg_bump = hugo_sub.add_parser("bump-version", help="Bump curriculum version in hugo.toml")
    _add_common_args(hg_bump)

    hg_build = hugo_sub.add_parser("build", help="Run Hugo build")
    _add_common_args(hg_build)

    # ── readme ────────────────────────────────────────────────────────────
    readme_p = sub.add_parser("readme", help="README generation commands")
    readme_sub = readme_p.add_subparsers(dest="readme_command", metavar="SUBCOMMAND")

    rm_gen = readme_sub.add_parser("generate", help="Generate README files from lesson guards")
    rm_gen.add_argument(
        "--docs-dir", dest="docs_dir", default="site/content",
        help="Docs directory (default: site/content)",
    )
    _add_common_args(rm_gen)

    # ── publish ───────────────────────────────────────────────────────────
    publish_p = sub.add_parser("publish", help="Publish readiness commands")
    publish_sub = publish_p.add_subparsers(dest="publish_command", metavar="SUBCOMMAND")

    pub_guide = publish_sub.add_parser("guide", help="Show publishing guide")
    pub_guide.add_argument("--path", default=".", help="Repository path")

    pub_check = publish_sub.add_parser("check", help="Check publish readiness")
    _add_common_args(pub_check)

    # Suppress unused-variable warnings for parsers we define but don't name
    _ = (
        status_p, phase_p, spec_p, config_p, scaffold_p, issue_p, plan_p,
        migrate_p, validate_p, syllabus_p, hugo_p, readme_p, publish_p,
        ph_get, ph_adv, ph_advsub, sp_get, sp_update, sp_concept, sp_model,
        sp_align, cfg_update, sc_struct, sc_lesson, sc_outline, sc_approve,
        sc_getout, sc_cp, iss_create, iss_list, pl_create, pl_register,
        pl_approve, pl_execute, pl_review, pl_close, mg_inv, mg_seq, mg_str, mg_hl,
        vl_lesson, vl_module, vl_course, vl_report, vl_save, sy_write,
        sy_val, hg_pages, hg_create, hg_fm, hg_setup, hg_bump, hg_build,
        rm_gen, pub_guide, pub_check,
    )

    return parser


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------

_GROUP_HANDLERS = {
    "init": _handle_init,
    "status": _handle_status,
    "phase": _handle_phase,
    "spec": _handle_spec,
    "config": _handle_config,
    "scaffold": _handle_scaffold,
    "issue": _handle_issue,
    "plan": _handle_plan,
    "migrate": _handle_migrate,
    "validate": _handle_validate,
    "syllabus": _handle_syllabus,
    "hugo": _handle_hugo,
    "readme": _handle_readme,
    "publish": _handle_publish,
}

# Subcommand attribute names for each group (used to detect missing subcommand)
_GROUP_SUBCMD_ATTR = {
    "phase": "phase_command",
    "spec": "spec_command",
    "config": "config_command",
    "scaffold": "scaffold_command",
    "issue": "issue_command",
    "plan": "plan_command",
    "migrate": "migrate_command",
    "validate": "validate_command",
    "syllabus": "syllabus_command",
    "hugo": "hugo_command",
    "readme": "readme_command",
    "publish": "publish_command",
}


def main(argv: list[str] | None = None) -> int:
    """Entry point for the curik CLI."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    # Emit legacy-layout warning before any command, except when running the
    # migration command itself (that's the resolution action, no need to warn).
    if not (
        args.command == "migrate"
        and getattr(args, "migrate_command", None) == "hugo-layout"
    ):
        root = Path(getattr(args, "path", ".")).resolve()
        warn = check_legacy_hugo_layout(root)
        if warn:
            print(warn, file=sys.stderr)

    handler = _GROUP_HANDLERS.get(args.command)
    if handler is None:
        parser.print_help()
        return 1

    # Check that a subcommand was provided for group commands
    subcmd_attr = _GROUP_SUBCMD_ATTR.get(args.command)
    if subcmd_attr is not None:
        subcmd_value = getattr(args, subcmd_attr, None)
        if subcmd_value is None:
            # Find the sub-parser for this group and print its help
            for action in parser._subparsers._group_actions:  # type: ignore[attr-defined]
                if hasattr(action, "_name_parser_map"):
                    group_parser = action._name_parser_map.get(args.command)
                    if group_parser:
                        group_parser.print_help()
                        return 1

    return handler(args)
