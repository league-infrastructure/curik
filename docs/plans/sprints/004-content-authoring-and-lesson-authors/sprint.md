---
id: "004"
title: "Content Authoring and Lesson Authors"
status: planning
branch: sprint/004-content-authoring-and-lesson-authors
use-cases: [SUC-001, SUC-002, SUC-003]
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 004: Content Authoring and Lesson Authors

## Goals

Introduce the two Lesson Author agents and the content skills they use to
produce lesson content. After this sprint, the system can take a scaffolded
course (output of Sprint 003) and draft complete lessons — Markdown files with
inline instructor guide sections — appropriate to the target tier. Tier 3-4
courses additionally get Jupyter notebook support.

## Problem

Sprint 003 produces scaffolded directories and lesson stubs, but there is no
agent or skill that knows how to fill those stubs with actual lesson content.
The stubs contain placeholder text and empty instructor guide sections. Without
specialized authoring agents, a generic AI will produce content that is
inconsistent across tiers, omits required instructor guide fields, and uses
formats unsuitable for the target grade level. Younger tiers need the
instructor guide to be the primary deliverable (the students do not read the
website), while older tiers need inline instructor guide sections embedded in
student-facing Markdown and notebooks.

## Solution

1. **Two Lesson Author agent definitions** — `lesson-author-young` (Tiers 1-2,
   grades 2-5) and `lesson-author-older` (Tiers 3-4, grades 6-12) — stored as
   YAML agent definitions in `.course/agents/`.
2. **Three content skills** — `lesson-writing-young`, `lesson-writing-older`,
   and `instructor-guide-sections` — stored as Markdown skill definitions in
   `.course/skills/`.
3. **Lesson stub templates** with tier-specific structure, including inline
   instructor guide `<div>` sections that are validated for completeness.
4. **Instructor guide validation** — a Python function that checks all 7
   required fields (Objectives, Materials, Timing, Key Concepts, Common
   Mistakes, Assessment Cues, Differentiation) are present and non-empty in
   every lesson file.
5. **Jupyter notebook support** for Tiers 3-4 via `create_notebook_stub` MCP
   tool and a notebook lesson template.

## Success Criteria

- Lesson Author Young agent definition exists and is loadable via MCP.
- Lesson Author Older agent definition exists and is loadable via MCP.
- All three content skills are defined and retrievable.
- Lesson stub templates for each tier include the correct instructor guide
  `<div>` sections with all 7 required fields.
- `create_notebook_stub` MCP tool produces a valid `.ipynb` file with
  instructor guide cells.
- `validate_instructor_guide` function correctly identifies missing or empty
  fields and returns actionable error messages.
- A round-trip test demonstrates: create stub, fill content via skill
  instructions, validate — with no missing fields.

## Scope

### In Scope

- Agent definitions for Lesson Author Young and Lesson Author Older.
- Skill definitions for `lesson-writing-young`, `lesson-writing-older`, and
  `instructor-guide-sections`.
- Tier-specific lesson stub templates (Tier 1, Tier 2, Tier 3, Tier 4).
- Inline instructor guide format using `<div class="instructor-guide" markdown>`.
- Instructor guide field validation (7 required fields).
- `create_notebook_stub` MCP tool for Jupyter notebooks (Tiers 3-4).
- `get_agent_definition` and `get_skill_definition` MCP tool support for the
  new agents and skills.
- Unit tests for template rendering, notebook creation, and validation.

### Out of Scope

- Quiz authoring (Sprint 006).
- Module-level or course-level validation (Sprint 006).
- Change cycle and issue management (Sprint 005).
- MkDocs build integration or CSS styling for instructor guide reveal.
- Actual lesson content for any specific course.
- Research Agent or Curriculum Architect changes.

## Test Strategy

- **Unit tests** for each new function: `create_lesson_stub` (per tier),
  `create_notebook_stub`, `validate_instructor_guide`.
- **Template tests**: render each tier's template and assert the correct
  instructor guide `<div>` structure and all 7 fields are present.
- **Validation tests**: positive case (all fields filled), negative cases
  (missing field, empty field, missing `<div>` wrapper).
- **Notebook tests**: generated `.ipynb` is valid JSON, contains instructor
  guide cells, opens without error.
- **Agent/skill loading tests**: agent and skill YAML/Markdown files parse
  correctly and are returned by MCP tools.
- **Integration test**: end-to-end stub creation through validation for one
  Tier 1 lesson and one Tier 3 lesson.

## Architecture Notes

- Agent definitions follow the pattern established in Sprint 002: YAML files
  in `.course/agents/` with `name`, `role`, `tier`, `allowed-tools`, and
  `instructions` fields.
- Skill definitions are Markdown files in `.course/skills/` with YAML
  frontmatter specifying `name`, `agent`, and `inputs`.
- Lesson stub templates are Python string templates in the `curik/templates/`
  module, selected by tier. They are not user-editable files.
- Instructor guide validation is a pure function in `curik/validation.py` that
  takes a file path and returns a list of errors. It does not modify files.
- Notebook stubs use `nbformat` to produce valid `.ipynb` files. If `nbformat`
  is unavailable, a minimal JSON template is written directly.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
