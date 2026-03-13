"""Integration tests: copy fixture curricula, scaffold, and build Hugo sites.

These tests operate on real curriculum fixtures from tests/content_source/,
copy them to tests/content_test/ (gitignored), run scaffold and Hugo setup,
and verify the result is a buildable Hugo site.

After running tests, you can inspect the output:
    cd tests/content_test/python-basics && hugo server
"""

from __future__ import annotations

import shutil
import unittest
from pathlib import Path

from curik.hugo import hugo_build
from curik.scaffolding import scaffold_structure

TESTS_DIR = Path(__file__).resolve().parent
CONTENT_SOURCE = TESTS_DIR / "content_source"
CONTENT_TEST = TESTS_DIR / "content_test"


def _copy_fixture(name: str) -> Path:
    """Copy a fixture from content_source/ to content_test/ and return the path."""
    src = CONTENT_SOURCE / name
    dest = CONTENT_TEST / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    return dest


class PythonBasicsIntegrationTest(unittest.TestCase):
    """Integration tests using the python-basics fixture (tier 2)."""

    FIXTURE = "python-basics"
    STRUCTURE = {
        "modules": [
            {
                "name": "01-variables",
                "lessons": ["01-what-are-variables.md", "02-types.md"],
            },
            {
                "name": "02-control-flow",
                "lessons": ["01-if-statements.md", "02-loops.md", "03-functions.md"],
            },
        ]
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = _copy_fixture(cls.FIXTURE)
        cls.result = scaffold_structure(cls.root, cls.STRUCTURE, tier=2)

    def test_content_dir_created(self) -> None:
        self.assertTrue((self.root / "content").is_dir())

    def test_content_index_md_exists(self) -> None:
        index = self.root / "content" / "_index.md"
        self.assertTrue(index.is_file())
        content = index.read_text()
        self.assertIn("title:", content)

    def test_modules_created_under_content(self) -> None:
        self.assertTrue((self.root / "content" / "01-variables").is_dir())
        self.assertTrue((self.root / "content" / "02-control-flow").is_dir())

    def test_module_index_files_exist(self) -> None:
        self.assertTrue(
            (self.root / "content" / "01-variables" / "_index.md").is_file()
        )
        self.assertTrue(
            (self.root / "content" / "02-control-flow" / "_index.md").is_file()
        )

    def test_lesson_stubs_created(self) -> None:
        self.assertTrue(
            (self.root / "content" / "01-variables" / "01-what-are-variables.md").is_file()
        )
        self.assertTrue(
            (self.root / "content" / "02-control-flow" / "03-functions.md").is_file()
        )

    def test_lesson_stubs_have_instructor_guide(self) -> None:
        lesson = (
            self.root / "content" / "01-variables" / "01-what-are-variables.md"
        ).read_text()
        self.assertIn("{{< instructor-guide >}}", lesson)
        # Tier 2 should NOT have student content section
        self.assertNotIn("Student Content", lesson)

    def test_hugo_toml_generated(self) -> None:
        toml_path = self.root / "hugo.toml"
        self.assertTrue(toml_path.is_file())
        toml = toml_path.read_text()
        self.assertIn('title = "Python Basics"', toml)
        self.assertIn('theme = "curriculum-hugo-theme"', toml)
        self.assertIn("instructorGuide = true", toml)

    def test_theme_copied(self) -> None:
        theme_dir = self.root / "themes" / "curriculum-hugo-theme"
        self.assertTrue(theme_dir.is_dir())
        # Theme should have at least a theme.toml or config file
        has_config = (
            (theme_dir / "theme.toml").is_file()
            or (theme_dir / "hugo.toml").is_file()
        )
        self.assertTrue(has_config, "Theme directory should contain theme.toml or hugo.toml")

    def test_scaffold_result_lists(self) -> None:
        self.assertIn("content/_index.md", self.result["created"])
        self.assertIn("content/01-variables", self.result["created"])
        self.assertIn("hugo.toml", self.result["created"])

    def test_no_modules_at_repo_root(self) -> None:
        """Modules must be under content/, not at repo root."""
        self.assertFalse((self.root / "01-variables").exists())
        self.assertFalse((self.root / "02-control-flow").exists())

    def test_source_fixture_not_modified(self) -> None:
        """The source fixture must never have content/ or hugo.toml."""
        src = CONTENT_SOURCE / self.FIXTURE
        self.assertFalse((src / "content").exists())
        self.assertFalse((src / "hugo.toml").exists())
        self.assertFalse((src / "themes").exists())

    @unittest.skipUnless(shutil.which("hugo"), "Hugo not installed")
    def test_hugo_build_succeeds(self) -> None:
        result = hugo_build(self.root)
        self.assertTrue(result["success"], f"Hugo build failed: {result['error']}")


class WebDevIntegrationTest(unittest.TestCase):
    """Integration tests using the web-dev fixture (tier 3)."""

    FIXTURE = "web-dev"
    STRUCTURE = {
        "modules": [
            {
                "name": "01-html-basics",
                "lessons": ["01-first-page.md", "02-elements.md"],
            },
            {
                "name": "02-css-styling",
                "lessons": ["01-selectors.md", "02-layout.md", "03-responsive.md"],
            },
        ]
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = _copy_fixture(cls.FIXTURE)
        cls.result = scaffold_structure(cls.root, cls.STRUCTURE, tier=3, language="python")

    def test_content_dir_created(self) -> None:
        self.assertTrue((self.root / "content").is_dir())

    def test_content_index_md_exists(self) -> None:
        self.assertTrue((self.root / "content" / "_index.md").is_file())

    def test_modules_created_under_content(self) -> None:
        self.assertTrue((self.root / "content" / "01-html-basics").is_dir())
        self.assertTrue((self.root / "content" / "02-css-styling").is_dir())

    def test_lesson_stubs_have_student_content(self) -> None:
        """Tier 3 lessons should have student content section."""
        lesson = (
            self.root / "content" / "01-html-basics" / "01-first-page.md"
        ).read_text()
        self.assertIn("## Student Content", lesson)
        self.assertIn("{{< instructor-guide >}}", lesson)

    def test_hugo_toml_generated(self) -> None:
        toml = (self.root / "hugo.toml").read_text()
        self.assertIn('title = "Web Development"', toml)
        # Tier 3 should NOT have instructorGuide param
        self.assertNotIn("instructorGuide", toml)

    def test_theme_copied(self) -> None:
        self.assertTrue(
            (self.root / "themes" / "curriculum-hugo-theme").is_dir()
        )

    def test_tier3_mirror_dirs_created(self) -> None:
        """Tier 3 should create lessons/ and projects/ mirror dirs."""
        self.assertTrue((self.root / "lessons" / "01-html-basics").is_dir())
        self.assertTrue((self.root / "projects" / "01-html-basics").is_dir())

    def test_devcontainer_created(self) -> None:
        """Tier 3 should create .devcontainer/."""
        dc = self.root / ".devcontainer" / "devcontainer.json"
        self.assertTrue(dc.is_file())

    def test_source_fixture_not_modified(self) -> None:
        src = CONTENT_SOURCE / self.FIXTURE
        self.assertFalse((src / "content").exists())
        self.assertFalse((src / "hugo.toml").exists())

    @unittest.skipUnless(shutil.which("hugo"), "Hugo not installed")
    def test_hugo_build_succeeds(self) -> None:
        result = hugo_build(self.root)
        self.assertTrue(result["success"], f"Hugo build failed: {result['error']}")


if __name__ == "__main__":
    unittest.main()
