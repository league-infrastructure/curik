---
id: "003"
title: "Update scaffolding.py for _index.md and nav weight assignments"
status: done
use-cases: [SUC-001]
depends-on: ["001"]
---

# Update scaffolding.py for _index.md and nav weight assignments

## Description

Update `scaffold_structure()` to create `_index.md` branch bundle files
in module directories (Hugo requires these for section pages). Update
`generate_nav()` to return weight assignments instead of MkDocs nav dicts.

## Acceptance Criteria

- [x] `scaffold_structure()` creates `_index.md` in each module directory
- [x] `_index.md` contains module title as H1 heading
- [x] `generate_nav()` returns weight assignment dicts (not MkDocs nav)
- [x] Weight values are sequential (10, 20, 30...) for reordering room
- [x] Tests updated and passing

## Testing

- **Existing tests to run**: `tests/test_scaffolding.py`
- **New tests to write**: `test_scaffold_creates_index_md`,
  `test_generate_nav_weights`
- **Verification command**: `uv run pytest tests/test_scaffolding.py`
