"""Integration tests for the Curik MCP server tools.

Tests call the tool handler functions directly (bypassing MCP transport)
to verify that each tool delegates correctly to curik.project and returns
the expected responses.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from curik.project import SPEC_SECTION_HEADINGS, init_course, update_spec
from curik import server


class MCPToolTest(unittest.TestCase):
    """Test each MCP tool function with a real temp project."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        # Point the server at our temp dir
        server._project_root = self.root

    def tearDown(self) -> None:
        self._tmp.cleanup()

    # -- init_course --

    def test_init_course_creates_structure(self) -> None:
        result = json.loads(server.tool_init_course())
        self.assertIn(".curik/spec.md", result["created"])
        self.assertTrue((self.root / ".curik" / "state.json").is_file())
        self.assertTrue((self.root / "course.yml").is_file())

    def test_init_course_idempotent(self) -> None:
        server.tool_init_course()
        result = json.loads(server.tool_init_course())
        # Second call should report everything as existing
        self.assertTrue(len(result["existing"]) > 0)

    # -- get_phase --

    def test_get_phase_returns_phase1(self) -> None:
        init_course(self.root)
        result = json.loads(server.tool_get_phase())
        self.assertEqual(result["phase"], "phase1")
        self.assertEqual(len(result["requirements"]), len(SPEC_SECTION_HEADINGS))

    def test_get_phase_error_no_init(self) -> None:
        result = server.tool_get_phase()
        self.assertTrue(result.startswith("Error:"))

    # -- get_spec --

    def test_get_spec_returns_content(self) -> None:
        init_course(self.root)
        result = server.tool_get_spec()
        self.assertIn("# Curik Course Specification", result)

    def test_get_spec_error_no_init(self) -> None:
        result = server.tool_get_spec()
        self.assertTrue(result.startswith("Error:"))

    # -- update_spec --

    def test_update_spec_success(self) -> None:
        init_course(self.root)
        result = server.tool_update_spec("course-concept", "My course concept")
        self.assertIn("Updated section", result)
        spec = server.tool_get_spec()
        self.assertIn("My course concept", spec)

    def test_update_spec_bad_section(self) -> None:
        init_course(self.root)
        result = server.tool_update_spec("nonexistent", "content")
        self.assertTrue(result.startswith("Error:"))

    def test_update_spec_empty_content(self) -> None:
        init_course(self.root)
        result = server.tool_update_spec("course-concept", "   ")
        self.assertTrue(result.startswith("Error:"))

    # -- record convenience tools --

    def test_record_course_concept(self) -> None:
        init_course(self.root)
        result = server.tool_record_course_concept("Concept content")
        self.assertIn("Recorded", result)

    def test_record_pedagogical_model(self) -> None:
        init_course(self.root)
        result = server.tool_record_pedagogical_model("Model content")
        self.assertIn("Recorded", result)

    def test_record_alignment(self) -> None:
        init_course(self.root)
        result = server.tool_record_alignment("Alignment content")
        self.assertIn("Recorded", result)

    # -- advance_phase --

    def test_advance_phase_blocked_incomplete(self) -> None:
        init_course(self.root)
        result = server.tool_advance_phase("phase2")
        self.assertTrue(result.startswith("Error:"))

    def test_advance_phase_success(self) -> None:
        init_course(self.root)
        for section in SPEC_SECTION_HEADINGS:
            update_spec(self.root, section, f"{section} real content")
        result = server.tool_advance_phase("phase2")
        self.assertIn("Advanced to phase2", result)
        # Verify phase actually changed
        phase_result = json.loads(server.tool_get_phase())
        self.assertEqual(phase_result["phase"], "phase2")

    # -- get_course_status --

    def test_get_course_status(self) -> None:
        init_course(self.root)
        result = json.loads(server.tool_get_course_status())
        self.assertEqual(result["phase"], "phase1")
        self.assertEqual(result["open_issues"], 0)
        self.assertEqual(result["active_change_plans"], 0)

    def test_get_course_status_counts_issues(self) -> None:
        init_course(self.root)
        # Create a fake open issue
        issue_dir = self.root / ".curik" / "issues" / "open"
        (issue_dir / "001-test-issue.md").write_text("# Test issue\n")
        result = json.loads(server.tool_get_course_status())
        self.assertEqual(result["open_issues"], 1)

    def test_get_course_status_error_no_init(self) -> None:
        result = server.tool_get_course_status()
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    unittest.main()
