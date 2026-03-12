---
id: "001"
title: "Implement read_syllabus_entries tool"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Implement read_syllabus_entries tool

## Description

Create the `curik/syllabus.py` module with a `read_syllabus_entries()` function that parses `syllabus.yaml` and returns a list of lesson entry dicts, each containing `uid`, `path`, `title`, and `url` fields. Add a corresponding `read_syllabus_entries` MCP tool wrapper in `server.py` that accepts a `course_path` argument pointing to the course root containing `syllabus.yaml` and returns the parsed entries as JSON. This is needed so that Curik and agents can programmatically inspect the syllabus to determine which lessons exist, which have UIDs, and which already have url fields populated.

## Acceptance Criteria

- [ ] `curik/syllabus.py` module exists with a `read_syllabus_entries(course_path)` function
- [ ] Function parses `syllabus.yaml` using PyYAML and returns a list of dicts with keys `uid`, `path`, `title`, `url`
- [ ] Entries missing `uid` or `url` fields are included with `None` values for those keys
- [ ] Function raises a clear error when `syllabus.yaml` does not exist at the given path
- [ ] `read_syllabus_entries` MCP tool is registered in `server.py` and callable via the MCP protocol
- [ ] MCP tool accepts a `course_path` parameter and returns JSON array of entry objects

## Testing

- **Existing tests to run**: `uv run pytest tests/` to verify no regressions
- **New tests to write**: Covered by ticket 007; basic smoke-test that `read_syllabus_entries` is importable and the MCP tool is registered
- **Verification command**: `uv run pytest tests/test_syllabus.py -v`
