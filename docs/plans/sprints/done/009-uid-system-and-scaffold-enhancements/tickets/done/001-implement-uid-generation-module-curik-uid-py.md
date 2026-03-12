---
id: "001"
title: "Implement UID generation module (curik/uid.py)"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Implement UID generation module (curik/uid.py)

## Description

Create a new `curik/uid.py` module that provides stable unique identifier
generation for courses and course units (modules, lessons, exercises). Courses
need a globally unique identifier for cross-system references (registries, LMS
imports, analytics), while units within a course need shorter identifiers that
are human-friendly yet collision-resistant. The module must depend only on the
Python standard library (`uuid`, `secrets`, `string`).

Two public functions:

- `generate_course_uid()` -- returns a UUID4 string (via `uuid.uuid4()`).
- `generate_unit_uid()` -- returns an 8-character base62 string drawn from
  `a-z`, `A-Z`, `0-9` using `secrets.choice` for randomness.

## Acceptance Criteria

- [ ] `curik/uid.py` exists and is importable as `from curik.uid import generate_course_uid, generate_unit_uid`
- [ ] `generate_course_uid()` returns a string that is parseable by `uuid.UUID(value, version=4)`
- [ ] `generate_unit_uid()` returns a string of exactly 8 characters
- [ ] Every character in a `generate_unit_uid()` result is in the set `[a-zA-Z0-9]`
- [ ] 10,000 sequential calls to `generate_unit_uid()` produce 10,000 distinct values
- [ ] The module imports only from the Python standard library (`uuid`, `secrets`, `string`)

## Implementation Notes

`jtl-syllabus` (now a project dependency) provides `syllabus.util.rand62(n)`
which generates n-character base62 random strings. This exists as a reference
implementation, but curik should maintain its own UID module for independence and
because curik has different requirements: UUID4 for courses (globally unique,
cross-system references) and deterministic 8-character base62 for units (using
`secrets.choice` for cryptographic randomness).

## Testing

- **Existing tests to run**: `uv run pytest tests/` -- confirm no regressions from adding the new module
- **New tests to write**: `tests/test_uid.py` -- UUID4 validity of `generate_course_uid`, length and charset of `generate_unit_uid`, uniqueness over 10,000 calls
- **Verification command**: `uv run pytest tests/test_uid.py -v`
