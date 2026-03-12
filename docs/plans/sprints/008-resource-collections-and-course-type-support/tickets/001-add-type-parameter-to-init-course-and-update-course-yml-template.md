---
id: "001"
title: "Add type parameter to init_course and update course.yml template"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Add type parameter to init_course and update course.yml template

## Description

Add a `course_type` parameter (default `"course"`) to `init_course()` and `tool_init_course()`. When a project is initialized, the selected type must be stored in both `state.json` (as `"type"`) and `course.yml` (as `type:`). Existing projects that lack a `type` field must default to `"course"` so backward compatibility is preserved. This is the foundation for resource-collection support: every downstream change (phase gating, scaffolding) reads the type set here.

## Acceptance Criteria

- [ ] `init_course()` accepts an optional `course_type` parameter with allowed values `"course"` and `"resource-collection"`, defaulting to `"course"`
- [ ] `tool_init_course()` accepts and forwards the `course_type` parameter to `init_course()`
- [ ] After initialization with `course_type="resource-collection"`, `state.json` contains `"type": "resource-collection"`
- [ ] After initialization with `course_type="resource-collection"`, `course.yml` contains `type: resource-collection`
- [ ] After initialization with no `course_type` argument (or `course_type="course"`), both files contain `type: course`
- [ ] Loading a legacy project whose `state.json` has no `type` field treats the type as `"course"` without error
- [ ] All existing tests in `tests/test_project.py` continue to pass without modification

## Testing

- **Existing tests to run**: `uv run pytest tests/test_project.py` — verify no regressions in init, phase advancement, or state loading
- **New tests to write**: Covered by ticket 005 (`tests/test_resource_collection.py`): init with default type, init with explicit `"resource-collection"`, legacy state without type field, server tool parameter forwarding
- **Verification command**: `uv run pytest`
