---
id: "002"
title: "Implement write_syllabus_url tool"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Implement write_syllabus_url tool

## Description

Add a `write_syllabus_url(course_path, uid, url)` function to `curik/syllabus.py` that locates a lesson entry in `syllabus.yaml` by its UID and sets or updates its `url` field, then writes the file back while preserving the existing YAML structure and comments as much as possible. Add a corresponding `write_syllabus_url` MCP tool wrapper in `server.py`. This is needed because after Curik creates an MkDocs page for a lesson, the url field in syllabus.yaml must be backfilled so that the syllabus points to the correct page. Doing this programmatically avoids manual editing and ensures consistency.

## Acceptance Criteria

- [ ] `write_syllabus_url(course_path, uid, url)` function exists in `curik/syllabus.py`
- [ ] Function finds the entry matching the given UID and sets its `url` field to the provided value
- [ ] Function preserves the rest of the YAML file structure (other entries, fields, ordering)
- [ ] Function raises a clear error if no entry with the given UID is found
- [ ] Function raises a clear error if `syllabus.yaml` does not exist
- [ ] `write_syllabus_url` MCP tool is registered in `server.py` with `course_path`, `uid`, and `url` parameters
- [ ] MCP tool returns a success/failure JSON response

## Implementation Notes

`jtl-syllabus` is now a project dependency (in `pyproject.toml`). Use
`Course.from_yaml(path)` to read `syllabus.yaml` into a Pydantic model, modify
the target `Lesson` object's fields directly, then call `Course.to_yaml(path)`
to write back. Pydantic handles the round-trip serialization, preserving
structure without manual YAML manipulation.

## Testing

- **Existing tests to run**: `uv run pytest tests/` to verify no regressions
- **New tests to write**: Covered by ticket 007; verify round-trip integrity (read, write url, read again) and error on missing UID
- **Verification command**: `uv run pytest tests/test_syllabus.py -v`
