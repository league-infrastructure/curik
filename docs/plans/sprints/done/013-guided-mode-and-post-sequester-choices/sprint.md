---
id: '013'
title: Guided Mode and Post-Sequester Choices
status: done
branch: sprint/013-guided-mode-and-post-sequester-choices
use-cases:
- SUC-001
- SUC-002
- SUC-003
---

# Sprint 013: Guided Mode and Post-Sequester Choices

## Goals

Make the Phase 1 agent experience fully guided: every agent stop ends with
a question and numbered options. Add post-sequester choices (import outline,
research alignment). These are all agent/skill markdown changes — no code.

## Problem

Curriculum developers don't know the process. When the agent finishes talking,
users don't know what to type. The import flow skips research. Post-sequester
doesn't offer to import the old structure.

## Solution

1. Add guided mode prompt to start-curik agent (ask at session start)
2. Update every skill to end every response with a "What next?" menu
3. Add post-sequester choices menu (import outline, research, start fresh)
4. Add research-agent instructions for existing-content research framing
5. Move completed TODOs to done/

## Success Criteria

- Every skill file ends its completion/transition sections with choice menus
- Start-curik agent asks about guided mode and presents post-sequester options
- Research agent has instructions for existing-content context

## Scope

### In Scope

- Agent/skill markdown file updates (no Python code changes)
- Moving TODO files to done/

### Out of Scope

- Python code changes
- New MCP tools
- Test changes

## Test Strategy

No code changes — existing tests should pass unchanged.

## Architecture Notes

All changes are to agent/skill instruction files (markdown). No code impact.

## Definition of Ready

- [x] Sprint planning documents complete
- [x] Architecture review passed
- [x] Stakeholder approved

## Tickets

(To be created after sprint approval.)
