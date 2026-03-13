"""Tests for register_change_plan and full change cycle integration."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from curik.changes import (
    approve_change_plan,
    close_change_plan,
    create_change_plan,
    create_issue,
    execute_change_plan,
    list_issues,
    register_change_plan,
    review_change_plan,
)
from curik.project import CurikError, init_course
from curik import server


class RegisterChangePlanTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_register_created_plan(self) -> None:
        create_issue(self.root, "Fix typo", "Typo in lesson 1")
        create_change_plan(self.root, "Fix typos", [1])
        result = register_change_plan(self.root, 1)
        self.assertEqual(result["number"], 1)
        self.assertEqual(result["title"], "Fix typos")
        self.assertEqual(result["status"], "draft")

    def test_register_nonexistent_plan_raises(self) -> None:
        with self.assertRaises(CurikError):
            register_change_plan(self.root, 99)

    def test_register_agent_written_plan(self) -> None:
        # Simulate an agent writing a plan file directly
        active_dir = self.root / ".course" / "change-plan" / "active"
        plan_content = (
            "---\n"
            "title: Agent-written plan\n"
            "status: draft\n"
            "issues:\n"
            "  - 1\n"
            "---\n\n"
            "Plan details here.\n"
        )
        (active_dir / "001-agent-written-plan.md").write_text(plan_content)

        result = register_change_plan(self.root, 1)
        self.assertEqual(result["title"], "Agent-written plan")
        self.assertEqual(result["status"], "draft")

    def test_register_plan_missing_title_raises(self) -> None:
        active_dir = self.root / ".course" / "change-plan" / "active"
        plan_content = "---\nstatus: draft\n---\n\nNo title.\n"
        (active_dir / "001-bad-plan.md").write_text(plan_content)

        with self.assertRaises(CurikError) as ctx:
            register_change_plan(self.root, 1)
        self.assertIn("missing 'title'", str(ctx.exception))

    def test_register_plan_missing_status_raises(self) -> None:
        active_dir = self.root / ".course" / "change-plan" / "active"
        plan_content = "---\ntitle: No status\n---\n\nNo status.\n"
        (active_dir / "001-no-status.md").write_text(plan_content)

        with self.assertRaises(CurikError) as ctx:
            register_change_plan(self.root, 1)
        self.assertIn("missing 'status'", str(ctx.exception))


class FullChangeCycleTest(unittest.TestCase):
    """Integration test: create issue → plan → approve → execute → review → close."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_full_cycle(self) -> None:
        # 1. Create issues
        issue1 = create_issue(self.root, "Lesson 3 too long", "Split into two lessons")
        issue2 = create_issue(self.root, "Missing quiz", "Lesson 5 has no quiz")
        self.assertEqual(issue1["number"], 1)
        self.assertEqual(issue2["number"], 2)

        # Verify issues are open
        open_issues = list_issues(self.root, "open")
        self.assertEqual(len(open_issues), 2)

        # 2. Create change plan referencing both issues
        plan = create_change_plan(self.root, "Sprint fixes", [1, 2])
        plan_number = plan["number"]

        # 3. Register the plan (verify it's valid)
        reg = register_change_plan(self.root, plan_number)
        self.assertEqual(reg["status"], "draft")

        # 4. Approve
        approve = approve_change_plan(self.root, plan_number)
        self.assertEqual(approve["status"], "approved")

        # 5. Execute
        execute = execute_change_plan(self.root, plan_number)
        self.assertEqual(execute["status"], "executed")

        # 6. Review (no gaps)
        review = review_change_plan(self.root, plan_number, [])
        self.assertEqual(len(review["new_issues"]), 0)

        # 7. Close
        close = close_change_plan(self.root, plan_number)
        self.assertEqual(close["status"], "closed")
        self.assertEqual(sorted(close["moved_issues"]), [1, 2])

        # Verify issues are in done/
        done_issues = list_issues(self.root, "done")
        self.assertEqual(len(done_issues), 2)

        # Verify no open issues remain
        open_issues = list_issues(self.root, "open")
        self.assertEqual(len(open_issues), 0)

    def test_cycle_with_review_gaps(self) -> None:
        # Create an issue and plan
        create_issue(self.root, "Bug", "Details")
        create_change_plan(self.root, "Fix bug", [1])
        approve_change_plan(self.root, 1)
        execute_change_plan(self.root, 1)

        # Review finds gaps — new issues created
        review = review_change_plan(self.root, 1, ["Missing test", "Docs outdated"])
        self.assertEqual(len(review["new_issues"]), 2)

        # New issues should be open
        open_issues = list_issues(self.root, "open")
        # Issue 1 is still open (not yet closed), plus 2 new gap issues
        self.assertEqual(len(open_issues), 3)

        # Close the plan — moves issue 1 to done
        close = close_change_plan(self.root, 1)
        self.assertIn(1, close["moved_issues"])

        # Gap issues remain open
        open_issues = list_issues(self.root, "open")
        self.assertEqual(len(open_issues), 2)


class MCPRegisterChangePlanToolTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        server._project_root = self.root
        init_course(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_tool_register_change_plan(self) -> None:
        server.tool_create_issue("Bug", "Details")
        server.tool_create_change_plan("Fix", "[1]")
        result = json.loads(server.tool_register_change_plan(1))
        self.assertEqual(result["status"], "draft")

    def test_tool_register_nonexistent(self) -> None:
        result = server.tool_register_change_plan(99)
        self.assertTrue(result.startswith("Error:"))


if __name__ == "__main__":
    unittest.main()
