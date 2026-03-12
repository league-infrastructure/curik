---
id: "011"
title: "Validation Enhancements and Missing Skills"
status: planning
branch: sprint/011-validation-enhancements-and-missing-skills
use-cases:
  - SUC-001
  - SUC-002
  - SUC-003
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 011: Validation Enhancements and Missing Skills

## Goals

Make the validation tools tier-aware so they catch structural problems in
Tier 3-4 courses that the current validators ignore: missing comment guards
in lesson files and inconsistencies between syllabus.yaml and the on-disk
course structure. Additionally, create the three infrastructure skill
definitions (repo-scaffolding, status-tracking, syllabus-integration) that
agents need to follow project conventions without relying on tribal knowledge.

## Problem

`validate_lesson()` and `validate_course()` currently apply the same checks
regardless of tier. Tier 3-4 courses have additional structural requirements
that are not validated:

1. Lesson files in Tier 3-4 courses must contain `<!-- readme-shared -->`
   comment guards that mark the boundary between student-facing content
   (shared with the generated README) and instructor-only content. Without
   these guards, README generation produces incomplete or incorrect output.

2. Every lesson referenced in `syllabus.yaml` must actually exist on disk,
   and every lesson on disk should have a corresponding syllabus entry.
   Today there is no automated check for this, so drift between the syllabus
   and the file tree goes unnoticed.

3. For Tier 3-4 courses, `validate_course()` does not verify that generated
   READMEs exist in the expected repo-root mirror directories or that
   syllabus.yaml entries are consistent with MkDocs page configuration.

Separately, three infrastructure skills are referenced in agent workflows
but have no definitions: repo-scaffolding, status-tracking, and
syllabus-integration. Agents encountering these references have no guidance
on the expected directory structures, file formats, or tooling conventions.

## Solution

Extend `validate_lesson()` to accept an optional `tier` parameter. When
the tier is 3 or 4, the function additionally checks for the presence of
`<!-- readme-shared -->` comment guards and verifies that the lesson's UID
appears in the course's `syllabus.yaml`. Extend `validate_course()` to
call a new `validate_syllabus_consistency()` helper for Tier 3-4 courses
that cross-references syllabus entries against MkDocs pages and checks
that README files exist in the expected repo-root mirror directories.

Create three new Markdown skill definitions under `curik/skills/` that
document the conventions for repository scaffolding, status tracking, and
syllabus integration respectively.

## Success Criteria

- `validate_lesson()` with `tier=3` on a lesson missing comment guards
  returns `valid: False` with a descriptive error.
- `validate_lesson()` with `tier=3` on a lesson whose UID is not in
  `syllabus.yaml` returns `valid: False` with a descriptive error.
- `validate_lesson()` with `tier=1` or `tier=2` does not check guards
  or syllabus entries (backward compatible).
- `validate_course()` on a Tier 3 course detects mismatches between
  `syllabus.yaml` entries and MkDocs `nav` pages.
- `validate_course()` on a Tier 3 course flags missing README files in
  repo-root mirror directories.
- All three skill files exist and are loadable via `get_skill_definition()`.
- All new validation behavior is covered by automated tests.

## Scope

### In Scope

- Optional `tier` parameter on `validate_lesson()` (default: `None`, no
  tier-specific checks)
- Comment guard check (`<!-- readme-shared -->`) for Tier 3-4 lessons
- Syllabus UID presence check for Tier 3-4 lessons
- `validate_syllabus_consistency()` helper in `validation.py`
- README-exists check in repo-root mirror directories for Tier 3-4 courses
- `curik/skills/repo-scaffolding.md` skill definition
- `curik/skills/status-tracking.md` skill definition
- `curik/skills/syllabus-integration.md` skill definition
- Unit tests for all new validation paths and skill file loading

### Out of Scope

- Changes to `validate_module()` (no tier-specific module rules yet)
- Automatic fix-up or generation of missing comment guards
- Syllabus.yaml write operations (covered by Sprint 010)
- Changes to the MCP server tool signatures beyond passing `tier`
- Agent definitions that consume the new skills

## Test Strategy

Unit tests in a new `tests/test_validation_enhanced.py` file:

- **Comment guard tests**: Create temp lesson files with and without
  `<!-- readme-shared -->` guards. Run `validate_lesson()` at tier 3 and
  confirm failures for missing guards and passes for present ones. Run at
  tier 2 and confirm guards are not checked.
- **Syllabus UID tests**: Create a temp course with a `syllabus.yaml`
  containing known UIDs. Run `validate_lesson()` at tier 3 for a lesson
  whose UID is present (pass) and absent (fail).
- **Syllabus consistency tests**: Create a temp course with `syllabus.yaml`
  and `mkdocs.yml` containing matching and mismatched entries. Run
  `validate_course()` and confirm mismatches are reported.
- **README existence tests**: Create a temp Tier 3 course with and without
  READMEs in mirror directories. Run `validate_course()` and confirm the
  missing-README error is reported.
- **Skill file tests**: Verify each of the three new skill files is
  loadable via the `get_skill_definition()` function and contains expected
  section headings.
- **Backward compatibility tests**: Run existing `validate_lesson()` and
  `validate_course()` calls without the `tier` parameter and confirm
  behavior is unchanged.

## Architecture Notes

The `tier` parameter is optional and defaults to `None`. When `None`, no
tier-specific checks run, preserving backward compatibility. The tier value
is not inferred from `course.yml` automatically; the caller (MCP tool or
CLI) must pass it. This avoids coupling the validator to file I/O beyond
the lesson file itself.

Syllabus reading depends on Sprint 010 delivering `syllabus.yaml` parsing
utilities. If Sprint 010 is incomplete, the syllabus checks will import a
`read_syllabus()` function and raise a clear error if it is unavailable.

The three skill files are static Markdown documents with YAML frontmatter,
following the same format as existing skills in `curik/skills/`. They are
loaded by the `get_skill_definition()` function in `curik/assets.py`.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

1. Enhance `validate_lesson` to check comment guards for Tier 3-4 courses
   and verify lesson UID in syllabus.yaml
2. Enhance `validate_course` to check syllabus.yaml consistency and README
   existence for Tier 3-4 courses
3. Create `repo-scaffolding` skill definition
4. Create `status-tracking` skill definition
5. Create `syllabus-integration` skill definition
6. Tests for enhanced validation (comment guards, syllabus consistency,
   README checks, skill loading, backward compatibility)
