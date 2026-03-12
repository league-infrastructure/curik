---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 005 Use Cases

## SUC-001: Designer Files Issues and Agent Collects into Change Plan

Parent: R4 (Change Cycle)

- **Actor**: Curriculum Designer (primary), Curriculum Architect Agent (secondary)
- **Preconditions**:
  - Course is initialized (`.course/` exists with `issues/open/` and `change-plan/active/` directories)
  - Course is in phase 2 or later (initial draft exists)
  - At least one problem or improvement has been identified
- **Main Flow**:
  1. Designer identifies a problem or desired improvement in the curriculum.
  2. Designer invokes `create_issue` with a title, description, category (structural/content/syl), and priority (high/medium/low).
  3. Tool creates a numbered Markdown file in `.course/issues/open/` with YAML frontmatter containing status, category, priority, and creation date.
  4. Designer repeats steps 1-3 for each issue found.
  5. Designer invokes `list_issues` with status filter `open` to review all filed issues.
  6. Designer asks the Curriculum Architect agent to create a change plan.
  7. Agent invokes `create_change_plan` with a title and list of issue numbers to address.
  8. Tool reads the referenced issues, creates a numbered change plan in `.course/change-plan/active/` with a steps list organized by execution order (structural first, content second, syl last), and links each step to its source issue.
  9. Agent presents the change plan to the designer for review.
- **Postconditions**:
  - One or more issue files exist in `.course/issues/open/`
  - One change plan file exists in `.course/change-plan/active/` with status `draft`
  - The plan references specific open issues and contains ordered steps
- **Acceptance Criteria**:
  - [ ] `create_issue` produces a well-formed Markdown file with correct YAML frontmatter
  - [ ] Issue numbers auto-increment across both `open/` and `done/` directories
  - [ ] `list_issues` returns issues filtered by status with parsed frontmatter
  - [ ] `create_change_plan` creates a plan referencing the specified issues
  - [ ] Plan steps are ordered: structural steps before content steps before syl steps
  - [ ] `create_change_plan` fails with an error if no open issues match the given numbers

## SUC-002: Agent Executes Approved Change Plan

Parent: R4 (Change Cycle)

- **Actor**: Curriculum Architect Agent (primary), Curriculum Designer (approval gate)
- **Preconditions**:
  - A change plan exists in `.course/change-plan/active/` with status `draft`
  - The plan contains one or more steps with types and pending status
- **Main Flow**:
  1. Designer reviews the change plan and decides to approve it.
  2. Designer invokes `approve_change_plan` with the plan number.
  3. Tool updates the plan frontmatter: sets status to `approved`, records approver name and approval timestamp.
  4. Agent invokes `execute_change_plan` with the plan number and the index of the step to mark as done.
  5. Tool verifies the plan is approved (raises error if not).
  6. Tool verifies execution ordering: if the step is a content step, all structural steps must already be done; if the step is a syl step, all content steps must already be done.
  7. Tool marks the step as done and records a completion timestamp.
  8. Agent performs the actual file changes described by the step.
  9. Agent repeats steps 4-8 for each step in the plan.
  10. Once all steps are done, the plan status is updated to `executed`.
- **Postconditions**:
  - Plan frontmatter shows status `executed` with approval and execution metadata
  - All steps in the plan are marked done with timestamps
  - The actual curriculum files have been modified according to the plan
- **Acceptance Criteria**:
  - [ ] `approve_change_plan` sets approval metadata in frontmatter
  - [ ] `execute_change_plan` raises `CurikError` if the plan is not approved
  - [ ] Execution ordering is enforced: structural before content before syl
  - [ ] `execute_change_plan` raises `CurikError` if ordering constraint is violated
  - [ ] Each step completion is recorded with a timestamp
  - [ ] Plan status transitions from `approved` to `executed` when all steps are done

## SUC-003: Reviewer Checks and Closes Change Plan

Parent: R4 (Change Cycle)

- **Actor**: Reviewer Agent (primary), Curriculum Designer (oversight)
- **Preconditions**:
  - A change plan exists with status `executed` (all steps completed)
  - The curriculum files have been modified according to the plan
- **Main Flow**:
  1. Designer or orchestrating agent invokes `review_change_plan` with the plan number.
  2. Reviewer examines each change made by the plan against the original issues.
  3. If gaps are found, reviewer invokes `review_change_plan` with the plan number, result `failed`, and a list of gap descriptions.
  4. Tool records the review result in plan frontmatter. For each gap description, tool invokes `create_issue` internally to file a new issue in `.course/issues/open/`, linking it back to the plan.
  5. If no gaps are found (or after gaps have been addressed in a subsequent cycle), reviewer invokes `review_change_plan` with result `passed`.
  6. Tool records the passing review in plan frontmatter and sets status to `reviewed`.
  7. Designer or agent invokes `close_change_plan` with the plan number.
  8. Tool verifies the plan has status `reviewed` with a passing review.
  9. Tool moves the plan file from `active/` to `done/`.
  10. Tool moves all issues referenced by the plan from `open/` to `done/`, updating their status in frontmatter.
  11. Tool returns a summary of closed issues and any remaining open issues (gap issues from review).
- **Postconditions**:
  - Plan file is in `.course/change-plan/done/` with status `closed`
  - Resolved issues are in `.course/issues/done/` with status `resolved`
  - Any gap issues remain in `.course/issues/open/` for the next cycle
- **Acceptance Criteria**:
  - [ ] `review_change_plan` records review result (passed/failed) in frontmatter
  - [ ] Failed review creates new gap issues in `.course/issues/open/`
  - [ ] Gap issues reference the originating change plan
  - [ ] `close_change_plan` raises `CurikError` if plan is not reviewed with a pass
  - [ ] `close_change_plan` moves plan file to `done/` directory
  - [ ] `close_change_plan` moves resolved issue files to `done/` directory
  - [ ] Issue frontmatter is updated to `resolved` status on close
  - [ ] Gap issues remain open and are not moved
