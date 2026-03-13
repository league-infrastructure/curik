---
id: "004"
title: "Add brand guide as packaged MCP reference resource"
status: todo
use-cases: [SUC-003]
depends-on: []
---

# Add brand guide as packaged MCP reference resource

## Description

Package the League web brand guide as a reference doc inside the curik
package. Add `get_reference()` and `list_references()` to `assets.py`
following the existing agents/skills pattern. Create `curik/references/`
as a proper Python package.

## Acceptance Criteria

- [ ] `curik/references/__init__.py` exists (empty)
- [ ] `curik/references/league-web-brand-guide.md` has full brand guide content
- [ ] `list_references()` returns `["league-web-brand-guide"]`
- [ ] `get_reference("league-web-brand-guide")` returns markdown content
- [ ] `get_reference("nonexistent")` raises appropriate error
- [ ] `pyproject.toml` includes `curik.references` in packages
- [ ] Tests pass

## Testing

- **Existing tests to run**: full suite (no regressions)
- **New tests to write**: `test_list_references`, `test_get_reference`,
  `test_get_reference_not_found`
- **Verification command**: `uv run pytest`
