---
id: "006"
title: "Validation and Quiz Authoring"
status: planning
branch: sprint/006-validation-and-quiz-authoring
use-cases:
  - SUC-006-001
  - SUC-006-002
  - SUC-006-003
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 006: Validation and Quiz Authoring

## Goals

Implement mechanical validation at lesson, module, and course level so that
incomplete or structurally broken curriculum cannot pass review. Create the
Quiz Author agent with tools for generating and validating quiz configuration
files. Create the Reviewer agent that uses validation tools to produce
actionable reports. Write the `validation-checklist` and `quiz-authoring`
skills.

## Problem

After Sprint 4 (Content Authoring) and Sprint 5 (Change Cycle), agents can
scaffold and draft curriculum, then iterate on it through issues and change
plans. But there is no automated enforcement that a lesson is actually
complete before it ships. Agents routinely produce content that looks finished
but is missing instructor guide sections, has placeholder objectives, omits
quiz configuration, or has a `syllabus.yaml` that is inconsistent with the
directory structure. Without mechanical validation, these gaps are only caught
by manual human review -- which does not scale and is error-prone.

Similarly, quiz configuration files (`quiz.yml`) need to be authored per
lesson and aligned to that lesson's learning objectives, but there is no
tooling to generate stubs, check alignment, or track quiz readiness.

## Solution

Build a three-level validation engine exposed as MCP tools:

1. **Lesson validation** (`validate_lesson`) -- checks that instructor guide
   sections are present and non-empty, that learning objectives exist, and
   that the lesson file is referenced in `syllabus.yaml`.
2. **Module validation** (`validate_module`) -- checks that all lessons in the
   module pass lesson validation and that a module overview file exists.
3. **Course validation** (`validate_course`) -- checks that all modules are
   valid, `course.yml` is complete (no TBD values), MkDocs builds without
   errors, and `syllabus.yaml` is consistent with the directory tree.

Add a `get_validation_report` tool that runs all three levels and produces a
structured report with pass/fail per item and actionable error messages.

Build quiz authoring tools:

- `generate_quiz_stub` -- creates a `quiz.yml` file for a lesson with topics
  derived from the lesson's objectives, default difficulty and question types.
- `validate_quiz_alignment` -- checks that quiz topics cover the lesson's
  learning objectives.
- `set_quiz_status` -- marks a quiz as draft, review, or approved.

Define two new agents:

- **Quiz Author** -- uses quiz authoring tools and the `quiz-authoring` skill
  to create quiz configuration files aligned to lesson content.
- **Reviewer** -- uses validation tools and the `validation-checklist` skill
  to run validation, produce reports, and approve or block publication.

## Success Criteria

- `validate_lesson` correctly identifies missing instructor guide sections,
  missing objectives, and lessons not in `syllabus.yaml`.
- `validate_module` fails when any lesson in the module fails validation or
  when the module overview is missing.
- `validate_course` fails when any module fails, `course.yml` has TBD fields,
  or `syllabus.yaml` is inconsistent with the directory tree.
- `get_validation_report` produces a structured JSON report covering all
  levels with actionable error messages.
- `generate_quiz_stub` creates a well-formed `quiz.yml` with topics derived
  from lesson objectives.
- `validate_quiz_alignment` detects when quiz topics do not cover lesson
  objectives.
- Quiz Author and Reviewer agent definitions are complete and loadable.
- `validation-checklist` and `quiz-authoring` skills are defined and usable.
- All new tools are exposed through the MCP server.
- Unit tests cover all validation rules and quiz tools.

## Scope

### In Scope

- `validate_lesson`, `validate_module`, `validate_course` MCP tools
- `get_validation_report` MCP tool
- `generate_quiz_stub`, `validate_quiz_alignment`, `set_quiz_status` MCP tools
- Quiz Author agent definition (`.course/agents/quiz-author.md`)
- Reviewer agent definition (`.course/agents/reviewer.md`)
- `validation-checklist` skill definition
- `quiz-authoring` skill definition
- `quiz.yml` schema definition (topics, difficulty, question_types,
  optional example_questions)
- Unit tests for all validation rules and quiz tools
- Integration of new tools into the existing MCP server

### Out of Scope

- Quiz execution or student-facing quiz runtime
- Automated fixing of validation failures (report only)
- CI/CD pipeline integration for validation (future sprint)
- Grading or scoring logic
- Changes to the `syl` tool itself
- MkDocs theme or build system changes

## Test Strategy

**Unit tests** for each validation function:

- Lesson validation: test with complete lesson, missing instructor guide,
  missing objectives, lesson not in syllabus. Test across tier variants
  (Tier 1 instructor-guide-only vs Tier 3 with notebooks).
- Module validation: test with all-valid lessons, one failing lesson,
  missing module overview.
- Course validation: test with complete course, incomplete `course.yml`,
  inconsistent `syllabus.yaml`.
- Quiz tools: test stub generation from sample objectives, alignment
  validation with matching/mismatched topics, status transitions.

**Integration tests**:

- End-to-end: init a course, scaffold structure, create lessons with
  content, run full validation, generate quiz stubs, validate alignment.
- MCP tool registration: verify all new tools appear in the MCP server
  tool list and respond to calls.

**Fixture-based testing**: Create minimal fixture directories representing
valid and invalid course structures to avoid heavy setup in each test.

## Architecture Notes

- Validation functions live in a new `curik/validation.py` module.
- Quiz tools live in a new `curik/quiz.py` module.
- Both modules are pure functions operating on `Path` -- they read the
  filesystem and return structured results, no side effects except
  `generate_quiz_stub` which writes `quiz.yml`.
- Validation results use a consistent schema: `{"valid": bool, "errors": [...], "warnings": [...]}`.
- The `get_validation_report` tool aggregates results from all three levels
  into a single structured report.
- Agent definitions follow the same format as existing agents (Curriculum
  Architect, Research Agent, Lesson Authors) -- Markdown files in
  `.course/agents/` with role, tools, and constraints sections.
- Skill definitions follow the same format as existing skills -- Markdown
  files in `.course/skills/` with steps, tools-used, and agent sections.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
