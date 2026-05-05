"""Path helpers for Hugo-related locations within a curriculum project.

This module is the single source of truth for all Hugo path construction.
It defines the ``SITE_DIR`` constant and five path-helper functions. Every
other curik module should import from here instead of hardcoding path strings.

No filesystem I/O is performed — all helpers are pure path-math functions.
"""

from __future__ import annotations

from pathlib import Path

SITE_DIR = "site"
THEME_NAME = "curriculum-hugo-theme"


def site_root(root: Path) -> Path:
    """Return the Hugo site directory: ``root/site``."""
    return root / SITE_DIR


def hugo_toml_path(root: Path) -> Path:
    """Return the path to ``hugo.toml``: ``root/site/hugo.toml``."""
    return root / SITE_DIR / "hugo.toml"


def content_dir(root: Path) -> Path:
    """Return the Hugo content directory: ``root/site/content``."""
    return root / SITE_DIR / "content"


def themes_dir(root: Path) -> Path:
    """Return the Hugo themes directory: ``root/site/themes``."""
    return root / SITE_DIR / "themes"


def theme_dir(root: Path) -> Path:
    """Return the installed theme directory: ``root/site/themes/curriculum-hugo-theme``."""
    return root / SITE_DIR / "themes" / THEME_NAME
