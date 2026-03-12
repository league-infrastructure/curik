---
id: 008
title: Resource Collections and Course Type Support
status: done
branch: sprint/008-resource-collections-and-course-type-support
use-cases:
- SUC-001
- SUC-002
- SUC-003
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 008: Resource Collections and Course Type Support

## Goals

Introduce a `resource-collection` course type alongside the existing `course`
type. Resource collections are sets of reference pages, activity descriptions,
and supporting materials rather than sequential lesson plans. They follow an
abbreviated Phase 1 process that skips the pedagogical model (1b) and alignment
decision (1d) sub-phases, since those concepts do not apply to reference
material.

## Problem

Curik currently assumes every project is a sequential lesson-based course. This
forces designers to go through pedagogical model selection and standards
alignment even when building a reference collection (e.g., a set of how-to
pages, activity cards, or supplementary materials). The Phase 1 gates reject
advancement if those sections are missing, so there is no way to skip them.
The scaffolding system also only creates a `lessons/` directory tree, which is
the wrong layout for reference material.

## Solution

Add a `type` field (`course` | `resource-collection`) to the project model.
The type is set at initialization time via a new `course_type` parameter on
`init_course` and stored in `state.json`. The `advance_phase` function reads
the type and adjusts which spec sections are required: resource collections
skip `pedagogical-model` and `alignment-decision`. The scaffolding system
branches on course type to create a `resources/` directory tree instead of
`lessons/`. A new `resource-collection-spec` skill definition guides designers
through the abbreviated Phase 1 process.

## Success Criteria

- `curik init` with `course_type="resource-collection"` creates a project
  whose `state.json` contains `"type": "resource-collection"` and whose
  `course.yml` includes `type: resource-collection`.
- `advance_phase("phase2")` succeeds for a resource collection without
  pedagogical-model or alignment-decision sections filled in.
- `advance_phase("phase2")` still requires all seven sections for a standard
  course (backward compatibility).
- `scaffold_structure` creates a `resources/` tree for resource collections
  and a `lessons/` tree for standard courses.
- The `resource-collection-spec` skill definition exists and documents the
  abbreviated Phase 1 workflow.
- All new behavior is covered by automated tests.

## Scope

### In Scope

- New `course_type` parameter on `init_course()` and `tool_init_course()`
- `type` field in `state.json` and `course.yml`
- Modified `advance_phase()` gate logic for resource collections
- Modified `scaffold_structure()` directory layout for resource collections
- New `resource-collection-spec` skill definition
- Unit tests for all changed and new behavior
- Backward compatibility: existing courses without a `type` field default to
  `course` behavior

### Out of Scope

- Resource-collection-specific validation rules (future sprint)
- Resource-collection-specific outline or change plan workflows
- Migration of existing courses to resource collections
- UI or CLI subcommand changes beyond the `course_type` parameter
- New agents for resource collection authoring

## Test Strategy

Unit tests in `tests/test_project.py` and a new `tests/test_resource_collection.py`:

- **init_course tests**: Verify `state.json` and `course.yml` contain the
  correct type for both `course` and `resource-collection` values. Verify
  that omitting the parameter defaults to `course`.
- **advance_phase tests**: Verify that a resource collection advances to
  phase2 with only the five required sections (concept, research-summary,
  course-structure-outline, assessment-plan, technical-decisions). Verify
  that a standard course still requires all seven.
- **scaffold_structure tests**: Verify that the structure input for a resource
  collection creates directories under a `resources/` path instead of
  `lessons/`. Verify standard courses are unchanged.
- **server tool tests**: Verify `tool_init_course` accepts the `course_type`
  parameter and passes it through.
- **skill file test**: Verify `resource-collection-spec.md` exists and is
  loadable via `get_skill_definition`.

## Architecture Notes

The `type` field is stored in two places: `state.json` (runtime state read by
`advance_phase`) and `course.yml` (project metadata visible to designers and
external tools). `state.json` is the authoritative source for phase gating
logic; `course.yml` is informational.

Backward compatibility is handled by treating a missing `type` field as
`"course"`. No migration step is needed for existing projects.

The abbreviated Phase 1 for resource collections requires these spec sections:
course-concept, research-summary, course-structure-outline, assessment-plan,
and technical-decisions. It skips: pedagogical-model and alignment-decision.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

1. Add `type` parameter to `init_course` and update `course.yml` template
2. Create `resource-collection-spec` skill definition
3. Update `scaffold_structure` for resource collection directory layout
4. Update `advance_phase` to skip gates for resource collections
5. Tests for all resource collection type support
