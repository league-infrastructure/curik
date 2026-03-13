"""Tests for curik.hugo — Hugo content page operations."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from curik.hugo import (
    create_content_page,
    hugo_build,
    list_content_pages,
    parse_frontmatter,
    render_frontmatter,
    update_frontmatter,
)
from curik.project import CurikError


class ParseFrontmatterTest(unittest.TestCase):
    def test_parses_yaml_frontmatter(self) -> None:
        text = "---\ntitle: Hello\nweight: 10\n---\n\nBody content."
        fm, body = parse_frontmatter(text)
        self.assertEqual(fm["title"], "Hello")
        self.assertEqual(fm["weight"], 10)
        self.assertEqual(body, "Body content.")

    def test_no_frontmatter(self) -> None:
        text = "Just body content."
        fm, body = parse_frontmatter(text)
        self.assertEqual(fm, {})
        self.assertEqual(body, "Just body content.")

    def test_empty_frontmatter(self) -> None:
        text = "---\n---\n\nBody."
        fm, body = parse_frontmatter(text)
        self.assertEqual(fm, {})

    def test_malformed_yaml(self) -> None:
        text = "---\n: invalid yaml [\n---\n\nBody."
        fm, body = parse_frontmatter(text)
        self.assertEqual(fm, {})


class RenderFrontmatterTest(unittest.TestCase):
    def test_renders_yaml(self) -> None:
        data = {"title": "Test", "weight": 5}
        result = render_frontmatter(data)
        self.assertTrue(result.startswith("---\n"))
        self.assertTrue(result.endswith("---\n"))
        self.assertIn("title: Test", result)
        self.assertIn("weight: 5", result)


class ListContentPagesTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_no_content_dir(self) -> None:
        result = list_content_pages(self.root)
        self.assertEqual(result, [])

    def test_lists_pages(self) -> None:
        content = self.root / "content"
        content.mkdir()
        (content / "_index.md").write_text("---\ntitle: Home\nweight: 1\n---\n")
        mod = content / "01-intro"
        mod.mkdir()
        (mod / "_index.md").write_text("---\ntitle: Intro\nweight: 10\n---\n")
        (mod / "01-hello.md").write_text("---\ntitle: Hello\ndraft: true\n---\nBody")

        pages = list_content_pages(self.root)
        self.assertEqual(len(pages), 3)
        paths = [p["path"] for p in pages]
        self.assertIn("content/01-intro/01-hello.md", paths)

        hello = next(p for p in pages if "01-hello" in p["path"])
        self.assertEqual(hello["title"], "Hello")
        self.assertTrue(hello["draft"])

    def test_section_filter(self) -> None:
        content = self.root / "content"
        content.mkdir()
        (content / "_index.md").write_text("---\ntitle: Home\n---\n")
        mod = content / "01-intro"
        mod.mkdir()
        (mod / "lesson.md").write_text("---\ntitle: Lesson\n---\n")

        pages = list_content_pages(self.root, section="01-intro")
        self.assertEqual(len(pages), 1)
        self.assertIn("01-intro", pages[0]["path"])


class CreateContentPageTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)
        (self.root / "content").mkdir()

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_creates_page(self) -> None:
        rel = create_content_page(self.root, "about.md", "About Us")
        self.assertEqual(rel, "content/about.md")
        page = (self.root / "content" / "about.md").read_text()
        self.assertIn("title: About Us", page)

    def test_creates_parent_dirs(self) -> None:
        create_content_page(self.root, "guides/setup.md", "Setup Guide")
        self.assertTrue((self.root / "content" / "guides" / "setup.md").exists())

    def test_extra_frontmatter(self) -> None:
        create_content_page(
            self.root, "page.md", "Test",
            extra_frontmatter={"weight": 5, "draft": True},
        )
        fm, _ = parse_frontmatter(
            (self.root / "content" / "page.md").read_text()
        )
        self.assertEqual(fm["weight"], 5)
        self.assertTrue(fm["draft"])

    def test_error_if_exists(self) -> None:
        create_content_page(self.root, "page.md", "First")
        with self.assertRaises(CurikError):
            create_content_page(self.root, "page.md", "Second")

    def test_path_traversal_blocked(self) -> None:
        with self.assertRaises(CurikError):
            create_content_page(self.root, "../evil.md", "Evil")

    def test_content_body(self) -> None:
        create_content_page(self.root, "page.md", "Title", content="Hello world")
        text = (self.root / "content" / "page.md").read_text()
        self.assertIn("Hello world", text)


class UpdateFrontmatterTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)
        content = self.root / "content"
        content.mkdir()
        (content / "page.md").write_text(
            "---\ntitle: Original\nweight: 1\n---\n\nBody content here."
        )

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_updates_existing_field(self) -> None:
        result = update_frontmatter(self.root, "content/page.md", {"weight": 99})
        self.assertEqual(result["weight"], 99)
        self.assertEqual(result["title"], "Original")

    def test_adds_new_field(self) -> None:
        result = update_frontmatter(self.root, "content/page.md", {"draft": True})
        self.assertTrue(result["draft"])

    def test_preserves_body(self) -> None:
        update_frontmatter(self.root, "content/page.md", {"weight": 2})
        text = (self.root / "content" / "page.md").read_text()
        self.assertIn("Body content here.", text)

    def test_error_file_not_found(self) -> None:
        with self.assertRaises(CurikError):
            update_frontmatter(self.root, "content/missing.md", {"weight": 1})


class HugoBuildTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_returns_dict_structure(self) -> None:
        result = hugo_build(self.root)
        self.assertIn("success", result)
        self.assertIn("output", result)
        self.assertIn("error", result)


class HugoSetupTest(unittest.TestCase):
    """Tests for hugo_setup() in templates.py."""

    def setUp(self) -> None:
        from curik.templates import hugo_setup, get_theme_source, THEME_NAME
        self.hugo_setup = hugo_setup
        self.theme_source = get_theme_source()
        self.theme_name = THEME_NAME

    def test_creates_hugo_toml(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.hugo_setup(root, "Test Course", 2)
            self.assertIn("hugo.toml", result["created"])
            toml = (root / "hugo.toml").read_text()
            self.assertIn('title = "Test Course"', toml)
            self.assertIn('theme = "curriculum-hugo-theme"', toml)
            self.assertIn("instructorGuide = true", toml)

    def test_copies_theme(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.hugo_setup(root, "Test", 3)
            theme_dir = root / "themes" / self.theme_name
            if self.theme_source.is_dir():
                self.assertTrue(theme_dir.is_dir())
                self.assertIn(f"themes/{self.theme_name}", result["created"])

    def test_existing_hugo_toml_not_overwritten(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "hugo.toml").write_text("existing config\n")
            result = self.hugo_setup(root, "Test", 2)
            self.assertIn("hugo.toml", result["existing"])
            self.assertEqual((root / "hugo.toml").read_text(), "existing config\n")

    def test_existing_theme_not_overwritten(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            theme_dir = root / "themes" / self.theme_name
            theme_dir.mkdir(parents=True)
            (theme_dir / "marker.txt").write_text("original")
            result = self.hugo_setup(root, "Test", 2)
            self.assertIn(f"themes/{self.theme_name}", result["existing"])
            self.assertEqual(
                (theme_dir / "marker.txt").read_text(), "original"
            )


if __name__ == "__main__":
    unittest.main()
