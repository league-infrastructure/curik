"""Tests for CLAUDE.md template rewrite."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from curik.project import init_course


class ClaudeMdTemplateTest(unittest.TestCase):
    """The CLAUDE.md template matches the CLI-based process-routing design."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_claude_md_contains_preflight(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertIn("curik status", claude_md)
        self.assertIn("curik phase get", claude_md)

    def test_claude_md_contains_rules(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertIn("CLI-first", claude_md)
        self.assertIn("Agent boundaries", claude_md)
        self.assertIn("Gates are gates", claude_md)

    def test_claude_md_lists_command_categories(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertIn("Status and Phase", claude_md)
        self.assertIn("Scaffolding", claude_md)
        self.assertIn("Validation", claude_md)

    def test_claude_md_no_mcp_tool_references(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertNotIn("get_activity_guide(activity)", claude_md)
        self.assertNotIn("MCP-first", claude_md)
        self.assertNotIn("Available MCP Tools", claude_md)

    def test_claude_md_has_cli_commands(self) -> None:
        claude_md = (self.root / "CLAUDE.md").read_text()
        self.assertIn("curik config update", claude_md)
        self.assertIn("curik publish check", claude_md)


if __name__ == "__main__":
    unittest.main()
