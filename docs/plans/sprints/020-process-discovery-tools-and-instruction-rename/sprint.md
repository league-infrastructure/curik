---
id: "020"
title: "Process Discovery Tools and Instruction Rename"
status: planning
branch: sprint/020-process-discovery-tools-and-instruction-rename
use-cases: [SUC-001, SUC-002, SUC-003]
---

# Sprint 020: Process Discovery Tools and Instruction Rename

## Goals

Add the two highest-value MCP tools from the spec — `get_process_guide()` and `get_activity_guide(activity)` — and rename "references" to "instructions" throughout the codebase to align with spec terminology.

## Problem

The Curik MCP server has 67 tools for doing work but no tools for telling the agent *what* to do. The spec identifies `get_process_guide()` and `get_activity_guide()` as "the most important tools" — they prevent the agent from going off the rails by providing process routing and bundled context. Currently the agent must rely entirely on CLAUDE.md cold-start content with no runtime reload path.

Additionally, the spec uses "instructions" for reference documents but the codebase uses "references" — creating a terminology mismatch.

## Solution

1. Write a process guide markdown document bundled in the package describing all 3 macro-phases, decision tree, agent/skill mappings
2. Implement `get_process_guide()` tool that returns this document
3. Implement `get_activity_guide(activity)` that bundles agent + skills + instructions for 10 named activities
4. Rename references → instructions in assets.py, server.py, pyproject.toml, tests

## Success Criteria

- `get_process_guide()` returns a comprehensive decision-tree document
- `get_activity_guide("spec-development")` returns curriculum-architect agent + 4 skills + 2 instructions
- All 10 activity mappings from the spec work correctly
- `list_instructions()` and `get_instruction()` replace `list_references()` and `get_reference()`
- All existing tests pass with renamed functions
- New tests cover both new tools

## Scope

### In Scope
- Process guide content document
- `get_process_guide()` MCP tool
- `get_activity_guide(activity)` MCP tool with 10 activity mappings
- Rename references → instructions (assets.py, server.py, pyproject.toml, tests)

### Out of Scope
- Writing the instruction file content (Sprint 021)
- Writing missing skill files (Sprint 022)
- CLAUDE.md template rewrite (Sprint 022)
- Change cycle tool refactoring (Sprint 023)

## Test Strategy

- Unit tests for `get_process_guide()` return content
- Unit tests for each of the 10 `get_activity_guide()` activity mappings
- Unit tests for unknown activity error handling
- Verify renamed `list_instructions()` / `get_instruction()` work identically to old references API
- Full regression: all 269 existing tests pass

## Architecture Notes

- Process guide is a bundled markdown file in `curik/references/` (keeping the directory name but renaming the API)
- Activity guide composites are built at call time by reading agent + skill + instruction files
- The rename is API-level only — the `curik/references/` directory stays as-is to avoid unnecessary churn

## Definition of Ready

- [x] Sprint planning documents are complete
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
