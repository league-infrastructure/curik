"""Tests for instruction files — verify all load and activity guides are complete."""

from __future__ import annotations

import unittest

from curik.assets import (
    ACTIVITY_MAPPINGS,
    get_activity_guide,
    get_instruction,
    list_instructions,
)


class InstructionFilesLoadTest(unittest.TestCase):
    """Each instruction file defined in the spec must load successfully."""

    EXPECTED_INSTRUCTIONS = [
        "curriculum-process",
        "course-taxonomy",
        "hugo-conventions",
        "lesson-page-template",
        "instructor-guide-requirements",
    ]

    def test_all_expected_instructions_exist(self) -> None:
        instructions = list_instructions()
        for name in self.EXPECTED_INSTRUCTIONS:
            self.assertIn(name, instructions, f"Missing instruction: {name}")

    def test_curriculum_process_loads(self) -> None:
        content = get_instruction("curriculum-process")
        self.assertIn("Curriculum Development Process", content)
        self.assertIn("Phase 1", content)
        self.assertIn("Phase 2", content)

    def test_course_taxonomy_loads(self) -> None:
        content = get_instruction("course-taxonomy")
        self.assertIn("Tier", content)
        self.assertIn("resource-collection", content)

    def test_hugo_conventions_loads(self) -> None:
        content = get_instruction("hugo-conventions")
        self.assertIn("hugo.toml", content)
        self.assertIn("shortcode", content.lower())

    def test_lesson_page_template_loads(self) -> None:
        content = get_instruction("lesson-page-template")
        self.assertIn("instructor-guide", content)
        self.assertIn("Tier 1", content)

    def test_instructor_guide_requirements_loads(self) -> None:
        content = get_instruction("instructor-guide-requirements")
        self.assertIn("7 Required Fields", content)
        self.assertIn("Objectives", content)
        self.assertIn("Differentiation", content)


class ActivityGuidesCompleteTest(unittest.TestCase):
    """After Sprint 021, no activity guide should have 'not yet written' placeholders
    for instruction files."""

    def test_no_instruction_placeholders(self) -> None:
        for activity in ACTIVITY_MAPPINGS:
            guide = get_activity_guide(activity)
            # Check that no instruction placeholders remain
            # (skill placeholders may still exist — those are Sprint 022)
            _, _, instruction_names = ACTIVITY_MAPPINGS[activity]
            for instr_name in instruction_names:
                self.assertNotIn(
                    f"Instruction `{instr_name}` not yet written",
                    guide,
                    f"Activity {activity!r} still has placeholder for instruction {instr_name!r}",
                )


if __name__ == "__main__":
    unittest.main()
