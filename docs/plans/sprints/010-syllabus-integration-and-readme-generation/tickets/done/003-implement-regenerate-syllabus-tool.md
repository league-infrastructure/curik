---
id: "003"
title: "Implement regenerate_syllabus tool"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Implement regenerate_syllabus tool

## Description

Add a `regenerate_syllabus(course_path)` function to `curik/syllabus.py` that invokes `syl compile` as a subprocess within the given course directory, returning success or failure with any output. Also add a `get_syllabus(course_path)` function that reads and returns the raw content of `syllabus.yaml` as a string. Add MCP tool wrappers for both in `server.py`. The `regenerate_syllabus` tool is needed so agents can trigger a syllabus rebuild from directory structure after making changes, and `get_syllabus` provides raw file access for inspection without parsing.

## Acceptance Criteria

- [ ] `regenerate_syllabus(course_path)` function exists in `curik/syllabus.py`
- [ ] Function runs `syl compile` as a subprocess with `cwd` set to `course_path`
- [ ] Function returns a result object containing success/failure status and subprocess stdout/stderr
- [ ] Function handles the case where `syl` is not installed or the command fails
- [ ] `get_syllabus(course_path)` function exists and returns the raw string content of `syllabus.yaml`
- [ ] `get_syllabus` raises a clear error if `syllabus.yaml` does not exist
- [ ] Both `regenerate_syllabus` and `get_syllabus` MCP tools are registered in `server.py`
- [ ] MCP tools accept `course_path` parameter and return appropriate JSON responses

## Implementation Notes

`jtl-syllabus` is now a project dependency (in `pyproject.toml`). Use
`syllabus.sync.compile_syllabus(lesson_dir)` directly instead of shelling out to
`syl compile` via subprocess. The function returns a `Course` object. Call
`.to_yaml(path)` to write the compiled syllabus to disk. This avoids subprocess
overhead and the requirement that `syl` be on `PATH`.

## Testing

- **Existing tests to run**: `uv run pytest tests/` to verify no regressions
- **New tests to write**: Covered by ticket 007; mock `subprocess.run` to verify `syl compile` invocation and test `get_syllabus` file reading
- **Verification command**: `uv run pytest tests/test_syllabus.py -v`
