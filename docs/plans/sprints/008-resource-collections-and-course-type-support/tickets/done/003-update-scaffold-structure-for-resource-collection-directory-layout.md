---
id: "003"
title: "Update scaffold_structure for resource collection directory layout"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Update scaffold_structure for resource collection directory layout

## Description

Modify `scaffold_structure()` to branch on the project's course type. When the type is `"resource-collection"`, the function must create a `resources/` directory tree instead of the standard `lessons/` tree. Resource collections organize content as reference pages and activity descriptions rather than sequential lessons, so the directory layout must reflect that. Standard courses (`type: "course"`) must continue to produce the existing `lessons/` tree with no changes.

## Acceptance Criteria

- [ ] `scaffold_structure()` reads the course type from `state.json`
- [ ] When type is `"resource-collection"`, scaffolding creates a `resources/` directory tree instead of `lessons/`
- [ ] When type is `"course"` (or missing/default), scaffolding creates the existing `lessons/` directory tree unchanged
- [ ] The `resources/` tree contains appropriate subdirectories for reference material (matching the structure input provided)
- [ ] No changes to the scaffolding behavior for standard courses (backward compatibility)

## Testing

- **Existing tests to run**: `uv run pytest tests/test_project.py` — verify standard course scaffolding is unchanged
- **New tests to write**: Covered by ticket 005 (`tests/test_resource_collection.py`): verify resource-collection scaffolding creates `resources/` paths, verify standard course scaffolding still creates `lessons/` paths
- **Verification command**: `uv run pytest`
