---
status: done
sprint: '002'
tickets:
- 002-001
---

# Replace MCP server with CLI

Rewrite curik/cli.py to expose all ~44 remaining MCP tools as CLI
subcommands using argparse with nested command groups: phase, spec,
config, scaffold, issue, plan, migrate, validate, syllabus, hugo,
readme, publish.

## Extract inline business logic from server.py

Four functions in server.py contain logic not in domain modules:

- `tool_update_course_yml` (YAML merge logic) → extract to project.py
- `tool_hugo_setup` (course.yml reading) → extract to templates.py
- `tool_get_publish_guide` + `_read_publish_state` + `tool_check_publish_ready` → new publish.py
- `COURSE_YML_REQUIRED_FIELDS` + `_is_tbd()` → move to project.py

## Build CLI

- Rewrite cli.py with full command tree (~44 subcommands in 12 groups)
- Shared helpers: `--path`, `--json`, JSON input via positional/--file/stdin
- Each handler is a thin wrapper calling the domain function

## Remove MCP

- Delete server.py
- Remove `mcp>=1.0` from pyproject.toml dependencies
- Remove curik entry from .mcp.json (keep clasi)

## Update init system

- init_command.py: remove MCP_CONFIG, VSCODE_MCP_CONFIG, _update_vscode_mcp_json()
- init_command.py: change permission from mcp__curik__* to Bash(curik *)
- init_command.py: stop creating .vscode/mcp.json curik entry
- project.py init_course(): stop writing curik entry to .mcp.json

## Update templates

- curik/init/claude-section.md: rewrite for CLI commands
- curik/init/curik-skill.md: rewrite for CLI commands
- Update bundled agent/skill/reference markdown if they reference MCP tools
