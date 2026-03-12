---
id: "002"
title: "Implement MCP server with Phase 1 tools"
status: todo
use-cases:
  - SUC-001
  - SUC-002
  - SUC-003
depends-on:
  - "001"
---

# Implement MCP server with Phase 1 tools

## Description

Create `curik/server.py` implementing an MCP server using the Python MCP SDK
with stdio transport. Register 9 tools that delegate to `curik.project`:
`init_course`, `get_phase`, `advance_phase`, `get_spec`, `update_spec`,
`record_course_concept`, `record_pedagogical_model`, `record_alignment`,
`get_course_status`. Add `mcp` to `pyproject.toml` dependencies and bump
version to 0.2.0.

## Acceptance Criteria

- [ ] `curik/server.py` exists with all 9 tools registered
- [ ] Each tool has name, description, and input schema
- [ ] Tools delegate to `curik.project` — no business logic in server
- [ ] `CurikError` mapped to MCP error responses
- [ ] Unexpected exceptions caught with generic error response
- [ ] `mcp` added to `pyproject.toml` dependencies
- [ ] Version bumped to 0.2.0 in `pyproject.toml`

## Testing

- **Existing tests to run**: `python -m pytest tests/test_project.py`
- **New tests to write**: Covered by ticket 004
- **Verification command**: `python -m pytest`
