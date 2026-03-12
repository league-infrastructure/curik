"""Tests for Phase 1 sub-phase tracking."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from curik.project import (
    CurikError,
    advance_sub_phase,
    get_phase,
    init_course,
)


class SubPhaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_init_sets_sub_phase_1a(self) -> None:
        init_course(self.root)
        state = json.loads((self.root / ".course" / "state.json").read_text())
        self.assertEqual(state["sub_phase"], "1a")

    def test_get_phase_returns_sub_phase(self) -> None:
        init_course(self.root)
        info = get_phase(self.root)
        self.assertEqual(info["sub_phase"], "1a")

    def test_advance_through_all_sub_phases(self) -> None:
        init_course(self.root)
        expected = [("1a", "1b"), ("1b", "1c"), ("1c", "1d"), ("1d", "1e")]
        for old, new in expected:
            result = advance_sub_phase(self.root)
            self.assertEqual(result["old"], old)
            self.assertEqual(result["new"], new)

    def test_cannot_advance_past_1e(self) -> None:
        init_course(self.root)
        for _ in range(4):  # 1a→1b→1c→1d→1e
            advance_sub_phase(self.root)
        with self.assertRaises(CurikError):
            advance_sub_phase(self.root)

    def test_resource_collection_skips_1b_and_1d(self) -> None:
        init_course(self.root, course_type="resource-collection")
        # 1a → 1c (skips 1b)
        result = advance_sub_phase(self.root)
        self.assertEqual(result["old"], "1a")
        self.assertEqual(result["new"], "1c")
        # 1c → 1e (skips 1d)
        result = advance_sub_phase(self.root)
        self.assertEqual(result["old"], "1c")
        self.assertEqual(result["new"], "1e")

    def test_sub_phase_not_returned_in_phase2(self) -> None:
        init_course(self.root)
        # Write state directly to phase2
        state_path = self.root / ".course" / "state.json"
        state = json.loads(state_path.read_text())
        state["phase"] = "phase2"
        state_path.write_text(json.dumps(state, indent=2) + "\n")
        info = get_phase(self.root)
        self.assertNotIn("sub_phase", info)

    def test_cannot_advance_sub_phase_in_phase2(self) -> None:
        init_course(self.root)
        state_path = self.root / ".course" / "state.json"
        state = json.loads(state_path.read_text())
        state["phase"] = "phase2"
        state_path.write_text(json.dumps(state, indent=2) + "\n")
        with self.assertRaises(CurikError):
            advance_sub_phase(self.root)

    def test_get_phase_persists_after_advance(self) -> None:
        init_course(self.root)
        advance_sub_phase(self.root)
        info = get_phase(self.root)
        self.assertEqual(info["sub_phase"], "1b")


if __name__ == "__main__":
    unittest.main()
