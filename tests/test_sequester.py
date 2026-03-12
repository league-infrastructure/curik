"""Tests for sequester_content() — moving existing repo files to _old/."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from curik.migrate import sequester_content
from curik.project import CURIK_DIR, init_course


class SequesterContentTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_empty_repo_moves_nothing(self) -> None:
        result = sequester_content(self.root)
        self.assertEqual(result["moved"], [])
        self.assertIn(CURIK_DIR, result["protected"])

    def test_moves_files_to_old(self) -> None:
        (self.root / "README.md").write_text("hello", encoding="utf-8")
        (self.root / "docs").mkdir()
        (self.root / "docs" / "index.md").write_text("hi", encoding="utf-8")

        result = sequester_content(self.root)
        self.assertIn("README.md", result["moved"])
        self.assertIn("docs", result["moved"])
        self.assertTrue((self.root / "_old" / "README.md").is_file())
        self.assertTrue((self.root / "_old" / "docs" / "index.md").is_file())
        self.assertFalse((self.root / "README.md").exists())
        self.assertFalse((self.root / "docs").exists())

    def test_protected_paths_not_moved(self) -> None:
        (self.root / "README.md").write_text("hello", encoding="utf-8")
        result = sequester_content(self.root)

        # These should still exist
        self.assertTrue((self.root / CURIK_DIR).is_dir())
        self.assertTrue((self.root / ".mcp.json").is_file())
        self.assertTrue((self.root / "course.yml").is_file())

        # Protected list should include them
        self.assertIn(CURIK_DIR, result["protected"])
        self.assertIn(".mcp.json", result["protected"])
        self.assertIn("course.yml", result["protected"])

    def test_idempotent_second_call(self) -> None:
        (self.root / "README.md").write_text("hello", encoding="utf-8")
        sequester_content(self.root)
        result = sequester_content(self.root)
        # Second call should move nothing (only _old/ is left, which is protected)
        self.assertEqual(result["moved"], [])

    def test_git_directory_protected(self) -> None:
        (self.root / ".git").mkdir()
        (self.root / ".git" / "config").write_text("x", encoding="utf-8")
        (self.root / "README.md").write_text("hello", encoding="utf-8")

        result = sequester_content(self.root)
        self.assertTrue((self.root / ".git").is_dir())
        self.assertIn(".git", result["protected"])
        self.assertIn("README.md", result["moved"])


if __name__ == "__main__":
    unittest.main()
