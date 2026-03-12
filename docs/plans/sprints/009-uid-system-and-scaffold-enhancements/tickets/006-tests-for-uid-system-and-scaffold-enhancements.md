---
id: "006"
title: "Tests for UID system and scaffold enhancements"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Tests for UID system and scaffold enhancements

## Description

Write comprehensive unit and integration tests covering all Sprint 009 changes.
This ticket consolidates the test effort to ensure full coverage of the UID
system and all scaffold enhancements. Tests validate both new functionality and
backward compatibility of modified functions.

Test files and coverage areas:

- **`tests/test_uid.py`** (new): Tests for `generate_course_uid()` (UUID4
  validity, string format) and `generate_unit_uid()` (8-char length, base62
  charset, uniqueness over 10,000 calls).
- **`tests/test_scaffolding.py`** (expanded): Tests for UID frontmatter
  injection in `create_lesson_stub` (with and without `uid` param), `course.yml`
  UID field from `init_course`, Tier 3-4 mirror directory creation (`lessons/`,
  `projects/`), Tier 1-2 unchanged behavior, `.devcontainer/devcontainer.json`
  generation for Tier 3-4, `generate_nav()` output structure, `get_mkdocs_yml()`
  with and without `nav` param.
- **Integration test**: End-to-end `init_course` followed by
  `scaffold_structure` for a Tier 3 course produces a complete directory tree
  with UIDs in frontmatter, mirror directories, devcontainer config, and
  explicit nav in `mkdocs.yml`.

## Acceptance Criteria

- [ ] `tests/test_uid.py` exists with tests for `generate_course_uid` UUID4 validity
- [ ] `tests/test_uid.py` includes tests for `generate_unit_uid` length, charset, and uniqueness (10,000 calls)
- [ ] `tests/test_scaffolding.py` includes tests for `create_lesson_stub` with `uid` parameter (frontmatter present)
- [ ] `tests/test_scaffolding.py` includes tests for `create_lesson_stub` without `uid` (no frontmatter, backward compatible)
- [ ] `tests/test_scaffolding.py` includes tests for `course.yml` containing a UUID4 `uid` field after `init_course`
- [ ] `tests/test_scaffolding.py` includes tests for Tier 3 mirror directories (`lessons/`, `projects/`) existence
- [ ] `tests/test_scaffolding.py` includes tests for Tier 1 courses having no mirror directories
- [ ] `tests/test_scaffolding.py` includes tests for `.devcontainer/devcontainer.json` generation on Tier 3-4
- [ ] `tests/test_scaffolding.py` includes tests for `generate_nav` returning correct MkDocs nav structure
- [ ] `tests/test_scaffolding.py` includes tests for `get_mkdocs_yml` with and without `nav` parameter
- [ ] An integration test verifies end-to-end Tier 3 scaffolding produces UIDs, mirror dirs, devcontainer, and nav
- [ ] All tests pass: `uv run pytest` exits with code 0

## Testing

- **Existing tests to run**: `uv run pytest tests/` -- full suite must pass
- **New tests to write**: `tests/test_uid.py` (new file), expanded `tests/test_scaffolding.py`
- **Verification command**: `uv run pytest tests/ -v --tb=short`
