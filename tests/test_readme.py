"""Tests for curik.readme module."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from curik.readme import generate_readme, generate_readmes, parse_guards
from curik import server


class ParseGuardsSharedTest(unittest.TestCase):
    def test_extracts_shared_content(self) -> None:
        content = (
            "# Title\n"
            "{{< readme-shared >}}\n"
            "Shared paragraph.\n"
            "{{< /readme-shared >}}\n"
            "Rest of page.\n"
        )
        guards = parse_guards(content)
        self.assertEqual(len(guards["shared"]), 1)
        self.assertEqual(guards["shared"][0], "Shared paragraph.")
        self.assertEqual(guards["only"], [])

    def test_extracts_multiple_shared_blocks(self) -> None:
        content = (
            "{{< readme-shared >}}\n"
            "Block 1\n"
            "{{< /readme-shared >}}\n"
            "gap\n"
            "{{< readme-shared >}}\n"
            "Block 2\n"
            "{{< /readme-shared >}}\n"
        )
        guards = parse_guards(content)
        self.assertEqual(len(guards["shared"]), 2)
        self.assertEqual(guards["shared"][0], "Block 1")
        self.assertEqual(guards["shared"][1], "Block 2")


class ParseGuardsOnlyTest(unittest.TestCase):
    def test_extracts_only_content(self) -> None:
        content = (
            "{{< readme-only >}}\n"
            "Only in README.\n"
            "{{< /readme-only >}}\n"
        )
        guards = parse_guards(content)
        self.assertEqual(len(guards["only"]), 1)
        self.assertEqual(guards["only"][0], "Only in README.")
        self.assertEqual(guards["shared"], [])


class ParseGuardsBothTest(unittest.TestCase):
    def test_extracts_both_types(self) -> None:
        content = (
            "{{< readme-shared >}}\n"
            "# Intro\n"
            "{{< /readme-shared >}}\n"
            "Site only content\n"
            "{{< readme-only >}}\n"
            "## Setup\n"
            "Run the code.\n"
            "{{< /readme-only >}}\n"
        )
        guards = parse_guards(content)
        self.assertEqual(len(guards["shared"]), 1)
        self.assertEqual(len(guards["only"]), 1)
        self.assertEqual(guards["shared"][0], "# Intro")
        self.assertIn("Run the code.", guards["only"][0])


class ParseGuardsEmptyTest(unittest.TestCase):
    def test_no_guards_returns_empty(self) -> None:
        content = "# Just a regular page\n\nNo guards here.\n"
        guards = parse_guards(content)
        self.assertEqual(guards["shared"], [])
        self.assertEqual(guards["only"], [])

    def test_empty_guard_content(self) -> None:
        content = (
            "{{< readme-shared >}}\n"
            "{{< /readme-shared >}}\n"
        )
        guards = parse_guards(content)
        self.assertEqual(len(guards["shared"]), 1)
        self.assertEqual(guards["shared"][0], "")


class GenerateReadmeTest(unittest.TestCase):
    def test_produces_correct_output(self) -> None:
        content = (
            "{{< readme-shared >}}\n"
            "# Title\n"
            "{{< /readme-shared >}}\n"
            "page stuff\n"
            "{{< readme-only >}}\n"
            "## Setup\n"
            "{{< /readme-only >}}\n"
        )
        result = generate_readme(content)
        self.assertIsNotNone(result)
        self.assertIn("# Title", result)
        self.assertIn("## Setup", result)
        self.assertTrue(result.endswith("\n"))

    def test_returns_none_for_no_guards(self) -> None:
        content = "# Regular page\n\nNo guards.\n"
        result = generate_readme(content)
        self.assertIsNone(result)

    def test_shared_only_concatenation_order(self) -> None:
        content = (
            "{{< readme-shared >}}\n"
            "First\n"
            "{{< /readme-shared >}}\n"
            "{{< readme-only >}}\n"
            "Second\n"
            "{{< /readme-only >}}\n"
        )
        result = generate_readme(content)
        self.assertIsNotNone(result)
        first_pos = result.index("First")
        second_pos = result.index("Second")
        self.assertLess(first_pos, second_pos)


class GenerateReadmesTest(unittest.TestCase):
    def test_writes_files_to_correct_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "content" / "01-intro"
            docs.mkdir(parents=True)
            (docs / "01-hello.md").write_text(
                "{{< readme-shared >}}\n"
                "# Hello\n"
                "{{< /readme-shared >}}\n",
                encoding="utf-8",
            )
            result = generate_readmes(root)
            self.assertEqual(len(result["generated"]), 1)
            readme_path = root / "lessons" / "01-intro" / "01-hello" / "README.md"
            self.assertTrue(readme_path.exists())
            content = readme_path.read_text(encoding="utf-8")
            self.assertIn("# Hello", content)

    def test_skips_files_without_guards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "content"
            docs.mkdir(parents=True)
            (docs / "index.md").write_text("# Index\n", encoding="utf-8")
            result = generate_readmes(root)
            self.assertEqual(len(result["generated"]), 0)
            self.assertEqual(len(result["skipped"]), 1)

    def test_multiple_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "content" / "mod1"
            docs.mkdir(parents=True)
            (docs / "a.md").write_text(
                "{{< readme-shared >}}\nA\n{{< /readme-shared >}}\n",
                encoding="utf-8",
            )
            (docs / "b.md").write_text("# No guards\n", encoding="utf-8")
            result = generate_readmes(root)
            self.assertEqual(len(result["generated"]), 1)
            self.assertEqual(len(result["skipped"]), 1)


class MCPReadmeToolTest(unittest.TestCase):
    """Test MCP tool wrapper returns JSON."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        server._project_root = self.root

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_tool_trigger_readme_generation_returns_json(self) -> None:
        docs = self.root / "content"
        docs.mkdir(parents=True)
        (docs / "test.md").write_text(
            "{{< readme-shared >}}\n# Test\n{{< /readme-shared >}}\n",
            encoding="utf-8",
        )
        result = server.tool_trigger_readme_generation()
        parsed = json.loads(result)
        self.assertIn("generated", parsed)

    def test_tool_trigger_readme_generation_error(self) -> None:
        result = server.tool_trigger_readme_generation()
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    unittest.main()
