"""Tests for asset loading and research tools."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from curik.assets import get_agent_definition, get_skill_definition, list_agents, list_skills
from curik.project import CurikError, init_course
from curik.research import get_research_findings, save_research_findings
from curik import server


class AssetLoadingTest(unittest.TestCase):
    def test_list_agents(self) -> None:
        agents = list_agents()
        self.assertIn("curriculum-architect", agents)
        self.assertIn("research-agent", agents)

    def test_list_skills(self) -> None:
        skills = list_skills()
        self.assertIn("course-concept", skills)
        self.assertIn("pedagogical-model", skills)
        self.assertIn("alignment-decision", skills)
        self.assertIn("spec-synthesis", skills)
        self.assertIn("structure-proposal", skills)

    def test_get_agent_definition(self) -> None:
        content = get_agent_definition("curriculum-architect")
        self.assertIn("Curriculum Architect", content)
        self.assertIn("Phase 1a", content)

    def test_get_skill_definition(self) -> None:
        content = get_skill_definition("course-concept")
        self.assertIn("Course Concept", content)
        self.assertIn("Target students", content)

    def test_get_agent_not_found(self) -> None:
        with self.assertRaises(CurikError):
            get_agent_definition("nonexistent-agent")

    def test_get_skill_not_found(self) -> None:
        with self.assertRaises(CurikError):
            get_skill_definition("nonexistent-skill")


class ResearchTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_save_research_findings(self) -> None:
        result = save_research_findings(self.root, "PCEP Syllabus", "Details about PCEP...")
        self.assertIn("path", result)
        self.assertEqual(result["number"], 1)
        self.assertTrue(Path(result["path"]).exists())

    def test_save_multiple_findings(self) -> None:
        save_research_findings(self.root, "Finding 1", "Content 1")
        result = save_research_findings(self.root, "Finding 2", "Content 2")
        self.assertEqual(result["number"], 2)

    def test_get_research_findings_empty(self) -> None:
        findings = get_research_findings(self.root)
        self.assertEqual(findings, [])

    def test_get_research_findings_roundtrip(self) -> None:
        save_research_findings(self.root, "Test Finding", "Some content")
        findings = get_research_findings(self.root)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["title"], "Test Finding")

    def test_save_empty_content_rejected(self) -> None:
        with self.assertRaises(CurikError):
            save_research_findings(self.root, "Title", "   ")

    def test_save_without_init_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(CurikError):
                save_research_findings(Path(tmp), "Title", "Content")


class MCPAssetResearchToolTest(unittest.TestCase):
    """Test MCP tool wrappers for assets and research."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        server._project_root = self.root
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_tool_list_agents(self) -> None:
        result = json.loads(server.tool_list_agents())
        self.assertIn("curriculum-architect", result)

    def test_tool_get_agent_definition(self) -> None:
        result = server.tool_get_agent_definition("curriculum-architect")
        self.assertIn("Curriculum Architect", result)

    def test_tool_get_agent_not_found(self) -> None:
        result = server.tool_get_agent_definition("nope")
        self.assertTrue(result.startswith("Error:"))

    def test_tool_list_skills(self) -> None:
        result = json.loads(server.tool_list_skills())
        self.assertIn("course-concept", result)

    def test_tool_get_skill_definition(self) -> None:
        result = server.tool_get_skill_definition("course-concept")
        self.assertIn("Course Concept", result)

    def test_tool_save_research_findings(self) -> None:
        result = json.loads(server.tool_save_research_findings("Test", "Content here"))
        self.assertIn("path", result)

    def test_tool_get_research_findings(self) -> None:
        server.tool_save_research_findings("Test", "Content here")
        result = json.loads(server.tool_get_research_findings())
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
