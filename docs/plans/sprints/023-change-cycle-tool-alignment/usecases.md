---
status: draft
---

# Sprint 023 Use Cases

## SUC-001: Agent registers a hand-written change plan
Parent: UC-001

- **Actor**: AI agent that has written a change plan document
- **Preconditions**: Agent has created a change plan file in change-plan/active/
- **Main Flow**:
  1. Agent writes a change plan markdown file with YAML frontmatter
  2. Agent calls `register_change_plan(plan_number)`
  3. Server validates the file exists and has correct structure
  4. Server indexes the plan in state metadata
- **Postconditions**: Plan is registered and can be approved
- **Acceptance Criteria**:
  - [x] register_change_plan validates file existence
  - [x] register_change_plan validates frontmatter structure
  - [x] Registered plan can be approved via approve_change_plan

## SUC-002: Full change cycle end-to-end
Parent: UC-001

- **Actor**: AI agent managing ongoing changes
- **Preconditions**: Course is initialized
- **Main Flow**:
  1. Create issue via create_issue()
  2. Create change plan via create_change_plan()
  3. Approve via approve_change_plan()
  4. Execute via execute_change_plan()
  5. Review via review_change_plan()
  6. Close via close_change_plan()
  7. Verify issue and plan both in done/
- **Postconditions**: Issue and plan in done/ directories
- **Acceptance Criteria**:
  - [x] Full cycle completes without errors
  - [x] Issue moved to done/
  - [x] Plan moved to done/
