"""Tests for curik.changes — change cycle and issue management."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from curik.project import CurikError, init_course
from curik.changes import (
    approve_change_plan,
    close_change_plan,
    create_change_plan,
    create_issue,
    execute_change_plan,
    list_issues,
    review_change_plan,
)


class TestCreateIssueAndListIssues(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_create_issue_returns_number_and_path(self) -> None:
        result = create_issue(self.root, "Fix typo in lesson 1", "The word 'teh' should be 'the'.")
        self.assertEqual(result["number"], 1)
        self.assertIn("001-fix-typo-in-lesson-1.md", result["path"])
        self.assertTrue(Path(result["path"]).exists())

    def test_create_issue_increments_number(self) -> None:
        r1 = create_issue(self.root, "First issue", "Content 1")
        r2 = create_issue(self.root, "Second issue", "Content 2")
        self.assertEqual(r1["number"], 1)
        self.assertEqual(r2["number"], 2)

    def test_create_issue_writes_frontmatter(self) -> None:
        result = create_issue(self.root, "Test issue", "Body text here.")
        text = Path(result["path"]).read_text(encoding="utf-8")
        self.assertIn("title: Test issue", text)
        self.assertIn("status: open", text)
        self.assertIn("created:", text)
        self.assertIn("Body text here.", text)

    def test_list_issues_open(self) -> None:
        create_issue(self.root, "Issue A", "Content A")
        create_issue(self.root, "Issue B", "Content B")
        issues = list_issues(self.root, "open")
        self.assertEqual(len(issues), 2)
        titles = {i["title"] for i in issues}
        self.assertEqual(titles, {"Issue A", "Issue B"})

    def test_list_issues_empty(self) -> None:
        issues = list_issues(self.root, "open")
        self.assertEqual(issues, [])

    def test_list_issues_done(self) -> None:
        issues = list_issues(self.root, "done")
        self.assertEqual(issues, [])


class TestChangePlanLifecycle(unittest.TestCase):
    """Full lifecycle: create -> approve -> execute -> review -> close."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)
        # Create some issues to reference
        self.issue1 = create_issue(self.root, "Issue one", "Content one")
        self.issue2 = create_issue(self.root, "Issue two", "Content two")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_full_lifecycle(self) -> None:
        # Create
        plan = create_change_plan(
            self.root, "Improve lesson flow",
            [self.issue1["number"], self.issue2["number"]],
        )
        self.assertEqual(plan["number"], 1)
        self.assertTrue(Path(plan["path"]).exists())

        # Approve
        result = approve_change_plan(self.root, plan["number"])
        self.assertEqual(result["status"], "approved")

        # Execute
        result = execute_change_plan(self.root, plan["number"])
        self.assertEqual(result["status"], "executed")

        # Review (no gaps)
        result = review_change_plan(self.root, plan["number"], [])
        self.assertEqual(result["new_issues"], [])

        # Close
        result = close_change_plan(self.root, plan["number"])
        self.assertEqual(result["status"], "closed")

        # Verify plan moved to done
        done_plans = list(
            (self.root / ".course" / "change-plan" / "done").glob("*.md")
        )
        self.assertEqual(len(done_plans), 1)
        active_plans = list(
            (self.root / ".course" / "change-plan" / "active").glob("*.md")
        )
        self.assertEqual(len(active_plans), 0)

        # Verify issues moved to done
        open_issues = list_issues(self.root, "open")
        done_issues = list_issues(self.root, "done")
        self.assertEqual(len(open_issues), 0)
        self.assertEqual(len(done_issues), 2)

    def test_review_with_gaps_creates_new_issues(self) -> None:
        plan = create_change_plan(self.root, "Plan with gaps", [self.issue1["number"]])
        approve_change_plan(self.root, plan["number"])
        execute_change_plan(self.root, plan["number"])

        result = review_change_plan(
            self.root, plan["number"],
            ["Missing assessment rubric", "Needs peer review section"],
        )
        self.assertEqual(len(result["new_issues"]), 2)

        # Check that new issues exist
        open_issues = list_issues(self.root, "open")
        # Original 2 issues + 2 gap issues = 4
        self.assertEqual(len(open_issues), 4)
        titles = {i["title"] for i in open_issues}
        self.assertIn("Missing assessment rubric", titles)
        self.assertIn("Needs peer review section", titles)


class TestStatusTransitionRejections(unittest.TestCase):
    """Test that wrong status transitions raise CurikError."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)
        self.issue = create_issue(self.root, "Test issue", "Content")
        self.plan = create_change_plan(self.root, "Test plan", [self.issue["number"]])

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_cannot_execute_draft_plan(self) -> None:
        with self.assertRaises(CurikError):
            execute_change_plan(self.root, self.plan["number"])

    def test_cannot_review_draft_plan(self) -> None:
        with self.assertRaises(CurikError):
            review_change_plan(self.root, self.plan["number"], [])

    def test_cannot_close_draft_plan(self) -> None:
        with self.assertRaises(CurikError):
            close_change_plan(self.root, self.plan["number"])

    def test_cannot_approve_approved_plan(self) -> None:
        approve_change_plan(self.root, self.plan["number"])
        with self.assertRaises(CurikError):
            approve_change_plan(self.root, self.plan["number"])

    def test_cannot_execute_executed_plan(self) -> None:
        approve_change_plan(self.root, self.plan["number"])
        execute_change_plan(self.root, self.plan["number"])
        with self.assertRaises(CurikError):
            execute_change_plan(self.root, self.plan["number"])

    def test_cannot_close_executed_plan(self) -> None:
        """Must be reviewed before closing."""
        approve_change_plan(self.root, self.plan["number"])
        execute_change_plan(self.root, self.plan["number"])
        with self.assertRaises(CurikError):
            close_change_plan(self.root, self.plan["number"])

    def test_cannot_approve_after_execute(self) -> None:
        approve_change_plan(self.root, self.plan["number"])
        execute_change_plan(self.root, self.plan["number"])
        with self.assertRaises(CurikError):
            approve_change_plan(self.root, self.plan["number"])


class TestClosePlanMovesFiles(unittest.TestCase):
    """Verify close_change_plan moves files correctly."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_close_moves_plan_and_issues(self) -> None:
        i1 = create_issue(self.root, "Issue alpha", "Alpha content")
        i2 = create_issue(self.root, "Issue beta", "Beta content")
        i3 = create_issue(self.root, "Issue gamma", "Gamma content")  # not referenced

        plan = create_change_plan(self.root, "Close test", [i1["number"], i2["number"]])
        approve_change_plan(self.root, plan["number"])
        execute_change_plan(self.root, plan["number"])
        review_change_plan(self.root, plan["number"], [])
        result = close_change_plan(self.root, plan["number"])

        # Plan is in done/
        self.assertTrue(Path(result["path"]).exists())
        self.assertIn("change-plan/done", result["path"])

        # Referenced issues moved to done
        self.assertIn(i1["number"], result["moved_issues"])
        self.assertIn(i2["number"], result["moved_issues"])

        # Unreferenced issue stays open
        open_issues = list_issues(self.root, "open")
        self.assertEqual(len(open_issues), 1)
        self.assertEqual(open_issues[0]["title"], "Issue gamma")

        # Referenced issues in done
        done_issues = list_issues(self.root, "done")
        self.assertEqual(len(done_issues), 2)

    def test_close_plan_not_found_raises(self) -> None:
        with self.assertRaises(CurikError):
            close_change_plan(self.root, 999)

    def test_plan_file_removed_from_active(self) -> None:
        issue = create_issue(self.root, "Temp issue", "Temp")
        plan = create_change_plan(self.root, "Temp plan", [issue["number"]])
        original_path = plan["path"]

        approve_change_plan(self.root, plan["number"])
        execute_change_plan(self.root, plan["number"])
        review_change_plan(self.root, plan["number"], [])
        close_change_plan(self.root, plan["number"])

        # Original active file should be gone
        self.assertFalse(Path(original_path).exists())


if __name__ == "__main__":
    unittest.main()
