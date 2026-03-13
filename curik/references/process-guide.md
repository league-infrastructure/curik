# Curik Curriculum Development Process

This document describes the full curriculum development process from the
agent's perspective. Call `get_course_status()` to determine where the
project stands, then use this guide to decide what to do next.

## Three Macro-Phases

1. **Project Initiation** — analyze starting materials, build the course spec
2. **First Version** — scaffold, outline, draft, validate
3. **Ongoing Changes** — issue → change plan → execute → review cycle

## Decision Tree: What Should I Do?

```
1. Call get_course_status()
2. Check the phase field:

   phase = "not-started"
     → Has existing content?
       YES → Load curriculum-architect agent
             → Use existing-content-analysis skill
             → Sequester to _old/, produce analysis
             → Begin Phase 1a with analysis context
       NO  → Load curriculum-architect agent
             → Begin Phase 1a (course-concept skill)

   phase = "phase1" (spec development)
     → Check sub_phase:
       1a → Load curriculum-architect + course-concept skill
       1b → Load curriculum-architect + pedagogical-model skill
       1c → Load research-agent (web search driven)
       1d → Load curriculum-architect + alignment-decision skill
       1e → Load curriculum-architect + spec-synthesis skill
     → After 1e: call advance_phase("phase2")

   phase = "phase2" (first version)
     → Has outlines been approved?
       NO  → Load curriculum-architect + structure-proposal skill
             → Create outlines, get designer approval via approve_outline()
       YES → Check tier:
             Tier 1-2 → Load lesson-author-young + lesson-writing-young skill
             Tier 3-4 → Load lesson-author-older + lesson-writing-older skill
     → After all lessons: Load quiz-author + quiz-authoring skill
     → After quizzes: Load reviewer + validation-checklist skill

   phase = "ongoing-changes"
     → Check for open issues via list_issues()
     → Load curriculum-architect + change-plan-execution skill
     → Follow the change cycle (see below)
```

## Phase 1: Project Initiation

### Sub-phases

| Sub-phase | Agent | Skill | Records |
|-----------|-------|-------|---------|
| 1a: Course Concept | curriculum-architect | course-concept | record_course_concept() |
| 1b: Pedagogical Model | curriculum-architect | pedagogical-model | record_pedagogical_model() |
| 1c: Research | research-agent | (web search) | Agent writes to spec directly |
| 1d: Alignment Decision | curriculum-architect | alignment-decision | record_alignment() |
| 1e: Spec Synthesis | curriculum-architect | spec-synthesis | Agent writes to spec directly |

Resource-collection projects skip 1b and 1d.

After each sub-phase, call `advance_sub_phase()` to progress.
After 1e is complete, call `advance_phase("phase2")`.

The phase gate checks that every required spec section has content.
If it fails, address the unmet conditions before retrying.

### Existing Content Path

If `get_course_status()` reports `has_existing_content: true`:

1. Load `get_skill("existing-content-analysis")`
2. Ask designer: sequester files and analyze them?
3. Move existing files to `_old/` via `sequester_content()`
4. Produce analysis report: topics, structure, approach, gaps
5. Proceed through Phase 1 sub-phases informed by the analysis

## Phase 2: First Version

### Three Paths

**Path A: From Scratch** (no existing content)
1. Scaffold with `scaffold_structure()`
2. Create outlines in `.course/outlines/`, get approval via `approve_outline()`
3. Draft lessons using the appropriate lesson author agent
4. Configure quizzes using quiz-author agent
5. Validate with reviewer agent

**Path B: Convert Existing Content**
1. Load `content-conversion` skill
2. Read old content from `_old/`, convert to Curik structure
3. Run scaffolding tools, `regenerate_syllabus()`
4. Designer reviews; enter Phase 3 for fixes

**Path C: Rebuild Informed by Old Content**
Same as Path A, but lesson authors reference `_old/` for examples and ideas.

### Lesson Writing Sequence

For each module:
1. Load the appropriate lesson author agent (young or older, based on tier)
2. Follow the lesson-writing skill step by step
3. For Tier 3-4: call `write_syllabus_url()` after each lesson
4. Call `trigger_readme_generation()` after completing a module (Tier 3-4)
5. Run `validate_module()` to check completeness

## Phase 3: Ongoing Changes

### The Change Cycle

1. **File issues**: Designer reports problems → `create_issue()`
2. **Collect**: Read open issues via `list_issues()`, write a change plan
3. **Approve**: Designer reviews → `approve_change_plan()`
4. **Execute**: Follow `change-plan-execution` skill — branch, structural moves first, content edits second, regenerate syllabus, validate
5. **Review**: Load reviewer agent → `validate_course()` or `validate_module()`
6. **Close**: `close_change_plan()` — moves plan and issues to done/

### Issue Sources

- Designer comments → `create_issue()`
- Validation failures → `create_issue()`
- Agent observations (with designer approval) → `create_issue()`

## Agent Roster

| Agent | Role | Primary Phase |
|-------|------|---------------|
| curriculum-architect | Orchestrates spec, structure, change management | Phase 1, throughout |
| research-agent | Investigates standards, existing courses | Phase 1c |
| lesson-author-young | Writes Tier 1-2 lessons (grades 2-5) | Phase 2 |
| lesson-author-older | Writes Tier 3-4 lessons (grades 6-12) | Phase 2 |
| quiz-author | Creates quiz configurations | Phase 2 |
| reviewer | Validates without modifying content | Phase 2 close, Phase 3 |

## Activity Quick Reference

Use `get_activity_guide(activity)` to load bundled context for:

| Activity | What It Bundles |
|----------|----------------|
| spec-development | curriculum-architect + spec skills + taxonomy |
| research | research-agent + curriculum-process |
| content-analysis | curriculum-architect + existing-content-analysis |
| scaffolding | curriculum-architect + scaffolding skills + hugo-conventions |
| lesson-writing-young | lesson-author-young + writing skills + templates |
| lesson-writing-older | lesson-author-older + writing skills + templates |
| quiz-authoring | quiz-author + quiz skill + process |
| content-conversion | lesson-author-older + conversion skills + templates |
| change-management | curriculum-architect + change skills + process |
| validation | reviewer + validation skills + conventions |

## Rules

- **MCP-first**: Use Curik tools for state changes, not direct file editing
- **Agent boundaries**: Respect the loaded agent's role limits
- **Skills are workflows**: Follow steps in order, don't skip
- **Gates are gates**: When `advance_phase()` fails, fix the conditions
- **Designer approval**: Change plans, outlines, and phase transitions need approval
