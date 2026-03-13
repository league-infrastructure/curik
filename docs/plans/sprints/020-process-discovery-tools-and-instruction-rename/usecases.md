---
status: draft
---

# Sprint 020 Use Cases

## SUC-001: Agent discovers current process state and routing
Parent: UC-001

- **Actor**: AI agent starting a new session
- **Preconditions**: Curik MCP server is running, project is initialized
- **Main Flow**:
  1. Agent calls `get_process_guide()`
  2. Server returns full 3-phase process decision tree
  3. Agent reads the guide and determines which phase, agent, and skill apply
- **Postconditions**: Agent has loaded process context for routing
- **Acceptance Criteria**:
  - [x] `get_process_guide()` returns markdown with all 3 macro-phases
  - [x] Document includes agent-to-phase mappings
  - [x] Document includes skill-to-agent mappings

## SUC-002: Agent loads bundled context for an activity
Parent: UC-001

- **Actor**: AI agent that knows which activity it needs to perform
- **Preconditions**: Agent has determined activity from process guide or status
- **Main Flow**:
  1. Agent calls `get_activity_guide("spec-development")`
  2. Server bundles curriculum-architect agent + course-concept, pedagogical-model, alignment-decision, spec-synthesis skills + curriculum-process, course-taxonomy instructions
  3. Server returns composite markdown document
- **Postconditions**: Agent has all context needed to perform the activity
- **Acceptance Criteria**:
  - [x] All 10 activity mappings from spec return correct bundles
  - [x] Missing files are handled gracefully (instruction files not yet written)
  - [x] Unknown activity returns clear error

## SUC-003: API uses "instructions" terminology
Parent: UC-001

- **Actor**: AI agent or developer using the MCP API
- **Preconditions**: Server is running
- **Main Flow**:
  1. Agent calls `list_instructions()` instead of `list_references()`
  2. Agent calls `get_instruction(name)` instead of `get_reference(name)`
  3. Both return the same content as before
- **Postconditions**: API terminology matches the spec
- **Acceptance Criteria**:
  - [x] `list_instructions()` works
  - [x] `get_instruction(name)` works
  - [x] Old `list_references()` / `get_reference()` still work (backward compat)
