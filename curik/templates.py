"""Reusable templates for course scaffolding: hugo, devcontainer, course.yml."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

# The theme source lives in the curik repo root. During scaffolding,
# it gets copied into each course repo at themes/curriculum-hugo-theme/.
# Later this will become a git submodule in each course repo.
THEME_NAME = "curriculum-hugo-theme"
_THEME_SOURCE = Path(__file__).resolve().parent.parent / THEME_NAME


def get_theme_source() -> Path:
    """Return the absolute path to the theme source in the curik repo."""
    return _THEME_SOURCE


def get_hugo_config(title: str, tier: int) -> str:
    """Return a tier-appropriate hugo.toml configuration string.

    All tiers reference the curriculum-hugo-theme (expected at
    ``themes/curriculum-hugo-theme/`` in the course repo). Tiers 1-2 include
    an ``instructorGuide = true`` parameter.
    """
    lines = [
        'baseURL = "/"',
        f'title = "{title}"',
        f'theme = "{THEME_NAME}"',
        "",
        "[markup]",
        "  [markup.highlight]",
        "    codeFences = true",
        "    guessSyntax = true",
        "    lineNos = false",
        "  [markup.tableOfContents]",
        "    startLevel = 2",
        "    endLevel = 4",
        "",
        "[params]",
        '  copyright = "The League of Amazing Programmers"',
        '  license = "CC BY-NC 4.0"',
    ]

    if tier in (1, 2):
        lines.append("  instructorGuide = true")

    lines.append("")
    return "\n".join(lines)


def hugo_setup(
    root: Path, title: str, tier: int, *, symlink_theme: bool = False,
) -> dict[str, list[str]]:
    """Generate hugo.toml and install the theme into a course repo.

    Writes ``hugo.toml`` to *root* and installs the bundled
    curriculum-hugo-theme into ``themes/curriculum-hugo-theme/``.

    If *symlink_theme* is True, creates a symlink to the theme source
    instead of copying it. This is useful during development so edits
    to the theme are reflected immediately.

    Returns ``{"created": [...], "existing": [...]}``.
    """
    root = root.resolve()
    created: list[str] = []
    existing: list[str] = []

    # Generate hugo.toml
    hugo_toml = root / "hugo.toml"
    rel_toml = str(hugo_toml.relative_to(root))
    if hugo_toml.exists():
        existing.append(rel_toml)
    else:
        hugo_toml.write_text(get_hugo_config(title, tier), encoding="utf-8")
        created.append(rel_toml)

    # Install theme (symlink or copy)
    theme_dest = root / "themes" / THEME_NAME
    rel_theme = str(theme_dest.relative_to(root))
    if theme_dest.exists() or theme_dest.is_symlink():
        existing.append(rel_theme)
    else:
        theme_src = get_theme_source()
        if theme_src.is_dir():
            theme_dest.parent.mkdir(parents=True, exist_ok=True)
            if symlink_theme:
                theme_dest.symlink_to(theme_src)
            else:
                shutil.copytree(theme_src, theme_dest)
            created.append(rel_theme)

    return {"created": created, "existing": existing}


def get_devcontainer_json(language: str) -> str:
    """Return a .devcontainer/devcontainer.json string for the given language.

    Supported languages: python, java.
    """
    language = language.lower()

    if language == "python":
        image = "mcr.microsoft.com/devcontainers/python:3.11"
        extensions = [
            "ms-python.python",
            "ms-python.vscode-pylance",
        ]
    elif language == "java":
        image = "mcr.microsoft.com/devcontainers/java:17"
        extensions = [
            "vscjava.vscode-java-pack",
        ]
    else:
        image = "mcr.microsoft.com/devcontainers/base:ubuntu"
        extensions = []

    config = {
        "name": f"{language.title()} Development",
        "image": image,
        "customizations": {
            "vscode": {
                "extensions": extensions,
            }
        },
        "postCreateCommand": "echo 'Container ready.'",
    }

    return json.dumps(config, indent=2) + "\n"


def get_course_yml_template(tier: int) -> str:
    """Return a course.yml template string with tier-appropriate defaults."""
    if tier == 1:
        grades = "K-2"
        category = "unplugged"
        estimated_weeks = 4
    elif tier == 2:
        grades = "3-5"
        category = "block-programming"
        estimated_weeks = 6
    elif tier == 3:
        grades = "6-8"
        category = "text-programming"
        estimated_weeks = 9
    elif tier == 4:
        grades = "9-12"
        category = "advanced"
        estimated_weeks = 12
    else:
        grades = "TBD"
        category = "TBD"
        estimated_weeks = 0

    lines = [
        "title: TBD",
        "slug: TBD",
        "uid: TBD",
        f"tier: {tier}",
        f"grades: {grades}",
        f"category: {category}",
        "topics: []",
        "prerequisites: []",
        "lessons: 0",
        f"estimated_weeks: {estimated_weeks}",
        "curriculum_url: TBD",
        "repo_url: TBD",
        "description: TBD",
        "",
    ]
    return "\n".join(lines)
