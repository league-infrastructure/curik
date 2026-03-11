from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from curik.project import CurikError, advance_phase, get_phase, init_course, update_spec


class CurikProjectTests(unittest.TestCase):
    def test_init_creates_expected_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = init_course(root)
            self.assertIn(".course/spec.md", result["created"])
            self.assertTrue((root / ".course" / "change-plan" / "active").is_dir())
            self.assertTrue((root / "course.yml").is_file())
            self.assertTrue((root / ".mcp.json").is_file())

    def test_advance_phase_requires_non_tbd_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            with self.assertRaises(CurikError):
                advance_phase(root, "phase2")

    def test_advance_phase_after_required_sections_filled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            for section in [
                "course-concept",
                "pedagogical-model",
                "research-summary",
                "alignment-decision",
                "course-structure-outline",
                "assessment-plan",
                "technical-decisions",
            ]:
                update_spec(root, section, f"{section} content")
            advance_phase(root, "phase2")
            self.assertEqual(get_phase(root)["phase"], "phase2")


if __name__ == "__main__":
    unittest.main()
