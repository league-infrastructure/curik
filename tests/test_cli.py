"""Tests for curik CLI."""

from __future__ import annotations

import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from curik.cli import main


class CliInitTest(unittest.TestCase):
    def test_init_prints_friendly_message(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["init", "--path", tmp])
            output = mock_stdout.getvalue()
            self.assertEqual(result, 0)
            self.assertIn("Curik is ready", output)
            self.assertIn("Start Curik", output)
            # Should NOT be raw JSON
            self.assertNotIn('"created"', output)

    def test_init_creates_course_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch("sys.stdout", new_callable=StringIO):
                main(["init", "--path", tmp])
            self.assertTrue((Path(tmp) / ".course").is_dir())


if __name__ == "__main__":
    unittest.main()
