---
id: "001"
title: "Fix scaffold_structure to place content under content/ and create content/_index.md"
status: todo
use-cases: [SUC-001]
depends-on: []
---

# Fix scaffold_structure to place content under content/ and create content/_index.md

## Description

Update `scaffold_structure()` in `curik/scaffolding.py` to create module
directories under `content/` instead of the repo root (line 57:
`root / mod_name` → `root / "content" / mod_name`). Also create
`content/_index.md` as the Hugo site landing page before the module loop.

Update `create_lesson_stub()` (line 173: `root / module` →
`root / "content" / module`) for consistency.

Update all existing unit tests in `tests/test_scaffolding.py` that assert
on paths without the `content/` prefix (~15+ assertions across
ScaffoldStructureTest, ScaffoldTierMirrorTest, ScaffoldDevcontainerTest,
LessonStubTest).

## Acceptance Criteria

- [ ] `scaffold_structure()` creates modules under `content/`, not repo root
- [ ] `content/_index.md` is created with course title frontmatter
- [ ] `create_lesson_stub()` creates lessons under `content/`
- [ ] Resource collections still go under `resources/` (unchanged)
- [ ] All existing unit tests updated and passing

## Testing

- **Existing tests to run**: `tests/test_scaffolding.py`
- **New tests to write**: None (existing tests updated to verify new paths)
- **Verification command**: `python3 -m pytest tests/test_scaffolding.py -v`
