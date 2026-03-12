---
id: '004'
title: Create status-tracking skill definition
status: done
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Create status-tracking skill definition

## Description

Create `curik/skills/status-tracking.md`, a skill definition that documents the
conventions for tracking course development status and progress. Agents need a
clear reference for how development status is recorded, what statuses are valid,
where status metadata lives, and how progress is reported. Without this skill
definition, agents have no guidance and must guess at conventions or ask the
stakeholder repeatedly.

The file should follow the same Markdown-with-YAML-frontmatter format as
existing skills in `curik/skills/` and be loadable via `get_skill_definition()`.

## Acceptance Criteria

- [ ] `curik/skills/status-tracking.md` exists with valid YAML frontmatter
- [ ] The frontmatter includes `name`, `description`, and `category` fields
- [ ] The skill documents the set of valid development statuses and their meanings
- [ ] The skill documents where status metadata is stored (e.g., YAML frontmatter, status files)
- [ ] The skill documents how to update and transition between statuses
- [ ] The skill documents conventions for tracking progress at course, module, and lesson levels
- [ ] The skill is loadable via `get_skill_definition("status-tracking")` without error

## Testing

- **Existing tests to run**: `uv run pytest tests/` to ensure no regressions from adding the file
- **New tests to write**: Covered by Ticket 006 in `tests/test_validation_enhanced.py` -- verify file is loadable via `get_skill_definition()` and contains expected section headings
- **Verification command**: `uv run pytest tests/ -v`
