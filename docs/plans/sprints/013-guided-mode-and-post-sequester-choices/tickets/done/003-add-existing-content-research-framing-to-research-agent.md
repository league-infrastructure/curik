---
id: "003"
title: "Add existing-content research framing to research agent"
status: done
use-cases: [SUC-003]
depends-on: []
---

# Add existing-content research framing to research agent

## Description

Add instructions to research-agent.md for framing research around
existing content when a course has old content (sequestered to `_old/`
or still in place). The agent should analyze existing content first,
then search for external resources that align with those topics.

## Acceptance Criteria

- [x] research-agent.md has "Existing Content Research" section
- [x] Instructions cover: analyze first, research in context, compare and contrast, recommend
- [x] Comparison table template included

## Testing

- **Existing tests to run**: `pytest tests/` — all 222 pass (no code changes)
- **New tests to write**: None (markdown-only changes)
- **Verification command**: `.venv/bin/python -m pytest tests/ -q`
