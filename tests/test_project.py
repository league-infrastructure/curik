from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from curik.project import (
    COURSE_YML_REQUIRED_FIELDS,
    CurikError,
    SPEC_SECTION_HEADINGS,
    _is_tbd,
    advance_phase,
    get_course_status,
    get_phase,
    init_course,
    update_course_yml,
    update_spec,
)


class CurikProjectTest(unittest.TestCase):
    def test_init_creates_expected_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = init_course(root)
            self.assertIn(".course/spec.md", result["created"])
            self.assertTrue((root / ".course" / "change-plan" / "active").is_dir())
            self.assertTrue((root / "course.yml").is_file())
            self.assertFalse((root / ".mcp.json").is_file())

    def test_advance_phase_blocked_by_tbd_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            with self.assertRaises(CurikError):
                advance_phase(root, "phase2")

    def test_advance_phase_after_required_sections_filled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            for section in SPEC_SECTION_HEADINGS:
                update_spec(root, section, f"{section} content")
            advance_phase(root, "phase2")
            self.assertEqual(get_phase(root)["phase"], "phase2")

    def test_update_spec_rejects_empty_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            with self.assertRaises(CurikError):
                update_spec(root, "course-concept", "   ")

    def test_get_course_status_returns_phase_and_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            result = get_course_status(root)
            self.assertEqual(result["phase"], "phase1")
            self.assertEqual(result["open_issues"], 0)
            self.assertEqual(result["active_change_plans"], 0)

    def test_get_course_status_counts_issues(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            # Manually create an open issue to verify counting
            issue_dir = root / ".course" / "issues" / "open"
            (issue_dir / "001-test-issue.md").write_text("# Test issue\n")
            result = get_course_status(root)
            self.assertEqual(result["open_issues"], 1)

    def test_get_course_status_error_no_init(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(CurikError):
                get_course_status(root)


class IsTbdTest(unittest.TestCase):
    def test_none_is_tbd(self) -> None:
        self.assertTrue(_is_tbd(None))

    def test_empty_string_is_tbd(self) -> None:
        self.assertTrue(_is_tbd(""))

    def test_whitespace_string_is_tbd(self) -> None:
        self.assertTrue(_is_tbd("   "))

    def test_tbd_string_is_tbd(self) -> None:
        self.assertTrue(_is_tbd("TBD"))

    def test_zero_string_is_tbd(self) -> None:
        self.assertTrue(_is_tbd("0"))

    def test_zero_int_is_tbd(self) -> None:
        self.assertTrue(_is_tbd(0))

    def test_zero_float_is_tbd(self) -> None:
        self.assertTrue(_is_tbd(0.0))

    def test_empty_list_is_tbd(self) -> None:
        self.assertTrue(_is_tbd([]))

    def test_nonempty_string_not_tbd(self) -> None:
        self.assertFalse(_is_tbd("Python Basics"))

    def test_nonzero_int_not_tbd(self) -> None:
        self.assertFalse(_is_tbd(3))

    def test_nonempty_list_not_tbd(self) -> None:
        self.assertFalse(_is_tbd(["item"]))

    def test_false_bool_is_tbd(self) -> None:
        # bool is a subclass of int in Python; False == 0, so _is_tbd(False) is True
        self.assertTrue(_is_tbd(False))


class UpdateCourseYmlTest(unittest.TestCase):
    def test_update_course_yml_merges_fields(self) -> None:
        """update_course_yml writes new values and returns updated_fields."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            result = update_course_yml(root, {"title": "My Course", "tier": 3})
            self.assertIn("title", result["updated_fields"])
            self.assertIn("tier", result["updated_fields"])
            # Verify the file was actually updated
            import yaml
            data = yaml.safe_load((root / "course.yml").read_text(encoding="utf-8"))
            self.assertEqual(data["title"], "My Course")
            self.assertEqual(data["tier"], 3)

    def test_update_course_yml_returns_content(self) -> None:
        """Result dict has content key with the written text."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            result = update_course_yml(root, {"description": "A test course"})
            self.assertIn("content", result)
            self.assertIn("description: A test course", result["content"])

    def test_update_course_yml_reports_tbd(self) -> None:
        """still_tbd lists required fields that remain placeholder values."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            # Only set one field — others should still be TBD
            result = update_course_yml(root, {"title": "My Course"})
            self.assertIn("still_tbd", result)
            tbd = result["still_tbd"]
            # tier, grades, category, description, repo_url are still TBD
            self.assertIn("tier", tbd)
            self.assertIn("description", tbd)
            self.assertNotIn("title", tbd)

    def test_update_course_yml_all_set_no_still_tbd(self) -> None:
        """When all required fields are filled, still_tbd is absent."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_course(root)
            updates = {
                "title": "My Course",
                "tier": 3,
                "grades": "6-8",
                "category": "text-programming",
                "description": "Intro to Python",
                "repo_url": "https://github.com/league-curriculum/my-course",
            }
            result = update_course_yml(root, updates)
            self.assertNotIn("still_tbd", result)
            self.assertEqual(result["message"], "All required fields are set.")

    def test_update_course_yml_missing_course_yml_raises(self) -> None:
        """Raises CurikError when course.yml does not exist."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(CurikError):
                update_course_yml(root, {"title": "X"})

    def test_course_yml_required_fields_is_list(self) -> None:
        """COURSE_YML_REQUIRED_FIELDS should be a non-empty list of strings."""
        self.assertIsInstance(COURSE_YML_REQUIRED_FIELDS, list)
        self.assertGreater(len(COURSE_YML_REQUIRED_FIELDS), 0)
        for f in COURSE_YML_REQUIRED_FIELDS:
            self.assertIsInstance(f, str)


if __name__ == "__main__":
    unittest.main()
