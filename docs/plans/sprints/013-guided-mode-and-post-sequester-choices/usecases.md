---
status: complete
---

# Sprint 013 Use Cases

## SUC-001: Post-sequester choices

- **Actor**: Curriculum developer (via agent)
- **Preconditions**: Existing content sequestered to `_old/`, analysis complete
- **Main Flow**:
  1. Agent presents analysis summary
  2. Agent shows numbered menu: import outline, research alignment, start fresh
  3. User picks an option
  4. Agent follows the chosen path
- **Postconditions**: User is on their chosen path into Phase 1
- **Acceptance Criteria**:
  - [x] Post-sequester menu exists in start-curik agent
  - [x] Import outline option described
  - [x] Research alignment option described

## SUC-002: Guided mode

- **Actor**: Curriculum developer
- **Preconditions**: Session started with "Start Curik"
- **Main Flow**:
  1. Agent asks if user wants fully guided experience
  2. If yes, every agent response ends with choices menu
  3. User never faces a blank prompt without options
- **Postconditions**: User always has clear next steps
- **Acceptance Criteria**:
  - [x] Guided mode prompt in start-curik agent
  - [x] All Phase 1 skills end with choice menus

## SUC-003: Research for existing content

- **Actor**: Agent (research agent)
- **Preconditions**: Old content analyzed, user chose research option
- **Main Flow**:
  1. Agent frames research around existing content topics
  2. Searches for standards, certs, similar courses
  3. Presents findings in context of what old content covers
- **Postconditions**: User has alignment context before Phase 1a
- **Acceptance Criteria**:
  - [x] Research agent has existing-content framing instructions
