---
id: "023"
title: "Change Cycle Tool Alignment"
status: planning
branch: sprint/023-change-cycle-tool-alignment
use-cases: [SUC-001, SUC-002]
---

# Sprint 023: Change Cycle Tool Alignment

## Goals

Add `register_change_plan()` tool and write an integration test covering the full change cycle. Align tool signatures with the MCP server spec.

## Problem

The spec defines `register_change_plan(plan_id)` for indexing agent-written change plans. Currently only `create_change_plan()` exists which creates the plan. The spec wants agents to write plans directly and then register them. Also need end-to-end test coverage for the full change cycle.

## Solution

1. Add `register_change_plan()` to changes.py and server.py
2. Write integration test: create issue → write plan → register → approve → execute → close

## Success Criteria

- `register_change_plan(plan_id)` indexes an agent-written plan
- Full change cycle integration test passes
- All existing tests pass

## Scope

### In Scope
- `register_change_plan()` function and MCP tool
- Integration test for full change cycle
- Tests for new tool

### Out of Scope
- Refactoring scaffold_structure signature (deferred — current signature works)

## Test Strategy

- Unit tests for register_change_plan
- Integration test: issue → plan → register → approve → execute → close
- Full regression

## Architecture Notes

`register_change_plan()` reads a plan file the agent has already written in `change-plan/active/`, validates it exists and has correct frontmatter, and registers it in state metadata. Unlike `create_change_plan()` which creates the file, this just indexes an existing one.

## Definition of Ready

- [x] Sprint planning documents are complete
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan
