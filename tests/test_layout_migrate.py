"""Tests for curik.layout_migrate — hugo-layout migration."""

from __future__ import annotations

import os
import subprocess
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from curik.layout_migrate import migrate_hugo_layout


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_legacy_project(root: Path, *, include_layouts: bool = False) -> None:
    """Create a minimal legacy-layout project (Hugo files at root, not in site/)."""
    # hugo.toml with the old mount format
    (root / "hugo.toml").write_text(
        'baseURL = "/"\n'
        'title = "Test Course"\n'
        'theme = "curriculum-hugo-theme"\n'
        "\n"
        "[[module.mounts]]\n"
        '  source = "content"\n'
        '  target = "content"\n'
        "[[module.mounts]]\n"
        '  source = "course.yml"\n'
        '  target = "data/course.yml"\n'
        "\n"
        "[params]\n"
        '  copyright = "League"\n'
        '  curriculum_version = "0.20260101.1"\n',
        encoding="utf-8",
    )
    (root / "themes" / "curriculum-hugo-theme").mkdir(parents=True)
    # Git can only track files, so add a placeholder inside the theme dir
    (root / "themes" / "curriculum-hugo-theme" / "theme.toml").write_text(
        'name = "curriculum-hugo-theme"\nversion = "0.1.0"\n'
    )
    (root / "content").mkdir()
    (root / "content" / "_index.md").write_text("---\ntitle: Home\n---\n")

    if include_layouts:
        (root / "layouts").mkdir()
        (root / "layouts" / "_default").mkdir()
        (root / "layouts" / "_default" / "baseof.html").write_text(
            "{{ block main . }}{{ end }}"
        )


def _make_git_repo(root: Path) -> None:
    """Initialize a git repo in *root* with an initial commit."""
    subprocess.run(["git", "init"], cwd=str(root), check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=str(root), check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=str(root), check=True, capture_output=True,
    )
    subprocess.run(["git", "add", "-A"], cwd=str(root), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=str(root), check=True, capture_output=True,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_fresh_project_no_op() -> None:
    """Already-migrated project (site/hugo.toml exists) returns nothing-to-do."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "site").mkdir()
        (root / "site" / "hugo.toml").write_text("[config]\n")

        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            result = migrate_hugo_layout(root)

        assert result["moved"] == []
        assert result["rewritten"] == []
        assert result["verify_success"] is None
        assert "nothing to do" in mock_out.getvalue().lower()


def test_legacy_migration_non_git() -> None:
    """Non-git project: files moved with shutil, site/hugo.toml mount rewritten."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)

        result = migrate_hugo_layout(root)

        # Required files must be moved
        assert (root / "site" / "hugo.toml").exists()
        assert (root / "site" / "themes" / "curriculum-hugo-theme").exists()
        assert (root / "site" / "content" / "_index.md").exists()

        # Originals must be gone
        assert not (root / "hugo.toml").exists()
        assert not (root / "themes").exists()
        assert not (root / "content").exists()

        # Mount rewritten
        toml_content = (root / "site" / "hugo.toml").read_text(encoding="utf-8")
        assert 'source = "../course.yml"' in toml_content
        assert 'source = "course.yml"' not in toml_content

        # Moved list is non-empty
        assert len(result["moved"]) >= 3


def test_params_section_preserved() -> None:
    """[params] section from original hugo.toml is preserved in site/hugo.toml."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)

        migrate_hugo_layout(root)

        toml_content = (root / "site" / "hugo.toml").read_text(encoding="utf-8")
        assert "[params]" in toml_content
        assert 'copyright = "League"' in toml_content
        assert 'curriculum_version = "0.20260101.1"' in toml_content


def test_dirty_tree_refusal() -> None:
    """Dirty git tree without --force raises RuntimeError."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)
        _make_git_repo(root)
        # Add an uncommitted change
        (root / "dirty.txt").write_text("uncommitted change")

        with pytest.raises(RuntimeError, match="uncommitted changes"):
            migrate_hugo_layout(root)


def test_dirty_tree_force_proceeds() -> None:
    """Dirty git tree with force=True proceeds with the migration."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)
        _make_git_repo(root)
        # Add an uncommitted change
        (root / "dirty.txt").write_text("uncommitted change")

        result = migrate_hugo_layout(root, force=True)

        # Migration should have completed
        assert (root / "site" / "hugo.toml").exists()
        assert len(result["moved"]) >= 3


def test_idempotency() -> None:
    """Second run reports nothing to do (idempotent)."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)

        migrate_hugo_layout(root)

        # Second run
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            result = migrate_hugo_layout(root)

        assert result["moved"] == []
        assert "nothing to do" in mock_out.getvalue().lower()


def test_dry_run_no_writes() -> None:
    """--dry-run returns planned moves but makes no filesystem changes."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)

        result = migrate_hugo_layout(root, dry_run=True)

        # No files should have moved
        assert (root / "hugo.toml").exists()
        assert (root / "themes").exists()
        assert (root / "content").exists()
        assert not (root / "site" / "hugo.toml").exists()

        # But the plan is returned
        assert len(result["moved"]) >= 3
        assert result["rewritten"] == []


def test_gitignore_rewritten() -> None:
    """.gitignore CURIK block is updated to site/ paths."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)

        # Write a legacy .gitignore with old paths
        (root / ".gitignore").write_text(
            "# -- CURIK:START --\n"
            "public/\n"
            "resources/_gen/\n"
            ".hugo_build.lock\n"
            "# -- CURIK:END --\n"
            "\n"
            "*.pyc\n",
            encoding="utf-8",
        )

        migrate_hugo_layout(root)

        gi = (root / ".gitignore").read_text(encoding="utf-8")
        assert "site/public/" in gi
        assert "site/resources/_gen/" in gi
        assert "site/.hugo_build.lock" in gi
        # Old paths should be gone
        assert "\npublic/\n" not in gi
        # User content preserved
        assert "*.pyc" in gi


def test_gitignore_no_block_appended() -> None:
    """.gitignore without CURIK block gets the block prepended."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)

        # .gitignore with no CURIK block
        (root / ".gitignore").write_text("*.log\n*.pyc\n", encoding="utf-8")

        migrate_hugo_layout(root)

        gi = (root / ".gitignore").read_text(encoding="utf-8")
        assert "# -- CURIK:START --" in gi
        assert "site/public/" in gi
        # Original content preserved
        assert "*.log" in gi


def test_gitignore_created_if_absent() -> None:
    """.gitignore is created with CURIK block if it does not exist."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)

        assert not (root / ".gitignore").exists()

        migrate_hugo_layout(root)

        gi = (root / ".gitignore").read_text(encoding="utf-8")
        assert "site/public/" in gi


def test_layouts_moved_if_exists() -> None:
    """layouts/ at root is moved into site/ when present."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root, include_layouts=True)

        result = migrate_hugo_layout(root)

        assert (root / "site" / "layouts" / "_default" / "baseof.html").exists()
        assert not (root / "layouts").exists()
        moved_srcs = [m[0] for m in result["moved"]]
        assert "layouts" in moved_srcs


def test_layouts_skipped_if_absent() -> None:
    """No error when layouts/ does not exist."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)  # no include_layouts=True

        # Should succeed without error
        result = migrate_hugo_layout(root)

        assert not (root / "site" / "layouts").exists()
        moved_srcs = [m[0] for m in result["moved"]]
        assert "layouts" not in moved_srcs


def test_git_mv_used_in_git_repo() -> None:
    """git mv is called instead of shutil.move when inside a git repo."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)
        _make_git_repo(root)

        result = migrate_hugo_layout(root, force=True)

        # Files should be in site/ and tracked by git
        assert (root / "site" / "hugo.toml").exists()
        assert len(result["moved"]) >= 3

        # Verify git knows about the new location
        git_status = subprocess.run(
            ["git", "status", "--short"],
            cwd=str(root),
            capture_output=True,
            text=True,
        )
        # git mv shows as rename (R) in status
        assert "site/hugo.toml" in git_status.stdout


def test_cli_subcommand_available() -> None:
    """curik migrate hugo-layout is available as a CLI subcommand."""
    from curik.cli import main

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)

        with patch("sys.stdout", new_callable=StringIO):
            rc = main(["migrate", "hugo-layout", "--path", str(root)])

        assert rc == 0
        assert (root / "site" / "hugo.toml").exists()


def test_cli_dry_run_flag() -> None:
    """--dry-run flag works through the CLI."""
    from curik.cli import main

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_legacy_project(root)

        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            rc = main(["migrate", "hugo-layout", "--dry-run", "--path", str(root)])

        assert rc == 0
        # Files should not have moved
        assert (root / "hugo.toml").exists()
        assert "dry-run" in mock_out.getvalue().lower()


def test_cli_already_migrated() -> None:
    """CLI reports nothing to do when site/hugo.toml already exists."""
    from curik.cli import main
    import os

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "site").mkdir()
        (root / "site" / "hugo.toml").write_text("[config]\n")

        with (
            patch("sys.stdout", new_callable=StringIO) as mock_out,
            patch.dict(os.environ, {"CURIK_NO_LAYOUT_WARNING": "1"}),
        ):
            rc = main(["migrate", "hugo-layout", "--path", str(root)])

        assert rc == 0
        assert "nothing to do" in mock_out.getvalue().lower()
