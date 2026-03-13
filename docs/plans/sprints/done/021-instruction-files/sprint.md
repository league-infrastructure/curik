---
id: '021'
title: Instruction Files
status: done
branch: sprint/021-instruction-files
use-cases:
- SUC-001
---

# Sprint 021: Instruction Files

## Goals

Write the 5 instruction documents required by the MCP server spec. These are reference documents loaded via `get_instruction()` and bundled into activity guides.

## Problem

The spec defines 5 instruction files that agents consult during work. Only 1 reference file exists (league-web-brand-guide.md). The `get_activity_guide()` tool returns "not yet written" placeholders.

## Solution

Write each instruction file as a comprehensive markdown document in `curik/references/`.

## Success Criteria

- All 5 instruction files load via `get_instruction()`
- `get_activity_guide()` returns real content, no "not yet written" placeholders
- Each document is substantive
- All existing tests pass

## Scope

### In Scope
- curriculum-process.md, course-taxonomy.md, hugo-conventions.md, lesson-page-template.md, instructor-guide-requirements.md

### Out of Scope
- New Python code, missing skills (Sprint 022), CLAUDE.md (Sprint 022)

## Test Strategy

- Verify each file loads via `get_instruction(name)`
- Verify `get_activity_guide()` returns real content
- Full regression

## Architecture Notes

Files go in `curik/references/` — auto-discovered by `list_instructions()`.

## Definition of Ready

- [x] Sprint planning documents are complete
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan
