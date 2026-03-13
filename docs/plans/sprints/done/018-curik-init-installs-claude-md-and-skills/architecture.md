---
status: complete
---

# Architecture

## Architecture Overview

Curik is a Python MCP server that guides AI agents through curriculum
development. Sprints 014–017 replaced MkDocs with Hugo across config
generation, content formats, agent/skill docs, and the League theme.

This sprint adds CLAUDE.md installation and skill deployment to `curik init`,
following the pattern established by CLASI's `init_command.py`.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────────┐
│ CLI          │────▶│ project.py   │────▶│ .course/, course.yml│
│ (cli.py)     │     │ init_course()│     │ .mcp.json           │
│              │     └──────────────┘     └─────────────────────┘
│              │     ┌──────────────┐     ┌─────────────────────┐
│  curik init  │────▶│ init_command │────▶│ CLAUDE.md           │
│              │     │  .py         │     │ .claude/skills/     │
│              │     │              │     │ .claude/settings    │
│              │     │              │     │ .vscode/mcp.json    │
│              │     └──────────────┘     └─────────────────────┘
│              │
│              │     ┌──────────────┐     ┌─────────────────────┐
│ MCP Server   │────▶│ server.py    │────▶│ instructions param  │
│ (server.py)  │     │              │     │ (Hugo conventions)  │
│              │     └──────────────┘     └─────────────────────┘
└─────────────┘
```

## Technology Stack

- **Python 3.12+** — existing project language
- **importlib.resources** — load template files from package
- **argparse** — existing CLI framework (no click dependency)

## Component Design

### Component: init_command (NEW)

**Purpose**: Install CLAUDE.md section, skills, and MCP permissions
into a target repository.

**Use Cases**: SUC-001, SUC-002, SUC-003

New module `curik/init_command.py` with these functions:

- `_update_claude_md(target: Path) -> bool`
  Creates/appends/replaces CLAUDE.md section using `<!-- CURIK:START -->`
  / `<!-- CURIK:END -->` markers. Template content loaded from
  `curik/init/claude-section.md`.

- `_write_curik_skill(target: Path) -> bool`
  Copies `/curik` skill from `curik/init/curik-skill.md` to
  `.claude/skills/curik/SKILL.md`. Returns False if unchanged.

- `_update_vscode_mcp_json(target: Path) -> bool`
  Merges curik server config into `.vscode/mcp.json` (VS Code format
  with `servers` key and `type` field).

- `_update_settings_json(settings_path: Path) -> bool`
  Adds `mcp__curik__*` to permissions allowlist. Merges with existing
  data (does not overwrite other permissions).

- `run_init(target: Path) -> dict[str, list[str]]`
  Orchestrates all of the above. Returns dict of created/updated/
  unchanged files for CLI output.

### Component: init templates (NEW)

**Purpose**: Bundled template files for CLAUDE.md and skills.

New package `curik/init/` with:

- `__init__.py` — empty
- `claude-section.md` — CLAUDE.md content between markers, covering:
  - Hugo as SSG, `content/` directory, `_index.md` branch bundles
  - Shortcodes: `instructor-guide`, `callout`, `readme-shared`, `readme-only`
  - League Hugo theme reference
  - Curriculum development phases and Curik MCP tools
- `curik-skill.md` — `/curik` skill dispatcher (similar to CLASI's `/se`)

### Component: project.py (MODIFIED)

**Purpose**: Call init_command functions from init_course().

**Use Cases**: SUC-001, SUC-002

Changes:
- Import and call `run_init()` from `init_command` at end of `init_course()`
- Merge returned file lists into the existing created/existing result

### Component: cli.py (MODIFIED)

**Purpose**: Update init command output messaging.

Changes:
- Print init_command results (CLAUDE.md, skills, permissions status)

### Component: server.py (MODIFIED)

**Purpose**: Update MCP server instructions.

Changes:
- Replace `instructions="Curik curriculum development tool"` with a
  descriptive string covering Hugo conventions, shortcode syntax,
  content directory, and available MCP tools.

## Dependency Map

```
cli.py
  └── project.py
        ├── init_command.py (NEW)
        │     └── curik/init/ templates (NEW)
        └── .course/ setup (existing)

server.py
  └── instructions string (updated)
```

## Data Model

No data model changes. New files created on disk during init:
- `CLAUDE.md` (created or updated)
- `.claude/skills/curik/SKILL.md` (created or updated)
- `.claude/settings.local.json` (created or updated)
- `.vscode/mcp.json` (created or updated)

## Security Considerations

- Permission entries use glob pattern `mcp__curik__*` — scoped to curik
  MCP tools only
- Template files are read-only package data, not user-editable
- JSON parsing handles malformed files gracefully (empty dict fallback)

## Sprint Changes

### Changed Components

- **init_command.py**: NEW — CLAUDE.md, skill, and permission installation
- **curik/init/**: NEW — template package with claude-section.md and curik-skill.md
- **project.py**: Call init_command.run_init() from init_course()
- **cli.py**: Updated init output messaging
- **server.py**: Descriptive MCP instructions string
- **pyproject.toml**: Add curik.init package and *.md package-data

### Migration Concerns

None — `curik init` gains new functionality. Existing initialized
projects can re-run `curik init` to pick up the new files (idempotent).
