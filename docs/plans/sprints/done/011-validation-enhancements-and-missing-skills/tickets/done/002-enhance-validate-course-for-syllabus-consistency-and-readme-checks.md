---
id: '002'
title: Enhance validate_course for syllabus consistency and README checks
status: done
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Enhance validate_course for syllabus consistency and README checks

## Description

Extend `validate_course()` in `curik/validation.py` to perform additional
checks when the course tier is 3 or 4. Specifically:

1. **Syllabus consistency** -- Add a `validate_syllabus_consistency()` helper
   function that cross-references `syllabus.yaml` entries against the MkDocs
   `nav` pages configuration. It should report entries present in one but
   missing from the other, catching drift between the syllabus and the site
   navigation.

2. **README existence** -- For Tier 3-4 courses, verify that README files exist
   in the expected repo-root mirror directories. Missing READMEs indicate that
   the lesson content has not been generated or synced to the student-facing
   repository structure.

`validate_course()` should call `validate_syllabus_consistency()` and the
README-exists check only when the tier is 3 or 4. When tier is `None`, 1, or 2,
course validation behaves exactly as before.

## Acceptance Criteria

- [ ] `validate_course()` accepts an optional `tier` parameter that defaults to `None`
- [ ] A new `validate_syllabus_consistency()` helper function exists in `curik/validation.py`
- [ ] `validate_syllabus_consistency()` detects entries in `syllabus.yaml` that are missing from MkDocs `nav` pages
- [ ] `validate_syllabus_consistency()` detects entries in MkDocs `nav` pages that are missing from `syllabus.yaml`
- [ ] For Tier 3-4 courses, `validate_course()` calls `validate_syllabus_consistency()` and reports mismatches
- [ ] For Tier 3-4 courses, `validate_course()` checks that README files exist in repo-root mirror directories
- [ ] Missing README files are reported with descriptive error messages including the expected path
- [ ] When `tier` is `None`, 1, or 2, the syllabus consistency and README checks do not run
- [ ] Existing calls to `validate_course()` without the `tier` argument continue to work identically

## Testing

- **Existing tests to run**: `uv run pytest tests/test_validation.py` to verify no regressions in current course validation
- **New tests to write**: Covered by Ticket 006 in `tests/test_validation_enhanced.py` -- syllabus/MkDocs mismatch detection, README presence/absence in mirror dirs, no-op at tier 1-2
- **Verification command**: `uv run pytest tests/ -v`
