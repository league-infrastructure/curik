---
status: done
sprint: '001'
tickets:
- 001-001
---

# Prune quiz, research, assets modules and trim syllabus for CLI migration

Preparation for migrating from MCP server to CLI. Remove modules that
don't need CLI equivalents — they are either unused, trivial file I/O
that agent instructions can describe, or asset-serving that Claude can
do by reading files directly.

## Deletions

- **curik/quiz.py** — not used yet, remove entirely
- **curik/research.py** — just numbered file I/O, agent instructions can
  describe the convention
- **curik/assets.py** — Claude reads agent/skill/instruction markdown
  files directly from the filesystem
- Associated tests (tests/test_assets_research.py, tests/test_quiz.py if
  it exists)

## Trimming

- **curik/syllabus.py** — remove `get_syllabus()`, `regenerate_syllabus()`,
  `read_syllabus_entries()` (and `_iter_lessons` helper). Keep
  `write_syllabus_url()` and `validate_syllabus_consistency()` which have
  real logic.

## Server cleanup

- Remove all imports and MCP tool registrations in `curik/server.py` for
  the deleted modules and trimmed syllabus functions
- Update syllabus imports to only import the two kept functions

## Preservation

- Move `ACTIVITY_MAPPINGS` dict from `assets.py` into a new reference
  file `curik/references/activity-mappings.md`

## Template cleanup

- Remove references to deleted tools from `curik/init/claude-section.md`
  and `curik/init/curik-skill.md`

## Test updates

- Remove tests for deleted modules
- Update syllabus tests to only cover kept functions
  (tests/test_syllabus.py)
