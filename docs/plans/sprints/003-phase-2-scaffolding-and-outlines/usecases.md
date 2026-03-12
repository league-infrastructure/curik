---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 003 Use Cases

## SUC-001: Agent generates change plan and scaffolds directory structure for a Tier 3 course
Parent: R3, R5, R8

- **Actor**: AI agent (Curriculum Architect) running in Claude Code
- **Preconditions**: Course is initialized and in Phase 2. `course.yml` has
  `tier: 3`. Spec is approved with a completed Course Structure Outline
  section defining modules and lessons.
- **Main Flow**:
  1. Agent calls `generate_change_plan` — tool reads spec and `course.yml`,
     produces a change plan listing all directories and files to create.
  2. Agent reviews the change plan with the stakeholder.
  3. Agent calls `scaffold_structure` with the project path — tool reads the
     change plan, creates module directories (e.g., `modules/01-intro/`,
     `modules/02-variables/`), lesson subdirectories, and tier-appropriate
     stub files (Markdown lessons, Jupyter notebook stubs, instructor guide
     stubs).
  4. Agent calls `regenerate_syllabus` — tool runs `syl` to produce
     `syllabus.yaml` from the new directory structure.
  5. Agent calls `get_syllabus` to verify the generated syllabus matches
     the intended structure.
- **Postconditions**: Module and lesson directories exist with stub files.
  `syllabus.yaml` reflects the directory structure. Change plan is recorded
  in `.course/change-plan/active/`.
- **Acceptance Criteria**:
  - [ ] `generate_change_plan` produces a structured plan from spec content
  - [ ] `scaffold_structure` creates correct Tier 3 directory layout (code
    directories, notebook stubs, instructor guides)
  - [ ] `create_lesson_stub` generates stubs with Tier 3 template (Markdown
    with code blocks, notebook reference, instructor guide sections)
  - [ ] `regenerate_syllabus` produces valid `syllabus.yaml`
  - [ ] `get_syllabus` returns the syllabus content
  - [ ] All tools reject calls when phase is not Phase 2

## SUC-002: Agent creates and gets human approval for module outlines before drafting
Parent: R3, R5

- **Actor**: AI agent (Curriculum Architect) and human stakeholder
- **Preconditions**: Course is in Phase 2. Directory structure is scaffolded.
  Module directories exist with stub files.
- **Main Flow**:
  1. Agent generates an outline for a module (e.g., "Module 01: Introduction
     to Python") — a Markdown document listing lesson titles, learning
     objectives per lesson, key concepts, exercises, and estimated duration.
  2. Agent calls `create_outline` with module identifier and outline content.
     Tool writes the outline to `.course/outlines/module-01-intro.md` with
     YAML frontmatter `status: draft`.
  3. Agent presents the outline to the stakeholder for review.
  4. Stakeholder requests changes; agent updates the outline via
     `create_outline` (overwrites the draft).
  5. Stakeholder approves; agent calls `approve_outline` with the outline
     identifier and `confirmed: true`.
  6. Tool verifies the `confirmed` flag, updates frontmatter to
     `status: approved`, and records approval timestamp.
- **Alternate Flow** (agent attempts approval without confirmation):
  1. Agent calls `approve_outline` without `confirmed: true`
  2. Tool rejects with error: "Outline approval requires explicit human
     confirmation (confirmed=true)"
  3. Outline remains in draft status
- **Postconditions**: Outline file in `.course/outlines/` has
  `status: approved`. Future drafting tools can check for approved outlines
  before allowing content generation.
- **Acceptance Criteria**:
  - [ ] `create_outline` writes Markdown with YAML frontmatter to
    `.course/outlines/`
  - [ ] `create_outline` overwrites existing draft outlines
  - [ ] `approve_outline` requires `confirmed: true` parameter
  - [ ] `approve_outline` rejects without confirmation flag
  - [ ] `approve_outline` updates frontmatter status to `approved` with
    timestamp
  - [ ] Outline files follow naming convention: `module-NN-slug.md`

## SUC-003: Agent uses repo-scaffolding skill to scaffold a Tier 1 course end-to-end
Parent: R3, R6, R8

- **Actor**: AI agent (Curriculum Architect) guided by the `repo-scaffolding`
  skill
- **Preconditions**: Course is in Phase 2. `course.yml` has `tier: 1`.
  Spec is approved.
- **Main Flow**:
  1. Agent loads the `repo-scaffolding` skill definition.
  2. Skill guides agent through: read spec, generate change plan, scaffold
     structure, create outlines for each module, present outlines for
     approval, regenerate syllabus.
  3. For Tier 1, scaffolding creates instructor-guide-only lesson stubs
     (no student-facing code, no notebooks, no website content). Each lesson
     stub contains sections for materials, setup, guided activity script,
     discussion prompts, and assessment notes.
  4. Agent creates outlines and obtains stakeholder approval for each module.
  5. Agent calls `regenerate_syllabus` to finalize.
- **Postconditions**: Full Tier 1 course structure is scaffolded with
  instructor-guide-only stubs. All module outlines are approved. Syllabus
  is generated.
- **Acceptance Criteria**:
  - [ ] `repo-scaffolding` skill definition exists and is loadable
  - [ ] Tier 1 stubs contain only instructor guide sections (no student code)
  - [ ] Tier 1 directory layout omits code directories and notebook files
  - [ ] Skill guides agent through the complete scaffolding workflow
  - [ ] Skill enforces outline approval before declaring scaffolding complete
