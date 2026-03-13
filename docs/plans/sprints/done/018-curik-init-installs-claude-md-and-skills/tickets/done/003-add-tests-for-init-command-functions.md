---
id: '003'
title: Add tests for init_command functions
status: done
use-cases:
- SUC-001
- SUC-002
- SUC-003
depends-on:
- '001'
- '002'
---

# Add tests for init_command functions

## Description

Write comprehensive tests for all init_command functions and the
updated init_course() integration.

Test file: `tests/test_init_command.py`

Test cases:
- CLAUDE.md creation from scratch
- CLAUDE.md append to existing file without CURIK markers
- CLAUDE.md replace-in-place with existing CURIK markers
- CLAUDE.md coexistence with CLASI markers
- Skill file creation and unchanged detection
- VS Code MCP config creation and merge
- Settings JSON creation and merge with existing permissions
- Full init_course() integration (produces all expected files)
- Idempotent re-run (second init produces no changes)

## Acceptance Criteria

- [ ] tests/test_init_command.py exists with all test cases above
- [ ] All new tests pass
- [ ] Full test suite passes (no regressions)

## Testing

- **Existing tests to run**: `pytest tests/`
- **New tests to write**: `tests/test_init_command.py`
- **Verification command**: `~/.local/pipx/venvs/curik/bin/python -m pytest tests/`
