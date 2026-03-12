"""Tests for validation and quiz authoring tools."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from curik.assets import get_agent_definition, get_skill_definition, list_agents, list_skills
from curik.project import CurikError, init_course
from curik.validation import (
    get_validation_report,
    save_validation_report,
    validate_course,
    validate_lesson,
    validate_module,
)
from curik.quiz import (
    generate_quiz_stub,
    set_quiz_status,
    validate_quiz_alignment,
)
from curik import server


COMPLETE_LESSON = """\
# Lesson: Variables

## Learning Objectives

- Define a variable in Python
- Assign values to variables

<div class="instructor-guide">

**Objectives**: Teach variable declaration and assignment

**Materials**: Python interpreter, projector

**Timing**: 10 min intro, 20 min guided practice, 15 min independent work

**Key concepts**: Variables, assignment operator, naming conventions

**Common mistakes**: Using reserved words, forgetting quotes on strings

**Assessment cues**: Student can declare and print a variable

**Differentiation**: Advanced students explore type conversion

</div>

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

<div class="instructor-guide">

**Objectives**: Teach variable declaration

**Materials**: Python interpreter

</div>

## Content

Variables store data...
"""

LESSON_NO_OBJECTIVES = """\
# Lesson: Variables

<div class="instructor-guide">

**Objectives**: Teach variables
**Materials**: Python
**Timing**: 45 min
**Key concepts**: Variables
**Common mistakes**: None
**Assessment cues**: Can declare vars
**Differentiation**: N/A

</div>

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


class QuizStubTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_generate_quiz_stub(self) -> None:
        result = generate_quiz_stub(self.root, "01-variables", ["variables", "assignment"])
        self.assertIn("path", result)
        path = Path(result["path"])
        self.assertTrue(path.exists())
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertEqual(data["lesson_id"], "01-variables")
        self.assertEqual(data["status"], "drafted")
        self.assertEqual(data["difficulty"], "beginner")
        self.assertEqual(data["topics"], ["variables", "assignment"])
        self.assertIn("multiple-choice", data["question_types"])

    def test_quiz_stub_creates_directory(self) -> None:
        result = generate_quiz_stub(self.root, "02-loops", ["loops"])
        self.assertTrue(Path(result["path"]).parent.is_dir())


class QuizAlignmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_aligned_quiz(self) -> None:
        # Create lesson
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON, encoding="utf-8")
        # Create quiz covering all objectives
        result = generate_quiz_stub(
            self.root, "01-variables", ["define a variable", "assign values"]
        )
        quiz_rel = str(Path(result["path"]).relative_to(self.root))
        alignment = validate_quiz_alignment(
            self.root, "modules/mod1/01-variables.md", quiz_rel
        )
        self.assertTrue(alignment["aligned"])
        self.assertEqual(alignment["uncovered_objectives"], [])

    def test_unaligned_quiz(self) -> None:
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON, encoding="utf-8")
        # Create quiz covering only one objective
        result = generate_quiz_stub(
            self.root, "01-variables", ["define a variable"]
        )
        quiz_rel = str(Path(result["path"]).relative_to(self.root))
        alignment = validate_quiz_alignment(
            self.root, "modules/mod1/01-variables.md", quiz_rel
        )
        self.assertFalse(alignment["aligned"])
        self.assertGreater(len(alignment["uncovered_objectives"]), 0)

    def test_missing_lesson_raises(self) -> None:
        result = generate_quiz_stub(self.root, "01-x", ["topic"])
        quiz_rel = str(Path(result["path"]).relative_to(self.root))
        with self.assertRaises(CurikError):
            validate_quiz_alignment(self.root, "nonexistent.md", quiz_rel)

    def test_missing_quiz_raises(self) -> None:
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON, encoding="utf-8")
        with self.assertRaises(CurikError):
            validate_quiz_alignment(
                self.root, "modules/mod1/01-variables.md", "nonexistent.yml"
            )


class QuizStatusTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_set_status(self) -> None:
        import yaml
        result = generate_quiz_stub(self.root, "01-vars", ["variables"])
        quiz_rel = str(Path(result["path"]).relative_to(self.root))
        set_quiz_status(self.root, quiz_rel, "reviewed")
        data = yaml.safe_load(Path(result["path"]).read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "reviewed")

    def test_invalid_status_raises(self) -> None:
        result = generate_quiz_stub(self.root, "01-vars", ["variables"])
        quiz_rel = str(Path(result["path"]).relative_to(self.root))
        with self.assertRaises(CurikError):
            set_quiz_status(self.root, quiz_rel, "invalid-status")


class NewAssetsTest(unittest.TestCase):
    """Verify new agents and skills load via the assets system."""

    def test_quiz_author_agent_loads(self) -> None:
        agents = list_agents()
        self.assertIn("quiz-author", agents)
        content = get_agent_definition("quiz-author")
        self.assertIn("Quiz Author", content)

    def test_reviewer_agent_loads(self) -> None:
        agents = list_agents()
        self.assertIn("reviewer", agents)
        content = get_agent_definition("reviewer")
        self.assertIn("Reviewer", content)

    def test_validation_checklist_skill_loads(self) -> None:
        skills = list_skills()
        self.assertIn("validation-checklist", skills)
        content = get_skill_definition("validation-checklist")
        self.assertIn("Validation Checklist", content)

    def test_quiz_authoring_skill_loads(self) -> None:
        skills = list_skills()
        self.assertIn("quiz-authoring", skills)
        content = get_skill_definition("quiz-authoring")
        self.assertIn("Quiz Authoring", content)


if __name__ == "__main__":
    unittest.main()
