"""Tests for curik.init_command — CLAUDE.md, skill, and MCP permission installation."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from curik.init_command import (
    _SECTION_END,
    _SECTION_START,
    _update_claude_md,
    _update_settings_json,
    _update_vscode_mcp_json,
    _write_curik_skill,
    run_init,
)


class UpdateClaudeMdTest(unittest.TestCase):
    """Tests for _update_claude_md()."""

    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.target = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_creates_claude_md_from_scratch(self) -> None:
        status = _update_claude_md(self.target)
        self.assertEqual(status, "created")
        content = (self.target / "CLAUDE.md").read_text()
        self.assertIn(_SECTION_START, content)
        self.assertIn(_SECTION_END, content)
        self.assertIn("Hugo", content)

    def test_appends_to_existing_without_markers(self) -> None:
        claude_md = self.target / "CLAUDE.md"
        claude_md.write_text("# My Project\n\nExisting content.\n")
        status = _update_claude_md(self.target)
        self.assertEqual(status, "updated")
        content = claude_md.read_text()
        self.assertIn("# My Project", content)
        self.assertIn(_SECTION_START, content)
        self.assertIn("Existing content.", content)

    def test_replaces_in_place_with_existing_markers(self) -> None:
        claude_md = self.target / "CLAUDE.md"
        claude_md.write_text(
            "# Header\n\n"
            f"{_SECTION_START}\nold content\n{_SECTION_END}\n\n"
            "# Footer\n"
        )
        status = _update_claude_md(self.target)
        self.assertEqual(status, "updated")
        content = claude_md.read_text()
        self.assertIn("# Header", content)
        self.assertIn("# Footer", content)
        self.assertNotIn("old content", content)
        self.assertIn("Hugo", content)

    def test_unchanged_when_content_matches(self) -> None:
        _update_claude_md(self.target)
        status = _update_claude_md(self.target)
        self.assertEqual(status, "unchanged")

    def test_coexists_with_clasi_markers(self) -> None:
        claude_md = self.target / "CLAUDE.md"
        clasi_section = (
            "<!-- CLASI:START -->\n"
            "## CLASI SE Process\nCLASI content here.\n"
            "<!-- CLASI:END -->\n"
        )
        claude_md.write_text(clasi_section)
        status = _update_claude_md(self.target)
        self.assertEqual(status, "updated")
        content = claude_md.read_text()
        self.assertIn("<!-- CLASI:START -->", content)
        self.assertIn("<!-- CLASI:END -->", content)
        self.assertIn(_SECTION_START, content)
        self.assertIn(_SECTION_END, content)
        self.assertIn("CLASI content here.", content)


class WriteCurikSkillTest(unittest.TestCase):
    """Tests for _write_curik_skill()."""

    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.target = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_creates_skill_file(self) -> None:
        status = _write_curik_skill(self.target)
        self.assertEqual(status, "created")
        skill_path = self.target / ".claude" / "skills" / "curik" / "SKILL.md"
        self.assertTrue(skill_path.exists())
        content = skill_path.read_text()
        self.assertIn("/curik", content)

    def test_unchanged_on_rerun(self) -> None:
        _write_curik_skill(self.target)
        status = _write_curik_skill(self.target)
        self.assertEqual(status, "unchanged")

    def test_updated_when_content_differs(self) -> None:
        _write_curik_skill(self.target)
        skill_path = self.target / ".claude" / "skills" / "curik" / "SKILL.md"
        skill_path.write_text("old content")
        status = _write_curik_skill(self.target)
        self.assertEqual(status, "updated")


class UpdateVscodeMcpJsonTest(unittest.TestCase):
    """Tests for _update_vscode_mcp_json()."""

    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.target = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_creates_vscode_mcp_json(self) -> None:
        status = _update_vscode_mcp_json(self.target)
        self.assertIn(status, ("created", "updated"))
        mcp_json = self.target / ".vscode" / "mcp.json"
        data = json.loads(mcp_json.read_text())
        self.assertIn("curik", data["servers"])
        self.assertEqual(data["servers"]["curik"]["type"], "stdio")

    def test_merges_with_existing_servers(self) -> None:
        vscode_dir = self.target / ".vscode"
        vscode_dir.mkdir()
        existing = {"servers": {"other": {"type": "stdio", "command": "other"}}}
        (vscode_dir / "mcp.json").write_text(json.dumps(existing))
        status = _update_vscode_mcp_json(self.target)
        self.assertEqual(status, "updated")
        data = json.loads((vscode_dir / "mcp.json").read_text())
        self.assertIn("other", data["servers"])
        self.assertIn("curik", data["servers"])

    def test_unchanged_when_already_configured(self) -> None:
        _update_vscode_mcp_json(self.target)
        status = _update_vscode_mcp_json(self.target)
        self.assertEqual(status, "unchanged")


class UpdateSettingsJsonTest(unittest.TestCase):
    """Tests for _update_settings_json()."""

    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.target = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_creates_settings_with_permission(self) -> None:
        status = _update_settings_json(self.target)
        self.assertIn(status, ("created", "updated"))
        settings_path = self.target / ".claude" / "settings.local.json"
        data = json.loads(settings_path.read_text())
        self.assertIn("mcp__curik__*", data["permissions"]["allow"])

    def test_merges_with_existing_permissions(self) -> None:
        claude_dir = self.target / ".claude"
        claude_dir.mkdir()
        existing = {"permissions": {"allow": ["mcp__clasi__*"]}}
        (claude_dir / "settings.local.json").write_text(json.dumps(existing))
        status = _update_settings_json(self.target)
        self.assertEqual(status, "updated")
        data = json.loads((claude_dir / "settings.local.json").read_text())
        self.assertIn("mcp__clasi__*", data["permissions"]["allow"])
        self.assertIn("mcp__curik__*", data["permissions"]["allow"])

    def test_unchanged_when_permission_exists(self) -> None:
        _update_settings_json(self.target)
        status = _update_settings_json(self.target)
        self.assertEqual(status, "unchanged")


class RunInitTest(unittest.TestCase):
    """Tests for run_init() orchestrator."""

    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.target = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_creates_all_files(self) -> None:
        result = run_init(self.target)
        self.assertIn("CLAUDE.md", result["created"])
        self.assertIn(".claude/skills/curik/SKILL.md", result["created"])
        self.assertIn(".vscode/mcp.json", result["created"])
        self.assertIn(".claude/settings.local.json", result["created"])

    def test_idempotent_rerun(self) -> None:
        run_init(self.target)
        result = run_init(self.target)
        self.assertEqual(len(result["created"]), 0)
        self.assertEqual(len(result["unchanged"]), 6)


class InitCourseIntegrationTest(unittest.TestCase):
    """Test that init_course() produces init_command files."""

    def setUp(self) -> None:
        self._tmpdir = TemporaryDirectory()
        self.root = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_init_course_creates_claude_md(self) -> None:
        from curik.project import init_course

        result = init_course(self.root)
        self.assertIn("CLAUDE.md", result["created"])
        claude_md = self.root / "CLAUDE.md"
        self.assertTrue(claude_md.exists())
        self.assertIn(_SECTION_START, claude_md.read_text())

    def test_init_course_creates_skill(self) -> None:
        from curik.project import init_course

        result = init_course(self.root)
        self.assertIn(".claude/skills/curik/SKILL.md", result["created"])
        skill = self.root / ".claude" / "skills" / "curik" / "SKILL.md"
        self.assertTrue(skill.exists())

    def test_init_course_creates_vscode_mcp(self) -> None:
        from curik.project import init_course

        result = init_course(self.root)
        self.assertIn(".vscode/mcp.json", result["created"])

    def test_init_course_creates_settings(self) -> None:
        from curik.project import init_course

        result = init_course(self.root)
        self.assertIn(".claude/settings.local.json", result["created"])

    def test_init_course_idempotent(self) -> None:
        from curik.project import init_course

        init_course(self.root)
        result = init_course(self.root)
        self.assertIn("CLAUDE.md", result["existing"])


if __name__ == "__main__":
    unittest.main()
