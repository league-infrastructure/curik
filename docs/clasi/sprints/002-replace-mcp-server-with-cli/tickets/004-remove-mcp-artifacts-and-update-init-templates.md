---
id: "004"
title: "Remove MCP artifacts and update init templates"
status: done
use-cases: [SUC-002, SUC-006]
depends-on: ["002", "003"]
github-issue: ""
todo: ""
---

# Remove MCP artifacts and update init templates

## Description

With the CLI built (ticket 002) and init system updated (ticket 003), this
ticket performs the final cleanup: delete server.py, remove the mcp dependency,
update the curik entry in .mcp.json, and rewrite the two init template files
that Claude reads in curriculum projects.

This ticket is the "commit point" — after it runs, curik has no MCP dependency
and the documentation in installed curriculum projects describes the CLI.

Tickets 002 and 003 must both be complete before this ticket runs, because:
- server.py must not be deleted until the CLI can replace all its functionality
- The template files describe the CLI commands, which must exist first

## Acceptance Criteria

- [x] `curik/server.py` is deleted; `import curik.server` raises ImportError
- [x] `mcp>=1.0` is removed from `pyproject.toml` dependencies
- [x] The curik entry is removed from `.mcp.json`; the clasi entry is preserved
- [x] `curik/init/claude-section.md` describes CLI commands, not MCP tools
- [x] `curik/init/curik-skill.md` dispatches to `Bash(curik ...)`, not MCP tools
- [x] `uv run pytest` passes with no regressions (test_mcp_server.py was already
  deleted or migrated in ticket 005, so this test file should not be present)

NOTE: ticket 005 (test updates) can run in parallel with this ticket in the
same execution group. The dependency here is on tickets 002 and 003.

## Implementation Plan

### Approach

Four independent changes, in this order to minimize risk:

1. Update init templates first (no test impact)
2. Remove curik from .mcp.json (no test impact)
3. Remove mcp dependency from pyproject.toml (no test impact until import)
4. Delete server.py last (after confirming tests pass without it)

### Files to Delete

**curik/server.py** — delete entirely

Verify before deleting: run `uv run pytest` to confirm all tests pass without
the import. The file should already be thin at this point (ticket 001 made
handlers delegates). Delete it and run tests once more to confirm.

### Files to Modify

**pyproject.toml**
- Remove `"mcp>=1.0"` from the `dependencies` list

**.mcp.json** (project root)
- Remove the `"curik"` key from `"mcpServers"`
- Keep the `"clasi"` key and any other entries unchanged
- If the file only had `"curik"`, the result is `{"mcpServers": {}}` or an
  empty servers dict (do not delete the file)

**curik/init/claude-section.md** — full rewrite

The new file must:
- Keep the `<!-- CURIK:START -->` / `<!-- CURIK:END -->` markers
- Change `## Before You Do Anything` to reference `curik status` and
  `curik phase get` instead of MCP tool calls
- Change `## Rules` to drop the MCP-first rule; replace with CLI-first rule
  explaining that Claude invokes `curik` via Bash
- Replace `## Available MCP Tools` section with `## Available Commands`
  listing the 14 CLI command groups with their key subcommands
- Keep the Hugo Theme and AskUserQuestion rules (still applicable)

**curik/init/curik-skill.md** — full rewrite

The new file must:
- Keep the YAML frontmatter with description
- Change the dispatch table from MCP tool calls to `Bash(curik <group> <subcommand>)` calls
- Update the publish workflow to use `curik publish check`, `curik publish guide`,
  `curik hugo bump-version` instead of MCP tool names
- Remove the reference to "start-curik agent definition" or update it to
  reflect the CLI-based workflow

### Testing Plan

No new unit tests needed for template changes (templates are text files).

After deleting server.py:
- Run `uv run pytest` and confirm all tests pass
- Specifically confirm `tests/test_mcp_server.py` is gone (or was replaced)
- Confirm `tests/test_cli.py` still passes

After removing mcp from pyproject.toml:
- Run `uv run pip install -e .` (or `uv sync`) to confirm the package installs
  without mcp
- Run `uv run pytest` again to confirm no import errors

### Documentation Updates

This ticket IS the documentation update. The init templates are documentation
that gets installed into curriculum projects. Write them carefully — they are
what Claude reads to understand how to use curik.
