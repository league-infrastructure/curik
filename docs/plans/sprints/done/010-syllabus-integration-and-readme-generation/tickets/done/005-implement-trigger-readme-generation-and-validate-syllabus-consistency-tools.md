---
id: "005"
title: "Implement trigger_readme_generation and validate_syllabus_consistency tools"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Implement trigger_readme_generation and validate_syllabus_consistency tools

## Description

Add two MCP tools to `server.py` that orchestrate higher-level operations. `trigger_readme_generation` accepts a `course_path`, iterates over all MkDocs lesson pages in the course, runs the README generation pipeline from ticket 004 on each, and returns a summary of which READMEs were generated or skipped. `validate_syllabus_consistency` accepts a `course_path`, compares syllabus.yaml entries against MkDocs pages on disk, and reports: entries without corresponding MkDocs pages, MkDocs pages without syllabus entries, and UID mismatches between syllabus entries and page frontmatter. These tools are needed so agents can trigger batch README generation after editing multiple lessons and verify that the syllabus and page structure are in sync before publishing.

## Acceptance Criteria

- [ ] `trigger_readme_generation` MCP tool is registered in `server.py`
- [ ] Tool accepts `course_path` and iterates all MkDocs lesson pages in the course
- [ ] Tool calls the README generation logic from `curik/readme.py` for each page
- [ ] Tool returns a JSON summary listing generated READMEs and skipped pages (no guards)
- [ ] `validate_syllabus_consistency` MCP tool is registered in `server.py`
- [ ] Tool accepts `course_path` and reads both syllabus.yaml entries and MkDocs page files
- [ ] Tool reports syllabus entries with no corresponding MkDocs page
- [ ] Tool reports MkDocs pages with no corresponding syllabus entry
- [ ] Tool reports UID mismatches between syllabus entries and MkDocs page frontmatter
- [ ] Both tools return structured JSON responses suitable for agent consumption

## Testing

- **Existing tests to run**: `uv run pytest tests/` to verify no regressions
- **New tests to write**: Covered by ticket 007; integration tests for batch README generation and consistency validation with mock course structures
- **Verification command**: `uv run pytest tests/test_syllabus.py tests/test_readme.py -v`
