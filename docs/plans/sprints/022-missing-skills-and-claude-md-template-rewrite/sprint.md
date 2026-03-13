---
id: "022"
title: "Missing Skills and CLAUDE.md Template Rewrite"
status: planning
branch: sprint/022-missing-skills-and-claude-md-template-rewrite
use-cases: [SUC-001, SUC-002]
---

# Sprint 022: Missing Skills and CLAUDE.md Template Rewrite

## Goals

Write the 3 missing skill files from the spec and rewrite the CLAUDE.md template installed by `curik init` to match the spec's process-routing design.

## Problem

The spec defines 18 skills; 15 exist. Three are missing: existing-content-analysis, content-conversion, and change-plan-execution. The CLAUDE.md template is Hugo-focused but the spec wants a process-routing document.

## Solution

1. Write 3 skill files in `curik/skills/`
2. Rewrite `curik/init/claude-section.md` to match spec's CLAUDE.md content

## Success Criteria

- All 3 skill files load via `get_skill()`
- `get_activity_guide()` returns real skill content (no placeholders)
- CLAUDE.md template matches spec's process-routing design
- All tests pass

## Scope

### In Scope
- existing-content-analysis.md, content-conversion.md, change-plan-execution.md skills
- curik/init/claude-section.md rewrite

### Out of Scope
- Change cycle tool refactoring (Sprint 023)
- New Python code beyond the markdown files

## Test Strategy

- Verify each skill loads via `get_skill(name)`
- Verify activity guides that reference these skills return real content
- Test CLAUDE.md template installation produces spec-matching output
- Full regression

## Architecture Notes

Skills go in `curik/skills/`, auto-discovered by `list_skills()`. CLAUDE.md template is in `curik/init/claude-section.md`, installed by `init_command.py`.

## Definition of Ready

- [x] Sprint planning documents are complete
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan
