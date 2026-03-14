"""Reusable templates for course scaffolding: hugo, devcontainer, course.yml."""

from __future__ import annotations

import json
import shutil
import subprocess
from importlib.metadata import version as pkg_version
from pathlib import Path
from typing import Any

import re
from datetime import date

THEME_NAME = "curriculum-hugo-theme"
THEME_REPO = "https://github.com/league-infrastructure/curriculum-hugo-theme.git"
CURRICULUM_BASE = "https://curriculum.jointheleague.org"

_VERSION_RE = re.compile(r'^(\s*curriculum_version)\s*=\s*"([^"]*)"', re.MULTILINE)


def _today() -> str:
    """Return today's date as YYYYMMDD."""
    return date.today().strftime("%Y%m%d")

# Local theme source — used only for symlink_theme (development mode).
_THEME_SOURCE = Path(__file__).resolve().parent.parent / THEME_NAME


def get_theme_source() -> Path:
    """Return the absolute path to the theme source in the curik repo."""
    return _THEME_SOURCE


def bump_curriculum_version(root: Path) -> str:
    """Bump the version in hugo.toml and return the new version string.

    Version format: ``0.YYYYMMDD.revision``. If today's date matches the
    current version date, increments the revision. Otherwise resets to
    ``0.<today>.1``.
    """
    hugo_toml = root / "hugo.toml"
    if not hugo_toml.exists():
        raise FileNotFoundError("hugo.toml not found")

    content = hugo_toml.read_text(encoding="utf-8")
    match = _VERSION_RE.search(content)
    if not match:
        raise ValueError("No curriculum_version field found in hugo.toml")

    key = match.group(1)  # preserves indentation
    old_version = match.group(2)
    today = _today()

    # Parse old version: 0.YYYYMMDD.revision
    parts = old_version.split(".")
    if len(parts) == 3 and parts[1] == today:
        new_rev = int(parts[2]) + 1
    else:
        new_rev = 1

    new_version = f"0.{today}.{new_rev}"
    new_content = content[:match.start()] + f'{key} = "{new_version}"' + content[match.end():]
    hugo_toml.write_text(new_content, encoding="utf-8")
    return new_version


def get_curik_version() -> str:
    """Return the installed curik version (e.g. '0.20260313.7')."""
    return pkg_version("curik")


def get_hugo_config(
    title: str, tier: int, *, slug: str = "", github_repo: str = "",
    description: str = "",
) -> str:
    """Return a tier-appropriate hugo.toml configuration string.

    All tiers reference the curriculum-hugo-theme (expected at
    ``themes/curriculum-hugo-theme/`` in the course repo). Tiers 1-2 include
    an ``instructorGuide = true`` parameter.

    If *slug* is provided, sets baseURL to the curriculum site subpath.
    If *github_repo* is provided, a GitHub icon link appears in the footer.
    """
    if slug and slug != "TBD":
        base_url = f"{CURRICULUM_BASE}/{slug}/"
    else:
        base_url = "/"
    lines = [
        f'baseURL = "{base_url}"',
        f'title = "{title}"',
        f'theme = "{THEME_NAME}"',
        "enableEmoji = true",
        "",
        "[markup]",
        "  [markup.goldmark.renderer]",
        "    unsafe = true",
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
        f'  curriculum_version = "0.{_today()}.1"',
    ]

    if description and description != "TBD":
        # Escape quotes in description
        lines.append(f'  description = "{description.replace(chr(34), chr(39))}"')

    curik_ver = get_curik_version()
    lines.append(f'  curik_version = "{curik_ver}"')

    if tier in (1, 2):
        lines.append("  instructorGuide = true")

    if github_repo and github_repo != "TBD":
        lines.append(f'  github_repo = "{github_repo}"')

    lines.append("")
    return "\n".join(lines)


def _clone_theme(dest: Path, tag: str) -> None:
    """Clone the theme repo at *tag* into *dest*."""
    subprocess.run(
        [
            "git", "clone",
            "--branch", tag,
            "--depth", "1",
            THEME_REPO,
            str(dest),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    # Remove the .git dir — this is a plain copy, not a submodule.
    git_dir = dest / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)


def _get_installed_theme_version(theme_dir: Path) -> str:
    """Read the version from an installed theme's theme.toml."""
    theme_toml = theme_dir / "theme.toml"
    if not theme_toml.exists():
        return ""
    for line in theme_toml.read_text(encoding="utf-8").splitlines():
        if line.startswith("version"):
            # version = "0.20260314.4"
            _, _, value = line.partition("=")
            return value.strip().strip('"').strip("'")
    return ""


def hugo_setup(
    root: Path, title: str, tier: int, *, slug: str = "",
    symlink_theme: bool = False, github_repo: str = "",
    description: str = "",
) -> dict[str, list[str]]:
    """Generate hugo.toml and install the theme into a course repo.

    Writes ``hugo.toml`` to *root* and installs the curriculum-hugo-theme
    into ``themes/curriculum-hugo-theme/``.

    In production mode (default), clones the theme from its GitHub repo
    at the tag matching curik's installed version (``v{version}``).

    If *symlink_theme* is True, creates a symlink to the local theme
    source instead. This is useful during development so edits to the
    theme are reflected immediately.

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
        hugo_toml.write_text(
            get_hugo_config(title, tier, slug=slug, github_repo=github_repo,
                           description=description),
            encoding="utf-8",
        )
        created.append(rel_toml)

    # Install or update theme
    theme_dest = root / "themes" / THEME_NAME
    rel_theme = str(theme_dest.relative_to(root))
    if theme_dest.is_symlink():
        # Symlink (dev mode) — always up to date, nothing to do
        existing.append(rel_theme)
    elif theme_dest.exists():
        # Theme exists — check if it needs updating
        if symlink_theme:
            # Switching to symlink mode: replace clone with symlink
            shutil.rmtree(theme_dest)
            theme_dest.symlink_to(get_theme_source())
            created.append(rel_theme)
        else:
            # Check version: compare installed theme version to curik version
            installed_version = _get_installed_theme_version(theme_dest)
            current_version = get_curik_version()
            if installed_version != current_version:
                shutil.rmtree(theme_dest)
                tag = f"v{current_version}"
                _clone_theme(theme_dest, tag)
                created.append(rel_theme)
            else:
                existing.append(rel_theme)
    else:
        theme_dest.parent.mkdir(parents=True, exist_ok=True)
        if symlink_theme:
            theme_dest.symlink_to(get_theme_source())
        else:
            tag = f"v{get_curik_version()}"
            _clone_theme(theme_dest, tag)
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
