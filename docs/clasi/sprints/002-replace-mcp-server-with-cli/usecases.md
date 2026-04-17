---
status: draft
---

# Sprint 002 Use Cases

## SUC-001: Claude invokes curik domain operations via Bash

- **Actor**: Claude Code (agent)
- **Preconditions**: curik is installed; Claude Code has `Bash(curik *)` permission
- **Main Flow**:
  1. Claude runs `curik <group> <subcommand> [args] [--path .] [--json]`
  2. CLI parses arguments, resolves the project root, calls the domain function
  3. CLI prints output (human-readable or JSON) to stdout
  4. Claude reads stdout and continues with the result
- **Postconditions**: Domain operation completed; result available to Claude
- **Acceptance Criteria**:
  - [ ] Every former MCP tool is reachable as a `curik` subcommand
  - [ ] `--json` flag causes machine-parseable JSON output
  - [ ] `--path` resolves the project root on every subcommand
  - [ ] Exit code 0 on success, 1 on error; error message on stderr

## SUC-002: Claude initializes a curriculum project without MCP

- **Actor**: Claude Code (agent)
- **Preconditions**: Empty or existing repository; curik installed
- **Main Flow**:
  1. Claude runs `curik init [--type course|resource-collection] [--path .]`
  2. CLI creates .course/ structure, course.yml, CLAUDE.md section, /curik skill
  3. CLI writes `Bash(curik *)` to .claude/settings.local.json permissions
  4. CLI does not write a curik entry to .mcp.json
- **Postconditions**: Project is ready for curriculum development without MCP
- **Acceptance Criteria**:
  - [ ] `Bash(curik *)` appears in .claude/settings.local.json allow list
  - [ ] No `curik` entry in .mcp.json after init
  - [ ] No .vscode/mcp.json curik entry written
  - [ ] CLAUDE.md describes CLI commands, not MCP tools

## SUC-003: Agent reads and updates course metadata via CLI

- **Actor**: Claude Code (agent)
- **Preconditions**: Project initialized with course.yml present
- **Main Flow**:
  1. Claude runs `curik config update '{"title": "Python Basics"}' --path .`
  2. CLI merges the JSON update into course.yml, preserving other fields
  3. CLI reports updated fields and any still-TBD required fields
- **Postconditions**: course.yml updated; required-field status reported
- **Acceptance Criteria**:
  - [ ] `curik config update` writes merged YAML back to course.yml
  - [ ] Returns list of updated fields and still-TBD fields
  - [ ] Handles JSON input via positional arg, `--file`/`-f`, or stdin

## SUC-004: Agent runs publish readiness check and guide via CLI

- **Actor**: Claude Code (agent)
- **Preconditions**: Project initialized; curik installed
- **Main Flow**:
  1. Claude runs `curik publish check [--path .]`
  2. CLI reads course state, checks all readiness conditions, returns JSON result
  3. Claude runs `curik publish guide [--path .]` for human-readable checklist
- **Postconditions**: Publish readiness status available; guide displayed
- **Acceptance Criteria**:
  - [ ] `curik publish check` returns JSON with per-check pass/fail and overall ready bool
  - [ ] `curik publish guide` returns the full personalized guide as text
  - [ ] Both commands work without the MCP server running

## SUC-005: Domain functions for update_course_yml and publish are importable

- **Actor**: CLI handler (code)
- **Preconditions**: curik package installed
- **Main Flow**:
  1. `from curik.project import update_course_yml` — function exists and works
  2. `from curik.publish import get_publish_guide, check_publish_ready` — module exists
  3. CLI handlers call these functions rather than reimplementing logic
- **Postconditions**: Business logic is in domain modules, not in server.py or cli.py
- **Acceptance Criteria**:
  - [ ] `project.update_course_yml(root, updates)` handles YAML merge and TBD reporting
  - [ ] `project.COURSE_YML_REQUIRED_FIELDS` and `project._is_tbd()` exist in project.py
  - [ ] `templates.hugo_setup_from_course(root)` reads course.yml and calls hugo_setup
  - [ ] `publish.py` contains `_read_publish_state`, `get_publish_guide`, `check_publish_ready`

## SUC-006: curik package has no mcp dependency

- **Actor**: Package consumer (pip install curik)
- **Preconditions**: curik source in pyproject.toml
- **Main Flow**:
  1. `pip install curik` installs the package
  2. No mcp or fastmcp package is pulled in as a dependency
- **Postconditions**: curik is a lighter package with no MCP protocol overhead
- **Acceptance Criteria**:
  - [ ] `mcp>=1.0` is absent from pyproject.toml dependencies
  - [ ] `curik/server.py` is deleted
  - [ ] `import curik.server` raises ImportError
  - [ ] curik entry is removed from `.mcp.json`

## SUC-007: CLI command groups cover all retained MCP tool groups

- **Actor**: Claude Code (agent)
- **Preconditions**: CLI built and installed
- **Main Flow**:
  1. Claude runs `curik --help` to discover available commands
  2. Groups listed: init, status, phase, spec, config, scaffold, issue, plan,
     migrate, validate, syllabus, hugo, readme, publish
  3. Each subcommand runs successfully against a real project
- **Postconditions**: All retained domain operations accessible via CLI
- **Acceptance Criteria**:
  - [ ] `curik phase get` replaces `tool_get_phase`
  - [ ] `curik phase advance TARGET` replaces `tool_advance_phase`
  - [ ] `curik phase advance-sub` replaces `tool_advance_sub_phase`
  - [ ] `curik spec get` replaces `tool_get_spec`
  - [ ] `curik spec update SECTION CONTENT` replaces `tool_update_spec`
  - [ ] `curik spec record-concept` / `record-model` / `record-alignment` replace respective tools
  - [ ] `curik scaffold structure`, `lesson`, `outline`, `approve-outline`, `get-outline`, `change-plan` cover scaffolding group
  - [ ] `curik issue create` / `list` cover issue group
  - [ ] `curik plan create` / `register` / `approve` / `execute` / `review` / `close` cover plan group
  - [ ] `curik migrate inventory` / `sequester` / `structure` cover migration group
  - [ ] `curik validate lesson` / `module` / `course` / `get-report` / `save-report` cover validation
  - [ ] `curik syllabus write-url` / `validate` cover syllabus group
  - [ ] `curik hugo pages` / `create-page` / `update-frontmatter` / `setup` / `bump-version` / `build` cover Hugo group
  - [ ] `curik readme generate` covers readme group
  - [ ] `curik publish guide` / `check` cover publish group
