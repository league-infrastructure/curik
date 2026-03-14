from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from curik.assets import get_skill_definition
from curik.project import (
    CurikError,
    SPEC_SECTION_HEADINGS,
    advance_phase,
    get_phase,
    init_course,
    update_spec,
)
from curik.scaffolding import scaffold_structure


def _fake_clone(dest: Path, tag: str) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "theme.toml").write_text(f'name = "curriculum-hugo-theme"\n')


_clone_patch = patch("curik.templates._clone_theme", side_effect=_fake_clone)


def setUpModule() -> None:
    _clone_patch.start()


def tearDownModule() -> None:
    _clone_patch.stop()


# Sections that resource collections skip.
_SKIP = {"pedagogical-model", "alignment-decision"}

# The five sections required for resource collections.
_RC_SECTIONS = [k for k in SPEC_SECTION_HEADINGS if k not in _SKIP]


class InitCourseTypeTest(unittest.TestCase):
    """Ticket 001: course_type parameter on init_course."""

    def test_default_type_is_course(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            state = json.loads((root / ".course" / "state.json").read_text())
            self.assertEqual(state["type"], "course")

    def test_resource_collection_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root, course_type="resource-collection")
            state = json.loads((root / ".course" / "state.json").read_text())
            self.assertEqual(state["type"], "resource-collection")

    def test_resource_collection_course_yml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root, course_type="resource-collection")
            yml = (root / "course.yml").read_text()
            self.assertIn("type: resource-collection", yml)

    def test_default_course_yml_has_type_course(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            yml = (root / "course.yml").read_text()
            self.assertIn("type: course", yml)

    def test_invalid_type_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(CurikError):
                init_course(root, course_type="invalid")


class GetPhaseRequirementsTest(unittest.TestCase):
    """Ticket 001: get_phase returns adjusted requirements."""

    def test_course_has_seven_requirements(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            info = get_phase(root)
            self.assertEqual(len(info["requirements"]), 7)

    def test_resource_collection_has_five_requirements(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root, course_type="resource-collection")
            info = get_phase(root)
            self.assertEqual(len(info["requirements"]), 5)
            for skipped in _SKIP:
                self.assertNotIn(skipped, info["requirements"])

    def test_missing_type_defaults_to_course(self) -> None:
        """Backward compat: state.json without 'type' behaves as course."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            # Remove 'type' from state to simulate legacy project
            state_path = root / ".course" / "state.json"
            state = json.loads(state_path.read_text())
            del state["type"]
            state_path.write_text(json.dumps(state, indent=2) + "\n")
            info = get_phase(root)
            self.assertEqual(len(info["requirements"]), 7)


class AdvancePhaseResourceCollectionTest(unittest.TestCase):
    """Ticket 004: advance_phase skips gates for resource collections."""

    def test_rc_advances_with_five_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root, course_type="resource-collection")
            for section in _RC_SECTIONS:
                update_spec(root, section, f"{section} content")
            advance_phase(root, "phase2")
            self.assertEqual(get_phase(root)["phase"], "phase2")

    def test_course_fails_with_only_five_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root, course_type="course")
            for section in _RC_SECTIONS:
                update_spec(root, section, f"{section} content")
            with self.assertRaises(CurikError) as ctx:
                advance_phase(root, "phase2")
            msg = str(ctx.exception)
            self.assertIn("pedagogical-model", msg)
            self.assertIn("alignment-decision", msg)

    def test_course_advances_with_all_seven_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            for section in SPEC_SECTION_HEADINGS:
                update_spec(root, section, f"{section} content")
            advance_phase(root, "phase2")
            self.assertEqual(get_phase(root)["phase"], "phase2")


class ScaffoldResourceCollectionTest(unittest.TestCase):
    """Ticket 003: scaffold_structure creates resources/ for RC."""

    _structure = {
        "modules": [
            {"name": "how-to-guides", "lessons": ["01-setup.md"]},
        ]
    }

    def test_rc_creates_under_resources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = scaffold_structure(
                root, self._structure, course_type="resource-collection"
            )
            self.assertTrue(
                (root / "resources" / "how-to-guides" / "01-setup.md").is_file()
            )
            self.assertIn(
                "resources/how-to-guides", result["created"]
            )
            self.assertIn(
                "resources/how-to-guides/01-setup.md", result["created"]
            )

    def test_default_creates_under_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = scaffold_structure(root, self._structure)
            self.assertTrue(
                (root / "content" / "how-to-guides" / "01-setup.md").is_file()
            )
            self.assertIn("content/how-to-guides", result["created"])
            self.assertNotIn("resources/how-to-guides", result["created"])


class SkillDefinitionTest(unittest.TestCase):
    """Ticket 002: resource-collection-spec skill exists."""

    def test_skill_loads(self) -> None:
        content = get_skill_definition("resource-collection-spec")
        self.assertIn("# Resource Collection Spec", content)
        self.assertIn("pedagogical-model", content)


if __name__ == "__main__":
    unittest.main()
