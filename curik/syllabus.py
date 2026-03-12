"""Syllabus integration: read, write, and validate syllabus.yaml entries."""

from __future__ import annotations

from pathlib import Path

import yaml
from syllabus.models import Course, LessonSet
from syllabus.sync import compile_syllabus

from .project import CurikError


def _iter_lessons(course: Course) -> list[dict]:
    """Flatten all lessons from a Course into a list of dicts."""
    entries: list[dict] = []
    for module in course.modules:
        for item in module.lessons:
            if isinstance(item, LessonSet):
                for lesson in item.lessons:
                    entries.append({
                        "uid": lesson.uid,
                        "name": lesson.name,
                        "lesson": lesson.lesson,
                        "exercise": lesson.exercise,
                    })
            else:
                entries.append({
                    "uid": item.uid,
                    "name": item.name,
                    "lesson": item.lesson,
                    "exercise": item.exercise,
                })
    return entries


def read_syllabus_entries(root: Path) -> list[dict]:
    """Read syllabus.yaml and return lesson entries with uid, name, path fields."""
    syllabus_path = root / "syllabus.yaml"
    if not syllabus_path.exists():
        raise CurikError(f"syllabus.yaml not found at {syllabus_path}")
    course = Course.from_yaml(syllabus_path)
    return _iter_lessons(course)


def write_syllabus_url(root: Path, uid: str, url: str) -> dict:
    """Update the url field for a lesson entry identified by UID.

    Uses raw YAML since the Lesson model may not have a url field.
    """
    syllabus_path = root / "syllabus.yaml"
    if not syllabus_path.exists():
        raise CurikError(f"syllabus.yaml not found at {syllabus_path}")

    text = syllabus_path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)

    found = False
    for module in data.get("modules", []):
        for lesson in module.get("lessons", []):
            if lesson.get("uid") == uid:
                lesson["url"] = url
                found = True
                break
            # Handle nested lesson sets
            if "lessons" in lesson:
                for sub_lesson in lesson["lessons"]:
                    if sub_lesson.get("uid") == uid:
                        sub_lesson["url"] = url
                        found = True
                        break
            if found:
                break
        if found:
            break

    if not found:
        raise CurikError(f"No lesson entry with uid '{uid}' found in syllabus.yaml")

    syllabus_path.write_text(
        yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return {"status": "ok", "uid": uid, "url": url}


def regenerate_syllabus(root: Path, lesson_dir: str = "lessons") -> dict:
    """Compile syllabus from lesson directory using syllabus.sync.compile_syllabus()."""
    target = root / lesson_dir
    if not target.is_dir():
        raise CurikError(f"Lesson directory not found: {target}")
    course = compile_syllabus(target)
    course.to_yaml(root / "syllabus.yaml")
    return {"status": "ok", "path": "syllabus.yaml"}


def get_syllabus(root: Path) -> str:
    """Return raw syllabus.yaml content."""
    syllabus_path = root / "syllabus.yaml"
    if not syllabus_path.exists():
        raise CurikError(f"syllabus.yaml not found at {syllabus_path}")
    return syllabus_path.read_text(encoding="utf-8")


def validate_syllabus_consistency(root: Path) -> dict:
    """Check syllabus entries against MkDocs pages and report mismatches."""
    syllabus_path = root / "syllabus.yaml"
    if not syllabus_path.exists():
        raise CurikError(f"syllabus.yaml not found at {syllabus_path}")

    course = Course.from_yaml(syllabus_path)
    entries = _iter_lessons(course)

    # Collect UIDs from syllabus
    syllabus_uids = {e["uid"] for e in entries if e.get("uid")}

    # Scan docs/docs for .md files with uid in frontmatter
    docs_dir = root / "docs" / "docs"
    page_uids: set[str] = set()
    pages_without_uid: list[str] = []

    if docs_dir.is_dir():
        for md_file in docs_dir.rglob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            if text.startswith("---"):
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    try:
                        fm = yaml.safe_load(parts[1])
                        if isinstance(fm, dict) and fm.get("uid"):
                            page_uids.add(fm["uid"])
                        else:
                            pages_without_uid.append(
                                str(md_file.relative_to(root))
                            )
                    except yaml.YAMLError:
                        pages_without_uid.append(
                            str(md_file.relative_to(root))
                        )

    entries_without_pages = sorted(syllabus_uids - page_uids)
    pages_without_entries = sorted(page_uids - syllabus_uids)

    return {
        "entries_without_pages": entries_without_pages,
        "pages_without_entries": pages_without_entries,
        "pages_without_uid": sorted(pages_without_uid),
        "syllabus_entry_count": len(entries),
        "page_count": len(page_uids) + len(pages_without_uid),
    }
