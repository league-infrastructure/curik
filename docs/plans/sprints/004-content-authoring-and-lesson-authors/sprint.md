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
produce tier-appropriate lessons with validated instructor guide sections.
After this sprint, a curriculum designer can invoke the correct Lesson Author
agent for their tier and receive a complete lesson file (Markdown or Jupyter
notebook) with an inline instructor guide that meets all seven required-field
checks.

## Problem

Curik can initialize a course, complete spec development (Phase 1), and
scaffold directories with lesson stubs (Phase 2), but there is no agent or
skill that actually writes lesson content. The scaffolded stubs are empty
shells. Without specialized authoring agents, content production relies on
unguided AI generation, which routinely omits instructor guide sections,
mismatches the target grade level, or fails to include required pedagogical
fields. The system needs enforced, tier-aware content authoring.

## Solution

1. **Two Lesson Author agent definitions** stored in `.course/agents/`:
   - **Lesson Author Young (Tiers 1-2)** -- targets grades 2-5, produces
     instructor-guide-primary lessons where the instructor guide is the main
     deliverable and student-facing content consists of activity descriptions.
   - **Lesson Author Older (Tiers 3-4)** -- targets grades 6-12, produces
     Markdown lessons and Jupyter notebooks with inline instructor guide
     sections using `<div class="instructor-guide" markdown>` wrappers.

2. **Three content skills** stored in `.course/skills/`:
   - `lesson-writing-young` -- guides the Young author through lesson
     creation for Tiers 1-2 (physical/hands-on activities, minimal screen
     time, instructor-guide-primary format).
   - `lesson-writing-older` -- guides the Older author through lesson
     creation for Tiers 3-4 (code-along exercises, Markdown + Jupyter
     notebooks, inline instructor guide format).
   - `instructor-guide-sections` -- shared skill that ensures all seven
     required instructor guide fields are present and non-empty.

3. **Lesson stub templates** -- tier-specific templates used by
   `create_lesson_stub` that pre-populate the correct structure (including
   instructor guide placeholders) so that authors start from a valid skeleton.

4. **Instructor guide validation** -- a validation function that checks the
   seven required fields (Objectives, Materials, Timing, Key Concepts, Common
   Mistakes, Assessment Cues, Differentiation) are present and contain real
   content rather than placeholders.

## Success Criteria

- Both Lesson Author agent definitions load successfully via `get_agent_definition`.
- All three content skills load successfully via `get_skill_definition`.
- The `lesson-writing-young` skill produces a Tier 1 lesson where the
  instructor guide is the primary content and all seven fields are present.
- The `lesson-writing-older` skill produces a Tier 3 lesson in Markdown with
  inline `<div class="instructor-guide" markdown>` sections containing all
  seven fields.
- The `lesson-writing-older` skill produces a Tier 3 Jupyter notebook with
  instructor guide cells containing all seven fields.
- `create_lesson_stub` generates tier-appropriate templates with instructor
  guide placeholders.
- A validation function detects missing or placeholder instructor guide fields
  and returns actionable error messages.
- All new code has unit test coverage.

## Scope

### In Scope

- Lesson Author Young agent definition (YAML + system prompt)
- Lesson Author Older agent definition (YAML + system prompt)
- `lesson-writing-young` skill definition
- `lesson-writing-older` skill definition
- `instructor-guide-sections` skill definition
- Tier-specific lesson stub templates (Tiers 1-4)
- Jupyter notebook stub template for Tiers 3-4
- Instructor guide field validation logic
- Update to `create_lesson_stub` to select template by tier
- Unit tests for all new components

### Out of Scope

- Quiz authoring (Sprint 6)
- Module-level or course-level validation (Sprint 6)
- Change cycle / issue management (Sprint 5)
- MkDocs build integration
- Deployment or publishing workflows
- The Reviewer agent (Sprint 6)
- Curriculum Architect or Research Agent changes
- `syl` integration beyond what Sprint 3 established

## Test Strategy

- **Unit tests** for instructor guide validation: confirm each of the seven
  fields is checked, confirm placeholder detection ("TBD", empty strings),
  confirm valid content passes.
- **Unit tests** for lesson stub template generation: confirm each tier
  produces the correct structure, confirm Jupyter notebook template is valid
  JSON (nbformat), confirm instructor guide placeholders are present.
- **Unit tests** for agent definition loading: confirm YAML parses, confirm
  required keys are present (name, role, tier, system_prompt).
- **Unit tests** for skill definition loading: confirm YAML parses, confirm
  required keys are present (name, steps, agent).
- **Integration test**: invoke `create_lesson_stub` with each tier value and
  verify the output file matches the expected template structure.

## Architecture Notes

- Agent definitions follow the pattern established by Sprint 2 (Curriculum
  Architect, Research Agent): YAML files in `.course/agents/` with `name`,
  `role`, `tier`, `allowed_tools`, and `system_prompt` fields.
- Skill definitions follow the same YAML pattern in `.course/skills/` with
  `name`, `agent`, `steps`, and `validation` fields.
- Lesson stub templates are stored as Python string templates in the
  `curik/templates/` module, selected by tier at `create_lesson_stub` call
  time.
- The inline instructor guide format uses `<div class="instructor-guide"
  markdown>` to wrap sections, which MkDocs Material renders as collapsible
  or styled blocks via CSS. This keeps instructor content co-located with
  student content rather than in separate files.
- Instructor guide validation is a pure function that takes a lesson file
  path and returns a list of missing/empty fields. It is designed to be
  called by the future Reviewer agent (Sprint 6) as well as by authors
  during drafting.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
