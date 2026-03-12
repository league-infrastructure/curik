"""Validation tools for lessons, modules, and courses."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .project import CurikError, _course_dir

INSTRUCTOR_GUIDE_FIELDS = [
    "Objectives",
    "Materials",
    "Timing",
    "Key concepts",
    "Common mistakes",
    "Assessment cues",
    "Differentiation",
]


def _parse_instructor_guide(text: str) -> dict[str, str]:
    """Extract field values from an instructor guide div block."""
    # Match <div class="instructor-guide"> ... </div>
    m = re.search(
        r'<div\s+class=["\']instructor-guide["\']\s*>(.*?)</div>',
        text,
        re.DOTALL,
    )
    if m is None:
        return {}
    block = m.group(1)
    fields: dict[str, str] = {}
    # Fields are bold labels followed by colon, e.g. **Objectives**: value
    for field in INSTRUCTOR_GUIDE_FIELDS:
        pattern = re.compile(
            rf'\*\*{re.escape(field)}\*\*\s*:\s*(.*?)(?=\*\*[A-Z]|\Z)',
            re.DOTALL,
        )
        fm = pattern.search(block)
        if fm:
            fields[field] = fm.group(1).strip()
    return fields


def validate_lesson(root: Path, lesson_path: str) -> dict:
    """Validate a single lesson file.

    Checks:
    - File exists
    - Has instructor guide div with all 7 required fields non-empty
    - Has learning objectives outside the instructor guide
    """
    root = root.resolve()
    full_path = root / lesson_path
    errors: list[str] = []

    if not full_path.exists():
        return {"valid": False, "errors": [f"Lesson file not found: {lesson_path}"]}

    text = full_path.read_text(encoding="utf-8")

    # Check for instructor guide div
    guide_match = re.search(
        r'<div\s+class=["\']instructor-guide["\']\s*>',
        text,
    )
    if not guide_match:
        errors.append("Missing instructor guide div")
    else:
        fields = _parse_instructor_guide(text)
        for field in INSTRUCTOR_GUIDE_FIELDS:
            if field not in fields:
                errors.append(f"Instructor guide missing field: {field}")
            elif not fields[field]:
                errors.append(f"Instructor guide field is empty: {field}")

    # Check for learning objectives outside the instructor guide
    # Remove the instructor guide block and check for objectives heading
    text_no_guide = re.sub(
        r'<div\s+class=["\']instructor-guide["\']\s*>.*?</div>',
        "",
        text,
        flags=re.DOTALL,
    )
    if not re.search(r'(?i)#+\s*learning\s+objectives?', text_no_guide):
        errors.append("Missing learning objectives section outside instructor guide")

    return {"valid": len(errors) == 0, "errors": errors}


def validate_module(root: Path, module_path: str) -> dict:
    """Validate a module directory.

    Checks:
    - Directory exists
    - Has README.md or overview file
    - All .md lesson files pass validate_lesson
    """
    root = root.resolve()
    full_path = root / module_path
    errors: list[str] = []
    lesson_results: dict[str, dict] = {}

    if not full_path.is_dir():
        return {
            "valid": False,
            "lesson_results": {},
            "errors": [f"Module directory not found: {module_path}"],
        }

    # Check for README or overview
    has_readme = (full_path / "README.md").exists()
    has_overview = (full_path / "overview.md").exists()
    if not has_readme and not has_overview:
        errors.append("Module missing README.md or overview.md")

    # Validate all .md lesson files (exclude README.md and overview.md)
    skip = {"readme.md", "overview.md"}
    lessons = sorted(
        f for f in full_path.iterdir()
        if f.suffix == ".md" and f.name.lower() not in skip
    )
    for lesson_file in lessons:
        rel = str(lesson_file.relative_to(root))
        result = validate_lesson(root, rel)
        lesson_results[rel] = result
        if not result["valid"]:
            errors.append(f"Lesson {lesson_file.name} has validation errors")

    return {
        "valid": len(errors) == 0,
        "lesson_results": lesson_results,
        "errors": errors,
    }


def validate_course(root: Path) -> dict:
    """Validate the entire course.

    Checks:
    - course.yml exists and has no TBD values
    - All module directories pass validate_module
    """
    root = root.resolve()
    errors: list[str] = []
    module_results: dict[str, dict] = {}

    course_yml = root / "course.yml"
    if not course_yml.exists():
        errors.append("course.yml not found")
    else:
        text = course_yml.read_text(encoding="utf-8")
        for line in text.splitlines():
            line_stripped = line.strip()
            if ":" in line_stripped:
                key, _, value = line_stripped.partition(":")
                value = value.strip()
                if value == "TBD":
                    errors.append(f"course.yml has TBD value for: {key.strip()}")

    # Find module directories — convention: directories under modules/
    modules_dir = root / "modules"
    if modules_dir.is_dir():
        for mod_dir in sorted(modules_dir.iterdir()):
            if mod_dir.is_dir():
                rel = str(mod_dir.relative_to(root))
                result = validate_module(root, rel)
                module_results[rel] = result
                if not result["valid"]:
                    errors.append(f"Module {mod_dir.name} has validation errors")

    return {
        "valid": len(errors) == 0,
        "module_results": module_results,
        "errors": errors,
    }


def get_validation_report(root: Path) -> dict:
    """Read the last saved validation report from CURIK_DIR/validation-report.json."""
    root = root.resolve()
    report_path = _course_dir(root) / "validation-report.json"
    if not report_path.exists():
        raise CurikError("No validation report found.")
    return json.loads(report_path.read_text(encoding="utf-8"))


def save_validation_report(root: Path, report: dict) -> dict:
    """Save a validation report to CURIK_DIR/validation-report.json."""
    root = root.resolve()
    report_path = _course_dir(root) / "validation-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return {"path": str(report_path)}


# ---------------------------------------------------------------------------
# Standalone instructor-guide validator (content-string based)
# ---------------------------------------------------------------------------

REQUIRED_GUIDE_FIELDS = [
    "Objectives",
    "Materials",
    "Timing",
    "Key Concepts",
    "Common Mistakes",
    "Assessment Cues",
    "Differentiation",
]


def validate_instructor_guide(content: str) -> dict:
    """Parse markdown *content* and check for required instructor guide fields.

    Looks for ``<div class="instructor-guide"`` sections and verifies that
    all 7 required fields are present and non-empty.

    Returns::

        {"valid": bool, "missing": [str, ...], "empty": [str, ...]}
    """
    guide_pattern = re.compile(
        r'<div\s+class="instructor-guide"[^>]*>(.+?)</div>',
        re.DOTALL,
    )
    guide_blocks = guide_pattern.findall(content)

    if not guide_blocks:
        return {
            "valid": False,
            "missing": list(REQUIRED_GUIDE_FIELDS),
            "empty": [],
        }

    combined = "\n".join(guide_blocks)

    # Build a lookahead alternation for field boundaries
    _field_alt = "|".join(re.escape(f) for f in REQUIRED_GUIDE_FIELDS)

    missing: list[str] = []
    empty: list[str] = []

    for field in REQUIRED_GUIDE_FIELDS:
        pattern = re.compile(
            rf'\*\*{re.escape(field)}\*\*\s*:\s*(.*?)(?=\*\*(?:{_field_alt})\*\*\s*:|</div>|\Z)',
            re.DOTALL,
        )
        match = pattern.search(combined)
        if not match:
            missing.append(field)
        elif not match.group(1).strip():
            empty.append(field)

    return {
        "valid": len(missing) == 0 and len(empty) == 0,
        "missing": missing,
        "empty": empty,
    }
