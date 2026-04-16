"""Tests for content authoring validation."""

from __future__ import annotations

import unittest

from curik.validation import validate_instructor_guide


COMPLETE_GUIDE = """\
# Lesson: Loops

Some intro text.

{{< instructor-guide >}}

## Instructor Guide

**Objectives**: Students will write a for-loop that prints each item in a list.

**Materials**:
- Projector with starter notebook
- Printed reference cards (1 per student)

**Timing**:
| Segment | Minutes | Activity |
|---------|---------|----------|
| Warm-up | 5 | Review question |
| Teach | 15 | Live demo |
| Activity | 25 | Loop challenges |
| Wrap-up | 5 | Exit ticket |

**Key Concepts**: A for-loop repeats a block of code once for each item in a sequence.

**Common Mistakes**: Students expect range(5) to include 5. Show list(range(5)).

**Assessment Cues**: Students who get it can modify the loop variable and range independently.

**Differentiation**:
- *Needs more support*: Provide syntax reference card.
- *Ready for more*: Nested loop challenge.

{{< /instructor-guide >}}
"""

MISSING_FIELDS_GUIDE = """\
{{< instructor-guide >}}

## Instructor Guide

**Objectives**: Write a function.

**Materials**: Computers.

**Timing**: 50 minutes total.

{{< /instructor-guide >}}
"""

EMPTY_FIELD_GUIDE = """\
{{< instructor-guide >}}

## Instructor Guide

**Objectives**:

**Materials**: Computers and notebooks.

**Timing**: 50 minutes.

**Key Concepts**: Functions encapsulate reusable logic.

**Common Mistakes**: Forgetting return statements.

**Assessment Cues**: Students can write a function with parameters.

**Differentiation**: Pair struggling students.

{{< /instructor-guide >}}
"""


class ValidateInstructorGuideTest(unittest.TestCase):
    """Test validate_instructor_guide function."""

    def test_complete_guide_is_valid(self) -> None:
        result = validate_instructor_guide(COMPLETE_GUIDE)
        self.assertTrue(result["valid"])
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["empty"], [])

    def test_missing_fields_detected(self) -> None:
        result = validate_instructor_guide(MISSING_FIELDS_GUIDE)
        self.assertFalse(result["valid"])
        self.assertIn("Key Concepts", result["missing"])
        self.assertIn("Common Mistakes", result["missing"])
        self.assertIn("Assessment Cues", result["missing"])
        self.assertIn("Differentiation", result["missing"])
        self.assertEqual(len(result["missing"]), 4)

    def test_empty_field_detected(self) -> None:
        result = validate_instructor_guide(EMPTY_FIELD_GUIDE)
        self.assertFalse(result["valid"])
        self.assertIn("Objectives", result["empty"])
        self.assertEqual(result["missing"], [])

    def test_no_instructor_guide_div(self) -> None:
        content = "# Just a regular lesson\n\nNo guide here.\n"
        result = validate_instructor_guide(content)
        self.assertFalse(result["valid"])
        self.assertEqual(result["missing"], [
            "Objectives", "Materials", "Timing", "Key Concepts",
            "Common Mistakes", "Assessment Cues", "Differentiation",
        ])
        self.assertEqual(result["empty"], [])


if __name__ == "__main__":
    unittest.main()
