---
status: active
---

# Project Overview

## Project Name

Curik — Curriculum Development Tool for the League of Amazing Programmers

## Problem Statement

The League teaches students from 2nd through 12th grade across Python, Java,
robotics, and technology courses. Curriculum is spread across multiple site
generators (Sphinx with Furo, VuePress, bare GitHub repos) with inconsistent
structure, no standard repository layout, no shared metadata format, no
automated catalog, and no process for ensuring a new course is complete before
it ships.

AI agents told to "follow the curriculum template" produce output that looks
right but is missing critical pieces — instructor guides, quiz configurations,
placeholder values that never get updated. The problem is not capability but
enforcement: agents know the rules and violate them anyway.

Curik solves this through mechanical enforcement — gated progression where you
cannot move between phases until validation checks pass. The same design
philosophy as CLASI (Claude Agent Skills Instructions), applied to curriculum
development instead of software engineering.

## Target Users

**Primary:** Curriculum designers — instructors with subject-matter expertise
but limited technical-writing or site-building experience. They work
interactively with an AI agent through Claude Code, from course concept to
fully authored, structured curriculum.

**Secondary:** The AI agents themselves — Curik's MCP tools constrain what
agents can do at each phase, preventing process violations.

## Key Constraints

- **Python package** with CLI entry point (`curik`) and MCP server running
  locally inside Claude Code
- **File-based state** — no database; the `.course/` directory inside the
  curriculum repo is the source of truth (lesson from CLASI: SQLite state
  degraded silently when unavailable)
- **Python >=3.10**, built with setuptools
- **Must integrate with existing League tooling:**
  - `syl` (syllabus tool) — generates `syllabus.yaml` from directory structure
  - MkDocs with Material theme — all curriculum sites
  - GitHub Pages — deployment via GitHub Actions
  - GitHub Codespaces / Code Server — student development environments
- **Must not replace** the `syl` tool, quiz runtime, or site build system
- **Solo developer** (AI-assisted), no external team

## High-Level Requirements

### R1: Project Initialization
Initialize a new curriculum repo with `.course/` directory structure, stub
files, MCP configuration, agent/skill definitions, and `course.yml`. From
`curik init`, the designer should be in a working repo ready for Phase 1.

### R2: Phase 1 — Spec Development (Gated)
Enforce a structured spec development process through five sub-phases:
- **1a Course Concept** — target students, goals, learning outcomes, format, scope
- **1b Pedagogical Model** — delivery format, pedagogical structure, session format, assessment
- **1c Research** — web search for standards, certifications, existing courses, alignment candidates
- **1d Alignment Decision** — map research to topic list, layered alignment
- **1e Spec Synthesis** — assemble complete specification from all sub-phase outputs

Gate: Cannot advance to Phase 2 until all spec sections are present and contain
real content (not placeholders).

### R3: Phase 2 — Scaffold and Draft
- Produce initial change plan from approved spec
- Scaffold directory structure and stub files from change plan
- Run `syl` to generate `syllabus.yaml`
- Produce outlines (per-module or whole-course) before drafting
- Draft lessons module by module with appropriate Lesson Author agent

### R4: Change Cycle (Ongoing)
After initial draft, support iterative improvement:
- File numbered issues in `.course/issues/open/`
- Collect open issues into change plans
- Human-approval gate before execution
- Execute changes (structural moves first, then content, then `syl`)
- Review completion, flag gaps as new issues
- Archive completed change plans and resolved issues

### R5: MCP Server with Enforcement Tools
Expose all state management through MCP tools that enforce process:
- Phase tracking and gated transitions (`get_phase`, `advance_phase`)
- Spec management (`get_spec`, `update_spec`, `record_*` convenience tools)
- Research persistence (`save_research_findings`, `get_research_findings`)
- Scaffolding (`scaffold_structure`, `create_lesson_stub`, `regenerate_syllabus`)
- Outline management with approval gate
- Issue and change plan lifecycle
- Validation (lesson, module, course level)
- Quiz configuration authoring and alignment validation

### R6: Agent Specialization
Six agents with hard role boundaries:
- **Curriculum Architect** — orchestrates process, edits spec/overview, creates change plans
- **Research Agent** — web search, finds resources and alignment candidates
- **Lesson Author (Young, Tiers 1-2)** — writes for grades 2-5, instructor-guide-primary
- **Lesson Author (Older, Tiers 3-4)** — writes for grades 6-12, Markdown + notebooks
- **Quiz Author** — creates `quiz.yml`, validates alignment to lesson objectives
- **Reviewer** — runs validation, produces reports, approves or blocks publication

### R7: Validation
Mechanical validation at lesson, module, and course level:
- Lesson: instructor guide sections present and non-empty, objectives exist
- Module: all lessons valid, module overview exists
- Course: all modules valid, `course.yml` complete, MkDocs builds, `syllabus.yaml` consistent
- Quiz: topics cover lesson objectives

### R8: Curriculum Structure Support
Support the League's four curriculum tiers and all delivery formats:
- Tier 1 (grades 2-3): instructor guide only, no student computers
- Tier 2 (grades 3-5): website linking to external platforms
- Tier 3 (grades 6-10): repo with code, Jupyter notebooks, Codespaces
- Tier 4 (grades 10-12): reference docs, project specs, independent work

### R9: Course Metadata and Registry Integration
- `course.yml` at repo root with standardized metadata
- Validation that `course.yml` is complete and well-formed
- Compatible with the curriculum registry (GitHub Action posts metadata on push)

## Technology Stack

- **Language:** Python >=3.10
- **Build:** setuptools >=68
- **CLI:** argparse (already implemented)
- **MCP:** Python MCP SDK (for the MCP server endpoint)
- **State:** JSON + Markdown files in `.course/` directory
- **Testing:** unittest (already in use)
- **Site generation:** MkDocs with Material theme (consumed, not owned)
- **Syllabus:** `syl` tool from `league-infrastructure/syllabus` (dependency)
- **Deployment:** GitHub Pages via GitHub Actions (not owned by Curik)

## Sprint Roadmap

### Sprint 1: MCP Server Foundation
Stand up the MCP server with the core Phase 1 tools already implemented in the
CLI. Expose `init_course`, `get_phase`, `advance_phase`, `get_spec`,
`update_spec`, `record_course_concept`, `record_pedagogical_model`,
`record_alignment`, and `get_course_status` as MCP tools. This makes the
existing functionality accessible to agents through Claude Code.

### Sprint 2: Phase 1 Agents and Skills
Create the Curriculum Architect and Research Agent definitions. Write the
Phase 1 skills: `course-concept`, `pedagogical-model`, `alignment-decision`,
`spec-synthesis`, and `structure-proposal`. Add the `web_search`,
`save_research_findings`, and `get_research_findings` MCP tools.

### Sprint 3: Phase 2 — Scaffolding and Outlines
Implement Phase 2 entry: initial change plan generation from approved spec.
Add `scaffold_structure`, `create_lesson_stub`, `regenerate_syllabus`,
`get_syllabus` tools. Add outline management with `create_outline` and
`approve_outline` (human-gated). Write the `repo-scaffolding` skill with
tier-specific templates.

### Sprint 4: Content Authoring — Lesson Authors
Create Lesson Author agents (Young and Older). Write content skills:
`lesson-writing-young`, `lesson-writing-older`, `instructor-guide-sections`.
Implement lesson stub templates with inline instructor guide sections.
Support Markdown lessons and Jupyter notebooks.

### Sprint 5: Change Cycle and Issue Management
Implement the full change cycle: `create_issue`, `list_issues`,
`create_change_plan`, `approve_change_plan`, `execute_change_plan`,
`review_change_plan`, `close_change_plan`. Write the `status-tracking` skill.

### Sprint 6: Validation and Quiz Authoring
Implement validation tools: `validate_lesson`, `validate_module`,
`validate_course`, `get_validation_report`. Create the Quiz Author agent and
tools: `generate_quiz_stub`, `validate_quiz_alignment`, `set_quiz_status`.
Write the `validation-checklist` and `quiz-authoring` skills. Create the
Reviewer agent.

### Sprint 7: Polish, Documentation, and Migration Support
End-to-end testing of the full workflow. Generate project documentation.
Create tier-specific template repos. Write migration tooling for converting
existing courses to the standard structure. Registry integration validation.

## Out of Scope

- **Writing `syllabus.yaml` directly** — Curik creates directory structure; `syl` generates the syllabus
- **Student identity, passphrases, or enrollment** — separate League systems
- **Building or deploying MkDocs sites** — Curik may call `make docs` but does not own the build
- **Replacing the `syl` tool** — Curik depends on it
- **Quiz execution or student assessment** — quiz configuration is authoring; the runtime is separate
- **The curriculum registry service itself** — Curik validates `course.yml`; the registry is separate infrastructure
- **Code Server deployment or management** — Curik generates `.devcontainer/` config only
- **Authentication or access control** — instructor guide uses cookie-based reveal, not auth
