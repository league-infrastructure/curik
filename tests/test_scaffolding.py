from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from curik.project import CurikError, init_course
from curik.scaffolding import (
    approve_outline,
    create_lesson_stub,
    create_outline,
    generate_change_plan,
    generate_nav,
    get_outline,
    scaffold_structure,
)
from curik.templates import get_mkdocs_yml


class ScaffoldStructureTest(unittest.TestCase):
    def test_creates_directories_and_stub_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            structure = {
                "modules": [
                    {
                        "name": "01-intro",
                        "lessons": ["01-hello.md", "02-variables.md"],
                    },
                    {
                        "name": "02-loops",
                        "lessons": ["01-for.md"],
                    },
                ]
            }
            result = scaffold_structure(root, structure)
            self.assertIn("01-intro", result["created"])
            self.assertIn("01-intro/01-hello.md", result["created"])
            self.assertIn("01-intro/02-variables.md", result["created"])
            self.assertIn("02-loops", result["created"])
            self.assertIn("02-loops/01-for.md", result["created"])
            self.assertEqual(result["existing"], [])

            # Files actually exist
            self.assertTrue((root / "01-intro" / "01-hello.md").is_file())
            self.assertTrue((root / "02-loops" / "01-for.md").is_file())

    def test_stub_content_has_title_and_instructor_guide(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            structure = {
                "modules": [
                    {"name": "mod", "lessons": ["01-hello-world.md"]},
                ]
            }
            scaffold_structure(root, structure)
            content = (root / "mod" / "01-hello-world.md").read_text()
            self.assertIn("# Hello World", content)
            self.assertIn('class="instructor-guide"', content)

    def test_existing_dirs_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "01-intro").mkdir()
            structure = {
                "modules": [
                    {"name": "01-intro", "lessons": ["01-hello.md"]},
                ]
            }
            result = scaffold_structure(root, structure)
            self.assertIn("01-intro", result["existing"])
            self.assertIn("01-intro/01-hello.md", result["created"])

    def test_rejects_empty_modules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(CurikError):
                scaffold_structure(root, {"modules": []})

    def test_rejects_missing_modules_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(CurikError):
                scaffold_structure(root, {})


class CreateLessonStubTest(unittest.TestCase):
    def test_tier1_instructor_guide_primary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = create_lesson_stub(root, "mod1", "01-basics.md", 1)
            self.assertEqual(rel, "mod1/01-basics.md")
            content = (root / "mod1" / "01-basics.md").read_text()
            self.assertIn("# Basics", content)
            self.assertIn('class="instructor-guide"', content)
            self.assertNotIn("Student Content", content)

    def test_tier2_instructor_guide_primary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_lesson_stub(root, "mod1", "01-basics.md", 2)
            content = (root / "mod1" / "01-basics.md").read_text()
            self.assertNotIn("Student Content", content)

    def test_tier3_has_student_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_lesson_stub(root, "mod1", "01-basics.md", 3)
            content = (root / "mod1" / "01-basics.md").read_text()
            self.assertIn("## Student Content", content)
            self.assertIn('class="instructor-guide"', content)

    def test_tier4_has_student_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_lesson_stub(root, "mod1", "01-basics.md", 4)
            content = (root / "mod1" / "01-basics.md").read_text()
            self.assertIn("## Student Content", content)

    def test_tier3_ipynb_creates_notebook(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_lesson_stub(root, "mod1", "01-lab.ipynb", 3)
            path = root / "mod1" / "01-lab.ipynb"
            self.assertTrue(path.is_file())
            nb = json.loads(path.read_text())
            self.assertEqual(nb["nbformat"], 4)
            self.assertEqual(nb["cells"][0]["cell_type"], "markdown")
            self.assertIn("# Lab", nb["cells"][0]["source"][0])

    def test_tier1_ipynb_no_notebook_stub(self) -> None:
        """Tier 1-2 .ipynb lessons do NOT get a companion notebook."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_lesson_stub(root, "mod1", "01-lab.ipynb", 1)
            path = root / "mod1" / "01-lab.ipynb"
            content = path.read_text()
            # Should be the markdown stub, not JSON
            self.assertIn("# Lab", content)
            self.assertNotIn("nbformat", content)

    def test_invalid_tier_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(CurikError):
                create_lesson_stub(root, "mod1", "01-basics.md", 5)


class OutlineTest(unittest.TestCase):
    def test_create_get_approve_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)

            rel = create_outline(root, "Module 1 Outline", "Some outline content here.")
            self.assertIn(".course/outlines/module-1-outline.md", rel)

            text = get_outline(root, "Module 1 Outline")
            self.assertIn("title: Module 1 Outline", text)
            self.assertIn("approved: false", text)
            self.assertIn("Some outline content here.", text)

            approve_outline(root, "Module 1 Outline")
            text = get_outline(root, "Module 1 Outline")
            self.assertIn("approved: true", text)

    def test_approve_missing_outline_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            with self.assertRaises(CurikError):
                approve_outline(root, "nonexistent")

    def test_get_missing_outline_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            with self.assertRaises(CurikError):
                get_outline(root, "nonexistent")

    def test_create_outline_without_init(self) -> None:
        """create_outline should work even without init (creates dir)."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = create_outline(root, "Quick Plan", "Content here.")
            self.assertTrue((root / ".course" / "outlines" / "quick-plan.md").is_file())


class ChangePlanTest(unittest.TestCase):
    def test_generate_change_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            items = [
                "Add module 3 on recursion",
                "Update assessment rubric",
                "Create lab exercises",
            ]
            rel = generate_change_plan(root, "Add Recursion Module", items)
            self.assertIn("change-plan/active/add-recursion-module.md", rel)

            path = root / ".course" / "change-plan" / "active" / "add-recursion-module.md"
            content = path.read_text()
            self.assertIn("title: Add Recursion Module", content)
            self.assertIn("status: active", content)
            self.assertIn("1. Add module 3 on recursion", content)
            self.assertIn("2. Update assessment rubric", content)
            self.assertIn("3. Create lab exercises", content)

    def test_empty_items_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            with self.assertRaises(CurikError):
                generate_change_plan(root, "Empty Plan", [])

    def test_generate_without_init(self) -> None:
        """generate_change_plan should work even without init (creates dir)."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = generate_change_plan(root, "Quick Fix", ["Do something"])
            self.assertTrue(
                (root / ".course" / "change-plan" / "active" / "quick-fix.md").is_file()
            )


class CreateLessonStubUidTest(unittest.TestCase):
    def test_with_uid_contains_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_lesson_stub(root, "mod1", "01-basics.md", 3, uid="abc12345")
            content = (root / "mod1" / "01-basics.md").read_text()
            self.assertTrue(content.startswith("---\nuid: abc12345\n---\n\n"))
            self.assertIn("# Basics", content)

    def test_without_uid_no_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_lesson_stub(root, "mod1", "01-basics.md", 3)
            content = (root / "mod1" / "01-basics.md").read_text()
            self.assertFalse(content.startswith("---"))
            self.assertTrue(content.startswith("# Basics"))


class ScaffoldTierMirrorTest(unittest.TestCase):
    def _structure(self) -> dict:
        return {
            "modules": [
                {"name": "01-intro", "lessons": ["01-hello.md"]},
                {"name": "02-loops", "lessons": ["01-for.md"]},
            ]
        }

    def test_tier3_creates_mirror_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = scaffold_structure(root, self._structure(), tier=3)
            self.assertTrue((root / "lessons" / "01-intro").is_dir())
            self.assertTrue((root / "lessons" / "02-loops").is_dir())
            self.assertTrue((root / "projects" / "01-intro").is_dir())
            self.assertTrue((root / "projects" / "02-loops").is_dir())
            self.assertIn("lessons/01-intro", result["created"])
            self.assertIn("projects/01-intro", result["created"])

    def test_tier1_no_mirror_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scaffold_structure(root, self._structure(), tier=1)
            self.assertFalse((root / "lessons").exists())
            self.assertFalse((root / "projects").exists())

    def test_tier_none_no_mirror_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scaffold_structure(root, self._structure())
            self.assertFalse((root / "lessons").exists())
            self.assertFalse((root / "projects").exists())


class ScaffoldDevcontainerTest(unittest.TestCase):
    def test_tier3_creates_devcontainer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            structure = {
                "modules": [{"name": "01-intro", "lessons": ["01-hello.md"]}]
            }
            result = scaffold_structure(root, structure, tier=3, language="python")
            dc_path = root / ".devcontainer" / "devcontainer.json"
            self.assertTrue(dc_path.is_file())
            content = json.loads(dc_path.read_text())
            self.assertIn("python", content["image"].lower())

    def test_tier1_no_devcontainer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            structure = {
                "modules": [{"name": "01-intro", "lessons": ["01-hello.md"]}]
            }
            scaffold_structure(root, structure, tier=1)
            self.assertFalse((root / ".devcontainer").exists())


class GenerateNavTest(unittest.TestCase):
    def test_produces_expected_nav_list(self) -> None:
        structure = {
            "modules": [
                {"name": "01-intro", "lessons": ["01-hello.md", "02-vars.md"]},
                {"name": "02-loops", "lessons": ["01-for.md"]},
            ]
        }
        nav = generate_nav(structure)
        self.assertEqual(len(nav), 2)
        self.assertIn("Intro", nav[0])
        self.assertEqual(
            nav[0]["Intro"], ["01-intro/01-hello.md", "01-intro/02-vars.md"]
        )
        self.assertIn("Loops", nav[1])
        self.assertEqual(nav[1]["Loops"], ["02-loops/01-for.md"])


class MkdocsNavTest(unittest.TestCase):
    def test_with_nav_includes_nav_section(self) -> None:
        nav = [{"Intro": ["01-intro/01-hello.md"]}]
        yml = get_mkdocs_yml("Test", 3, nav=nav)
        self.assertIn("nav:", yml)
        self.assertIn("Intro:", yml)
        self.assertIn("01-intro/01-hello.md", yml)

    def test_without_nav_omits_nav_section(self) -> None:
        yml = get_mkdocs_yml("Test", 3)
        self.assertNotIn("nav:", yml)


if __name__ == "__main__":
    unittest.main()
