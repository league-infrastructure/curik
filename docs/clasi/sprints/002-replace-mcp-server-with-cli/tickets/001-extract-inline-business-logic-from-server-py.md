---
id: "001"
title: "Extract inline business logic from server.py"
status: done
use-cases: [SUC-005]
depends-on: []
github-issue: ""
todo: "replace-mcp-server-with-cli.md"
---

# Extract inline business logic from server.py

## Description

server.py contains four pockets of inline business logic that belong in domain
modules. This ticket moves them before the CLI is built, so the CLI can call
domain functions rather than reimplementing logic.

The four extractions:

1. `COURSE_YML_REQUIRED_FIELDS` + `_is_tbd()` — move to `project.py` (lines
   712-732 of server.py). Used by both `tool_update_course_yml` and
   `_read_publish_state`.

2. `tool_update_course_yml` YAML merge logic — extract to
   `project.update_course_yml(root: Path, updates: dict) -> dict` (server.py
   lines 202-268). The new function accepts a dict (not a JSON string) and
   returns a dict with keys `updated_fields`, `content`, `message`, and
   optionally `still_tbd`.

3. `tool_hugo_setup` course.yml reading — extract to
   `templates.hugo_setup_from_course(root: Path) -> dict` (server.py lines
   639-676). Reads title, tier, repo_url from course.yml then calls the
   existing `hugo_setup(root, title, tier, repo_url=repo_url)`.

4. `_read_publish_state` + `tool_get_publish_guide` + `tool_check_publish_ready`
   — move to new `curik/publish.py` (server.py lines 735-1099).
   Public API: `get_publish_guide(root: Path) -> str` and
   `check_publish_ready(root: Path) -> dict` (returns dict, not JSON string).
   `_read_publish_state` stays private within publish.py.

After this ticket, server.py tool handlers become thin wrappers that import
from the new domain locations. server.py must still work and all existing
tests must pass.

## Acceptance Criteria

- [x] `from curik.project import COURSE_YML_REQUIRED_FIELDS, _is_tbd` works
- [x] `from curik.project import update_course_yml` works; calling it writes merged course.yml and returns a result dict
- [x] `from curik.templates import hugo_setup_from_course` works; it reads course.yml and delegates to `hugo_setup`
- [x] `from curik.publish import get_publish_guide, check_publish_ready` works
- [x] server.py tool handlers for update_course_yml, hugo_setup, get_publish_guide, check_publish_ready delegate to the new functions
- [x] `uv run pytest` passes with no regressions

## Implementation Plan

### Approach

Extract in dependency order: COURSE_YML_REQUIRED_FIELDS + _is_tbd first
(other extractions depend on them), then update_course_yml, then
hugo_setup_from_course, then publish.py. Update server.py imports after each
extraction to keep tests green throughout.

### Files to Modify

**curik/project.py**
- Add `COURSE_YML_REQUIRED_FIELDS` list (copy from server.py lines 712-719)
- Add `_is_tbd(value: object) -> bool` (copy from server.py lines 722-732)
- Add `update_course_yml(root: Path, updates: dict) -> dict` — adapt from
  server.py lines 220-268: accept root and updates dict directly (not JSON),
  perform YAML read-merge-write, return result dict

**curik/templates.py**
- Add `hugo_setup_from_course(root: Path) -> dict` — adapt from server.py
  lines 656-676: read course.yml, extract title/tier/repo_url, call
  `hugo_setup(root, title, tier, repo_url=repo_url)`, return its result

**curik/server.py** (temporary — deleted in ticket 004)
- Add imports: `COURSE_YML_REQUIRED_FIELDS`, `_is_tbd`, `update_course_yml`
  from `.project`; `hugo_setup_from_course` from `.templates`;
  `get_publish_guide`, `check_publish_ready` from `.publish`
- Remove now-duplicated definitions of COURSE_YML_REQUIRED_FIELDS and _is_tbd
- Simplify `tool_update_course_yml`: parse JSON, call `update_course_yml`,
  return `json.dumps(result, indent=2)`
- Simplify `tool_hugo_setup`: when title is empty, call
  `hugo_setup_from_course(_root())`; otherwise call `hugo_setup` directly
- Simplify `tool_get_publish_guide`: call `get_publish_guide(_root())`
- Simplify `tool_check_publish_ready`: call `check_publish_ready(_root())`,
  return `json.dumps(result, indent=2)`

### New Files to Create

**curik/publish.py**
- Copy `_read_publish_state` verbatim from server.py (update import paths)
- Define `get_publish_guide(root: Path) -> str` with the guide builder body
- Define `check_publish_ready(root: Path) -> dict` returning the checks dict
- Imports: `from __future__ import annotations`, `import json`, `from pathlib
  import Path`, `import yaml`, `from .project import COURSE_YML_REQUIRED_FIELDS,
  _is_tbd`, `from .hugo import hugo_build`

### Testing Plan

- Run existing `tests/test_mcp_server.py` to confirm no regressions
- Add `tests/test_publish.py` with:
  - `test_check_publish_ready_missing_course_yml`: assert `course_yml_exists: False`
  - `test_check_publish_ready_with_tbd_fields`: init course, assert TBD fields listed
  - `test_get_publish_guide_returns_string`: assert result is a non-empty string
- Add to `tests/test_project.py`:
  - `test_update_course_yml_merges_fields`: init, call update_course_yml, read back
  - `test_update_course_yml_reports_tbd`: check still_tbd list for TBD fields
  - `test_is_tbd_various_values`: cover None, "", "TBD", 0, [], truthy values

### Documentation Updates

No documentation updates needed beyond code changes.
