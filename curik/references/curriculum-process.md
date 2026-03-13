# Curriculum Development Process

This document describes the full curriculum development process for the
League of Amazing Programmers. All agents consult this reference.

## Three Macro-Phases

### Phase 1: Project Initiation (Spec Development)

Build the course specification through structured conversation with the
designer. Five sub-phases, executed in order:

| Sub-phase | Name | Agent | Skill | Output |
|-----------|------|-------|-------|--------|
| 1a | Course Concept | Curriculum Architect | course-concept | Target students, goals, format, scope |
| 1b | Pedagogical Model | Curriculum Architect | pedagogical-model | Delivery format, pedagogical structure |
| 1c | Research | Research Agent | (web search) | Standards alignment, existing resources |
| 1d | Alignment Decision | Curriculum Architect | alignment-decision | Alignment targets, topic list |
| 1e | Spec Synthesis | Curriculum Architect | spec-synthesis | Complete spec document |

**Resource-collection projects** skip 1b (pedagogical model) and 1d
(alignment decision).

After each sub-phase, call `advance_sub_phase()`. After 1e, call
`advance_phase("phase2")`. The gate checks that all required spec
sections have content.

### Phase 2: First Version (Content Production)

Scaffold the site, create outlines, draft lessons, configure quizzes,
and validate.

**Sequence:**
1. Scaffold directory structure (`scaffold_structure()`)
2. Create outlines in `.course/outlines/`, get designer approval (`approve_outline()`)
3. Draft lessons module by module using the appropriate lesson author
4. Configure quizzes for each lesson (`quiz-authoring` skill)
5. Validate the full course (`validate_course()`)

**Path selection** depends on existing content:
- **Path A** (from scratch): Scaffold → outline → draft → validate
- **Path B** (convert): Use `content-conversion` skill on `_old/` content
- **Path C** (rebuild): Path A, but lesson authors reference `_old/` content

### Phase 3: Ongoing Changes

The steady-state cycle for the life of the course:

1. **File issues** — designer feedback, validation failures, agent observations
2. **Collect** — synthesize open issues into a change plan
3. **Approve** — designer reviews the plan
4. **Execute** — branch, structural moves, content edits, syllabus, validate
5. **Review** — reviewer checks the changes
6. **Close** — move plan and issues to done/

## Designer Approval Points

The designer must approve:
- Phase transition (Phase 1 → Phase 2)
- Each module outline before drafting begins
- Each change plan before execution
- Course publication readiness

## Gate Enforcement

| Gate | Check | Tool |
|------|-------|------|
| Spec completeness | All required sections non-empty | `advance_phase()` |
| Outline approval | Designer has approved | `approve_outline()` |
| Change plan approval | Designer has approved | `approve_change_plan()` |
| Lesson completeness | Instructor guide, objectives present | `validate_lesson()` |
| Syllabus consistency | Every entry has a matching content page | `validate_syllabus_consistency()` |

## Agent Boundaries

- **Curriculum Architect**: Does NOT write lesson content
- **Lesson Authors**: Do NOT modify course structure or spec
- **Research Agent**: Does NOT make decisions — presents findings
- **Quiz Author**: Does NOT modify lesson content
- **Reviewer**: Does NOT make changes — reports issues
