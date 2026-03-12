---
id: "004"
title: "Enhance curik init CLI output and add start-curik agent"
status: todo
use-cases: [SUC-001, SUC-004]
depends-on: ["001"]
---

# Enhance curik init CLI output and add start-curik agent

## Description

1. Change `curik init` CLI to print a human-friendly message instead of
   raw JSON. Message should say what was created and end with:
   "Open Claude Code in this directory and say: Start Curik"

2. Create `curik/agents/start-curik.md` agent definition that handles the
   "Start Curik" trigger. The agent should: verify MCP server, check for
   existing content, ask about sequestering, and begin Phase 1a.

## Acceptance Criteria

- [ ] `curik init` prints human-readable output (not JSON)
- [ ] Output includes "Start Curik" instruction
- [ ] `start-curik.md` agent exists in `curik/agents/`
- [ ] Agent handles empty repo and existing-content repo scenarios
- [ ] CLI test verifies output format

## Testing

- **Existing tests to run**: `uv run pytest tests/test_cli.py`
- **New tests to write**: CLI output format test
- **Verification command**: `uv run pytest`
