from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .init_command import run_init
from .uid import generate_course_uid

SPEC_SECTION_HEADINGS: dict[str, str] = {
    "course-concept": "## Course Concept",
    "pedagogical-model": "## Pedagogical Model",
    "research-summary": "## Research Summary",
    "alignment-decision": "## Alignment Decision",
    "course-structure-outline": "## Course Structure Outline",
    "assessment-plan": "## Assessment Plan",
    "technical-decisions": "## Technical Decisions",
}


CURIK_DIR = ".course"
"""Name of the hidden directory created inside each project root."""


class CurikError(ValueError):
    pass


def _course_dir(root: Path) -> Path:
    return root / CURIK_DIR


def _state_file(root: Path) -> Path:
    return _course_dir(root) / "state.json"


def _spec_file(root: Path) -> Path:
    return _course_dir(root) / "spec.md"


def _default_spec() -> str:
    blocks = ["# Curik Course Specification", ""]
    for heading in SPEC_SECTION_HEADINGS.values():
        blocks.extend([heading, "TBD", ""])
    return "\n".join(blocks).rstrip() + "\n"


VALID_COURSE_TYPES = ("course", "resource-collection")
"""Allowed values for the ``course_type`` parameter."""


def _course_yml_template(course_type: str, uid: str) -> dict[str, Any]:
    """Return the canonical course.yml fields with defaults."""
    return {
        "title": "TBD",
        "slug": "TBD",
        "uid": uid,
        "type": course_type,
        "tier": "TBD",
        "grades": "TBD",
        "category": "TBD",
        "topics": [],
        "prerequisites": [],
        "lessons": 0,
        "estimated_weeks": 0,
        "curriculum_url": "TBD",
        "repo_url": "TBD",
        "description": "TBD",
    }


def _merge_course_yml(root: Path, course_type: str) -> tuple[str, str]:
    """Create or merge course.yml. Returns (content, status).

    If course.yml doesn't exist, creates it with defaults.
    If it exists, merges: known fields are updated (old values kept if not TBD),
    unknown fields from the old file go into an ``old:`` subsection.
    Status is "created", "updated", or "unchanged".
    """
    course_yml = root / "course.yml"
    uid = generate_course_uid()
    template = _course_yml_template(course_type, uid)
    template_keys = set(template.keys())

    if not course_yml.exists():
        lines = []
        for key, value in template.items():
            if isinstance(value, list):
                lines.append(f"{key}: {json.dumps(value)}")
            else:
                lines.append(f"{key}: {value}")
        lines.append("")
        content = "\n".join(lines)
        return content, "created"

    # Read existing
    old_text = course_yml.read_text(encoding="utf-8")
    try:
        old_data = yaml.safe_load(old_text)
        if not isinstance(old_data, dict):
            old_data = {}
    except yaml.YAMLError:
        old_data = {}

    # Merge: template fields first, preserving old non-TBD values
    merged: dict[str, Any] = {}
    for key, default in template.items():
        old_val = old_data.get(key)
        if old_val is not None and old_val != "TBD":
            merged[key] = old_val
        elif key == "uid" and "uid" in old_data:
            # Always keep existing uid
            merged[key] = old_data["uid"]
        elif key == "type" and "type" in old_data:
            merged[key] = old_data["type"]
        else:
            merged[key] = default

    # Collect unknown keys into "old" subsection
    unknown = {k: v for k, v in old_data.items() if k not in template_keys and k != "old"}

    # Build output
    lines = []
    for key, value in merged.items():
        if isinstance(value, list):
            lines.append(f"{key}: {json.dumps(value)}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        else:
            lines.append(f"{key}: {value}")

    if unknown:
        lines.append("")
        lines.append("# Fields from previous course.yml not in the current template.")
        lines.append("# Move these to the appropriate place or delete if no longer needed.")
        lines.append("old:")
        for key, value in unknown.items():
            if isinstance(value, list):
                lines.append(f"  {key}: {json.dumps(value)}")
            elif isinstance(value, dict):
                lines.append(f"  {key}:")
                for k2, v2 in value.items():
                    lines.append(f"    {k2}: {v2}")
            else:
                lines.append(f"  {key}: {value}")

    lines.append("")
    content = "\n".join(lines)

    if content == old_text:
        return content, "unchanged"
    return content, "updated"


def init_course(
    root: Path, course_type: str = "course"
) -> dict[str, list[str]]:
    if course_type not in VALID_COURSE_TYPES:
        raise CurikError(
            f"Invalid course_type: {course_type!r}. "
            f"Must be one of {VALID_COURSE_TYPES}."
        )
    root = root.resolve()
    created: list[str] = []
    updated: list[str] = []
    existing: list[str] = []
    course_dir = _course_dir(root)
    dirs = [
        course_dir,
        course_dir / "outlines",
        course_dir / "change-plan" / "active",
        course_dir / "change-plan" / "done",
        course_dir / "issues" / "open",
        course_dir / "issues" / "done",
    ]
    for directory in dirs:
        if directory.exists():
            existing.append(str(directory.relative_to(root)))
        else:
            directory.mkdir(parents=True, exist_ok=True)
            created.append(str(directory.relative_to(root)))

    defaults = {
        course_dir / "spec.md": _default_spec(),
        course_dir / "overview.md": "# Course Overview\n\nTBD\n",
        course_dir / "research.md": "# Research Findings\n\nTBD\n",
        _state_file(root): json.dumps(
            {"phase": "phase1", "sub_phase": "1a", "type": course_type}, indent=2
        )
        + "\n",
    }
    for path, content in defaults.items():
        if path.exists():
            existing.append(str(path.relative_to(root)))
            continue
        path.write_text(content, encoding="utf-8")
        created.append(str(path.relative_to(root)))

    # course.yml: create or merge (preserves old values, collects unknowns)
    course_yml_path = root / "course.yml"
    course_yml_content, course_yml_status = _merge_course_yml(root, course_type)
    if course_yml_status == "created":
        course_yml_path.write_text(course_yml_content, encoding="utf-8")
        created.append("course.yml")
    elif course_yml_status == "updated":
        course_yml_path.write_text(course_yml_content, encoding="utf-8")
        updated.append("course.yml")
    else:
        existing.append("course.yml")

    # .mcp.json is curik-owned — always update to latest config
    mcp_json_path = root / ".mcp.json"
    mcp_json_content = json.dumps(
        {"mcpServers": {"curik": {"command": "curik", "args": ["mcp"]}}},
        indent=2,
    ) + "\n"
    rel_mcp = str(mcp_json_path.relative_to(root))
    if mcp_json_path.exists():
        if mcp_json_path.read_text(encoding="utf-8") == mcp_json_content:
            existing.append(rel_mcp)
        else:
            mcp_json_path.write_text(mcp_json_content, encoding="utf-8")
            created.append(rel_mcp)
    else:
        mcp_json_path.write_text(mcp_json_content, encoding="utf-8")
        created.append(rel_mcp)

    # Install CLAUDE.md section, /curik skill, and MCP permissions
    init_result = run_init(root)
    for path in init_result.get("created", []):
        created.append(path)
    for path in init_result.get("unchanged", []):
        existing.append(path)
    for path in init_result.get("updated", []):
        updated.append(path)

    return {
        "created": sorted(created),
        "updated": sorted(updated),
        "existing": sorted(existing),
    }


def _read_state(root: Path) -> dict[str, str]:
    state_path = _state_file(root)
    if not state_path.exists():
        raise CurikError("Course not initialized. Run 'curik init'.")
    return json.loads(state_path.read_text(encoding="utf-8"))


RESOURCE_COLLECTION_SKIP_SECTIONS = {"pedagogical-model", "alignment-decision"}
"""Spec sections skipped for resource-collection projects."""

PHASE1_SUB_PHASES = ("1a", "1b", "1c", "1d", "1e")
"""Ordered sub-phases within Phase 1."""

RESOURCE_COLLECTION_SKIP_SUB_PHASES = {"1b", "1d"}
"""Sub-phases skipped for resource-collection projects."""


def get_phase(root: Path) -> dict[str, str | list[str]]:
    state = _read_state(root)
    course_type = state.get("type", "course")
    sub_phase = state.get("sub_phase", "1a")
    requirements: list[str] = []
    if state["phase"] == "phase1":
        requirements = list(SPEC_SECTION_HEADINGS.keys())
        if course_type == "resource-collection":
            requirements = [
                r for r in requirements
                if r not in RESOURCE_COLLECTION_SKIP_SECTIONS
            ]
    result: dict[str, str | list[str]] = {
        "phase": state["phase"],
        "requirements": requirements,
    }
    if state["phase"] == "phase1":
        result["sub_phase"] = sub_phase
    return result


def get_spec(root: Path) -> str:
    spec_path = _spec_file(root)
    if not spec_path.exists():
        raise CurikError("Spec file missing. Run 'curik init'.")
    return spec_path.read_text(encoding="utf-8")


def update_spec(root: Path, section: str, content: str) -> None:
    if section not in SPEC_SECTION_HEADINGS:
        raise CurikError(f"Unknown spec section: {section}")
    if not content or not content.strip():
        raise CurikError("Spec content cannot be empty.")
    text = get_spec(root)
    heading = SPEC_SECTION_HEADINGS[section]
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == heading), None)
    if start is None:
        raise CurikError(f"Missing heading in spec: {heading}")
    end = len(lines)
    for idx in range(start + 1, len(lines)):
        if lines[idx].startswith("## "):
            end = idx
            break
    updated = lines[: start + 1] + [content.strip(), ""] + lines[end:]
    _spec_file(root).write_text("\n".join(updated).rstrip() + "\n", encoding="utf-8")


def record_course_concept(root: Path, content: str) -> None:
    update_spec(root, "course-concept", content)


def record_pedagogical_model(root: Path, content: str) -> None:
    update_spec(root, "pedagogical-model", content)


def record_alignment(root: Path, content: str) -> None:
    update_spec(root, "alignment-decision", content)


def advance_sub_phase(root: Path) -> dict[str, str]:
    """Advance to the next Phase 1 sub-phase.

    For resource-collections, sub-phases 1b and 1d are skipped.
    Raises CurikError if already at 1e (use ``advance_phase`` to move to phase2).

    Returns ``{"old": old_sub_phase, "new": new_sub_phase}``.
    """
    root = root.resolve()
    state = _read_state(root)
    if state["phase"] != "phase1":
        raise CurikError("Cannot advance sub-phase: not in phase1.")

    course_type = state.get("type", "course")
    current = state.get("sub_phase", "1a")

    if current == "1e":
        raise CurikError(
            "Already at sub-phase 1e. Use advance_phase('phase2') to proceed."
        )

    idx = PHASE1_SUB_PHASES.index(current)
    # Find the next applicable sub-phase
    for candidate in PHASE1_SUB_PHASES[idx + 1:]:
        if (
            course_type == "resource-collection"
            and candidate in RESOURCE_COLLECTION_SKIP_SUB_PHASES
        ):
            continue
        state["sub_phase"] = candidate
        _state_file(root).write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        return {"old": current, "new": candidate}

    # Should not reach here since 1e is always valid
    raise CurikError("No valid sub-phase to advance to.")


def advance_phase(root: Path, target_phase: str) -> None:
    if target_phase != "phase2":
        raise CurikError("Only advancing to phase2 is supported in the initial version.")
    state = _read_state(root)
    course_type = state.get("type", "course")
    spec = get_spec(root)
    missing = []
    for section_key, heading in SPEC_SECTION_HEADINGS.items():
        if (
            course_type == "resource-collection"
            and section_key in RESOURCE_COLLECTION_SKIP_SECTIONS
        ):
            continue
        marker = f"{heading}\n"
        if marker not in spec:
            missing.append(section_key)
            continue
        segment = spec.split(marker, 1)[1]
        next_heading_index = segment.find("\n## ")
        body = segment[:next_heading_index] if next_heading_index >= 0 else segment
        body_lines = [line.strip() for line in body.splitlines() if line.strip()]
        if not body_lines or all(line == "TBD" for line in body_lines):
            missing.append(section_key)
    if missing:
        raise CurikError(
            f"Cannot advance to phase2; incomplete spec sections: {', '.join(missing)}"
        )

    state = _read_state(root)
    state["phase"] = "phase2"
    _state_file(root).write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def get_course_status(root: Path) -> dict[str, str | int]:
    """Return a summary of the course state: phase, open issues, active change plans."""
    root = root.resolve()
    state = _read_state(root)
    course_dir = _course_dir(root)

    open_issues = 0
    issues_dir = course_dir / "issues" / "open"
    if issues_dir.is_dir():
        open_issues = sum(1 for f in issues_dir.iterdir() if f.suffix == ".md")

    active_plans = 0
    plans_dir = course_dir / "change-plan" / "active"
    if plans_dir.is_dir():
        active_plans = sum(1 for f in plans_dir.iterdir() if f.suffix == ".md")

    return {
        "phase": state["phase"],
        "open_issues": open_issues,
        "active_change_plans": active_plans,
    }
