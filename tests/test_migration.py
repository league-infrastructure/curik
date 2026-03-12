"""Tests for migration tools and templates."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from curik.migrate import inventory_course, migrate_structure
from curik.templates import get_course_yml_template, get_devcontainer_json, get_mkdocs_yml


class TestInventoryCourseEmpty(unittest.TestCase):
    """inventory_course on an empty directory."""

    def test_empty_dir_returns_all_false(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = inventory_course(tmp)
            self.assertFalse(result["has_course_yml"])
            self.assertFalse(result["has_docs"])
            self.assertFalse(result["has_lessons"])
            self.assertEqual(result["tier_guess"], 0)
            self.assertEqual(result["generator_guess"], "unknown")
            self.assertEqual(result["lesson_count"], 0)
            self.assertFalse(result["has_devcontainer"])


class TestInventoryCoursePopulated(unittest.TestCase):
    """inventory_course on a directory with course.yml and docs/."""

    def test_detects_course_yml_and_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "course.yml").write_text("title: Test\ntier: 3\n")
            docs = root / "docs"
            docs.mkdir()
            (docs / "lesson1.md").write_text("# Lesson 1\n")
            (docs / "lesson2.md").write_text("# Lesson 2\n")

            result = inventory_course(tmp)
            self.assertTrue(result["has_course_yml"])
            self.assertTrue(result["has_docs"])
            self.assertTrue(result["has_lessons"])
            self.assertEqual(result["tier_guess"], 3)
            self.assertEqual(result["lesson_count"], 2)

    def test_detects_mkdocs_generator(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "mkdocs.yml").write_text("site_name: test\n")
            result = inventory_course(tmp)
            self.assertEqual(result["generator_guess"], "mkdocs")

    def test_detects_devcontainer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".devcontainer").mkdir()
            result = inventory_course(tmp)
            self.assertTrue(result["has_devcontainer"])


class TestMigrateStructure(unittest.TestCase):
    """migrate_structure creates expected directories for tier 3."""

    def test_creates_tier3_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            modules = ["01-intro", "02-variables", "03-loops"]
            result = migrate_structure(root, 3, modules)

            # .course/ should be initialized
            self.assertTrue((root / ".course" / "state.json").is_file())

            # docs/ and mkdocs.yml should exist
            self.assertTrue((root / "docs").is_dir())
            self.assertTrue((root / "mkdocs.yml").is_file())

            # Each module should have a directory and index.md
            for mod in modules:
                self.assertTrue((root / "docs" / mod).is_dir())
                self.assertTrue((root / "docs" / mod / "index.md").is_file())

            # created list should contain relevant paths
            self.assertIn("docs", result["created"])
            self.assertIn("mkdocs.yml", result["created"])

    def test_idempotent_on_existing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            modules = ["01-intro"]
            migrate_structure(root, 3, modules)
            # Run again — should not fail
            result2 = migrate_structure(root, 3, modules)
            # Nothing new should be created on second run
            self.assertEqual(result2["created"], [])


class TestGetMkdocsYml(unittest.TestCase):
    """get_mkdocs_yml returns valid YAML with Material theme."""

    def test_tier3_has_material_theme(self) -> None:
        content = get_mkdocs_yml("Test Course", 3)
        parsed = yaml.safe_load(content)
        self.assertEqual(parsed["theme"]["name"], "material")
        self.assertEqual(parsed["site_name"], "Test Course")

    def test_tier1_includes_instructor_css(self) -> None:
        content = get_mkdocs_yml("Tier 1 Course", 1)
        parsed = yaml.safe_load(content)
        self.assertIn("css/instructor-guide.css", parsed["extra_css"])
        self.assertIn("js/instructor-guide.js", parsed["extra_javascript"])

    def test_tier3_no_instructor_css(self) -> None:
        content = get_mkdocs_yml("Tier 3 Course", 3)
        parsed = yaml.safe_load(content)
        self.assertNotIn("extra_css", parsed)


class TestGetDevcontainerJson(unittest.TestCase):
    """get_devcontainer_json returns valid JSON."""

    def test_python_devcontainer(self) -> None:
        content = get_devcontainer_json("python")
        parsed = json.loads(content)
        self.assertIn("python", parsed["image"].lower())
        self.assertEqual(parsed["name"], "Python Development")

    def test_java_devcontainer(self) -> None:
        content = get_devcontainer_json("java")
        parsed = json.loads(content)
        self.assertIn("java", parsed["image"].lower())


class TestGetCourseYmlTemplate(unittest.TestCase):
    """get_course_yml_template returns appropriate defaults per tier."""

    def test_tier1_defaults(self) -> None:
        content = get_course_yml_template(1)
        self.assertIn("tier: 1", content)
        self.assertIn("grades: K-2", content)
        self.assertIn("category: unplugged", content)

    def test_tier3_defaults(self) -> None:
        content = get_course_yml_template(3)
        self.assertIn("tier: 3", content)
        self.assertIn("grades: 6-8", content)
        self.assertIn("category: text-programming", content)

    def test_tier4_defaults(self) -> None:
        content = get_course_yml_template(4)
        self.assertIn("tier: 4", content)
        self.assertIn("grades: 9-12", content)
        self.assertIn("estimated_weeks: 12", content)


if __name__ == "__main__":
    unittest.main()
