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
    get_outline,
    scaffold_structure,
)


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
            self.assertIn(".curik/outlines/module-1-outline.md", rel)

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
            self.assertTrue((root / ".curik" / "outlines" / "quick-plan.md").is_file())


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

            path = root / ".curik" / "change-plan" / "active" / "add-recursion-module.md"
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
                (root / ".curik" / "change-plan" / "active" / "quick-fix.md").is_file()
            )


if __name__ == "__main__":
    unittest.main()
