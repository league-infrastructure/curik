---
id: '002'
title: Integrate init_command into curik init and update MCP instructions
status: done
use-cases:
- SUC-001
- SUC-002
depends-on:
- '001'
---

# Integrate init_command into curik init and update MCP instructions

## Description

Wire init_command.run_init() into project.py's init_course() so that
`curik init` creates all new files. Update cli.py output messaging.
Update server.py MCP instructions to describe Hugo conventions.

Changes:
- `project.py`: import and call `run_init()` from init_command, merge results
- `cli.py`: print detailed init results
- `server.py`: replace `instructions="Curik curriculum development tool"`
  with descriptive Hugo/curriculum instructions

## Acceptance Criteria

- [ ] `init_course()` calls `run_init()` and merges file lists
- [ ] CLI prints status for each init artifact (created/updated/unchanged)
- [ ] MCP server `instructions` describes Hugo, shortcodes, content dir, and tools
- [ ] All existing tests pass

## Testing

- **Existing tests to run**: `pytest tests/test_project.py tests/test_cli.py`
- **New tests to write**: Covered by Ticket 003
- **Verification command**: `~/.local/pipx/venvs/curik/bin/python -m pytest tests/`
