---
status: complete
---

# Architecture

## Architecture Overview

Curik is a Python CLI + MCP server that manages curriculum development projects.
It provides file-based state tracking, scaffolding, validation, and change
management tools orchestrated by AI agents via the MCP protocol.

## Technology Stack

- Python 3.12+, setuptools packaging
- MCP SDK (FastMCP, stdio transport)
- jtl-syllabus for syllabus management
- PyYAML for frontmatter parsing

## Component Design

### Component: project (project.py)

**Purpose**: Core state management — init, phase tracking, spec management.

**Boundary**: Owns `.course/` directory, state.json, spec.md.

**Use Cases**: SUC-001, SUC-003

### Component: migrate (migrate.py)

**Purpose**: Inventory existing repos and migrate/sequester content.

**Boundary**: Read-only analysis + file moves for sequestering.

**Use Cases**: SUC-002

### Component: cli (cli.py)

**Purpose**: CLI entry point for `curik` command.

**Boundary**: Argument parsing, human-readable output.

**Use Cases**: SUC-001

### Component: server (server.py)

**Purpose**: MCP tool wrappers exposing all Curik functions to agents.

**Boundary**: Thin wrappers, JSON serialization.

**Use Cases**: SUC-001, SUC-002, SUC-003, SUC-004

### Component: agents (curik/agents/*.md)

**Purpose**: Agent definitions guiding AI behavior.

**Boundary**: Markdown instruction files, no code.

**Use Cases**: SUC-004

## Data Model

State file (`.course/state.json`):
```json
{
  "phase": "phase1",
  "sub_phase": "1a",
  "type": "course"
}
```

## Security Considerations

No authentication — local CLI tool. File operations restricted to project root.

## Design Rationale

**Rename `.curik` → `.course`**: The user guide uses `.course/` consistently.
Since the tool is pre-release with no deployed projects, this is a clean rename
with no migration concerns.

**Sub-phase tracking**: Adding `sub_phase` to state.json is minimally invasive.
Existing projects without the field default to `"1a"` for backward compatibility.

**Sequester vs delete**: Moving to `_old/` preserves content for reference,
matching the user guide's "nothing is deleted" promise.

## Sprint Changes

### Changed Components

- **project.py**: `CURIK_DIR = ".course"`, sub-phase tracking in state
- **migrate.py**: New `sequester_content()` function
- **cli.py**: Enhanced init output message
- **server.py**: New MCP tools for sequester and sub-phase
- **agents/start-curik.md**: New agent definition
- **All tests**: Updated for `.course/` directory name

### Migration Concerns

Breaking change: `.curik/` → `.course/`. Acceptable for pre-release.
