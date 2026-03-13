---
id: '001'
title: Create init templates package and init_command module
status: done
use-cases:
- SUC-001
- SUC-002
- SUC-003
depends-on: []
---

# Create init templates package and init_command module

## Description

Create the `curik/init/` package with template files and the
`curik/init_command.py` module with all init helper functions.
This is the core implementation ticket.

Files to create:
- `curik/init/__init__.py` — empty
- `curik/init/claude-section.md` — CLAUDE.md section template
- `curik/init/curik-skill.md` — `/curik` skill dispatcher
- `curik/init_command.py` — init helper functions

Functions in init_command.py:
- `_read_template(name)` — load template from curik/init/ package
- `_update_claude_md(target)` — create/append/replace CLAUDE.md section
- `_write_curik_skill(target)` — install /curik skill
- `_update_vscode_mcp_json(target)` — configure VS Code MCP
- `_update_settings_json(settings_path)` — add mcp__curik__* permission
- `run_init(target)` — orchestrate all init steps

Update pyproject.toml to include `curik.init` package with `*.md` data.

## Acceptance Criteria

- [ ] `curik/init/__init__.py` exists
- [ ] `curik/init/claude-section.md` has CURIK:START/END markers and describes Hugo conventions
- [ ] `curik/init/curik-skill.md` defines a /curik slash command
- [ ] `curik/init_command.py` implements all helper functions
- [ ] `pyproject.toml` includes `curik.init` in packages and package-data

## Testing

- **Existing tests to run**: `pytest tests/`
- **New tests to write**: Ticket 003
- **Verification command**: `~/.local/pipx/venvs/curik/bin/python -m pytest tests/`
