---
id: "002"
title: "Add choice menus to all Phase 1 skills"
status: done
use-cases: [SUC-002]
depends-on: []
---

# Add choice menus to all Phase 1 skills

## Description

Add "What next?" numbered choice menus at every stopping point in all
Phase 1 skill and agent files. In guided mode, the user should never
face a blank prompt — every response ends with options.

## Acceptance Criteria

- [x] course-concept.md ends every interaction with choice menus
- [x] pedagogical-model.md has transition menus between all 6 steps
- [x] alignment-decision.md has menus after research summary, alignment options, evaluation, and topic list
- [x] spec-synthesis.md has menus after each drafted section and final review
- [x] curriculum-architect.md has guided mode rule and menu template
- [x] All files include "Guided Mode Rule" section

## Testing

- **Existing tests to run**: `pytest tests/` — all 222 pass (no code changes)
- **New tests to write**: None (markdown-only changes)
- **Verification command**: `.venv/bin/python -m pytest tests/ -q`
