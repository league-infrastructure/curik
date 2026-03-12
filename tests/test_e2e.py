"""End-to-end integration test: full Phase 1 workflow through the Python API."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from curik.project import (
    SPEC_SECTION_HEADINGS,
    advance_phase,
    get_course_status,
    get_phase,
    get_spec,
    init_course,
    update_spec,
)


class TestPhase1Workflow(unittest.TestCase):
    """Walk through the full Phase 1 workflow: init, fill spec, advance."""

    def test_full_phase1_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            # Step 1: init_course
            result = init_course(root)
            self.assertIn(".curik/spec.md", result["created"])
            self.assertTrue((root / ".curik" / "state.json").is_file())
            self.assertTrue((root / "course.yml").is_file())

            # Verify we start in phase1
            phase_info = get_phase(root)
            self.assertEqual(phase_info["phase"], "phase1")
            self.assertEqual(
                sorted(phase_info["requirements"]),
                sorted(SPEC_SECTION_HEADINGS.keys()),
            )

            # Step 2: Fill all spec sections via update_spec
            spec_content = {
                "course-concept": (
                    "An introductory Python course for middle schoolers "
                    "covering variables, loops, and functions."
                ),
                "pedagogical-model": (
                    "Project-based learning with scaffolded exercises. "
                    "Each module builds a small project."
                ),
                "research-summary": (
                    "Research shows hands-on coding projects improve retention "
                    "by 40% compared to lecture-only approaches."
                ),
                "alignment-decision": (
                    "Aligned to CSTA K-12 standards for grades 6-8. "
                    "Topics: 2-AP-10, 2-AP-12, 2-AP-13."
                ),
                "course-structure-outline": (
                    "Module 1: Variables and Types\n"
                    "Module 2: Conditionals\n"
                    "Module 3: Loops\n"
                    "Module 4: Functions\n"
                    "Module 5: Final Project"
                ),
                "assessment-plan": (
                    "Formative: in-module checkpoints after each lesson.\n"
                    "Summative: end-of-module project rubric."
                ),
                "technical-decisions": (
                    "Language: Python 3.11\n"
                    "IDE: VS Code with devcontainer\n"
                    "Docs: MkDocs Material"
                ),
            }

            for section, content in spec_content.items():
                update_spec(root, section, content)

            # Verify spec was updated
            spec_text = get_spec(root)
            for content in spec_content.values():
                # Each content block should appear in the spec
                self.assertIn(content.splitlines()[0], spec_text)

            # Step 3: Advance to phase2
            advance_phase(root, "phase2")

            # Step 4: Verify get_course_status shows phase2
            status = get_course_status(root)
            self.assertEqual(status["phase"], "phase2")
            self.assertEqual(status["open_issues"], 0)
            self.assertEqual(status["active_change_plans"], 0)

            # Also verify get_phase reflects the change
            phase_info = get_phase(root)
            self.assertEqual(phase_info["phase"], "phase2")


if __name__ == "__main__":
    unittest.main()
