---
id: "002"
title: "Trim syllabus.py and clean server.py registrations"
status: done
use-cases: [SUC-004]
depends-on: ['001']
github-issue: ""
todo: ""
---

# Trim syllabus.py and clean server.py registrations

## Description

Remove three low-value functions from curik/syllabus.py: get_syllabus (one-line
file read), regenerate_syllabus (thin wrapper over the syllabus library), and
read_syllabus_entries (thin wrapper over Course.from_yaml). Retain
write_syllabus_url and validate_syllabus_consistency, which contain non-trivial
logic. Retain the private _iter_lessons helper, which validate_syllabus_consistency
calls.

Remove the corresponding MCP tool registrations from server.py and update the
syllabus import statement to only name the two retained public functions.

This ticket depends on 001 because server.py will already have been edited there;
doing this in sequence avoids editing the same region of the file twice.

## Acceptance Criteria

- [x] curik/syllabus.py contains exactly: _iter_lessons (private),
      write_syllabus_url, validate_syllabus_consistency — nothing else
- [x] The `from syllabus.sync import compile_syllabus` line is removed from
      syllabus.py (it was only used by regenerate_syllabus)
- [x] `from syllabus.models import Course, LessonSet` is retained in syllabus.py
      (used by validate_syllabus_consistency)
- [x] server.py syllabus import reads only write_syllabus_url and
      validate_syllabus_consistency
- [x] server.py has no tool_read_syllabus_entries, tool_regenerate_syllabus,
      or tool_get_syllabus functions
- [x] tool_write_syllabus_url and tool_validate_syllabus_consistency remain
      and their implementations are unchanged
- [x] `uv run pytest` passes (3 pre-existing failures unrelated to this ticket;
      test_syllabus.py import errors addressed in ticket 003)

## Implementation Plan

### Approach

1. Edit curik/syllabus.py:
   - Remove `from syllabus.sync import compile_syllabus` (line 9; used only by
     regenerate_syllabus)
   - Remove read_syllabus_entries function (lines 37-43)
   - Remove regenerate_syllabus function (lines 87-94)
   - Remove get_syllabus function (lines 97-102)
   - Confirm _iter_lessons remains (lines 14-34; still needed by
     validate_syllabus_consistency)

2. Edit curik/server.py — update the syllabus import block (lines 74-80) from:
   ```python
   from .syllabus import (
       get_syllabus,
       read_syllabus_entries,
       regenerate_syllabus,
       validate_syllabus_consistency,
       write_syllabus_url,
   )
   ```
   to:
   ```python
   from .syllabus import (
       validate_syllabus_consistency,
       write_syllabus_url,
   )
   ```

3. Edit curik/server.py — remove tool functions (all in the `# -- Syllabus tools --`
   section, lines 732-771):
   - Remove tool_read_syllabus_entries
   - Remove tool_regenerate_syllabus
   - Remove tool_get_syllabus
   - Leave tool_write_syllabus_url and tool_validate_syllabus_consistency intact

4. Run `uv run pytest`.

### Files to Modify

- curik/syllabus.py — remove three functions and one import
- curik/server.py — update syllabus import; remove three tool functions

### Files to Create

None.

### Files to Delete

None.

### Testing Plan

- Run `uv run pytest` after changes
- WriteSyllabusUrlTest and ValidateSyllabusConsistencyTest must still pass
- No NameError or ImportError from the removed compile_syllabus import

### Documentation Updates

None — init template cleanup is handled in ticket 003.
