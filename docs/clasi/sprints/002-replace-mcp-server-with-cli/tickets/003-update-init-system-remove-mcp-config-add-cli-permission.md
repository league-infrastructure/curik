---
id: "003"
title: "Update init system (remove MCP config, add CLI permission)"
status: done
use-cases: [SUC-002]
depends-on: ["001"]
github-issue: ""
todo: ""
---

# Update init system (remove MCP config, add CLI permission)

## Description

When a developer runs `curik init`, the tool currently installs:
- An MCP config entry for the curik server in .mcp.json
- An MCP permission `mcp__curik__*` in .claude/settings.local.json
- A VS Code MCP config in .vscode/mcp.json

After this sprint, curik is a CLI, not an MCP server. `curik init` must instead:
- Install `Bash(curik *)` permission in .claude/settings.local.json
- Not write any curik MCP entries

This ticket makes those changes without touching the CLI or templates (those
are handled in tickets 002 and 004). The only files changed here are
`init_command.py` and `project.py`.

Ticket 001 must be complete first since init_course() in project.py will need
to work cleanly without writing MCP config.

## Acceptance Criteria

- [x] `curik init` writes `Bash(curik *)` to .claude/settings.local.json allow list
- [x] `curik init` does NOT write `mcp__curik__*` to .claude/settings.local.json
- [x] `curik init` does NOT write a curik entry to .vscode/mcp.json
- [x] `curik init` does NOT write a curik entry to .mcp.json (neither creates nor modifies)
- [x] Re-running `curik init` on a project that has old MCP permission does not re-add it
- [x] `uv run pytest` passes with no regressions

## Implementation Plan

### Approach

Make targeted changes to `init_command.py` and `project.py`. Remove MCP
infrastructure. Change the permission string. Leave all other init behavior
(CLAUDE.md, gitignore, GitHub workflow, course.yml, spec.md) untouched.

### Files to Modify

**curik/init_command.py**

1. Remove the `MCP_CONFIG` constant (lines 17-21).
2. Remove the `VSCODE_MCP_CONFIG` constant (lines 23-29).
3. Remove the `_update_vscode_mcp_json()` function (lines 88-114).
4. In `_update_settings_json()`: change the target permission from
   `"mcp__curik__*"` to `"Bash(curik *)"`.
   - Also update the existing-check: look for `"Bash(curik *)"` in the allow
     list, not `"mcp__curik__*"`.
   - If the old `"mcp__curik__*"` is present in the allow list, remove it and
     add `"Bash(curik *)"` instead (migration: re-running init on old projects
     upgrades the permission).
5. In `run_init()`: remove the `.vscode/mcp.json` entry from the `actions`
   list. The remaining actions are: CLAUDE.md, .claude/skills/curik/SKILL.md,
   .claude/settings.local.json, .gitignore, .github/workflows/deploy-pages.yml.

**curik/project.py** — `init_course()`

Remove the block at lines 212-227 that writes .mcp.json with the curik server
entry. Specifically:
- Remove the `mcp_json_path` variable declaration
- Remove the `mcp_json_content` JSON string
- Remove the `rel_mcp` computation
- Remove the if/else block that writes or verifies .mcp.json

The .mcp.json file (which may still contain a clasi entry) must not be touched
by `init_course()`.

### Testing Plan

Existing tests to update: `tests/test_init_command.py` — update assertions:
- Remove any assertion that `.vscode/mcp.json` is created
- Remove any assertion that `mcp__curik__*` is in the settings
- Add assertion that `Bash(curik *)` is in the settings allow list
- Add test: if old `mcp__curik__*` permission exists, re-running init replaces
  it with `Bash(curik *)`

Existing tests to run unchanged:
- `tests/test_project.py` — init_course tests that check .course/ creation,
  course.yml, spec.md, state.json must all still pass
- `tests/test_mcp_server.py` — still passes because server.py is not touched here

New tests to add:
- `test_run_init_no_vscode_mcp_json`: assert .vscode/mcp.json not created
- `test_run_init_bash_permission`: assert `Bash(curik *)` in allow list
- `test_init_course_no_mcp_json`: assert init_course does not create .mcp.json
- `test_init_course_existing_mcp_json_untouched`: create .mcp.json with clasi
  entry, run init_course, assert clasi entry still there and no curik entry added

### Documentation Updates

No documentation changes in this ticket. Template files are updated in ticket 004.
