---
id: '006'
title: Tests for enhanced validation and skill loading
status: done
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Tests for enhanced validation and skill loading

## Description

Create `tests/test_validation_enhanced.py` containing comprehensive unit tests
for all new validation behavior introduced by Tickets 001-005. This test file
ensures that the tier-aware validation logic, syllabus consistency checks, README
existence checks, and skill file loading all work correctly. It also includes
backward compatibility tests that confirm existing validation calls without the
`tier` parameter continue to behave identically.

This ticket depends on Tickets 001-005 being complete, as it tests their
implementations.

## Acceptance Criteria

- [ ] `tests/test_validation_enhanced.py` exists and is discoverable by pytest
- [ ] Comment guard tests: temp lesson files with and without `<!-- readme-shared -->` guards are validated at tier 3 (fail/pass) and tier 2 (no-op)
- [ ] Syllabus UID tests: temp course with `syllabus.yaml` validates lesson UID presence at tier 3 (pass when present, fail when absent)
- [ ] Syllabus consistency tests: temp course with matching and mismatched `syllabus.yaml`/`mkdocs.yml` entries verifies `validate_course()` reports mismatches
- [ ] README existence tests: temp Tier 3 course with and without READMEs in mirror directories verifies `validate_course()` reports missing READMEs
- [ ] Skill loading tests: each of `repo-scaffolding`, `status-tracking`, and `syllabus-integration` is loadable via `get_skill_definition()` and contains expected section headings
- [ ] Backward compatibility tests: `validate_lesson()` and `validate_course()` called without `tier` produce unchanged behavior compared to pre-sprint baseline
- [ ] All tests pass with `uv run pytest tests/test_validation_enhanced.py -v`

## Implementation Notes

`jtl-syllabus` is available as a project dependency (in `pyproject.toml`). Tests
can use `Course.to_yaml()` to create `syllabus.yaml` test fixtures
programmatically from Pydantic models, rather than writing raw YAML strings.

## Testing

- **Existing tests to run**: `uv run pytest tests/test_validation.py` to confirm existing tests still pass alongside the new file
- **New tests to write**: This ticket IS the test ticket -- all tests listed in the acceptance criteria above are the new tests
- **Verification command**: `uv run pytest tests/test_validation_enhanced.py -v`
