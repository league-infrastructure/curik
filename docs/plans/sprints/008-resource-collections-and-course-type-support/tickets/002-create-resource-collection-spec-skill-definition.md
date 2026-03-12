---
id: "002"
title: "Create resource-collection-spec skill definition"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Create resource-collection-spec skill definition

## Description

Create a new skill definition file at `curik/skills/resource-collection-spec.md` that documents the abbreviated Phase 1 workflow for resource collections. Resource collections skip the pedagogical-model (1b) and alignment-decision (1d) sub-phases because those concepts do not apply to reference material. The skill file must describe the five required sections: course-concept, research-summary, course-structure-outline, assessment-plan, and technical-decisions. This gives designers clear guidance on what to produce and agents a loadable skill via `get_skill_definition("resource-collection-spec")`.

## Acceptance Criteria

- [ ] File `curik/skills/resource-collection-spec.md` exists
- [ ] The skill file documents the abbreviated Phase 1 workflow with exactly 5 required sections: course-concept, research-summary, course-structure-outline, assessment-plan, and technical-decisions
- [ ] The skill file explicitly states that pedagogical-model and alignment-decision are skipped and explains why
- [ ] The skill file is loadable via `get_skill_definition("resource-collection-spec")` without error
- [ ] The skill file follows the same format and conventions as existing skill definitions in `curik/skills/`

## Testing

- **Existing tests to run**: `uv run pytest tests/` — verify no regressions from adding a new skill file
- **New tests to write**: Covered by ticket 005 (`tests/test_resource_collection.py`): verify the file exists and is loadable via the skill loading mechanism
- **Verification command**: `uv run pytest`
