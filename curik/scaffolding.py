"""Phase 2 scaffolding: directory trees, lesson stubs, outlines, change plans."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .project import CurikError, _course_dir


# ---------------------------------------------------------------------------
# Scaffold structure
# ---------------------------------------------------------------------------


def scaffold_structure(root: Path, structure: dict[str, Any]) -> dict[str, list[str]]:
    """Create the directory tree and stub files described by *structure*.

    *structure* has the form::

        {"modules": [
            {"name": "01-intro", "lessons": ["01-hello.md", "02-variables.md"]},
        ]}

    Returns ``{"created": [...], "existing": [...]}``.
    """
    root = root.resolve()
    created: list[str] = []
    existing: list[str] = []

    modules = structure.get("modules")
    if not modules:
        raise CurikError("Structure must contain a non-empty 'modules' list.")

    for mod in modules:
        mod_name = mod.get("name")
        if not mod_name:
            raise CurikError("Each module must have a 'name' key.")

        mod_dir = root / mod_name
        if mod_dir.exists():
            existing.append(mod_name)
        else:
            mod_dir.mkdir(parents=True, exist_ok=True)
            created.append(mod_name)

        for lesson in mod.get("lessons", []):
            lesson_path = mod_dir / lesson
            rel = str(lesson_path.relative_to(root))
            if lesson_path.exists():
                existing.append(rel)
            else:
                lesson_path.parent.mkdir(parents=True, exist_ok=True)
                title = _title_from_filename(lesson)
                lesson_path.write_text(
                    f"# {title}\n\n"
                    '<div class="instructor-guide">\n\n'
                    "Instructor guide content goes here.\n\n"
                    "</div>\n",
                    encoding="utf-8",
                )
                created.append(rel)

    return {"created": sorted(created), "existing": sorted(existing)}


# ---------------------------------------------------------------------------
# Lesson stubs
# ---------------------------------------------------------------------------


def create_lesson_stub(
    root: Path, module: str, lesson: str, tier: int
) -> str:
    """Create a single lesson stub file and return its relative path.

    * Tiers 1-2 produce an instructor-guide-primary stub.
    * Tiers 3-4 add a student content section before the instructor guide.
    * For tiers 3-4, if *lesson* ends with ``.ipynb`` a companion notebook
      stub is also created.
    """
    root = root.resolve()
    if tier not in (1, 2, 3, 4):
        raise CurikError(f"Tier must be 1-4, got {tier}.")

    mod_dir = root / module
    mod_dir.mkdir(parents=True, exist_ok=True)
    lesson_path = mod_dir / lesson
    title = _title_from_filename(lesson)

    if tier in (1, 2):
        content = (
            f"# {title}\n\n"
            '<div class="instructor-guide">\n\n'
            "Instructor guide content goes here.\n\n"
            "</div>\n"
        )
    else:
        content = (
            f"# {title}\n\n"
            "## Student Content\n\n"
            "Student-facing content goes here.\n\n"
            '<div class="instructor-guide">\n\n'
            "Instructor guide content goes here.\n\n"
            "</div>\n"
        )

    lesson_path.write_text(content, encoding="utf-8")
    created = str(lesson_path.relative_to(root))

    # Companion notebook for tier 3-4 .ipynb lessons
    if tier in (3, 4) and lesson.endswith(".ipynb"):
        nb_path = mod_dir / lesson
        # The lesson IS the notebook — write a minimal Jupyter stub
        nb_stub: dict[str, Any] = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [f"# {title}\n"],
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        nb_path.write_text(
            json.dumps(nb_stub, indent=2) + "\n", encoding="utf-8"
        )

    return created


# ---------------------------------------------------------------------------
# Outlines
# ---------------------------------------------------------------------------

_OUTLINE_FRONTMATTER_RE = re.compile(
    r"^---\n(.*?)\n---\n", re.DOTALL
)


def create_outline(root: Path, name: str, content: str) -> str:
    """Write an outline document to ``CURIK_DIR/outlines/{name}.md``.

    Returns the relative path of the created file.
    """
    root = root.resolve()
    outlines_dir = _course_dir(root) / "outlines"
    outlines_dir.mkdir(parents=True, exist_ok=True)

    filename = _slugify(name) + ".md"
    path = outlines_dir / filename

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = (
        "---\n"
        f"title: {name}\n"
        f"created: {now}\n"
        "approved: false\n"
        "---\n\n"
        f"{content.rstrip()}\n"
    )
    path.write_text(text, encoding="utf-8")
    return str(path.relative_to(root))


def approve_outline(root: Path, name: str) -> str:
    """Mark an outline as approved by flipping its frontmatter flag.

    Raises CurikError if the outline does not exist.
    Returns the relative path.
    """
    root = root.resolve()
    filename = _slugify(name) + ".md"
    path = _course_dir(root) / "outlines" / filename
    if not path.exists():
        raise CurikError(f"Outline not found: {filename}")

    text = path.read_text(encoding="utf-8")
    updated = text.replace("approved: false", "approved: true", 1)
    path.write_text(updated, encoding="utf-8")
    return str(path.relative_to(root))


def get_outline(root: Path, name: str) -> str:
    """Read and return the content of an outline document.

    Raises CurikError if the outline does not exist.
    """
    root = root.resolve()
    filename = _slugify(name) + ".md"
    path = _course_dir(root) / "outlines" / filename
    if not path.exists():
        raise CurikError(f"Outline not found: {filename}")
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Change plans
# ---------------------------------------------------------------------------


def generate_change_plan(
    root: Path, title: str, items: list[str]
) -> str:
    """Create a numbered change plan in ``CURIK_DIR/change-plan/active/``.

    Returns the relative path of the created file.
    """
    root = root.resolve()
    if not items:
        raise CurikError("Change plan must have at least one item.")

    active_dir = _course_dir(root) / "change-plan" / "active"
    active_dir.mkdir(parents=True, exist_ok=True)

    slug = _slugify(title)
    filename = f"{slug}.md"
    path = active_dir / filename

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "---",
        f"title: {title}",
        f"created: {now}",
        "status: active",
        "---",
        "",
        f"# {title}",
        "",
    ]
    for i, item in enumerate(items, 1):
        lines.append(f"{i}. {item}")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path.relative_to(root))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _title_from_filename(filename: str) -> str:
    """Derive a human title from a filename like ``01-hello.md``."""
    stem = Path(filename).stem
    # Strip leading number prefix (e.g., "01-")
    stem = re.sub(r"^\d+-", "", stem)
    return stem.replace("-", " ").replace("_", " ").title()


def _slugify(text: str) -> str:
    """Turn a title into a filesystem-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")
