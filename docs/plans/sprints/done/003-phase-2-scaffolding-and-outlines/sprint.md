---
id: '003'
title: Phase 2 Scaffolding and Outlines
status: done
branch: sprint/003-phase-2-scaffolding-and-outlines
use-cases:
- SUC-001
- SUC-002
- SUC-003
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 003: Phase 2 Scaffolding and Outlines

## Goals

Implement the Phase 2 entry point: once a spec is approved, the system can
generate a change plan, scaffold the course directory structure with stub
files, produce outlines for human review, and integrate with the `syl` tool
to generate `syllabus.yaml`. This sprint bridges the gap between a completed
spec and content authoring.

## Problem

After a course spec is approved and the phase advances to Phase 2, there is
no automated path from spec to directory structure. A curriculum designer
must manually create directories, stub files, and outlines — or an agent
must improvise the structure without guardrails. This leads to inconsistent
layouts, missing files, and tier-inappropriate templates. There is also no
gate between outlining and drafting: agents jump straight to writing content
without human approval of the outline, producing lessons that miss the mark.

## Solution

Add MCP tools that read the approved spec (tier, module count, lesson count,
structure) and mechanically scaffold the correct directory tree with stub
files. Introduce an outline management system where outlines are stored in
`.course/outlines/`, created via `create_outline`, and require explicit
human approval via `approve_outline` before drafting can proceed. Integrate
with `syl` through `regenerate_syllabus` and `get_syllabus` tools. Wrap the
full scaffolding workflow in a `repo-scaffolding` skill with tier-specific
templates.

## Success Criteria

- `scaffold_structure` creates the correct directory tree for each tier (1-4)
- `create_lesson_stub` generates tier-appropriate stub files
- `regenerate_syllabus` calls `syl` and produces valid `syllabus.yaml`
- `get_syllabus` returns the current syllabus content
- `create_outline` writes an outline to `.course/outlines/`
- `approve_outline` requires human confirmation and marks outline as approved
- Outlines cannot be bypassed — drafting tools (future sprint) will check
  for approved outlines
- The `repo-scaffolding` skill guides agents through the full scaffolding flow

## Scope

### In Scope

- Initial change plan generation from approved spec (`generate_change_plan`)
- `scaffold_structure` MCP tool — creates directories and stub files based
  on spec tier and structure
- `create_lesson_stub` MCP tool — generates a single lesson stub with
  tier-appropriate template
- `regenerate_syllabus` MCP tool — runs `syl` to produce `syllabus.yaml`
- `get_syllabus` MCP tool — reads and returns current `syllabus.yaml`
- `create_outline` MCP tool — writes module or course outline to
  `.course/outlines/`
- `approve_outline` MCP tool — human-gated approval of an outline
- Outline storage format and directory structure in `.course/outlines/`
- `repo-scaffolding` skill definition with tier-specific template guidance
- Tier-specific stub templates (Tier 1: instructor guide only; Tier 2:
  website with external links; Tier 3: repo with code and notebooks;
  Tier 4: reference docs and project specs)
- Unit and integration tests for all new tools
- Phase gating: scaffold tools require Phase 2 state

### Out of Scope

- Content authoring / lesson writing (Sprint 4)
- Lesson Author agent definitions (Sprint 4)
- Change cycle / issue management (Sprint 5)
- Validation tools (Sprint 6)
- Quiz authoring (Sprint 6)
- MkDocs configuration or site building
- Codespaces / devcontainer setup

## Test Strategy

- **Unit tests** for scaffolding logic: verify correct directory trees for
  each tier, correct stub file contents, correct outline file format.
- **Unit tests** for phase gating: verify scaffold tools reject calls when
  not in Phase 2.
- **Integration tests** for MCP tools: start the MCP server, call each new
  tool, verify file system results.
- **Integration test** for `regenerate_syllabus`: mock `syl` invocation,
  verify `syllabus.yaml` is written.
- **Approval gate test**: verify `approve_outline` requires confirmation
  parameter and rejects unapproved outlines.

## Architecture Notes

- Scaffolding reads `course.yml` (tier) and `.course/spec.md` (structure
  outline section) to determine what directories and files to create.
- Stub templates are Python string templates in a new `curik/templates.py`
  module, keyed by tier.
- Outlines are Markdown files in `.course/outlines/` with YAML frontmatter
  containing `status: draft|approved` and metadata (module name, author).
- `approve_outline` is a human-gated tool: it requires a `confirmed: true`
  parameter that agents must obtain from the stakeholder. The tool refuses
  to approve without this flag.
- `regenerate_syllabus` shells out to the `syl` command-line tool. It does
  not implement syllabus generation itself.
- All new tools enforce Phase 2 gating: they read state.json and raise
  `CurikError` if the phase is not `phase2`.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
