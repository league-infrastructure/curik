---
id: "002"
title: "Build new CLI (cli.py rewrite)"
status: done
use-cases: [SUC-001, SUC-003, SUC-004, SUC-007]
depends-on: ["001"]
github-issue: ""
todo: ""
---

# Build new CLI (cli.py rewrite)

## Description

Completely rewrite `curik/cli.py` from its current 98-line stub to a full
~900-line CLI that exposes all remaining MCP tool equivalents as argparse
subcommands, organized in 14 command groups.

Ticket 001 must be complete first because this CLI calls `update_course_yml`,
`hugo_setup_from_course`, `get_publish_guide`, and `check_publish_ready` from
the domain modules extracted there.

The command tree to implement (based on tools remaining in server.py after
sprint 001):

```
curik init [--type course|resource-collection] [--path]
curik status [--path] [--json]

curik phase get [--path] [--json]
curik phase advance TARGET [--path]
curik phase advance-sub [--path] [--json]

curik spec get [--path]
curik spec update SECTION [CONTENT] [-f FILE] [--path]
curik spec record-concept [CONTENT] [-f FILE] [--path]
curik spec record-model [CONTENT] [-f FILE] [--path]
curik spec record-alignment [CONTENT] [-f FILE] [--path]

curik config update [UPDATES_JSON] [-f FILE] [--path] [--json]

curik scaffold structure [STRUCTURE_JSON] [-f FILE] [--path] [--json]
curik scaffold lesson MODULE LESSON --tier TIER [--path]
curik scaffold outline NAME [CONTENT] [-f FILE] [--path]
curik scaffold approve-outline NAME [--path]
curik scaffold get-outline NAME [--path]
curik scaffold change-plan TITLE [ITEMS_JSON] [-f FILE] [--path]

curik issue create TITLE [CONTENT] [-f FILE] [--path] [--json]
curik issue list [--status open|done] [--path] [--json]

curik plan create TITLE [ISSUE_NUMBERS_JSON] [-f FILE] [--path] [--json]
curik plan register PLAN_NUMBER [--path] [--json]
curik plan approve PLAN_NUMBER [--path] [--json]
curik plan execute PLAN_NUMBER [--path] [--json]
curik plan review PLAN_NUMBER [--gaps-json GAPS] [--path] [--json]
curik plan close PLAN_NUMBER [--path] [--json]

curik migrate inventory REPO_PATH [--json]
curik migrate sequester [--path] [--json]
curik migrate structure --tier TIER [MODULES_JSON] [-f FILE] [--path] [--json]

curik validate lesson LESSON_PATH [--tier TIER] [--path] [--json]
curik validate module MODULE_PATH [--path] [--json]
curik validate course [--tier TIER] [--path] [--json]
curik validate get-report [--path] [--json]
curik validate save-report [REPORT_JSON] [-f FILE] [--path] [--json]

curik syllabus write-url UID URL [--path] [--json]
curik syllabus validate [--path] [--json]

curik hugo pages [--section SECTION] [--path] [--json]
curik hugo create-page PAGE_PATH TITLE [--content CONTENT] [--frontmatter-json FM] [--path]
curik hugo update-frontmatter PAGE_PATH [UPDATES_JSON] [-f FILE] [--path] [--json]
curik hugo setup [--title TITLE] [--tier TIER] [--path] [--json]
curik hugo bump-version [--path] [--json]
curik hugo build [--path] [--json]

curik readme generate [--docs-dir DIR] [--path] [--json]

curik publish guide [--path]
curik publish check [--path] [--json]
```

NOTE: `curik research` is NOT included — research module was removed in sprint 001.

## Acceptance Criteria

- [x] `curik --help` lists all 14 top-level command groups
- [x] Every subcommand listed above exists and dispatches to the correct domain function
- [x] `--path` on every subcommand resolves to an absolute Path before calling domain functions
- [x] `--json` flag causes JSON output on all subcommands that have it
- [x] `_json_input(args)` helper resolves JSON from positional arg → `--file`/`-f` → stdin, raises clear error if none provide valid JSON
- [x] `curik phase get` prints phase info; exit code 0 on success, 1 on error
- [x] `curik config update '{"title": "Foo"}'` updates course.yml and reports result
- [x] `curik validate course` calls `validate_course` and prints result
- [x] `curik hugo setup` calls `hugo_setup_from_course` when no title given
- [x] `curik publish check` returns JSON with per-check status
- [x] `curik publish guide` returns the full guide text
- [x] Old flat subcommands (`get-phase`, `get-spec`, `update-spec`, `advance-phase`, `mcp`) are removed
- [x] `uv run pytest` passes with no regressions

## Implementation Plan

### Approach

Rewrite cli.py top-to-bottom. Structure the file in sections:

1. Imports and `_json_input` helper
2. `_build_parser()` — builds the full argparse tree
3. One `_handle_<group>(args)` function per command group (14 functions)
4. `main(argv)` — parses, dispatches to the right handler, catches CurikError

Each handler function resolves `root = Path(args.path).resolve()` and
calls the domain function. For `--json` subcommands, `print(json.dumps(result,
indent=2))` on success. For human-readable subcommands, format output
appropriately (matching or improving on the current server.py output).

Error handling: catch `CurikError` in each handler; print to stderr and
return exit code 1. Catch `json.JSONDecodeError` in `_json_input`.

### Files to Modify

**curik/cli.py** — complete rewrite

Imports needed:
```python
from .project import (
    CurikError, advance_phase, advance_sub_phase, get_course_status,
    get_phase, get_spec, init_course, record_alignment,
    record_course_concept, record_pedagogical_model, update_course_yml,
    update_spec,
)
from .changes import (
    approve_change_plan, close_change_plan, create_change_plan,
    create_issue, execute_change_plan, list_issues, register_change_plan,
    review_change_plan,
)
from .hugo import (create_content_page, hugo_build, list_content_pages, update_frontmatter)
from .migrate import inventory_course, migrate_structure, sequester_content
from .validation import (
    get_validation_report, save_validation_report, validate_course,
    validate_lesson, validate_module,
)
from .readme import generate_readmes
from .scaffolding import (
    approve_outline, create_lesson_stub, create_outline,
    generate_change_plan, get_outline, scaffold_structure,
)
from .templates import hugo_setup, hugo_setup_from_course, bump_curriculum_version
from .syllabus import validate_syllabus_consistency, write_syllabus_url
from .publish import check_publish_ready, get_publish_guide
```

**`_json_input(args, attr="content")` helper signature:**
```python
def _json_input(args, attr: str = "content") -> Any:
    """Resolve JSON from positional arg, --file, or stdin."""
```
Returns parsed object. Raises `SystemExit(1)` with message on failure.

### Testing Plan

Existing `tests/test_cli.py` has two tests that must still pass:
- `test_init_prints_friendly_message`
- `test_init_creates_course_dir`

Add a new `TestCli<Group>` class per group with at minimum:
- Happy-path test: call `main([group, subcommand, ...])` with a real temp dir
  and assert exit code 0 and expected output shape
- Error-path test: call without init'd project and assert exit code 1

Priority groups for test coverage (most complex / highest risk):
- phase: get, advance, advance-sub
- config: update (JSON merge)
- scaffold: structure, lesson
- validate: lesson, course
- hugo: setup, build
- publish: check, guide

Remaining groups can have single smoke tests.

### Documentation Updates

No documentation changes in this ticket. Template files (claude-section.md,
curik-skill.md) are updated in ticket 004.
