---
id: "001"
title: "Add get_course_status to project module"
status: todo
use-cases:
  - SUC-003
depends-on: []
---

# Add get_course_status to project module

## Description

Add a `get_course_status()` function to `curik/project.py` that reads
`state.json` and returns a summary: current phase, open issues count,
active change plans. Export it from `curik/__init__.py`.

## Acceptance Criteria

- [ ] `get_course_status(path)` returns dict with phase, open issues count, active change plans count
- [ ] Returns meaningful error if `.course/` doesn't exist
- [ ] Exported from `curik/__init__.py`
- [ ] Unit test in `test_project.py`

## Testing

- **Existing tests to run**: `python -m pytest tests/test_project.py`
- **New tests to write**: `test_get_course_status` — init a course, check status returns phase1 and zero counts
- **Verification command**: `python -m pytest`
