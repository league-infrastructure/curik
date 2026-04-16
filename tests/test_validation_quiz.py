"""Tests for validation tools."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from curik.project import CurikError, init_course
from curik.validation import (
    get_validation_report,
    save_validation_report,
    validate_course,
    validate_lesson,
    validate_module,
)


COMPLETE_LESSON = """\
# Lesson: Variables

## Learning Objectives

- Define a variable in Python
- Assign values to variables

{{< instructor-guide >}}

**Objectives**: Teach variable declaration and assignment

**Materials**: Python interpreter, projector

**Timing**: 10 min intro, 20 min guided practice, 15 min independent work

**Key concepts**: Variables, assignment operator, naming conventions

**Common mistakes**: Using reserved words, forgetting quotes on strings

**Assessment cues**: Student can declare and print a variable

**Differentiation**: Advanced students explore type conversion

{{< /instructor-guide >}}

## Content

Variables store data...
"""

INCOMPLETE_LESSON_NO_GUIDE = """\
# Lesson: Variables

## Learning Objectives

- Define a variable in Python

## Content

Variables store data...
"""

INCOMPLETE_LESSON_MISSING_FIELDS = """\
# Lesson: Variables

## Learning Objectives

- Define a variable in Python

{{< instructor-guide >}}

**Objectives**: Teach variable declaration

**Materials**: Python interpreter

{{< /instructor-guide >}}

## Content

Variables store data...
"""

LESSON_NO_OBJECTIVES = """\
# Lesson: Variables

{{< instructor-guide >}}

**Objectives**: Teach variables
**Materials**: Python
**Timing**: 45 min
**Key concepts**: Variables
**Common mistakes**: None
**Assessment cues**: Can declare vars
**Differentiation**: N/A

{{< /instructor-guide >}}

## Content

Variables store data...
"""


class ValidateLessonTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_complete_lesson_is_valid(self) -> None:
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON, encoding="utf-8")
        result = validate_lesson(self.root, "modules/mod1/01-variables.md")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_missing_file_is_invalid(self) -> None:
        result = validate_lesson(self.root, "modules/mod1/nonexistent.md")
        self.assertFalse(result["valid"])
        self.assertTrue(any("not found" in e for e in result["errors"]))

    def test_no_instructor_guide_is_invalid(self) -> None:
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(INCOMPLETE_LESSON_NO_GUIDE, encoding="utf-8")
        result = validate_lesson(self.root, "modules/mod1/01-variables.md")
        self.assertFalse(result["valid"])
        self.assertTrue(any("instructor guide" in e.lower() for e in result["errors"]))

    def test_missing_guide_fields_is_invalid(self) -> None:
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(INCOMPLETE_LESSON_MISSING_FIELDS, encoding="utf-8")
        result = validate_lesson(self.root, "modules/mod1/01-variables.md")
        self.assertFalse(result["valid"])
        # Should mention missing fields like Timing, Key concepts, etc.
        missing_fields = [e for e in result["errors"] if "missing field" in e.lower()]
        self.assertGreater(len(missing_fields), 0)

    def test_no_objectives_outside_guide_is_invalid(self) -> None:
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(LESSON_NO_OBJECTIVES, encoding="utf-8")
        result = validate_lesson(self.root, "modules/mod1/01-variables.md")
        self.assertFalse(result["valid"])
        self.assertTrue(any("objectives" in e.lower() for e in result["errors"]))


class ValidateModuleTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_valid_module(self) -> None:
        mod = self.root / "modules" / "mod1"
        mod.mkdir(parents=True)
        (mod / "README.md").write_text("# Module 1\n", encoding="utf-8")
        (mod / "01-variables.md").write_text(COMPLETE_LESSON, encoding="utf-8")
        result = validate_module(self.root, "modules/mod1")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_missing_directory_is_invalid(self) -> None:
        result = validate_module(self.root, "modules/nonexistent")
        self.assertFalse(result["valid"])
        self.assertTrue(any("not found" in e for e in result["errors"]))

    def test_missing_readme_is_invalid(self) -> None:
        mod = self.root / "modules" / "mod1"
        mod.mkdir(parents=True)
        (mod / "01-variables.md").write_text(COMPLETE_LESSON, encoding="utf-8")
        result = validate_module(self.root, "modules/mod1")
        self.assertFalse(result["valid"])
        self.assertTrue(any("README" in e or "overview" in e for e in result["errors"]))

    def test_invalid_lesson_fails_module(self) -> None:
        mod = self.root / "modules" / "mod1"
        mod.mkdir(parents=True)
        (mod / "README.md").write_text("# Module 1\n", encoding="utf-8")
        (mod / "01-bad.md").write_text("# Bad lesson\nNo guide here.\n", encoding="utf-8")
        result = validate_module(self.root, "modules/mod1")
        self.assertFalse(result["valid"])
        self.assertIn("modules/mod1/01-bad.md", result["lesson_results"])


class ValidateCourseTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_course_with_tbd_is_invalid(self) -> None:
        result = validate_course(self.root)
        self.assertFalse(result["valid"])
        self.assertTrue(any("TBD" in e for e in result["errors"]))

    def test_course_no_tbd_no_modules_is_valid(self) -> None:
        # Write a course.yml with no TBD values
        (self.root / "course.yml").write_text(
            "title: Intro to Python\n"
            "slug: intro-python\n"
            "tier: 1\n"
            "grades: 6-8\n"
            "category: programming\n"
            "topics: [python, variables]\n"
            "prerequisites: []\n"
            "lessons: 5\n"
            "estimated_weeks: 10\n"
            "curriculum_url: https://example.com\n"
            "repo_url: https://github.com/example\n"
            "description: Learn Python basics\n",
            encoding="utf-8",
        )
        result = validate_course(self.root)
        self.assertTrue(result["valid"])

    def test_course_with_invalid_module(self) -> None:
        (self.root / "course.yml").write_text(
            "title: Intro to Python\nslug: intro-python\n",
            encoding="utf-8",
        )
        mod = self.root / "modules" / "mod1"
        mod.mkdir(parents=True)
        # No README, no valid lessons
        (mod / "01-bad.md").write_text("# Bad lesson\n", encoding="utf-8")
        result = validate_course(self.root)
        self.assertFalse(result["valid"])


class ValidationReportTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_save_and_get_report(self) -> None:
        report = {"valid": True, "errors": []}
        save_validation_report(self.root, report)
        loaded = get_validation_report(self.root)
        self.assertEqual(loaded, report)

    def test_get_report_when_none_exists(self) -> None:
        with self.assertRaises(CurikError):
            get_validation_report(self.root)


if __name__ == "__main__":
    unittest.main()
