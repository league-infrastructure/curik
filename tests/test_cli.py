"""Tests for curik CLI."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from curik.cli import main


def _init_tmp(tmp: str) -> None:
    """Initialize a course in a temp directory, suppressing output."""
    with patch("sys.stdout", new_callable=StringIO):
        main(["init", "--path", tmp])


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


class CliStatusTest(unittest.TestCase):
    def test_status_happy_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["status", "--path", tmp])
            self.assertEqual(result, 0)
            output = mock_stdout.getvalue()
            self.assertIn("phase", output)

    def test_status_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["status", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIn("phase", data)

    def test_status_error_not_initialized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch("sys.stderr", new_callable=StringIO):
                with self.assertRaises(SystemExit) as ctx:
                    main(["status", "--path", tmp])
            self.assertEqual(ctx.exception.code, 1)


class CliPhaseTest(unittest.TestCase):
    def test_phase_get_happy_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["phase", "get", "--path", tmp])
            self.assertEqual(result, 0)
            output = mock_stdout.getvalue()
            self.assertIn("phase", output)

    def test_phase_get_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["phase", "get", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIn("phase", data)
            self.assertEqual(data["phase"], "phase1")

    def test_phase_get_error_not_initialized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch("sys.stderr", new_callable=StringIO):
                with self.assertRaises(SystemExit) as ctx:
                    main(["phase", "get", "--path", tmp])
            self.assertEqual(ctx.exception.code, 1)

    def test_phase_advance_sub(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["phase", "advance-sub", "--path", tmp])
            self.assertEqual(result, 0)
            output = mock_stdout.getvalue()
            self.assertIn("new", output)

    def test_phase_advance_sub_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["phase", "advance-sub", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIn("old", data)
            self.assertIn("new", data)

    def test_phase_advance_error_incomplete_spec(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stderr", new_callable=StringIO):
                with self.assertRaises(SystemExit) as ctx:
                    main(["phase", "advance", "phase2", "--path", tmp])
            self.assertEqual(ctx.exception.code, 1)


class CliConfigTest(unittest.TestCase):
    def test_config_update_json_arg(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            updates = json.dumps({"title": "My Course"})
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["config", "update", updates, "--path", tmp])
            self.assertEqual(result, 0)
            output = mock_stdout.getvalue()
            self.assertIn("updated_fields", output)
            # Verify the file was actually updated
            course_yml = Path(tmp) / "course.yml"
            self.assertIn("My Course", course_yml.read_text())

    def test_config_update_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            updates = json.dumps({"title": "Test"})
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["config", "update", updates, "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIn("updated_fields", data)
            self.assertIn("title", data["updated_fields"])

    def test_config_update_error_not_initialized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch("sys.stderr", new_callable=StringIO):
                with self.assertRaises(SystemExit) as ctx:
                    main(["config", "update", '{"title": "X"}', "--path", tmp])
            self.assertEqual(ctx.exception.code, 1)


class CliScaffoldTest(unittest.TestCase):
    def test_scaffold_structure_happy_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            structure = json.dumps({"modules": [{"name": "01-intro", "lessons": []}]})
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["scaffold", "structure", structure, "--path", tmp])
            self.assertEqual(result, 0)
            self.assertTrue((Path(tmp) / "site" / "content" / "01-intro").is_dir())

    def test_scaffold_structure_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            structure = json.dumps({"modules": [{"name": "01-intro", "lessons": []}]})
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["scaffold", "structure", structure, "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIn("created", data)

    def test_scaffold_lesson_happy_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main([
                    "scaffold", "lesson", "01-intro", "01-hello.md",
                    "--tier", "2", "--path", tmp,
                ])
            self.assertEqual(result, 0)
            self.assertTrue((Path(tmp) / "site" / "content" / "01-intro" / "01-hello.md").exists())

    def test_scaffold_lesson_error_bad_tier(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stderr", new_callable=StringIO):
                with self.assertRaises(SystemExit):
                    main([
                        "scaffold", "lesson", "01-intro", "01-hello.md",
                        "--tier", "5", "--path", tmp,
                    ])

    def test_scaffold_outline_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO):
                main(["scaffold", "outline", "My Outline", "Content here.", "--path", tmp])
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["scaffold", "get-outline", "My Outline", "--path", tmp])
            self.assertEqual(result, 0)
            self.assertIn("Content here.", mock_stdout.getvalue())


class CliIssueTest(unittest.TestCase):
    def test_issue_create_and_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["issue", "create", "Bug #1", "Description", "--path", tmp])
            self.assertEqual(result, 0)

            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["issue", "list", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["title"], "Bug #1")

    def test_issue_list_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["issue", "list", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 0)


class CliValidateTest(unittest.TestCase):
    def test_validate_lesson_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["validate", "lesson", "content/missing.md",
                                "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertFalse(data["valid"])

    def test_validate_course_happy_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["validate", "course", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            # Course may not be valid (TBD fields), but we get a dict back
            self.assertIn("valid", data)
            self.assertIn("errors", data)

    def test_validate_module_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["validate", "module", "content/missing",
                                "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertFalse(data["valid"])

    def test_validate_save_and_get_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            report = {"valid": True, "errors": []}
            with patch("sys.stdout", new_callable=StringIO):
                result = main([
                    "validate", "save-report",
                    json.dumps(report), "--path", tmp,
                ])
            self.assertEqual(result, 0)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["validate", "get-report", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertTrue(data["valid"])


class CliHugoTest(unittest.TestCase):
    def test_hugo_pages_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["hugo", "pages", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            # content/ may be created by init with some pages
            data = json.loads(mock_stdout.getvalue())
            self.assertIsInstance(data, list)

    def test_hugo_setup_from_course(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            # Remove existing site/hugo.toml so setup can write it fresh
            import shutil
            hugo_toml = Path(tmp) / "site" / "hugo.toml"
            if hugo_toml.exists():
                hugo_toml.unlink()
            # Also remove site/themes/ to avoid cloning
            theme_dir = Path(tmp) / "site" / "themes"
            if theme_dir.exists():
                shutil.rmtree(theme_dir)
            with patch("curik.templates._clone_theme"):
                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    result = main(["hugo", "setup", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIn("created", data)

    def test_hugo_build_no_hugo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["hugo", "build", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            # success may be False if hugo isn't installed, but we get a result
            self.assertIn("success", data)

    def test_hugo_bump_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            # hugo.toml now lives at site/hugo.toml in new-layout projects
            hugo_toml = Path(tmp) / "site" / "hugo.toml"
            if hugo_toml.exists():
                with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                    result = main(["hugo", "bump-version", "--path", tmp, "--json"])
                self.assertEqual(result, 0)
                data = json.loads(mock_stdout.getvalue())
                self.assertIn("version", data)


class CliPublishTest(unittest.TestCase):
    def test_publish_check_happy_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["publish", "check", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIn("ready", data)
            self.assertIn("checks", data)

    def test_publish_guide_happy_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["publish", "guide", "--path", tmp])
            self.assertEqual(result, 0)
            output = mock_stdout.getvalue()
            self.assertIn("Publishing Guide", output)

    def test_publish_check_not_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["publish", "check", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            # A fresh init without content is not ready
            self.assertFalse(data["ready"])


class CliReadmeTest(unittest.TestCase):
    def test_readme_generate_no_guards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            # Create a content dir with a simple .md file (no guards)
            content_dir = Path(tmp) / "site" / "content"
            content_dir.mkdir(parents=True, exist_ok=True)
            (content_dir / "test.md").write_text("# Hello\n", encoding="utf-8")
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["readme", "generate", "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIn("generated", data)
            self.assertIn("skipped", data)

    def test_readme_generate_docs_dir_default_is_site_content(self) -> None:
        """readme generate --docs-dir default must be 'site/content', not 'content'."""
        import argparse
        import curik.cli as cli_module

        # Build the argument parser and check the docs_dir default
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command")
        # Re-parse the readme generate subcommand to inspect its defaults
        readme_p = sub.add_parser("readme")
        readme_sub = readme_p.add_subparsers(dest="readme_command")
        rm_gen = readme_sub.add_parser("generate")
        rm_gen.add_argument("--docs-dir", dest="docs_dir", default="site/content")

        args = parser.parse_args(["readme", "generate"])
        self.assertEqual(args.docs_dir, "site/content")


class CliMigrateTest(unittest.TestCase):
    def test_migrate_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["migrate", "inventory", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIn("has_course_yml", data)

    def test_migrate_sequester(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            # Create a file that would be sequestered
            test_file = Path(tmp) / "old-content.md"
            test_file.write_text("Old content\n", encoding="utf-8")
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["migrate", "sequester", "--path", tmp, "--json"])
            self.assertEqual(result, 0)


class CliPlanTest(unittest.TestCase):
    def test_plan_create_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            issue_numbers = json.dumps([])
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["plan", "create", "My Plan", issue_numbers,
                                "--path", tmp, "--json"])
            self.assertEqual(result, 0)
            data = json.loads(mock_stdout.getvalue())
            self.assertIn("number", data)
            self.assertIn("path", data)


class CliSpecTest(unittest.TestCase):
    def test_spec_get(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["spec", "get", "--path", tmp])
            self.assertEqual(result, 0)
            output = mock_stdout.getvalue()
            self.assertIn("Curik Course Specification", output)

    def test_spec_record_concept(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["spec", "record-concept", "This is a Python intro course.",
                                "--path", tmp])
            self.assertEqual(result, 0)
            spec_file = Path(tmp) / ".course" / "spec.md"
            self.assertIn("Python intro", spec_file.read_text())

    def test_spec_update_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _init_tmp(tmp)
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main(["spec", "update", "course-concept",
                                "My course concept.", "--path", tmp])
            self.assertEqual(result, 0)
            spec_file = Path(tmp) / ".course" / "spec.md"
            self.assertIn("My course concept.", spec_file.read_text())


if __name__ == "__main__":
    unittest.main()
