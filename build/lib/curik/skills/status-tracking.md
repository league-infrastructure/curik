# Status Tracking

## Purpose

Document the conventions for tracking course development status so that
agents can accurately assess progress, identify blockers, and determine
what work remains.

## Phase System

Curik courses progress through a two-phase lifecycle:

### Phase 1 — Planning and Design

Phase 1 has sub-phases that must be completed in order:

- **1a — Course Concept**: Define the course idea, target audience,
  learning goals, and high-level scope.
- **1b — Pedagogical Model**: Choose the instructional approach (direct
  instruction, project-based, inquiry-based, etc.) and justify it.
- **1c — Spec Synthesis**: Combine concept and pedagogy into a complete
  course specification document.
- **1d — Alignment Decision**: Decide on curriculum standards alignment
  and list topics/modules.

Phase 1 gates: The spec document must have all required sections filled
in (no TBD values) before advancing to Phase 2.

### Phase 2 — Content Development

Phase 2 is the implementation phase where lessons, exercises, quizzes,
and supporting materials are authored. Work in Phase 2 is tracked at
the module and lesson level.

Phase 2 gates: All modules must pass validation (`validate_course`)
before the course is considered complete.

## course.yml Fields

The `course.yml` file at the repository root tracks key metadata:

- **title**: Course display name
- **slug**: URL-safe identifier
- **tier**: Complexity tier (1-4)
- **grades**: Target grade range
- **category**: Subject category
- **topics**: List of topic tags
- **prerequisites**: List of prerequisite course slugs
- **lessons**: Expected total lesson count
- **estimated_weeks**: Duration estimate
- **curriculum_url**: Link to rendered curriculum site
- **repo_url**: Link to source repository
- **description**: Short course description

Fields with value `TBD` indicate incomplete metadata that must be
filled in before Phase 2.

## Spec Sections as Progress Indicators

The spec document (`CURIK_DIR/spec.md`) contains sections that serve
as progress checkpoints:

- **Course Concept** — filled in Phase 1a
- **Pedagogical Model** — filled in Phase 1b
- **Module Outline** — filled in Phase 1c/1d
- **Assessment Strategy** — filled in Phase 1c
- **Differentiation Plan** — filled in Phase 1c

A section containing placeholder text or `TBD` indicates that the
corresponding sub-phase is not yet complete.

## Validation Reports

Validation reports (`CURIK_DIR/validation-report.json`) provide a
snapshot of the course's structural health:

- **valid**: Overall pass/fail
- **errors**: List of specific problems found
- **module_results**: Per-module validation detail
- **lesson_results**: Per-lesson validation detail

Use `tool_validate_course` to generate a fresh report and
`tool_save_validation_report` to persist it. Use
`tool_get_validation_report` to read the last saved report.

## Tracking Workflow

1. Check `tool_get_phase` to see the current phase.
2. Check `tool_get_course_status` for a summary including open issues
   and active change plans.
3. Run `tool_validate_course` to assess structural completeness.
4. Review `course.yml` for TBD fields that need attention.
5. Use the spec document to identify which planning sub-phases are
   complete and which still need work.
