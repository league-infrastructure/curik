---
id: "002"
title: "Add sequester_content function and MCP tool"
status: todo
use-cases: [SUC-002]
depends-on: ["001"]
---

# Add sequester_content function and MCP tool

## Description

Add `sequester_content()` to `migrate.py` that moves all non-Curik files
in the repo root to `_old/`, preserving directory structure. Protected
paths (`.course/`, `.git/`, `.mcp.json`, `course.yml`, `_old/`) are not moved.
Expose as `tool_sequester_content` MCP tool in `server.py`.

## Acceptance Criteria

- [ ] `sequester_content()` moves files/dirs to `_old/`
- [ ] Protected paths are never moved
- [ ] Returns `{"moved": [...], "protected": [...]}`
- [ ] MCP tool wrapper exists in server.py
- [ ] Tests cover: empty repo, repo with files, protected paths, idempotent call

## Testing

- **Existing tests to run**: `uv run pytest tests/test_migrate.py`
- **New tests to write**: `tests/test_sequester.py`
- **Verification command**: `uv run pytest`
