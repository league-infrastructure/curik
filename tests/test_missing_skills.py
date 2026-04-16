"""Tests for CLAUDE.md template rewrite."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from curik.project import init_course


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
        self.assertNotIn("Agent and Skill Loading", claude_md)
        self.assertIn("State Management", claude_md)

    def test_claude_md_includes_activity_guide(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertIn("get_activity_guide(activity)", claude_md)


if __name__ == "__main__":
    unittest.main()
