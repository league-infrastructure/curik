from __future__ import annotations

import json
from pathlib import Path

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


CURIK_DIR = ".curik"
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
            {"phase": "phase1", "type": course_type}, indent=2
        )
        + "\n",
        root / "course.yml": (
            "title: TBD\n"
            "slug: TBD\n"
            f"uid: {generate_course_uid()}\n"
            f"type: {course_type}\n"
            "tier: TBD\n"
            "grades: TBD\n"
            "category: TBD\n"
            "topics: []\n"
            "prerequisites: []\n"
            "lessons: 0\n"
            "estimated_weeks: 0\n"
            "curriculum_url: TBD\n"
            "repo_url: TBD\n"
            "description: TBD\n"
        ),
        root / ".mcp.json": json.dumps(
            {"mcpServers": {"curik": {"command": "curik", "args": ["mcp"]}}},
            indent=2,
        )
        + "\n",
    }
    for path, content in defaults.items():
        if path.exists():
            existing.append(str(path.relative_to(root)))
            continue
        path.write_text(content, encoding="utf-8")
        created.append(str(path.relative_to(root)))

    return {"created": sorted(created), "existing": sorted(existing)}


def _read_state(root: Path) -> dict[str, str]:
    state_path = _state_file(root)
    if not state_path.exists():
        raise CurikError("Course not initialized. Run 'curik init'.")
    return json.loads(state_path.read_text(encoding="utf-8"))


RESOURCE_COLLECTION_SKIP_SECTIONS = {"pedagogical-model", "alignment-decision"}
"""Spec sections skipped for resource-collection projects."""


def get_phase(root: Path) -> dict[str, str | list[str]]:
    state = _read_state(root)
    course_type = state.get("type", "course")
    requirements: list[str] = []
    if state["phase"] == "phase1":
        requirements = list(SPEC_SECTION_HEADINGS.keys())
        if course_type == "resource-collection":
            requirements = [
                r for r in requirements
                if r not in RESOURCE_COLLECTION_SKIP_SECTIONS
            ]
    return {"phase": state["phase"], "requirements": requirements}


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
