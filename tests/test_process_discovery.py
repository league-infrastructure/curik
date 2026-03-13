"""Tests for process discovery tools and instruction rename."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from curik.assets import (
    ACTIVITY_MAPPINGS,
    get_activity_guide,
    get_instruction,
    get_process_guide,
    get_reference,
    list_instructions,
    list_references,
)
from curik.project import CurikError, init_course
from curik import server


class ProcessGuideTest(unittest.TestCase):
    def test_returns_markdown(self) -> None:
        guide = get_process_guide()
        self.assertIn("# Curik Curriculum Development Process", guide)

    def test_contains_three_phases(self) -> None:
        guide = get_process_guide()
        self.assertIn("Project Initiation", guide)
        self.assertIn("First Version", guide)
        self.assertIn("Ongoing Changes", guide)

    def test_contains_decision_tree(self) -> None:
        guide = get_process_guide()
        self.assertIn("get_course_status()", guide)
        self.assertIn("phase1", guide) or self.assertIn("phase =", guide)

    def test_contains_agent_roster(self) -> None:
        guide = get_process_guide()
        self.assertIn("curriculum-architect", guide)
        self.assertIn("research-agent", guide)
        self.assertIn("lesson-author-young", guide)
        self.assertIn("lesson-author-older", guide)
        self.assertIn("quiz-author", guide)
        self.assertIn("reviewer", guide)

    def test_contains_activity_reference(self) -> None:
        guide = get_process_guide()
        self.assertIn("get_activity_guide", guide)
        self.assertIn("spec-development", guide)


class ActivityGuideTest(unittest.TestCase):
    def test_all_activities_defined(self) -> None:
        expected = {
            "spec-development", "research", "content-analysis",
            "scaffolding", "lesson-writing-young", "lesson-writing-older",
            "quiz-authoring", "content-conversion", "change-management",
            "validation",
        }
        self.assertEqual(set(ACTIVITY_MAPPINGS.keys()), expected)

    def test_spec_development_bundles_correctly(self) -> None:
        guide = get_activity_guide("spec-development")
        self.assertIn("Activity Guide: spec-development", guide)
        # Should include the curriculum-architect agent
        self.assertIn("Curriculum Architect", guide)
        # Should include spec skills
        self.assertIn("course-concept", guide)
        self.assertIn("pedagogical-model", guide)

    def test_research_has_no_skills(self) -> None:
        guide = get_activity_guide("research")
        self.assertIn("research-agent", guide)
        # Should not have a Skills section (no skills for research)
        self.assertNotIn("## Skills", guide)

    def test_unknown_activity_raises(self) -> None:
        with self.assertRaises(CurikError) as ctx:
            get_activity_guide("nonexistent")
        self.assertIn("Unknown activity", str(ctx.exception))
        self.assertIn("spec-development", str(ctx.exception))

    def test_missing_instruction_handled_gracefully(self) -> None:
        # Instructions not yet written should show placeholder
        guide = get_activity_guide("spec-development")
        # curriculum-process and course-taxonomy don't exist yet
        self.assertIn("not yet written", guide)

    def test_each_activity_returns_nonempty(self) -> None:
        for activity in ACTIVITY_MAPPINGS:
            guide = get_activity_guide(activity)
            self.assertIn(f"Activity Guide: {activity}", guide)
            self.assertTrue(len(guide) > 100, f"{activity} guide too short")

    def test_validation_includes_reviewer(self) -> None:
        guide = get_activity_guide("validation")
        self.assertIn("Reviewer", guide)

    def test_lesson_writing_older_includes_readme_guards(self) -> None:
        guide = get_activity_guide("lesson-writing-older")
        self.assertIn("readme-guards", guide)


class InstructionRenameTest(unittest.TestCase):
    def test_list_instructions(self) -> None:
        instructions = list_instructions()
        self.assertIn("league-web-brand-guide", instructions)
        self.assertIn("process-guide", instructions)

    def test_get_instruction(self) -> None:
        content = get_instruction("league-web-brand-guide")
        self.assertIn("League", content)

    def test_get_instruction_not_found(self) -> None:
        with self.assertRaises(CurikError):
            get_instruction("nonexistent")

    def test_backward_compat_list_references(self) -> None:
        self.assertEqual(list_references(), list_instructions())

    def test_backward_compat_get_reference(self) -> None:
        self.assertEqual(
            get_reference("league-web-brand-guide"),
            get_instruction("league-web-brand-guide"),
        )


class MCPProcessDiscoveryToolTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        server._project_root = self.root
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_tool_get_process_guide(self) -> None:
        result = server.tool_get_process_guide()
        self.assertIn("Curik Curriculum Development Process", result)
        self.assertNotIn("Error:", result)

    def test_tool_get_activity_guide(self) -> None:
        result = server.tool_get_activity_guide("spec-development")
        self.assertIn("Curriculum Architect", result)
        self.assertNotIn("Error:", result)

    def test_tool_get_activity_guide_unknown(self) -> None:
        result = server.tool_get_activity_guide("bogus")
        self.assertTrue(result.startswith("Error:"))

    def test_tool_list_instructions(self) -> None:
        result = json.loads(server.tool_list_instructions())
        self.assertIn("process-guide", result)

    def test_tool_get_instruction(self) -> None:
        result = server.tool_get_instruction("league-web-brand-guide")
        self.assertIn("League", result)
        self.assertNotIn("Error:", result)

    def test_tool_list_references_backward_compat(self) -> None:
        result = json.loads(server.tool_list_references())
        self.assertIn("process-guide", result)

    def test_tool_get_reference_backward_compat(self) -> None:
        result = server.tool_get_reference("league-web-brand-guide")
        self.assertIn("League", result)


if __name__ == "__main__":
    unittest.main()
