---
id: "003"
title: "Add sub-phase tracking for Phase 1"
status: todo
use-cases: [SUC-003]
depends-on: ["001"]
---

# Add sub-phase tracking for Phase 1

## Description

Add `sub_phase` field to state.json (values: "1a", "1b", "1c", "1d", "1e").
Add `advance_sub_phase()` function that moves to the next sub-phase.
Update `get_phase()` to return the sub_phase. Update `init_course()` to
set initial sub_phase to "1a". Add `tool_advance_sub_phase` MCP tool.

Sub-phase sequence: 1a (concept) → 1b (pedagogical) → 1c (research) →
1d (alignment) → 1e (synthesis). After 1e, `advance_phase("phase2")`
is used as before.

For resource-collections, 1b and 1d are skipped (1a → 1c → 1e).

## Acceptance Criteria

- [ ] `init_course()` sets `sub_phase: "1a"` in state.json
- [ ] `get_phase()` returns `sub_phase` field
- [ ] `advance_sub_phase()` advances correctly for both course types
- [ ] Resource collections skip 1b and 1d
- [ ] Cannot advance past 1e (use `advance_phase` for that)
- [ ] MCP tool wrapper exists

## Testing

- **Existing tests to run**: `uv run pytest tests/test_project.py`
- **New tests to write**: Sub-phase advancement tests in `tests/test_sub_phases.py`
- **Verification command**: `uv run pytest`
