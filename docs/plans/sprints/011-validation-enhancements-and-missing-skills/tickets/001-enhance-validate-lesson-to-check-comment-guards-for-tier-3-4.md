---
id: "001"
title: "Enhance validate_lesson to check comment guards for Tier 3-4"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Enhance validate_lesson to check comment guards for Tier 3-4

## Description

Add an optional `tier` parameter (default `None`) to `validate_lesson()` in
`curik/validation.py`. When `tier` is 3 or 4, the function must perform two
additional checks beyond the existing validation logic:

1. **Comment guard check** -- Verify that the lesson Markdown file contains at
   least one `<!-- readme-shared -->` comment guard. These guards mark the
   boundary between student-facing content (shared with the generated README)
   and instructor-only content. Without them, README generation produces
   incomplete or incorrect output.

2. **Syllabus UID check** -- Verify that the lesson's UID appears in the
   course's `syllabus.yaml`. This catches drift between the syllabus and the
   file tree that currently goes unnoticed.

When `tier` is `None`, 1, or 2, these additional checks must not run, preserving
full backward compatibility with existing callers.

## Acceptance Criteria

- [ ] `validate_lesson()` accepts an optional `tier` parameter that defaults to `None`
- [ ] When `tier=3` or `tier=4`, the function checks for the presence of `<!-- readme-shared -->` in the lesson file
- [ ] A Tier 3-4 lesson missing the comment guard returns `valid: False` with a descriptive error message mentioning the missing guard
- [ ] A Tier 3-4 lesson containing the comment guard passes the guard check
- [ ] When `tier=3` or `tier=4`, the function verifies the lesson UID exists in `syllabus.yaml`
- [ ] A Tier 3-4 lesson whose UID is absent from `syllabus.yaml` returns `valid: False` with a descriptive error
- [ ] A Tier 3-4 lesson whose UID is present in `syllabus.yaml` passes the UID check
- [ ] When `tier` is `None`, 1, or 2, neither the guard check nor the syllabus UID check runs
- [ ] Existing calls to `validate_lesson()` without the `tier` argument continue to work identically

## Testing

- **Existing tests to run**: `uv run pytest tests/test_validation.py` to verify no regressions in current lesson validation
- **New tests to write**: Covered by Ticket 006 in `tests/test_validation_enhanced.py` -- comment guard presence/absence at tier 3, syllabus UID presence/absence at tier 3, no-op at tier 1-2 and tier None
- **Verification command**: `uv run pytest tests/ -v`
