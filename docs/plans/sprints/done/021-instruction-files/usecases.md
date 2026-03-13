---
status: draft
---

# Sprint 021 Use Cases

## SUC-001: Activity guides return complete content
Parent: UC-001

- **Actor**: AI agent calling `get_activity_guide()`
- **Preconditions**: Sprint 020 complete, activity guide tool exists
- **Main Flow**:
  1. Agent calls `get_activity_guide("spec-development")`
  2. Response includes curriculum-process and course-taxonomy content
  3. No "not yet written" placeholders
- **Postconditions**: Agent has all reference material
- **Acceptance Criteria**:
  - [x] All 5 instruction files load successfully
  - [x] No activity guide returns "not yet written" placeholders
