---
id: "003"
title: "Clean up tests and init templates"
status: done
use-cases: [SUC-001, SUC-002, SUC-003, SUC-004]
depends-on: ['001', '002']
github-issue: ""
todo: ""
---

# Clean up tests and init templates

## Description

After tickets 001 and 002 delete modules and trim syllabus.py, this ticket
finalizes the cleanup:

1. Remove test classes in tests/test_syllabus.py that cover functions removed in
   ticket 002 (ReadSyllabusEntriesTest, GetSyllabusTest, and MCPSyllabusToolTest
   methods for the removed tools).
2. Update curik/init/claude-section.md to remove the Syllabus subsection entries
   for regenerate_syllabus, get_syllabus, read_syllabus_entries and the entire
   Quiz subsection.
3. Review curik/init/curik-skill.md for any references to removed tools (the
   current file does not list those tools, but verify and document the check).

This ticket depends on both 001 and 002 so that test files reflect the final
state of the codebase before they are modified.

## Acceptance Criteria

- [x] tests/test_syllabus.py has no ReadSyllabusEntriesTest class
- [x] tests/test_syllabus.py has no GetSyllabusTest class
- [x] tests/test_syllabus.py MCPSyllabusToolTest class (if retained) has no
      test_tool_read_syllabus_entries_*, test_tool_get_syllabus_* methods
- [x] WriteSyllabusUrlTest and ValidateSyllabusConsistencyTest are unchanged and
      still pass
- [x] curik/init/claude-section.md Syllabus line does not mention
      regenerate_syllabus, get_syllabus, or read_syllabus_entries
- [x] curik/init/claude-section.md has no Quiz subsection line
- [x] curik/init/curik-skill.md has no references to removed tools (verify;
      document finding)
- [x] `uv run pytest` passes with no failures

## Implementation Plan

### Approach

1. Edit tests/test_syllabus.py:
   - Remove the ReadSyllabusEntriesTest class (lines 75-102)
   - Remove the GetSyllabusTest class (lines 137-150)
   - In MCPSyllabusToolTest: remove test_tool_read_syllabus_entries_returns_json,
     test_tool_read_syllabus_entries_error, and test_tool_get_syllabus_returns_content
     methods (lines 213-228)
   - Remove get_syllabus and read_syllabus_entries from the import at lines 13-18
   - Verify the remaining import is:
     `from curik.syllabus import (validate_syllabus_consistency, write_syllabus_url,)`

2. Edit curik/init/claude-section.md:
   - Update the Syllabus line (line 49) from:
     `- Syllabus: regenerate_syllabus, get_syllabus, write_syllabus_url, trigger_readme_generation, validate_syllabus_consistency`
     to:
     `- Syllabus: write_syllabus_url, trigger_readme_generation, validate_syllabus_consistency`
   - Remove the Quiz line (line 53):
     `- Quiz: generate_quiz_stub, validate_quiz_alignment, set_quiz_status`

3. Review curik/init/curik-skill.md: The current file contains only the /curik
   dispatch table (status, spec, phase, validate, agents, skills, refs, publish)
   and the publish workflow. It does not reference quiz, research, or syllabus
   tools directly. Confirm and note — no changes needed.

4. Run `uv run pytest`.

### Files to Modify

- tests/test_syllabus.py — remove three test classes/methods and update import
- curik/init/claude-section.md — update Syllabus line, remove Quiz line

### Files to Create

None.

### Files to Delete

None (tests/test_assets_research.py was deleted in ticket 001).

### Testing Plan

- Run `uv run pytest` after changes
- WriteSyllabusUrlTest must still pass (3 tests)
- ValidateSyllabusConsistencyTest must still pass (3 tests)
- MCPSyllabusToolTest must still have test_tool_write_syllabus_url_returns_json
  and test_tool_validate_syllabus_consistency_returns_json passing

### Documentation Updates

The changes to curik/init/claude-section.md are themselves the documentation
update — they correct the tool listing that is installed into curriculum
project CLAUDE.md files on next `curik init`.
