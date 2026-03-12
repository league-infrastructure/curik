---
id: "001"
title: "Rename CURIK_DIR from .curik to .course"
status: todo
use-cases: [SUC-001]
depends-on: []
---

# Rename CURIK_DIR from .curik to .course

## Description

The user guide consistently refers to `.course/` as the hidden directory.
Change `CURIK_DIR` constant from `".curik"` to `".course"` in `project.py`
and update all tests that reference `.curik/`.

## Acceptance Criteria

- [ ] `CURIK_DIR` constant is `".course"`
- [ ] All existing tests pass with `.course/` paths
- [ ] `init_course()` creates `.course/` directory

## Testing

- **Existing tests to run**: All tests (`uv run pytest`)
- **New tests to write**: None — existing tests cover directory creation
- **Verification command**: `uv run pytest`
