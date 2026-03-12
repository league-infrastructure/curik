---
status: draft
---

# Sprint 001 Use Cases

## SUC-001: Agent initializes a new curriculum project via MCP
Parent: R1

- **Actor**: AI agent (Curriculum Architect) running in Claude Code
- **Preconditions**: Curik MCP server is running, working directory is empty or has no `.course/`
- **Main Flow**:
  1. Agent calls `init_course` MCP tool with the project path
  2. Server delegates to `curik.project.init_course()`
  3. Server returns success with created directory structure
- **Postconditions**: `.course/` directory exists with spec.md, overview.md, state.json, and subdirectories; `course.yml` exists at repo root
- **Acceptance Criteria**:
  - [ ] `init_course` tool is registered and callable
  - [ ] Returns structured response with created paths
  - [ ] Returns error if `.course/` already exists

## SUC-002: Agent reads and updates spec sections via MCP
Parent: R2

- **Actor**: AI agent (Curriculum Architect) running in Claude Code
- **Preconditions**: Course is initialized, MCP server is running
- **Main Flow**:
  1. Agent calls `get_spec` to read current spec content
  2. Agent calls `update_spec` with section name and content
  3. Server validates content is non-empty, updates spec.md
  4. Agent calls `get_spec` to verify the update
- **Postconditions**: Spec section is updated in `.course/spec.md`
- **Acceptance Criteria**:
  - [ ] `get_spec` returns full spec or specific section
  - [ ] `update_spec` validates section name against known headings
  - [ ] `update_spec` rejects empty content
  - [ ] Convenience tools (`record_course_concept`, `record_pedagogical_model`, `record_alignment`) work correctly

## SUC-003: Agent advances phase through MCP with gating
Parent: R2, R5

- **Actor**: AI agent running in Claude Code
- **Preconditions**: Course is initialized in Phase 1, MCP server is running
- **Main Flow**:
  1. Agent calls `get_phase` to check current phase and requirements
  2. Agent fills in all spec sections via `update_spec`
  3. Agent calls `advance_phase` with target "phase2"
  4. Server checks all spec sections are present and non-placeholder
  5. Server advances phase and returns success
- **Alternate Flow** (incomplete spec):
  1. Agent calls `advance_phase` before all sections are filled
  2. Server returns error listing which sections are missing or placeholder
  3. Agent remains in Phase 1
- **Postconditions**: Phase is advanced to Phase 2 in state.json (or remains Phase 1 with error)
- **Acceptance Criteria**:
  - [ ] `get_phase` returns current phase and gate requirements
  - [ ] `advance_phase` blocks when spec sections contain "TBD" placeholders
  - [ ] `advance_phase` succeeds when all sections have real content
  - [ ] `get_course_status` returns summary including phase, open issues count
