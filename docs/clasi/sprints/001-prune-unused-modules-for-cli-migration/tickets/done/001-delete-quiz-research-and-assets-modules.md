---
id: '001'
title: Delete quiz, research, and assets modules
status: done
use-cases:
- SUC-001
- SUC-002
- SUC-003
depends-on: []
github-issue: ''
todo: prune-modules-for-cli-migration.md
---

# Delete quiz, research, and assets modules

## Description

Delete curik/quiz.py, curik/research.py, and curik/assets.py outright. Before
deleting assets.py, extract the ACTIVITY_MAPPINGS dict and write it as a
markdown table to curik/references/activity-mappings.md. Remove all server.py
imports and @mcp.tool() registrations that reference these three modules.
Delete tests/test_assets_research.py.

These modules are being removed as the first step in a CLI migration. They
either were never used (quiz), are trivially described in agent instructions
(research), or serve files that Claude can read directly from the filesystem
(assets).

## Acceptance Criteria

- [x] curik/quiz.py does not exist
- [x] curik/research.py does not exist
- [x] curik/assets.py does not exist
- [x] curik/references/activity-mappings.md exists and contains the ACTIVITY_MAPPINGS
      data as a readable markdown table
- [x] server.py has no import from .quiz, .research, or .assets
- [x] server.py has none of these tool functions:
      tool_generate_quiz_stub, tool_validate_quiz_alignment, tool_set_quiz_status,
      tool_save_research_findings, tool_get_research_findings,
      tool_list_agents, tool_get_agent_definition, tool_list_skills,
      tool_get_skill_definition, tool_list_instructions, tool_get_instruction,
      tool_list_references, tool_get_reference, tool_get_process_guide,
      tool_get_activity_guide
- [x] tests/test_assets_research.py does not exist
- [x] `uv run pytest` passes with no failures or import errors (3 pre-existing failures unrelated to this ticket remain unchanged)

## Implementation Plan

### Approach

1. Read ACTIVITY_MAPPINGS from curik/assets.py.
2. Write curik/references/activity-mappings.md with the mappings as a markdown
   table (columns: Activity, Agent, Skills, Instructions).
3. Delete curik/quiz.py.
4. Delete curik/research.py.
5. Delete curik/assets.py.
6. Delete tests/test_assets_research.py.
7. Edit curik/server.py:
   - Remove the `from .quiz import ...` line (lines 54)
   - Remove the `from .research import ...` line (lines 55)
   - Remove the `from .assets import ...` block (lines 11-23)
   - Remove the `# -- Asset tools --` section and all tool functions within it:
     tool_list_agents, tool_get_agent_definition, tool_list_skills,
     tool_get_skill_definition, tool_list_instructions, tool_get_instruction,
     tool_list_references, tool_get_reference
   - Remove the `# -- Process discovery tools --` section and functions:
     tool_get_process_guide, tool_get_activity_guide
   - Remove the `# -- Research tools --` section and functions:
     tool_save_research_findings, tool_get_research_findings
   - Remove the `# -- Quiz tools --` section and functions:
     tool_generate_quiz_stub, tool_validate_quiz_alignment, tool_set_quiz_status
   - Remove ACTIVITY_MAPPINGS usage in tool_update_course_yml (the dict is used
     only in the import block, not in the tool itself — verify no other usages)
8. Run `uv run pytest` to confirm no failures.

### Files to Create

- curik/references/activity-mappings.md (new)

### Files to Delete

- curik/quiz.py
- curik/research.py
- curik/assets.py
- tests/test_assets_research.py

### Files to Modify

- curik/server.py — remove imports and tool registrations for deleted modules

### Testing Plan

- Run `uv run pytest` after deletions to confirm no import errors
- Verify python -c "import curik.server" succeeds (or equivalent import check)
- No new tests to write (this is a deletion ticket)

### Documentation Updates

None — template cleanup is handled in ticket 003.
