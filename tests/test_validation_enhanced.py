"""Tests for tier-aware validation enhancements and new skill definitions."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from curik.assets import get_skill_definition, list_skills
from curik.project import init_course
from curik.validation import validate_course, validate_lesson


# ---------------------------------------------------------------------------
# Lesson content fixtures
# ---------------------------------------------------------------------------

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

COMPLETE_LESSON_WITH_GUARD = """\
---
uid: test-uid-001
---
<!-- readme-shared -->
# Lesson: Variables

## Learning Objectives

- Define a variable in Python
- Assign values to variables
<!-- /readme-shared -->

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

COMPLETE_LESSON_WITH_GUARD_BAD_UID = """\
---
uid: nonexistent-uid-999
---
<!-- readme-shared -->
# Lesson: Variables

## Learning Objectives

- Define a variable in Python

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


class ValidateLessonTierTest(unittest.TestCase):
    """Tests for tier-aware validate_lesson enhancements."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_tier3_missing_guard_is_error(self) -> None:
        """Tier 3 lesson without <!-- readme-shared --> guard produces error."""
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON, encoding="utf-8")
        result = validate_lesson(self.root, "modules/mod1/01-variables.md", tier=3)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("readme-shared" in e for e in result["errors"]),
            f"Expected readme-shared error, got: {result['errors']}",
        )

    def test_tier3_with_guard_no_guard_error(self) -> None:
        """Tier 3 lesson with <!-- readme-shared --> guard has no guard error."""
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON_WITH_GUARD, encoding="utf-8")
        result = validate_lesson(self.root, "modules/mod1/01-variables.md", tier=3)
        guard_errors = [e for e in result["errors"] if "readme-shared" in e]
        self.assertEqual(guard_errors, [], f"Unexpected guard errors: {guard_errors}")

    def test_tier4_missing_guard_is_error(self) -> None:
        """Tier 4 also checks for guards."""
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON, encoding="utf-8")
        result = validate_lesson(self.root, "modules/mod1/01-variables.md", tier=4)
        self.assertTrue(any("readme-shared" in e for e in result["errors"]))

    def test_tier2_guards_not_checked(self) -> None:
        """Tier 2 does not check for guards (backward compatible)."""
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON, encoding="utf-8")
        result = validate_lesson(self.root, "modules/mod1/01-variables.md", tier=2)
        guard_errors = [e for e in result["errors"] if "readme-shared" in e]
        self.assertEqual(guard_errors, [])

    def test_tier_none_guards_not_checked(self) -> None:
        """tier=None does not check for guards."""
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON, encoding="utf-8")
        result = validate_lesson(self.root, "modules/mod1/01-variables.md", tier=None)
        guard_errors = [e for e in result["errors"] if "readme-shared" in e]
        self.assertEqual(guard_errors, [])

    def test_tier3_uid_not_in_syllabus_is_error(self) -> None:
        """Tier 3 lesson with UID not found in syllabus produces error."""
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON_WITH_GUARD_BAD_UID, encoding="utf-8")

        # Mock read_syllabus_entries to return entries without the bad UID
        mock_entries = [{"uid": "test-uid-001", "name": "Test", "lesson": "", "exercise": ""}]
        with patch("curik.syllabus.read_syllabus_entries", return_value=mock_entries):
            # Create a dummy syllabus.yaml so the check triggers
            (self.root / "syllabus.yaml").write_text("title: Test\nmodules: []\n", encoding="utf-8")
            result = validate_lesson(self.root, "modules/mod1/01-variables.md", tier=3)

        self.assertTrue(
            any("UID not found in syllabus" in e for e in result["errors"]),
            f"Expected syllabus UID error, got: {result['errors']}",
        )

    def test_tier3_uid_in_syllabus_no_error(self) -> None:
        """Tier 3 lesson with UID found in syllabus has no UID error."""
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON_WITH_GUARD, encoding="utf-8")

        mock_entries = [{"uid": "test-uid-001", "name": "Test", "lesson": "", "exercise": ""}]
        with patch("curik.syllabus.read_syllabus_entries", return_value=mock_entries):
            (self.root / "syllabus.yaml").write_text("title: Test\nmodules: []\n", encoding="utf-8")
            result = validate_lesson(self.root, "modules/mod1/01-variables.md", tier=3)

        uid_errors = [e for e in result["errors"] if "UID" in e]
        self.assertEqual(uid_errors, [])


class ValidateCourseTierTest(unittest.TestCase):
    """Tests for tier-aware validate_course enhancements."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)
        # Write a course.yml with no TBD values
        (self.root / "course.yml").write_text(
            "title: Intro to Python\n"
            "slug: intro-python\n"
            "tier: 3\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_tier3_missing_readme_in_mirror_dir(self) -> None:
        """Tier 3 course flags missing README in lessons/<mod>/ mirror."""
        # Create modules dir and lessons mirror dir without README
        mod = self.root / "modules" / "mod1"
        mod.mkdir(parents=True)
        (mod / "README.md").write_text("# Mod\n", encoding="utf-8")
        mirror = self.root / "lessons" / "mod1"
        mirror.mkdir(parents=True)
        # No README.md in mirror
        result = validate_course(self.root, tier=3)
        self.assertTrue(
            any("Missing README.md in lessons/mod1/" in e for e in result["errors"]),
            f"Expected missing README error, got: {result['errors']}",
        )

    def test_tier3_readme_present_no_error(self) -> None:
        """Tier 3 course with README in mirror dir has no mirror error."""
        mod = self.root / "modules" / "mod1"
        mod.mkdir(parents=True)
        (mod / "README.md").write_text("# Mod\n", encoding="utf-8")
        mirror = self.root / "lessons" / "mod1"
        mirror.mkdir(parents=True)
        (mirror / "README.md").write_text("# Mod README\n", encoding="utf-8")
        result = validate_course(self.root, tier=3)
        mirror_errors = [e for e in result["errors"] if "Missing README" in e]
        self.assertEqual(mirror_errors, [])

    def test_tier3_syllabus_consistency_errors(self) -> None:
        """Tier 3 course reports syllabus consistency mismatches."""
        (self.root / "syllabus.yaml").write_text("title: Test\nmodules: []\n", encoding="utf-8")
        mock_consistency = {
            "entries_without_pages": ["orphan-uid"],
            "pages_without_entries": ["stray-uid"],
            "pages_without_uid": [],
            "syllabus_entry_count": 1,
            "page_count": 1,
        }
        with patch("curik.syllabus.validate_syllabus_consistency", return_value=mock_consistency):
            result = validate_course(self.root, tier=3)

        self.assertTrue(
            any("orphan-uid" in e for e in result["errors"]),
            f"Expected orphan-uid error, got: {result['errors']}",
        )
        self.assertTrue(
            any("stray-uid" in e for e in result["errors"]),
            f"Expected stray-uid error, got: {result['errors']}",
        )

    def test_tier_none_no_tier_checks(self) -> None:
        """tier=None does not run tier-specific checks."""
        # Create a mirror dir without README — should not be flagged
        mod = self.root / "modules" / "mod1"
        mod.mkdir(parents=True)
        (mod / "README.md").write_text("# Mod\n", encoding="utf-8")
        mirror = self.root / "lessons" / "mod1"
        mirror.mkdir(parents=True)
        result = validate_course(self.root, tier=None)
        mirror_errors = [e for e in result["errors"] if "Missing README" in e]
        self.assertEqual(mirror_errors, [])


class BackwardCompatibilityTest(unittest.TestCase):
    """Existing calls without tier parameter still work unchanged."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_validate_lesson_without_tier(self) -> None:
        lesson = self.root / "modules" / "mod1" / "01-variables.md"
        lesson.parent.mkdir(parents=True)
        lesson.write_text(COMPLETE_LESSON, encoding="utf-8")
        result = validate_lesson(self.root, "modules/mod1/01-variables.md")
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_validate_course_without_tier(self) -> None:
        (self.root / "course.yml").write_text(
            "title: Intro to Python\nslug: intro-python\n",
            encoding="utf-8",
        )
        result = validate_course(self.root)
        self.assertTrue(result["valid"])


class SkillLoadingTest(unittest.TestCase):
    """Verify all three new skill files load via the assets system."""

    def test_repo_scaffolding_skill_loads(self) -> None:
        skills = list_skills()
        self.assertIn("repo-scaffolding", skills)
        content = get_skill_definition("repo-scaffolding")
        self.assertIn("Repo Scaffolding", content)

    def test_status_tracking_skill_loads(self) -> None:
        skills = list_skills()
        self.assertIn("status-tracking", skills)
        content = get_skill_definition("status-tracking")
        self.assertIn("Status Tracking", content)

    def test_syllabus_integration_skill_loads(self) -> None:
        skills = list_skills()
        self.assertIn("syllabus-integration", skills)
        content = get_skill_definition("syllabus-integration")
        self.assertIn("Syllabus Integration", content)


if __name__ == "__main__":
    unittest.main()
