"""Tests for curik.paths — Hugo path helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from curik.paths import (
    SITE_DIR,
    content_dir,
    hugo_toml_path,
    site_root,
    theme_dir,
    themes_dir,
)

ROOT = Path("/tmp/my-course")


def test_site_dir_constant() -> None:
    assert SITE_DIR == "site"
    assert isinstance(SITE_DIR, str)
    assert not SITE_DIR.endswith("/")


def test_site_root_returns_path() -> None:
    result = site_root(ROOT)
    assert isinstance(result, Path)


def test_site_root_value() -> None:
    assert site_root(ROOT) == Path("/tmp/my-course/site")


def test_hugo_toml_path_returns_path() -> None:
    result = hugo_toml_path(ROOT)
    assert isinstance(result, Path)


def test_hugo_toml_path_value() -> None:
    assert hugo_toml_path(ROOT) == Path("/tmp/my-course/site/hugo.toml")


def test_content_dir_returns_path() -> None:
    result = content_dir(ROOT)
    assert isinstance(result, Path)


def test_content_dir_value() -> None:
    assert content_dir(ROOT) == Path("/tmp/my-course/site/content")


def test_themes_dir_returns_path() -> None:
    result = themes_dir(ROOT)
    assert isinstance(result, Path)


def test_themes_dir_value() -> None:
    assert themes_dir(ROOT) == Path("/tmp/my-course/site/themes")


def test_theme_dir_returns_path() -> None:
    result = theme_dir(ROOT)
    assert isinstance(result, Path)


def test_theme_dir_value() -> None:
    assert theme_dir(ROOT) == Path(
        "/tmp/my-course/site/themes/curriculum-hugo-theme"
    )


@pytest.mark.parametrize(
    "helper, expected_suffix",
    [
        (site_root, "site"),
        (hugo_toml_path, "site/hugo.toml"),
        (content_dir, "site/content"),
        (themes_dir, "site/themes"),
        (theme_dir, "site/themes/curriculum-hugo-theme"),
    ],
)
def test_helpers_parametrized(helper, expected_suffix: str) -> None:
    result = helper(ROOT)
    assert isinstance(result, Path)
    assert result == ROOT / expected_suffix


def test_importable_from_curik_paths() -> None:
    """Verify the public import surface works as documented."""
    from curik.paths import content_dir as cd
    from curik.paths import site_root as sr

    assert sr(ROOT) == Path("/tmp/my-course/site")
    assert cd(ROOT) == Path("/tmp/my-course/site/content")
