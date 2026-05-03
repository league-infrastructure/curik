---
id: '005'
title: Update tests (migrate MCP tests, add CLI coverage)
status: done
use-cases:
- SUC-001
- SUC-007
depends-on:
- '002'
- '003'
github-issue: ''
todo: ''
---

# Update tests (migrate MCP tests, add CLI coverage)

## Description

With the CLI built (ticket 002) and init system updated (ticket 003), the
test suite needs to be updated in two ways:

1. `tests/test_mcp_server.py` imports from `curik.server` and tests MCP tool
   handlers directly. When server.py is deleted (ticket 004), this file will
   break. The valuable test coverage it provides must migrate to other test
   files before that deletion.

2. `tests/test_cli.py` currently has only 2 tests covering `curik init`. It
   must be expanded to cover the new command groups from ticket 002.

This ticket runs in parallel with ticket 004 (same execution group). Ticket
004 deletes server.py; this ticket deletes test_mcp_server.py. Both depend on
tickets 002 and 003 being complete.

## Acceptance Criteria

- [x] `tests/test_mcp_server.py` is deleted
- [x] The domain-logic coverage from test_mcp_server.py is preserved in other test files
- [x] `tests/test_cli.py` has tests for at least 8 of the 14 command groups
- [x] At minimum one happy-path and one error-path test per covered group
- [x] `tests/test_init_command.py` has been updated to match ticket 003's changes (no MCP assertions, Bash permission assertion present)
- [x] `uv run pytest` passes with all tests green

## Implementation Plan

### Approach

**Step 1: Audit test_mcp_server.py** — identify which tests cover logic that
now lives in domain modules vs. logic that is trivially covered by the CLI
tests.

**Step 2: Migrate surviving coverage** — move test cases for `update_course_yml`,
`get_publish_guide`, and `check_publish_ready` to the appropriate test files.
Most of the MCP server test coverage tests domain behavior (init, phase, spec,
scaffolding, etc.) that is already covered in test_project.py, test_scaffolding.py,
test_changes.py, test_hugo.py, etc. Audit for gaps and add to those files.

**Step 3: Delete test_mcp_server.py** — once coverage is migrated.

**Step 4: Expand test_cli.py** — add TestCli classes per command group.

### Files to Delete

**tests/test_mcp_server.py**

After migrating its coverage, delete this file. It was testing MCP transport
wrappers; the underlying domain is tested elsewhere.

### Files to Modify

**tests/test_cli.py** — add test classes for command groups

Add at minimum:

```
TestCliPhase
  test_phase_get_returns_json
  test_phase_advance_succeeds
  test_phase_advance_sub_succeeds

TestCliSpec
  test_spec_get_returns_content
  test_spec_update_writes_section
  test_spec_record_concept

TestCliConfig
  test_config_update_merges_json
  test_config_update_reports_tbd_fields
  test_config_update_via_file_flag
  test_config_update_via_stdin

TestCliScaffold
  test_scaffold_structure_creates_dirs
  test_scaffold_lesson_creates_stub

TestCliValidate
  test_validate_course_returns_result
  test_validate_lesson_returns_result

TestCliHugo
  test_hugo_setup_reads_course_yml
  test_hugo_bump_version

TestCliPublish
  test_publish_check_returns_json
  test_publish_guide_returns_string

TestCliIssue
  test_issue_create_and_list

TestCliPlan
  test_plan_create

TestCliMigrate
  test_migrate_sequester

TestCliSyllabus
  test_syllabus_write_url
  test_syllabus_validate

TestCliReadme
  test_readme_generate
```

Pattern for each test:
```python
def test_phase_get_returns_json(self) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        main(["init", "--path", tmp])
        with patch("sys.stdout", new_callable=StringIO) as out:
            rc = main(["phase", "get", "--json", "--path", tmp])
        self.assertEqual(rc, 0)
        data = json.loads(out.getvalue())
        self.assertIn("phase", data)
```

**tests/test_publish.py** (new file, created in ticket 001's testing plan)

Verify this file exists and has the tests described there:
- `test_check_publish_ready_missing_course_yml`
- `test_check_publish_ready_with_tbd_fields`
- `test_get_publish_guide_returns_string`

If not created in ticket 001, create it here.

**tests/test_init_command.py** — update for ticket 003's changes

- Remove assertions about `.vscode/mcp.json` being created
- Remove assertions about `mcp__curik__*` in settings
- Add assertion: `Bash(curik *)` is in `data["permissions"]["allow"]`
- Add test: old `mcp__curik__*` entry is replaced on re-init

### Testing Plan

The testing plan IS this ticket. Run `uv run pytest` after each step to
maintain a green test suite throughout. Do not proceed to deleting
test_mcp_server.py until all its coverage is confirmed in other files.

### Documentation Updates

None.
