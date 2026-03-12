---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 002 Use Cases

## SUC-001: Curriculum Architect drives the Phase 1 conversation
Parent: UC-001

- **Actor**: AI agent (Curriculum Architect) running in Claude Code
- **Preconditions**: Course is initialized (`init_course` has run), MCP
  server is running, agent has loaded its definition via
  `get_agent_definition("curriculum-architect")`
- **Main Flow**:
  1. Agent calls `get_agent_definition("curriculum-architect")` and
     receives its role, capabilities, boundaries, and skill list
  2. Agent calls `get_skill_definition("course-concept")` to load the
     Phase 1a workflow
  3. Agent follows the skill's question sequence, interviewing the
     designer about target students, goals, format, and scope
  4. Agent calls `record_course_concept` to persist Phase 1a output
  5. Agent calls `get_skill_definition("pedagogical-model")` and drives
     Phase 1b: delivery format, pedagogical structure, session format
  6. Agent calls `record_pedagogical_model` to persist Phase 1b output
  7. Agent delegates to the Research Agent for Phase 1c (see SUC-002)
  8. Agent calls `get_skill_definition("alignment-decision")` and drives
     Phase 1d using research findings
  9. Agent calls `record_alignment` to persist Phase 1d output
  10. Agent calls `get_skill_definition("spec-synthesis")` and assembles
      the complete spec from all prior phase outputs
  11. Agent calls `update_spec` for remaining sections (course structure
      outline, assessment plan, technical decisions)
  12. Agent calls `advance_phase("phase2")` -- succeeds because all spec
      sections are complete
- **Postconditions**: `.course/spec.md` contains a complete course
  specification with all seven sections filled in. Phase is now `phase2`.
- **Acceptance Criteria**:
  - [ ] `get_agent_definition("curriculum-architect")` returns a
    non-empty markdown document containing role, capabilities,
    boundaries, and skill references
  - [ ] All five Phase 1 skills are loadable via `get_skill_definition`
  - [ ] Each skill contains a step-by-step procedure (not placeholders)
  - [ ] The agent definition lists exactly the skills the Curriculum
    Architect is allowed to use

## SUC-002: Research Agent finds alignment candidates and resources
Parent: UC-002

- **Actor**: AI agent (Research Agent) invoked by the Curriculum
  Architect during Phase 1c
- **Preconditions**: Course concept and pedagogical model are recorded in
  the spec. MCP server is running.
- **Main Flow**:
  1. Curriculum Architect invokes the Research Agent (agent handoff)
  2. Research Agent calls
     `get_agent_definition("research-agent")` to load its definition
  3. Research Agent calls `web_search` with queries derived from the
     course concept (e.g., "PCEP certification syllabus",
     "python beginner curriculum")
  4. Research Agent evaluates results and calls
     `save_research_findings` for each meaningful finding, providing
     a title, source URLs, finding type (standard, course, tutorial,
     resource), and structured summary
  5. Research Agent calls `get_research_findings` to review accumulated
     findings and identify alignment candidates
  6. Research Agent produces a research summary recommending alignment
     targets and resources, then returns control to the Curriculum
     Architect
- **Postconditions**: `.course/research/` contains numbered finding
  files. The research summary is available for the alignment decision.
- **Acceptance Criteria**:
  - [ ] `get_agent_definition("research-agent")` returns a non-empty
    definition with role, capabilities, and boundaries
  - [ ] `web_search` accepts a query string and returns results
  - [ ] `save_research_findings` creates a numbered file in
    `.course/research/` with YAML frontmatter and markdown body
  - [ ] `get_research_findings` returns all saved findings
  - [ ] Research Agent definition explicitly states it cannot edit spec
    documents or make alignment decisions

## SUC-003: Spec synthesis produces a complete specification
Parent: UC-003

- **Actor**: AI agent (Curriculum Architect) running in Claude Code
- **Preconditions**: Phases 1a through 1d are complete (course concept,
  pedagogical model, research, and alignment decision are all recorded
  in the spec). Research findings exist in `.course/research/`.
- **Main Flow**:
  1. Agent calls `get_skill_definition("spec-synthesis")` to load the
     synthesis workflow
  2. Agent calls `get_spec` to read all existing spec sections
  3. Agent calls `get_research_findings` to pull in research data
  4. Agent follows the skill procedure to assemble the Course Structure
     Outline section, choosing the correct outline format based on the
     pedagogical structure recorded in Phase 1b
  5. Agent calls `update_spec("course-structure-outline", ...)` with
     the module/lesson skeleton
  6. Agent assembles the Assessment Plan section and calls
     `update_spec("assessment-plan", ...)`
  7. Agent assembles the Technical Decisions section and calls
     `update_spec("technical-decisions", ...)`
  8. Agent calls `get_phase` to confirm all gates are met
  9. Agent calls `advance_phase("phase2")` -- succeeds
- **Postconditions**: All seven spec sections contain real content. The
  spec is a complete, coherent document ready for Phase 2 scaffolding.
- **Acceptance Criteria**:
  - [ ] `spec-synthesis` skill contains explicit instructions for each
    spec section, including which pedagogical-structure variant to use
    for the Course Structure Outline
  - [ ] After synthesis, `advance_phase("phase2")` succeeds (no
    missing or placeholder sections)
  - [ ] The spec document is internally consistent: the course structure
    outline matches the pedagogical model, alignment references match
    the alignment decision
