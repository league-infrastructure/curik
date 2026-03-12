---
id: "012"
title: "User Guide UX Alignment"
status: planning
branch: sprint/012-user-guide-ux-alignment
use-cases: [SUC-001, SUC-002, SUC-003, SUC-004]
---

# Sprint 012: User Guide UX Alignment

## Goals

Align the Curik codebase with the UX described in `docs/curik-user-guide.md`.
The user guide describes the experience from a curriculum developer's perspective;
this sprint closes the gaps between that description and the actual implementation.

## Problem

The user guide references several behaviors and naming conventions that differ
from the current code:

1. The guide calls the hidden directory `.course/`; code uses `.curik/`.
2. The guide describes sequestering existing repo content into `_old/` — not implemented.
3. `curik init` should print a friendly "Open Claude Code and say Start Curik" message.
4. Phase 1 has five sub-phases (1a–1e) but state only tracks a single `phase1`.
5. No "Start Curik" agent exists to orchestrate the initial startup flow.

## Solution

1. Rename `CURIK_DIR` from `.curik` to `.course` everywhere.
2. Add `sequester_content()` to migrate.py and expose as MCP tool.
3. Improve `curik init` CLI output with human-friendly instructions.
4. Add sub-phase tracking to state.json (`sub_phase` field) with advancement functions.
5. Create a `start-curik` agent definition for the startup flow.

## Success Criteria

- All tests pass with `.course/` as the hidden directory name.
- `sequester_content()` moves non-curik files to `_old/` and returns inventory.
- `curik init` prints the "Start Curik" message.
- Sub-phases 1a–1e are tracked in state and can be queried/advanced.
- A start-curik agent definition exists with instructions for the startup flow.

## Scope

### In Scope

- Rename `.curik` → `.course` (constant, tests, docs)
- Sequester function (move files to `_old/`, skip `.course/`, `.git/`, `.mcp.json`)
- CLI init output message
- Sub-phase state tracking (1a through 1e)
- Start Curik agent definition
- MCP tool wrappers for new functions

### Out of Scope

- Full conversational agent behavior (that's in skill/agent markdown, not code)
- Content analysis AI (analysis report is agent-driven, not code-driven)
- Publication workflow (GitHub Actions, registry)
- Quiz authoring changes

## Test Strategy

- Unit tests for `.course/` directory name across all modules
- Unit tests for `sequester_content()` with various repo layouts
- Unit tests for sub-phase tracking and advancement
- Update all existing tests that reference `.curik/`

## Architecture Notes

The rename from `.curik` to `.course` is a breaking change for any existing
initialized projects. This is acceptable at this stage since the tool is
pre-release.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
