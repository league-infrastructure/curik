---
id: '002'
title: Replace MCP Server with CLI
status: done
branch: sprint/002-replace-mcp-server-with-cli
use-cases:
- SUC-001
- SUC-002
- SUC-003
- SUC-004
- SUC-005
- SUC-006
- SUC-007
todo: replace-mcp-server-with-cli.md
---

# Sprint 002: Replace MCP Server with CLI

## Goals

Replace the curik MCP server entirely with a comprehensive CLI. Claude Code
invokes the CLI via its Bash tool instead of calling MCP tools. This makes
curik a standalone Python package with no MCP dependency.

## Problem

The curik package currently exposes ~44 tools via a FastMCP server
(curik/server.py). This requires the MCP protocol for all interactions:
Claude must have the curik MCP server running, registered in .mcp.json, and
connected before it can do anything. The MCP server also contains inline
business logic (course.yml update, hugo_setup reading, publish state checking)
that belongs in domain modules.

Sprint 001 pruned quiz, research, and assets modules, reducing the server
surface. This sprint completes the migration.

## Solution

1. Extract the four pockets of inline business logic from server.py into
   domain modules (project.py, templates.py, new publish.py).
2. Rewrite cli.py as a full-coverage argparse CLI with ~44 subcommands in
   12 groups, each a thin wrapper over a domain function.
3. Update the init system to install CLI permissions instead of MCP config.
4. Delete server.py, remove the mcp dependency, and update .mcp.json.
5. Update init templates (claude-section.md, curik-skill.md) to describe
   the CLI instead of MCP tools.
6. Update or replace tests that test the MCP server.

## Success Criteria

- `curik --help` lists all 12 command groups
- Every former MCP tool is reachable as a CLI subcommand
- `curik init` installs `Bash(curik *)` permission instead of `mcp__curik__*`
- `curik init` does not write a curik entry to .mcp.json
- server.py is deleted; `mcp>=1.0` is not in pyproject.toml
- All existing tests pass; new CLI tests cover each command group
- claude-section.md and curik-skill.md describe CLI commands

## Scope

### In Scope

- Extract `tool_update_course_yml` YAML merge logic → `project.update_course_yml()`
- Extract `COURSE_YML_REQUIRED_FIELDS` + `_is_tbd()` → project.py
- Extract `tool_hugo_setup` course.yml reading → templates.py wrapper
- Extract `_read_publish_state`, `tool_get_publish_guide`, `tool_check_publish_ready` → new `curik/publish.py`
- Rewrite `curik/cli.py` with all 12 command groups (~44 subcommands)
- JSON input helper: positional arg, `--file`/`-f`, or stdin
- `--json` flag for machine-parseable output on all appropriate subcommands
- `--path` on every subcommand, default `.`
- Update `curik/init_command.py`: remove MCP_CONFIG, VSCODE_MCP_CONFIG, `_update_vscode_mcp_json()`; change permission from `mcp__curik__*` to `Bash(curik *)`
- Update `curik/project.py` `init_course()`: stop writing curik entry to .mcp.json
- Rewrite `curik/init/claude-section.md` for CLI commands
- Rewrite `curik/init/curik-skill.md` for CLI commands
- Delete `curik/server.py`
- Remove `mcp>=1.0` from `pyproject.toml`
- Remove curik entry from `.mcp.json` (keep clasi)
- Update `tests/test_mcp_server.py`: migrate surviving tests to CLI; delete file when done
- Update `tests/test_cli.py`: add tests for new command groups
- Update `tests/test_init_command.py`: remove MCP-config assertions

### Out of Scope

- `curik research save` / `curik research list` — removed in sprint 001
- `curik spec update-spec` taking `--file` input for reading existing spec — future sprint
- Publishing to PyPI or distributing the CLI binary
- Changes to domain logic beyond what is needed to expose functions to the CLI

## Test Strategy

- Unit tests for each new domain function extracted in ticket 001
- CLI handler tests for every command group using subprocess or direct `main()` calls
- Existing passing tests must continue to pass
- `test_mcp_server.py` is migrated or deleted — no MCP-dependent tests remain at sprint end

## Architecture Notes

- Keep argparse. No new framework dependency.
- cli.py mirrors server.py's role: thin wrapper over domain modules.
- JSON input precedence: positional arg → `--file`/`-f` → stdin.
- `publish.py` is a new module. It depends on project.py and hugo.py but
  nothing in publish.py may depend on server.py.
- `_read_publish_state` is a private helper inside publish.py, not exported.

## GitHub Issues

None.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

| # | Title | Depends On | Group |
|---|-------|------------|-------|
| 001 | Extract inline business logic from server.py | — | 1 |
| 002 | Build new CLI (cli.py rewrite) | 001 | 2 |
| 003 | Update init system | 001 | 2 |
| 004 | Remove MCP artifacts and update templates | 002, 003 | 3 |
| 005 | Update tests | 002, 003 | 3 |

**Groups**: Tickets in the same group can execute in parallel.
Groups execute sequentially (1 before 2, etc.).
