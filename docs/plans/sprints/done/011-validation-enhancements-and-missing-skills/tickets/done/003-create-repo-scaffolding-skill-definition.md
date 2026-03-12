---
id: '003'
title: Create repo-scaffolding skill definition
status: done
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Create repo-scaffolding skill definition

## Description

Create `curik/skills/repo-scaffolding.md`, a skill definition that documents
the conventions for repository directory structures, file layouts, and naming
used across League course projects. Agents currently have no authoritative
reference for how to scaffold a new course repository, which leads to
inconsistent structures and manual correction. This skill provides that
reference so agents can follow project conventions without relying on tribal
knowledge.

The file should follow the same Markdown-with-YAML-frontmatter format as
existing skills in `curik/skills/` and be loadable via `get_skill_definition()`.

## Acceptance Criteria

- [ ] `curik/skills/repo-scaffolding.md` exists with valid YAML frontmatter
- [ ] The frontmatter includes `name`, `description`, and `category` fields
- [ ] The skill documents the expected top-level directory structure for a course repository
- [ ] The skill documents file naming conventions (e.g., lesson files, module directories, config files)
- [ ] The skill documents per-tier layout differences where applicable
- [ ] The skill is loadable via `get_skill_definition("repo-scaffolding")` without error
- [ ] The content includes expected section headings (e.g., Directory Structure, Naming Conventions)

## Testing

- **Existing tests to run**: `uv run pytest tests/` to ensure no regressions from adding the file
- **New tests to write**: Covered by Ticket 006 in `tests/test_validation_enhanced.py` -- verify file is loadable via `get_skill_definition()` and contains expected section headings
- **Verification command**: `uv run pytest tests/ -v`
