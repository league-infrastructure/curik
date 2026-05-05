"""One-shot opt-in migration from the legacy root Hugo layout to ``site/``.

Moves Hugo files (``hugo.toml``, ``themes/``, ``content/``, and optional
``layouts/``, ``static/``, ``data/``, ``assets/``) from the project root
into the ``site/`` subdirectory using ``git mv`` when inside a git repo,
falling back to ``shutil.move`` otherwise.

After moving files, rewrites ``site/hugo.toml`` to use ``../course.yml``
in its data mount and updates the ``.gitignore`` CURIK block to reference
the new ``site/`` paths.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from .paths import site_root, hugo_toml_path
from .templates import _extract_params_section, _replace_params_section

_GITIGNORE_START = "# -- CURIK:START --"
_GITIGNORE_END = "# -- CURIK:END --"

_NEW_GITIGNORE_BLOCK = """\
# -- CURIK:START --
# Managed by curik — do not edit this section manually.
# Run `curik init` to update.

# Hugo build output (now under site/)
site/public/
site/resources/_gen/

# OS files
.DS_Store
Thumbs.db

# Hugo lock file
site/.hugo_build.lock
# -- CURIK:END --"""

# Files/dirs that must be moved (always required for a Hugo project)
_REQUIRED_MOVES = ["hugo.toml", "themes", "content"]
# Optional files/dirs moved only if they exist
_OPTIONAL_MOVES = ["layouts", "static", "data", "assets"]


def _is_git_repo(root: Path) -> bool:
    """Return True if *root* is inside a git repository."""
    return (root / ".git").exists()


def _git_mv(root: Path, src: Path, dst: Path) -> None:
    """Move *src* to *dst* using ``git mv``."""
    subprocess.run(
        ["git", "mv", str(src), str(dst)],
        check=True,
        cwd=str(root),
        capture_output=True,
        text=True,
    )


def _move(root: Path, src: Path, dst: Path, use_git: bool) -> None:
    """Move *src* to *dst* using git mv or shutil.move."""
    if use_git:
        _git_mv(root, src, dst)
    else:
        shutil.move(str(src), str(dst))


def _is_dirty(root: Path) -> bool:
    """Return True if the git working tree has uncommitted changes."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def _rewrite_hugo_toml(hugo_toml: Path) -> None:
    """Rewrite the data mount in *hugo_toml* to use ``../course.yml``.

    Changes ``source = "course.yml"`` to ``source = "../course.yml"`` in the
    ``[[module.mounts]]`` block, preserving the user-managed ``[params]``
    section.
    """
    content = hugo_toml.read_text(encoding="utf-8")
    # Extract params before rewriting so user edits are preserved
    old_params = _extract_params_section(content)
    # Rewrite the mount source
    new_content = content.replace(
        'source = "course.yml"',
        'source = "../course.yml"',
    )
    # Re-apply original params section if it existed
    if old_params is not None:
        new_params = _extract_params_section(new_content)
        if new_params != old_params:
            new_content = _replace_params_section(new_content, old_params)
    hugo_toml.write_text(new_content, encoding="utf-8")


def _update_gitignore(root: Path) -> None:
    """Update the .gitignore CURIK block to reference ``site/`` paths."""
    gitignore = root / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8")
        if _GITIGNORE_START in content and _GITIGNORE_END in content:
            start_idx = content.index(_GITIGNORE_START)
            end_idx = content.index(_GITIGNORE_END) + len(_GITIGNORE_END)
            new_content = content[:start_idx] + _NEW_GITIGNORE_BLOCK + content[end_idx:]
        else:
            # No CURIK block — prepend the new block
            new_content = _NEW_GITIGNORE_BLOCK + "\n\n" + content
        gitignore.write_text(new_content, encoding="utf-8")
    else:
        gitignore.write_text(_NEW_GITIGNORE_BLOCK + "\n", encoding="utf-8")


def migrate_hugo_layout(
    root: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
    verify: bool = False,
) -> dict:
    """Migrate Hugo files from the project root into ``site/``.

    Steps:
    1. Idempotency check — if ``site/hugo.toml`` already exists, return
       immediately (nothing to do).
    2. Dirty-tree check — abort if there are uncommitted changes, unless
       ``force=True``.
    3. Dry-run mode — if ``dry_run=True``, print planned moves and return
       without making any filesystem changes.
    4. Create ``site/``.
    5. Move files using ``git mv`` (or ``shutil.move`` if not in a git repo).
    6. Rewrite ``site/hugo.toml`` mount to ``../course.yml``.
    7. Update ``.gitignore`` CURIK block.
    8. Optionally verify with ``hugo --source site``.

    Args:
        root: Absolute path to the project root.
        dry_run: If True, print planned moves and exit without changes.
        force: If True, skip the dirty-tree check.
        verify: If True, run ``hugo --source site`` after migration.

    Returns:
        dict with keys:
          - ``"moved"``: list of (src, dst) string tuples that were moved
          - ``"rewritten"``: list of file paths that were rewritten
          - ``"verify_success"``: bool or None if verify was not requested
    """
    root = root.resolve()

    # 1. Idempotency check
    if hugo_toml_path(root).exists():
        print("Already on new layout — nothing to do.")
        return {"moved": [], "rewritten": [], "verify_success": None}

    use_git = _is_git_repo(root)

    # 2. Dirty-tree check
    if use_git and not force:
        if _is_dirty(root):
            raise RuntimeError(
                "Cannot migrate: git working tree has uncommitted changes. "
                "Commit or stash your changes first, or pass --force to skip this check."
            )

    # Determine which moves to make
    planned_moves: list[tuple[Path, Path]] = []
    site = site_root(root)

    for name in _REQUIRED_MOVES:
        src = root / name
        if src.exists():
            dst = site / name
            planned_moves.append((src, dst))

    for name in _OPTIONAL_MOVES:
        src = root / name
        if src.exists():
            dst = site / name
            planned_moves.append((src, dst))

    # 3. Dry-run mode
    if dry_run:
        print("Planned moves (dry-run, no changes made):")
        for src, dst in planned_moves:
            print(f"  {src.relative_to(root)} -> {dst.relative_to(root)}")
        return {
            "moved": [(str(s.relative_to(root)), str(d.relative_to(root))) for s, d in planned_moves],
            "rewritten": [],
            "verify_success": None,
        }

    # 4. Create site/ directory
    site.mkdir(parents=True, exist_ok=True)

    # 5. Move files
    moved: list[tuple[str, str]] = []
    for src, dst in planned_moves:
        _move(root, src, dst, use_git)
        moved.append((str(src.relative_to(root)), str(dst.relative_to(root))))

    # 6. Rewrite site/hugo.toml
    rewritten: list[str] = []
    new_hugo_toml = hugo_toml_path(root)
    if new_hugo_toml.exists():
        _rewrite_hugo_toml(new_hugo_toml)
        rewritten.append(str(new_hugo_toml.relative_to(root)))

    # 7. Update .gitignore
    _update_gitignore(root)
    rewritten.append(".gitignore")

    # 8. Optional verification
    verify_success: bool | None = None
    if verify:
        result = subprocess.run(
            ["hugo", "--source", "site"],
            cwd=str(root),
            capture_output=True,
            text=True,
        )
        verify_success = result.returncode == 0
        if verify_success:
            print("Verification: hugo --source site succeeded.")
        else:
            print(f"Verification: hugo --source site FAILED.\n{result.stderr}")

    return {
        "moved": moved,
        "rewritten": rewritten,
        "verify_success": verify_success,
    }
