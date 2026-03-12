---
id: "004"
title: "Update advance_phase to skip gates for resource collections"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Update advance_phase to skip gates for resource collections

## Description

Modify `advance_phase()` to adjust its gate requirements based on the project's course type. For resource collections, the Phase 1-to-Phase 2 gate must only require 5 spec sections: course-concept, research-summary, course-structure-outline, assessment-plan, and technical-decisions. The pedagogical-model and alignment-decision sections must be skipped because they do not apply to reference material. Standard courses must continue to require all 7 sections. The function reads the type from `state.json` and selects the appropriate required-sections list before checking completeness.

## Acceptance Criteria

- [ ] `advance_phase()` reads the course type from `state.json` before evaluating gate requirements
- [ ] For `type: "resource-collection"`, advancement to phase2 requires only 5 sections: course-concept, research-summary, course-structure-outline, assessment-plan, technical-decisions
- [ ] For `type: "resource-collection"`, the pedagogical-model and alignment-decision sections are not checked and may be absent or empty
- [ ] For `type: "course"` (or missing/default), advancement to phase2 still requires all 7 sections including pedagogical-model and alignment-decision
- [ ] `advance_phase()` rejects advancement for a resource collection if any of the 5 required sections are missing
- [ ] Existing phase advancement tests for standard courses continue to pass without modification

## Testing

- **Existing tests to run**: `uv run pytest tests/test_project.py` — verify standard course phase gating is unchanged
- **New tests to write**: Covered by ticket 005 (`tests/test_resource_collection.py`): resource collection advances with 5 sections, resource collection fails with missing required section, standard course still requires all 7 sections
- **Verification command**: `uv run pytest`
