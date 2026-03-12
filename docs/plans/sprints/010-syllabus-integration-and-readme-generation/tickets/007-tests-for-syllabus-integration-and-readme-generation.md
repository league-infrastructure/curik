---
id: "007"
title: "Tests for syllabus integration and README generation"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Tests for syllabus integration and README generation

## Description

Write comprehensive unit tests in `tests/test_syllabus.py` and `tests/test_readme.py` covering all new functionality from this sprint. Syllabus tests cover: parsing entries with various structures (with/without url, with/without uid), writing url fields with YAML round-trip integrity verification, handling of missing syllabus.yaml, subprocess mocking for `syl compile`, and raw content retrieval via `get_syllabus`. README tests cover: comment guard regex parsing with single and multiple guards, nested Markdown content within guards, edge cases (empty guards, unclosed guards), README assembly from parsed sections, file I/O for writing README.md to correct directories, and handling pages with no guards. Integration-level tests verify MCP tool wrappers return correct JSON responses and that consistency validation catches mismatches.

## Acceptance Criteria

- [ ] `tests/test_syllabus.py` exists with tests for `read_syllabus_entries` (valid input, missing fields, missing file)
- [ ] `tests/test_syllabus.py` includes tests for `write_syllabus_url` (success, missing UID, round-trip preservation)
- [ ] `tests/test_syllabus.py` includes tests for `regenerate_syllabus` with mocked `subprocess.run`
- [ ] `tests/test_syllabus.py` includes tests for `get_syllabus` (valid file, missing file)
- [ ] `tests/test_readme.py` exists with tests for guard parsing (single guard, multiple guards, nested content)
- [ ] `tests/test_readme.py` includes edge case tests (empty guards, unclosed guards, no guards)
- [ ] `tests/test_readme.py` includes tests for README assembly from parsed sections
- [ ] `tests/test_readme.py` includes tests for README file writing to correct directories
- [ ] Integration tests verify MCP tool wrappers return well-formed JSON responses
- [ ] Integration tests verify `validate_syllabus_consistency` detects missing pages, missing entries, and UID mismatches
- [ ] All tests pass: `uv run pytest tests/test_syllabus.py tests/test_readme.py -v`

## Testing

- **Existing tests to run**: `uv run pytest tests/` to verify no regressions in existing test suite
- **New tests to write**: All tests described in acceptance criteria above -- this is the primary test ticket for the sprint
- **Verification command**: `uv run pytest tests/test_syllabus.py tests/test_readme.py -v`
