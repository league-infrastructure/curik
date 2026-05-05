"""Tests for curik.publish domain module."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from curik.project import init_course
from curik.publish import check_publish_ready, get_publish_guide


class CheckPublishReadyTest(unittest.TestCase):
    def test_check_publish_ready_missing_course_yml(self) -> None:
        """Without init, course_yml_exists should be False."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = check_publish_ready(root)
            self.assertFalse(result["checks"]["course_yml_exists"])
            self.assertFalse(result["ready"])

    def test_check_publish_ready_with_tbd_fields(self) -> None:
        """After init, required fields are still TBD — should be listed."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            result = check_publish_ready(root)
            self.assertTrue(result["checks"]["course_yml_exists"])
            # All required fields start as TBD after init
            self.assertIn("course_yml_tbd_fields", result)
            tbd = result["course_yml_tbd_fields"]
            self.assertIsInstance(tbd, list)
            self.assertGreater(len(tbd), 0)
            # course_yml_complete should be False since fields are TBD
            self.assertFalse(result["checks"]["course_yml_complete"])

    def test_check_publish_ready_returns_expected_keys(self) -> None:
        """Result dict must have the standard keys."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = check_publish_ready(root)
            expected_top_keys = {"ready", "checks", "title", "url",
                                  "base_url", "expected_base_url",
                                  "content_sections", "content_pages"}
            self.assertTrue(expected_top_keys.issubset(result.keys()))
            expected_check_keys = {
                "course_yml_exists", "course_yml_complete",
                "hugo_toml_exists", "base_url_configured",
                "repo_url_set", "theme_installed", "gitignore_installed",
                "workflow_installed", "has_content", "hugo_builds",
            }
            self.assertEqual(set(result["checks"].keys()), expected_check_keys)


class GetPublishGuideTest(unittest.TestCase):
    def test_get_publish_guide_returns_string(self) -> None:
        """Guide should be a non-empty string even without a course initialized."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            guide = get_publish_guide(root)
            self.assertIsInstance(guide, str)
            self.assertGreater(len(guide), 0)

    def test_get_publish_guide_contains_key_sections(self) -> None:
        """Guide should contain the expected structural headings."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            guide = get_publish_guide(root)
            self.assertIn("Pre-Publish Checklist", guide)
            self.assertIn("Post-Publish Checklist", guide)
            self.assertIn("GitHub Repo Setup", guide)

    def test_get_publish_guide_with_initialized_course(self) -> None:
        """Guide for an initialized course references TBD fields."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            guide = get_publish_guide(root)
            # Should mention that fields are still TBD
            self.assertIn("still TBD", guide)


class CheckPublishReadyHugoLayoutTest(unittest.TestCase):
    """Verify publish readiness checks use site/ layout paths."""

    def test_hugo_toml_at_site_detected(self) -> None:
        """hugo_toml_exists is True when site/hugo.toml is present."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "site").mkdir()
            (root / "site" / "hugo.toml").write_text('[config]\ntitle = "Test"\n')
            result = check_publish_ready(root)
            self.assertTrue(result["checks"]["hugo_toml_exists"])

    def test_hugo_toml_at_root_not_detected(self) -> None:
        """hugo_toml_exists is False when hugo.toml is only at root (legacy layout)."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "hugo.toml").write_text('[config]\ntitle = "Test"\n')
            result = check_publish_ready(root)
            # Legacy root-level hugo.toml is NOT detected by the new layout check
            self.assertFalse(result["checks"]["hugo_toml_exists"])

    def test_theme_at_site_themes_detected(self) -> None:
        """theme_installed is True when site/themes/curriculum-hugo-theme/ exists."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            theme_path = root / "site" / "themes" / "curriculum-hugo-theme"
            theme_path.mkdir(parents=True)
            result = check_publish_ready(root)
            self.assertTrue(result["checks"]["theme_installed"])

    def test_theme_at_root_themes_not_detected(self) -> None:
        """theme_installed is False when theme is only at root/themes/ (legacy layout)."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy_theme = root / "themes" / "curriculum-hugo-theme"
            legacy_theme.mkdir(parents=True)
            result = check_publish_ready(root)
            self.assertFalse(result["checks"]["theme_installed"])

    def test_has_content_uses_site_content(self) -> None:
        """has_content is True when site/content/ has more than one .md file."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content_path = root / "site" / "content"
            content_path.mkdir(parents=True)
            # Needs more than one .md file (has_content = len(pages) > 1)
            (content_path / "_index.md").write_text("---\ntitle: Home\n---\n")
            (content_path / "intro.md").write_text("---\ntitle: Intro\n---\n")
            result = check_publish_ready(root)
            self.assertTrue(result["checks"]["has_content"])


class BaseUrlConfiguredTest(unittest.TestCase):
    """Verify base_url_configured uses TOML parsing and is CNAME-aware."""

    def _make_site(self, root: Path, *, base_url: str, cname: str | None = None) -> None:
        site = root / "site"
        site.mkdir(parents=True)
        (site / "hugo.toml").write_text(
            f'baseURL = "{base_url}"\ntitle = "Test"\n', encoding="utf-8"
        )
        if cname is not None:
            static = site / "static"
            static.mkdir()
            (static / "CNAME").write_text(cname + "\n", encoding="utf-8")

    def test_subpath_match_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "course.yml").write_text(
                "title: T\nrepo_url: https://github.com/league-curriculum/Motors\n",
                encoding="utf-8",
            )
            self._make_site(root, base_url="/Motors/")
            result = check_publish_ready(root)
            self.assertTrue(result["checks"]["base_url_configured"])
            self.assertEqual(result["expected_base_url"], "/Motors/")

    def test_subpath_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "course.yml").write_text(
                "title: T\nrepo_url: https://github.com/league-curriculum/Motors\n",
                encoding="utf-8",
            )
            self._make_site(root, base_url="/SomethingElse/")
            result = check_publish_ready(root)
            self.assertFalse(result["checks"]["base_url_configured"])

    def test_cname_match_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "course.yml").write_text(
                "title: T\nrepo_url: https://github.com/league-curriculum/labs\n",
                encoding="utf-8",
            )
            self._make_site(
                root,
                base_url="https://labs.jointheleague.org/",
                cname="labs.jointheleague.org",
            )
            result = check_publish_ready(root)
            self.assertTrue(result["checks"]["base_url_configured"])
            self.assertEqual(result["url"], "https://labs.jointheleague.org/")

    def test_cname_present_but_subpath_baseurl_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "course.yml").write_text(
                "title: T\nrepo_url: https://github.com/league-curriculum/labs\n",
                encoding="utf-8",
            )
            self._make_site(
                root, base_url="/labs/", cname="labs.jointheleague.org"
            )
            result = check_publish_ready(root)
            self.assertFalse(result["checks"]["base_url_configured"])

    def test_baseurl_parsed_with_inline_comment(self) -> None:
        """Substring matching used to break on comments; TOML parsing handles them."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "course.yml").write_text(
                "title: T\nrepo_url: https://github.com/league-curriculum/Motors\n",
                encoding="utf-8",
            )
            site = root / "site"
            site.mkdir()
            (site / "hugo.toml").write_text(
                'baseURL = "/Motors/" # inline comment\ntitle = "Test"\n',
                encoding="utf-8",
            )
            result = check_publish_ready(root)
            self.assertTrue(result["checks"]["base_url_configured"])


if __name__ == "__main__":
    unittest.main()
