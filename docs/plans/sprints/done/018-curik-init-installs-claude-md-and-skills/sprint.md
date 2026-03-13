---
id: 018
title: Curik Init Installs CLAUDE.md and Skills
status: done
branch: sprint/018-curik-init-installs-claude-md-and-skills
use-cases:
- SUC-001
- SUC-002
- SUC-003
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 018: Curik Init Installs CLAUDE.md and Skills

## Goals

Make `curik init` follow the same pattern as `clasi init`: install a
CLAUDE.md section (with `<!-- CURIK:START -->`/`<!-- CURIK:END -->` markers),
install a `/curik` skill stub, configure MCP permissions, and update the
MCP server instructions to describe Hugo conventions.

## Problem

`curik init` currently creates `.course/`, `course.yml`, and `.mcp.json`
but does NOT install a CLAUDE.md section or skills. Agents connecting to
a Curik-initialized project have no guidance about Hugo shortcodes,
`content/` directory structure, the League theme, or curriculum workflow
conventions. They only see the sparse MCP server instructions string
`"Curik curriculum development tool"`.

CLASI solved this with `clasi init` which writes a CLAUDE.md section,
installs a `/se` skill, and configures permissions. Curik needs the same.

## Solution

1. Create a new `curik/init_command.py` module (following CLASI's pattern)
   with functions to:
   - Write/update CLAUDE.md with a `<!-- CURIK:START -->`/`<!-- CURIK:END -->`
     section describing Hugo, shortcodes, content directory, and workflow
   - Install a `/curik` skill stub to `.claude/skills/curik/SKILL.md`
   - Add `mcp__curik__*` to `.claude/settings.local.json` permissions
   - Configure `.vscode/mcp.json` for VS Code MCP support

2. Create bundled template files:
   - `curik/init/claude-section.md` — the CLAUDE.md section content
   - `curik/init/curik-skill.md` — the `/curik` slash command skill

3. Update `curik init` (cli.py + project.py) to call the new init functions.

4. Update MCP server `instructions` to be informative about Hugo and
   curriculum conventions.

## Success Criteria

- `curik init` in a fresh directory creates CLAUDE.md with Curik section
- `curik init` in a directory with existing CLAUDE.md appends the section
- `curik init` re-run replaces the section in place (idempotent)
- `/curik` skill is installed to `.claude/skills/curik/SKILL.md`
- `mcp__curik__*` permission added to `.claude/settings.local.json`
- `.vscode/mcp.json` configured with curik server
- MCP server `instructions` describes Hugo conventions
- All existing tests still pass

## Scope

### In Scope

- `curik/init_command.py` — new module with init helper functions
- `curik/init/` — new package with template files (claude-section.md, curik-skill.md)
- `curik/project.py` — call new init functions from `init_course()`
- `curik/server.py` — update `instructions` parameter
- `curik/cli.py` — update init output messaging
- `pyproject.toml` — add `curik.init` to packages and package-data
- Tests for all new init functions

### Out of Scope

- Curik-specific agents installed locally (agents stay in the MCP server)
- Changes to curriculum content generation
- Hugo binary installation/management

## Test Strategy

Unit tests for each init helper function using tmp_path fixtures:
- CLAUDE.md create/append/replace-in-place scenarios
- Skill file write/unchanged detection
- Settings JSON merge with existing data
- VS Code MCP config merge
- Integration test of full init_course() producing all expected files

## Architecture Notes

- Follow CLASI's init_command.py pattern exactly for consistency
- Template files live in `curik/init/` subpackage (not inline strings)
- No `click` dependency — Curik uses `argparse`, so use `print()` instead
- The CLAUDE.md section should tell agents about:
  - Hugo as the static site generator (not MkDocs)
  - `content/` directory structure with `_index.md` branch bundles
  - Hugo shortcodes: `instructor-guide`, `callout`, `readme-shared`, `readme-only`
  - The League Hugo theme
  - Curriculum development workflow (Phase 1 → Phase 2)

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
