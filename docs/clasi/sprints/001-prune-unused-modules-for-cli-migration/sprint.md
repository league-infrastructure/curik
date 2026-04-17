---
id: "001"
title: "Prune Unused Modules for CLI Migration"
status: planning
branch: sprint/001-prune-unused-modules-for-cli-migration
use-cases: [SUC-001, SUC-002, SUC-003, SUC-004]
todo: prune-modules-for-cli-migration.md
---

# Sprint 001: Prune Unused Modules for CLI Migration

## Goals

Remove modules that have no meaningful CLI equivalent and clean up their
server-side registrations, tests, and template references. This is the
first step in migrating curik from an MCP server model to a CLI.

## Problem

The curik package carries several modules that were written in anticipation of
features that were never deployed, or that perform trivial file I/O that can be
described in agent instructions rather than executed as server tools. These
modules add surface area with no value and will not translate to CLI commands:

- `curik/quiz.py` — quiz stub generation and alignment checking; not yet used
- `curik/research.py` — numbered file I/O for research findings; trivially
  described by instructions
- `curik/assets.py` — serves agent/skill/reference markdown by reading package
  resources; Claude can read these files directly from the filesystem

Additionally, three functions in `curik/syllabus.py` expose low-value wrappers
(`get_syllabus`, `regenerate_syllabus`, `read_syllabus_entries`) that duplicate
what Claude can do by reading `syllabus.yaml` directly or calling the
`syllabus` library.

The `ACTIVITY_MAPPINGS` dict in `assets.py` documents which agents, skills,
and instructions belong to each named activity. This reference value must be
preserved as a markdown document before assets.py is deleted.

## Solution

Delete `quiz.py`, `research.py`, and `assets.py` outright. Trim `syllabus.py`
to the two functions with real logic. Remove all associated MCP tool
registrations from `server.py`, drop the deleted-module test files, and trim
`test_syllabus.py` to cover only the surviving functions. Clean up the two init
template files that document the removed tools.

Note: `assets.py` is the import source for `get_activity_guide` and the asset
loading functions (`get_agent_definition`, `list_agents`, etc.) that `server.py`
currently uses. All of those functions will be deleted along with the module.
Server.py imports from `assets.py` must be removed entirely; the `ACTIVITY_MAPPINGS`
dict is preserved as a reference markdown file.

## Success Criteria

- `curik/quiz.py`, `curik/research.py`, and `curik/assets.py` are deleted
- `curik/syllabus.py` contains only `write_syllabus_url` and
  `validate_syllabus_consistency` (plus `_iter_lessons` which is used by
  `validate_syllabus_consistency`)
- `curik/server.py` has no imports or tool registrations for removed code
- `curik/references/activity-mappings.md` documents the ACTIVITY_MAPPINGS dict
- Tests for deleted modules are removed; surviving syllabus tests pass
- `curik/init/claude-section.md` and `curik/init/curik-skill.md` no longer
  reference deleted tools
- `uv run pytest` passes with no failures

## Scope

### In Scope

- Delete curik/quiz.py
- Delete curik/research.py
- Delete curik/assets.py
- Trim curik/syllabus.py to keep write_syllabus_url and validate_syllabus_consistency
  (keep _iter_lessons as it is used by validate_syllabus_consistency)
- Remove all server.py imports and @mcp.tool() registrations for the above
- Create curik/references/activity-mappings.md preserving ACTIVITY_MAPPINGS
- Delete tests/test_assets_research.py
- Remove test classes ReadSyllabusEntriesTest, GetSyllabusTest, and MCP wrapper
  tests for deleted tools from tests/test_syllabus.py
- Remove references to deleted tools from curik/init/claude-section.md and
  curik/init/curik-skill.md

### Out of Scope

- Migrating any other modules to CLI
- Adding CLI entry points or argument parsers
- Modifying the remaining curik/syllabus.py functions' behavior
- Any changes to curik/project.py, curik/validation.py, curik/hugo.py,
  curik/scaffolding.py, curik/changes.py, curik/templates.py, curik/readme.py,
  curik/migrate.py

## Test Strategy

Run `uv run pytest` after changes. The surviving test suite must pass cleanly.
Key checks:
- `tests/test_assets_research.py` is deleted (not just skipped)
- `tests/test_syllabus.py` retains WriteSyllabusUrlTest and
  ValidateSyllabusConsistencyTest; removes ReadSyllabusEntriesTest,
  GetSyllabusTest, and MCP wrappers for removed tools
- No import errors in server.py or anywhere else

## Architecture Notes

The assets loading functions (`get_agent_definition`, `list_agents`,
`get_skill_definition`, `list_skills`, `get_instruction`, `list_instructions`,
`get_process_guide`, `get_activity_guide`) live in `curik/assets.py`. These will
all be removed. The MCP tool wrappers in `server.py` that call these functions
must be removed too (tool_list_agents, tool_get_agent_definition,
tool_list_skills, tool_get_skill_definition, tool_list_instructions,
tool_get_instruction, tool_list_references, tool_get_reference,
tool_get_process_guide, tool_get_activity_guide).

The ACTIVITY_MAPPINGS dict has documentation value — it maps activity names to
(agent, skills, instructions) triples. Preserve it as a reference markdown table
in curik/references/activity-mappings.md so future CLI or agent instructions
can reference it.

## GitHub Issues

(None)

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

| # | Title | Depends On | Group |
|---|-------|------------|-------|
| 001 | Delete quiz, research, and assets modules | — | 1 |
| 002 | Trim syllabus.py and clean server.py | 001 | 2 |
| 003 | Clean up tests and init templates | 001, 002 | 3 |

**Groups**: Tickets in the same group can execute in parallel.
Groups execute sequentially (1 before 2, etc.).
