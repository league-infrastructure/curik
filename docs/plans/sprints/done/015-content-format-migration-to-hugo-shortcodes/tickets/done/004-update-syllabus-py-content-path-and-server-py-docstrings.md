---
id: "004"
title: "Update syllabus.py content path and server.py docstrings"
status: todo
use-cases: [SUC-002]
depends-on: ["002"]
---

# Update syllabus.py content path and server.py docstrings

## Description

Update validate_syllabus_consistency() to scan `content/` instead of `docs/docs/`.
Update server.py docstring to reference shortcodes. Verify no remaining MkDocs
references in Python source.

## Acceptance Criteria

- [ ] syllabus.py scans content/ not docs/docs/
- [ ] server.py docstring references shortcodes
- [ ] No remaining "docs/docs" or "mkdocs" references in Python source
- [ ] Tests pass

## Testing

- **Existing tests to run**: full suite
- **New tests to write**: none
- **Verification command**: `python3 -m pytest tests/ -v`
