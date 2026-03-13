"""Tests for Sprint 022 — missing skills and CLAUDE.md template rewrite."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from curik.assets import (
    ACTIVITY_MAPPINGS,
    get_activity_guide,
    get_skill_definition,
    list_skills,
)
from curik.project import init_course


class MissingSkillsLoadTest(unittest.TestCase):
    """All 3 previously missing skills must load."""

    def test_existing_content_analysis_loads(self) -> None:
        content = get_skill_definition("existing-content-analysis")
        self.assertIn("Existing Content Analysis", content)
        self.assertIn("_old/", content)

    def test_content_conversion_loads(self) -> None:
        content = get_skill_definition("content-conversion")
        self.assertIn("Content Conversion", content)
        self.assertIn("Path B", content)

    def test_change_plan_execution_loads(self) -> None:
        content = get_skill_definition("change-plan-execution")
        self.assertIn("Change Plan Execution", content)
        self.assertIn("structural", content.lower())

    def test_all_18_skills_present(self) -> None:
        skills = list_skills()
        expected = [
            "alignment-decision",
            "change-plan-execution",
            "content-conversion",
            "course-concept",
            "existing-content-analysis",
            "instructor-guide-sections",
            "lesson-writing-older",
            "lesson-writing-young",
            "pedagogical-model",
            "quiz-authoring",
            "readme-guards",
            "repo-scaffolding",
            "resource-collection-spec",
            "spec-synthesis",
            "status-tracking",
            "structure-proposal",
            "syllabus-integration",
            "validation-checklist",
        ]
        for name in expected:
            self.assertIn(name, skills, f"Missing skill: {name}")


class ActivityGuidesNoSkillPlaceholdersTest(unittest.TestCase):
    """After Sprint 022, no activity guide should have skill placeholders."""

    def test_no_skill_placeholders(self) -> None:
        for activity in ACTIVITY_MAPPINGS:
            guide = get_activity_guide(activity)
            _, skill_names, _ = ACTIVITY_MAPPINGS[activity]
            for skill_name in skill_names:
                self.assertNotIn(
                    f"Skill `{skill_name}` not yet written",
                    guide,
                    f"Activity {activity!r} still has placeholder for skill {skill_name!r}",
                )

    def test_no_placeholders_at_all(self) -> None:
        """No activity guide should have ANY 'not yet written' placeholders."""
        for activity in ACTIVITY_MAPPINGS:
            guide = get_activity_guide(activity)
            self.assertNotIn(
                "not yet written",
                guide,
                f"Activity {activity!r} still has placeholders",
            )


class ClaudeMdTemplateTest(unittest.TestCase):
    """The CLAUDE.md template matches the spec's process-routing design."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_claude_md_contains_preflight(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertIn("get_course_status()", claude_md)
        self.assertIn("get_process_guide()", claude_md)

    def test_claude_md_contains_rules(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertIn("MCP-first", claude_md)
        self.assertIn("Agent boundaries", claude_md)
        self.assertIn("Gates are gates", claude_md)

    def test_claude_md_lists_tool_categories(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertIn("Process Discovery", claude_md)
        self.assertIn("Agent and Skill Loading", claude_md)
        self.assertIn("State Management", claude_md)

    def test_claude_md_references_instructions_not_references(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertIn("list_instructions()", claude_md)
        self.assertIn("get_instruction(name)", claude_md)

    def test_claude_md_includes_activity_guide(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertIn("get_activity_guide(activity)", claude_md)


if __name__ == "__main__":
    unittest.main()
