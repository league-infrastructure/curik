---
id: '005'
title: Create syllabus-integration skill definition
status: done
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Create syllabus-integration skill definition

## Description

Create `curik/skills/syllabus-integration.md`, a skill definition that documents
the conventions for working with `syllabus.yaml` and the `syl` tool. Agents
need to understand the syllabus file format, how lesson UIDs map to file paths,
how to use the `syl` CLI tool for reading and manipulating syllabus data, and
how the syllabus relates to MkDocs navigation configuration. Without this skill,
agents have no reference for syllabus-related operations.

The file should follow the same Markdown-with-YAML-frontmatter format as
existing skills in `curik/skills/` and be loadable via `get_skill_definition()`.

## Acceptance Criteria

- [ ] `curik/skills/syllabus-integration.md` exists with valid YAML frontmatter
- [ ] The frontmatter includes `name`, `description`, and `category` fields
- [ ] The skill documents the `syllabus.yaml` file format and schema
- [ ] The skill documents how lesson UIDs map to file paths on disk
- [ ] The skill documents the `syl` CLI tool and its common commands
- [ ] The skill documents the relationship between `syllabus.yaml` entries and MkDocs `nav` configuration
- [ ] The skill is loadable via `get_skill_definition("syllabus-integration")` without error

## Testing

- **Existing tests to run**: `uv run pytest tests/` to ensure no regressions from adding the file
- **New tests to write**: Covered by Ticket 006 in `tests/test_validation_enhanced.py` -- verify file is loadable via `get_skill_definition()` and contains expected section headings
- **Verification command**: `uv run pytest tests/ -v`
