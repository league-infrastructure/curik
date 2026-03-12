---
id: '004'
title: Integration tests for MCP tools
status: done
use-cases:
- SUC-001
- SUC-002
- SUC-003
depends-on:
- '003'
---

# Integration tests for MCP tools

## Description

Create `tests/test_mcp_server.py` with integration tests for all 9 MCP
tools. Use MCP SDK test client if available; otherwise test handler
functions directly. Cover happy paths, error paths, and phase gating.

## Acceptance Criteria

- [ ] `tests/test_mcp_server.py` exists
- [ ] Tests cover all 9 MCP tools
- [ ] Tests verify `init_course` creates expected structure
- [ ] Tests verify `advance_phase` gating works through MCP
- [ ] Tests verify error responses for invalid inputs
- [ ] All tests pass: `python -m pytest`

## Testing

- **Existing tests to run**: `python -m pytest tests/test_project.py`
- **New tests to write**: Full test suite in `test_mcp_server.py`
- **Verification command**: `python -m pytest`
