---
id: "005"
title: "Update server.py docstrings and add get_reference tool"
status: todo
use-cases: [SUC-001, SUC-002, SUC-003]
depends-on: ["001", "002", "003", "004"]
---

# Update server.py docstrings and add get_reference tool

## Description

Update all MCP tool docstrings in `server.py` that reference MkDocs.
Add `tool_list_references()` and `tool_get_reference()` MCP tools.
Update imports for the new Hugo config function.

## Acceptance Criteria

- [ ] No references to "mkdocs"/"MkDocs" in `server.py` docstrings
- [ ] `tool_list_references()` MCP tool works
- [ ] `tool_get_reference(name)` MCP tool returns content
- [ ] Imports updated (no `get_mkdocs_yml`)
- [ ] All existing MCP tools still work
- [ ] Tests pass

## Testing

- **Existing tests to run**: full suite
- **New tests to write**: none (thin wrappers; functions tested in ticket 004)
- **Verification command**: `uv run pytest`
