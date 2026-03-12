---
id: "005"
title: "Tests for all resource collection type support"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Tests for all resource collection type support

## Description

Write a comprehensive test file at `tests/test_resource_collection.py` covering all resource-collection behavior introduced in this sprint. This is the single test file for the feature and must exercise init, advance_phase, scaffold_structure, the server tool, and skill file loading. The tests validate both the new resource-collection path and backward compatibility with standard courses.

## Acceptance Criteria

- [ ] `tests/test_resource_collection.py` exists and is discoverable by pytest
- [ ] Test: `init_course()` with default `course_type` sets `type: "course"` in `state.json` and `course.yml`
- [ ] Test: `init_course(course_type="resource-collection")` sets `type: "resource-collection"` in `state.json` and `course.yml`
- [ ] Test: loading a legacy `state.json` without a `type` field defaults to `"course"`
- [ ] Test: `advance_phase("phase2")` succeeds for a resource collection with only the 5 required sections filled in
- [ ] Test: `advance_phase("phase2")` fails for a resource collection when a required section (e.g., course-concept) is missing
- [ ] Test: `advance_phase("phase2")` still requires all 7 sections for a standard course
- [ ] Test: `scaffold_structure()` creates `resources/` directories for a resource collection
- [ ] Test: `scaffold_structure()` creates `lessons/` directories for a standard course
- [ ] Test: `tool_init_course()` accepts and forwards the `course_type` parameter
- [ ] Test: `curik/skills/resource-collection-spec.md` exists and is loadable
- [ ] All tests pass with `uv run pytest tests/test_resource_collection.py`

## Testing

- **Existing tests to run**: `uv run pytest tests/test_project.py` — confirm existing tests still pass alongside new test file
- **New tests to write**: This ticket IS the test ticket. All tests are written in `tests/test_resource_collection.py` as listed in the acceptance criteria above
- **Verification command**: `uv run pytest tests/test_resource_collection.py -v`
