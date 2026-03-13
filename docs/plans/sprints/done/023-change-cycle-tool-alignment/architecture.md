---
status: draft
---

# Architecture

## Architecture Overview

Curik is a Python MCP server for curriculum development. This sprint adds
`register_change_plan()` and integration tests for the change cycle.

## Component Design

### Component: register_change_plan (new)

**Purpose**: Index an agent-written change plan file.

**Location**: `curik/changes.py` + `curik/server.py`

The function reads `change-plan/active/NNN-*.md`, validates:
- File exists
- Has YAML frontmatter with title and status fields
- Status is "draft"

Then updates the plan's frontmatter to confirm registration.

## Sprint Changes

### New Components
- `register_change_plan()` in changes.py
- `tool_register_change_plan()` in server.py
- Integration test for full change cycle

### Changed Components
- `changes.py` — new function added
- `server.py` — new tool registration
