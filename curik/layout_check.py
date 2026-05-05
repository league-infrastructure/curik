"""Legacy Hugo layout detector.

This module checks whether a curriculum project is using the old root-level
Hugo layout (hugo.toml at root) rather than the new ``site/`` subdirectory
layout. It returns a warning string when the legacy layout is detected, or
``None`` when the layout is correct or no Hugo files are present.

No mutations are performed — this module is read-only.
"""

from __future__ import annotations

import os
from pathlib import Path

from .paths import hugo_toml_path

_WARNING = (
    "WARNING: This project uses the legacy Hugo layout (hugo.toml at root).\n"
    "Run `curik migrate hugo-layout` to move Hugo files into site/.\n"
    "The legacy layout will stop working in a future release."
)


def check_legacy_hugo_layout(root: Path) -> str | None:
    """Return a warning string if the project uses the legacy Hugo layout.

    Detection rule: return the warning string if ANY of the following exist:
    - ``root/hugo.toml``
    - ``root/themes/curriculum-hugo-theme/``
    - ``root/content/_index.md``

    AND ``root/site/hugo.toml`` does NOT exist.

    Returns ``None`` if:
    - The new layout is in place (``site/hugo.toml`` exists).
    - No Hugo files are detected at all (non-Hugo project).
    - The ``CURIK_NO_LAYOUT_WARNING`` environment variable is set.

    Args:
        root: Absolute path to the project root directory.

    Returns:
        A warning string, or ``None``.
    """
    if os.environ.get("CURIK_NO_LAYOUT_WARNING"):
        return None

    # If the new layout is already in place, no warning needed.
    if hugo_toml_path(root).exists():
        return None

    legacy_indicators = [
        root / "hugo.toml",
        root / "themes" / "curriculum-hugo-theme",
        root / "content" / "_index.md",
    ]
    if any(p.exists() for p in legacy_indicators):
        return _WARNING

    return None
