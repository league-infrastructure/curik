"""Tests for curik.syllabus module."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from curik.project import CurikError
from curik.syllabus import (
    get_syllabus,
    read_syllabus_entries,
    validate_syllabus_consistency,
    write_syllabus_url,
)
from curik import server


def _write_syllabus(root: Path, data: dict) -> None:
    """Helper to write a syllabus.yaml from a dict."""
    (root / "syllabus.yaml").write_text(
        yaml.dump(data, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )


def _sample_syllabus_data() -> dict:
    return {
        "name": "Test Course",
        "uid": "course-001",
        "modules": [
            {
                "name": "Module 1",
                "uid": "mod-001",
                "lessons": [
                    {
                        "name": "Lesson A",
                        "uid": "les-001",
                        "lesson": "lesson_a.py",
                        "exercise": "exercise_a.py",
                    },
                    {
                        "name": "Lesson B",
                        "uid": "les-002",
                        "lesson": "lesson_b.py",
                        "exercise": None,
                    },
                ],
            },
            {
                "name": "Module 2",
                "uid": "mod-002",
                "lessons": [
                    {
                        "name": "Lesson Set X",
                        "uid": "set-001",
                        "lessons": [
                            {
                                "name": "Sub Lesson",
                                "uid": "les-003",
                                "lesson": "sub_lesson.py",
                                "exercise": "sub_ex.py",
                            },
                        ],
                    },
                ],
            },
        ],
    }


class ReadSyllabusEntriesTest(unittest.TestCase):
    def test_reads_flat_and_nested_lessons(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_syllabus(root, _sample_syllabus_data())
            entries = read_syllabus_entries(root)
            uids = [e["uid"] for e in entries]
            self.assertIn("les-001", uids)
            self.assertIn("les-002", uids)
            self.assertIn("les-003", uids)
            self.assertEqual(len(entries), 3)

    def test_entries_have_expected_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_syllabus(root, _sample_syllabus_data())
            entries = read_syllabus_entries(root)
            first = entries[0]
            self.assertEqual(first["uid"], "les-001")
            self.assertEqual(first["name"], "Lesson A")
            self.assertEqual(first["lesson"], "lesson_a.py")
            self.assertEqual(first["exercise"], "exercise_a.py")

    def test_missing_file_raises_curik_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(CurikError):
                read_syllabus_entries(root)


class WriteSyllabusUrlTest(unittest.TestCase):
    def test_writes_url_for_uid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_syllabus(root, _sample_syllabus_data())
            result = write_syllabus_url(root, "les-001", "https://example.com/a")
            self.assertEqual(result["status"], "ok")

            # Verify the url was written
            data = yaml.safe_load((root / "syllabus.yaml").read_text())
            lesson = data["modules"][0]["lessons"][0]
            self.assertEqual(lesson["url"], "https://example.com/a")

    def test_writes_url_for_nested_lesson(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_syllabus(root, _sample_syllabus_data())
            result = write_syllabus_url(root, "les-003", "https://example.com/sub")
            self.assertEqual(result["status"], "ok")

            data = yaml.safe_load((root / "syllabus.yaml").read_text())
            sub = data["modules"][1]["lessons"][0]["lessons"][0]
            self.assertEqual(sub["url"], "https://example.com/sub")

    def test_unknown_uid_raises_curik_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_syllabus(root, _sample_syllabus_data())
            with self.assertRaises(CurikError):
                write_syllabus_url(root, "nonexistent", "https://example.com")


class GetSyllabusTest(unittest.TestCase):
    def test_returns_raw_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = "name: Test\nmodules: []\n"
            (root / "syllabus.yaml").write_text(content, encoding="utf-8")
            result = get_syllabus(root)
            self.assertEqual(result, content)

    def test_missing_file_raises_curik_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(CurikError):
                get_syllabus(root)


class ValidateSyllabusConsistencyTest(unittest.TestCase):
    def test_detects_entries_without_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_syllabus(root, _sample_syllabus_data())
            # No docs dir -> all entries have no pages
            result = validate_syllabus_consistency(root)
            self.assertIn("les-001", result["entries_without_pages"])
            self.assertIn("les-002", result["entries_without_pages"])

    def test_detects_pages_without_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_syllabus(root, _sample_syllabus_data())
            docs_dir = root / "content" / "mod1"
            docs_dir.mkdir(parents=True)
            (docs_dir / "extra.md").write_text(
                "---\nuid: extra-uid\n---\n# Extra\n", encoding="utf-8"
            )
            result = validate_syllabus_consistency(root)
            self.assertIn("extra-uid", result["pages_without_entries"])

    def test_matching_uids_no_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = {
                "name": "Test",
                "uid": "c1",
                "modules": [
                    {
                        "name": "M1",
                        "uid": "m1",
                        "lessons": [
                            {"name": "L1", "uid": "uid-a", "lesson": "a.py"},
                        ],
                    }
                ],
            }
            _write_syllabus(root, data)
            docs_dir = root / "content" / "m1"
            docs_dir.mkdir(parents=True)
            (docs_dir / "l1.md").write_text(
                "---\nuid: uid-a\n---\n# L1\n", encoding="utf-8"
            )
            result = validate_syllabus_consistency(root)
            self.assertEqual(result["entries_without_pages"], [])
            self.assertEqual(result["pages_without_entries"], [])


class MCPSyllabusToolTest(unittest.TestCase):
    """Test MCP tool wrappers return JSON."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        server._project_root = self.root

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_tool_read_syllabus_entries_returns_json(self) -> None:
        _write_syllabus(self.root, _sample_syllabus_data())
        result = server.tool_read_syllabus_entries()
        parsed = json.loads(result)
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), 3)

    def test_tool_read_syllabus_entries_error(self) -> None:
        result = server.tool_read_syllabus_entries()
        self.assertTrue(result.startswith("Error:"))

    def test_tool_get_syllabus_returns_content(self) -> None:
        content = "name: Test\nmodules: []\n"
        (self.root / "syllabus.yaml").write_text(content, encoding="utf-8")
        result = server.tool_get_syllabus()
        self.assertEqual(result, content)

    def test_tool_write_syllabus_url_returns_json(self) -> None:
        _write_syllabus(self.root, _sample_syllabus_data())
        result = server.tool_write_syllabus_url("les-001", "https://example.com")
        parsed = json.loads(result)
        self.assertEqual(parsed["status"], "ok")

    def test_tool_validate_syllabus_consistency_returns_json(self) -> None:
        _write_syllabus(self.root, _sample_syllabus_data())
        result = server.tool_validate_syllabus_consistency()
        parsed = json.loads(result)
        self.assertIn("entries_without_pages", parsed)


if __name__ == "__main__":
    unittest.main()
