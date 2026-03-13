---
status: draft
---

# Sprint 022 Use Cases

## SUC-001: Missing skills load in activity guides
Parent: UC-001

- **Actor**: AI agent calling `get_activity_guide()`
- **Preconditions**: Sprint 021 complete
- **Main Flow**:
  1. Agent calls `get_activity_guide("content-analysis")`
  2. Response includes existing-content-analysis skill content
  3. Agent calls `get_activity_guide("change-management")`
  4. Response includes change-plan-execution skill content
- **Postconditions**: All activity guides return complete content
- **Acceptance Criteria**:
  - [x] existing-content-analysis, content-conversion, change-plan-execution all load
  - [x] No activity guide returns "not yet written" for any skill

## SUC-002: CLAUDE.md template routes agents to MCP tools
Parent: UC-001

- **Actor**: AI agent reading CLAUDE.md in a new curriculum project
- **Preconditions**: `curik init` has been run
- **Main Flow**:
  1. Agent reads CLAUDE.md
  2. CLAUDE.md instructs: call get_course_status(), get_process_guide()
  3. CLAUDE.md lists available MCP tools by category
- **Postconditions**: Agent knows to consult MCP server before acting
- **Acceptance Criteria**:
  - [x] CLAUDE.md contains pre-flight check instructions
  - [x] CLAUDE.md lists all MCP tool categories
  - [x] CLAUDE.md matches spec's "CLAUDE.md — Full Content" section
