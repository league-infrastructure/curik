from __future__ import annotations

import re
import unittest
import uuid

from curik.uid import generate_course_uid, generate_unit_uid


class GenerateCourseUidTest(unittest.TestCase):
    def test_returns_valid_uuid4(self) -> None:
        uid = generate_course_uid()
        parsed = uuid.UUID(uid)
        self.assertEqual(parsed.version, 4)

    def test_returns_string(self) -> None:
        uid = generate_course_uid()
        self.assertIsInstance(uid, str)


class GenerateUnitUidTest(unittest.TestCase):
    def test_length_is_8(self) -> None:
        uid = generate_unit_uid()
        self.assertEqual(len(uid), 8)

    def test_all_base62_chars(self) -> None:
        uid = generate_unit_uid()
        self.assertRegex(uid, r"^[a-zA-Z0-9]{8}$")

    def test_uniqueness_10000(self) -> None:
        uids = {generate_unit_uid() for _ in range(10_000)}
        self.assertEqual(len(uids), 10_000)


if __name__ == "__main__":
    unittest.main()
