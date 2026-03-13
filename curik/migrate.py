"""Migration tools: inventory existing course repos and migrate to Curik structure."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import shutil

from .project import CURIK_DIR, CurikError, _course_dir, init_course
from .templates import get_hugo_config


def inventory_course(repo_path: str | Path) -> dict[str, Any]:
    """Read-only analysis of a course repository's current state.

    Returns a dict describing: has_course_yml, has_docs, has_lessons,
    tier_guess, generator_guess, lesson_count, has_devcontainer.
    """
    root = Path(repo_path).resolve()
    if not root.is_dir():
        raise CurikError(f"Path is not a directory: {root}")

    has_course_yml = (root / "course.yml").is_file()
    has_docs = (root / "docs").is_dir()
    has_devcontainer = (root / ".devcontainer").is_dir()

    # Detect static-site generator
    generator_guess = "unknown"
    if (root / "hugo.toml").is_file():
        generator_guess = "hugo"
    elif (root / "mkdocs.yml").is_file():
        generator_guess = "mkdocs"
    elif (root / "conf.py").is_file() or (root / "docs" / "conf.py").is_file():
        generator_guess = "sphinx"
    elif (root / "docs" / ".vuepress").is_dir() or (root / ".vuepress").is_dir():
        generator_guess = "vuepress"

    # Count lessons — look for markdown files in common lesson directories
    lesson_dirs = ["lessons", "docs/lessons", "modules", "docs"]
    lesson_count = 0
    has_lessons = False
    for ld in lesson_dirs:
        d = root / ld
        if d.is_dir():
            md_files = list(d.rglob("*.md"))
            if md_files:
                has_lessons = True
                lesson_count += len(md_files)

    # Guess tier from course.yml if present
    tier_guess = 0
    if has_course_yml:
        try:
            text = (root / "course.yml").read_text(encoding="utf-8")
            for line in text.splitlines():
                if line.startswith("tier:"):
                    val = line.split(":", 1)[1].strip()
                    if val.isdigit():
                        tier_guess = int(val)
                    break
        except OSError:
            pass

    return {
        "has_course_yml": has_course_yml,
        "has_docs": has_docs,
        "has_lessons": has_lessons,
        "tier_guess": tier_guess,
        "generator_guess": generator_guess,
        "lesson_count": lesson_count,
        "has_devcontainer": has_devcontainer,
    }


def migrate_structure(
    root: str | Path, tier: int, modules: list[str]
) -> dict[str, list[str]]:
    """Create the standard Curik directory structure for a course repository.

    Calls init_course first if CURIK_DIR/ does not exist. Creates content/
    with a hugo.toml config and module directories with _index.md stubs.

    Returns {"created": [list of created paths]}.
    """
    root = Path(root).resolve()
    if not root.is_dir():
        raise CurikError(f"Path is not a directory: {root}")

    created: list[str] = []

    # Ensure CURIK_DIR/ structure exists
    course_dir = _course_dir(root)
    if not course_dir.is_dir():
        result = init_course(root)
        created.extend(result["created"])

    # Create content/ directory
    content_dir = root / "content"
    if not content_dir.is_dir():
        content_dir.mkdir(parents=True, exist_ok=True)
        created.append("content")

    # Create hugo.toml
    hugo_path = root / "hugo.toml"
    if not hugo_path.is_file():
        title = root.name.replace("-", " ").replace("_", " ").title()
        hugo_path.write_text(get_hugo_config(title, tier), encoding="utf-8")
        created.append("hugo.toml")

    # Create root _index.md
    root_index = content_dir / "_index.md"
    if not root_index.is_file():
        title = root.name.replace("-", " ").replace("_", " ").title()
        root_index.write_text(f"# {title}\n\nCourse overview.\n", encoding="utf-8")
        created.append("content/_index.md")

    # Create module directories with _index.md stubs
    for mod_name in modules:
        mod_dir = content_dir / mod_name
        if not mod_dir.is_dir():
            mod_dir.mkdir(parents=True, exist_ok=True)
            created.append(f"content/{mod_name}")

        index_path = mod_dir / "_index.md"
        if not index_path.is_file():
            title = mod_name.replace("-", " ").replace("_", " ").title()
            index_path.write_text(f"# {title}\n\nModule overview.\n", encoding="utf-8")
            created.append(f"content/{mod_name}/_index.md")

    return {"created": created}


# Paths that sequester_content() will never move.
_PROTECTED_NAMES = frozenset({
    CURIK_DIR,    # .course/
    ".git",
    ".mcp.json",
    ".claude",
    ".vscode",
    "CLAUDE.md",
    "course.yml",
    "_old",
})


def sequester_content(root: str | Path) -> dict[str, list[str]]:
    """Move all non-Curik files in *root* into ``_old/``.

    Protected paths (``.course/``, ``.git/``, ``.mcp.json``, ``course.yml``,
    ``_old/``) are never moved.  Directory structure is preserved inside
    ``_old/``.

    Returns ``{"moved": [...], "protected": [...]}``.
    """
    root = Path(root).resolve()
    if not root.is_dir():
        raise CurikError(f"Path is not a directory: {root}")

    old_dir = root / "_old"
    moved: list[str] = []
    protected: list[str] = []

    for entry in sorted(root.iterdir()):
        name = entry.name
        if name in _PROTECTED_NAMES:
            protected.append(name)
            continue

        dest = old_dir / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(entry), str(dest))
        moved.append(name)

    return {"moved": moved, "protected": sorted(protected)}
