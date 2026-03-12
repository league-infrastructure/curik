---
id: "005"
title: "Change Cycle and Issue Management"
status: planning
branch: sprint/005-change-cycle-and-issue-management
use-cases: [SUC-001, SUC-002, SUC-003]
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 005: Change Cycle and Issue Management

## Goals

Implement the full iterative change cycle that supports post-draft curriculum
improvement. After initial content is authored (Sprints 3-4), designers and
reviewers need a structured process to file issues, collect them into change
plans, execute approved changes, and close completed work. This sprint delivers
seven MCP tools (`create_issue`, `list_issues`, `create_change_plan`,
`approve_change_plan`, `execute_change_plan`, `review_change_plan`,
`close_change_plan`) and the `status-tracking` skill.

## Problem

Once a course has been drafted, there is no structured mechanism for iterative
improvement. Designers notice problems (missing content, incorrect sequencing,
broken references) but have no way to file them as trackable issues. Agents
making ad-hoc fixes risk introducing inconsistencies because there is no
approval gate, no execution ordering, and no review step. Without a formal
change cycle, improvements are uncoordinated and unverifiable.

The existing codebase already creates the directory structure for issues and
change plans during `init_course` (`.course/issues/open/`,
`.course/issues/done/`, `.course/change-plan/active/`,
`.course/change-plan/done/`) but provides no tools to manage files in those
directories.

## Solution

Build a six-phase change cycle managed entirely through file-based state in the
`.course/` directory:

1. **Comment** -- Designer files numbered issues to `.course/issues/open/` via
   `create_issue`. Each issue is a Markdown file with YAML frontmatter tracking
   status, category, and priority.
2. **Collect** -- Agent synthesizes open issues into a change plan via
   `create_change_plan`. The plan lives in `.course/change-plan/active/` and
   references the issues it addresses.
3. **Approve** -- Human-gated approval via `approve_change_plan`. The plan's
   frontmatter is updated with approval timestamp and approver. No execution
   can proceed without approval.
4. **Execute** -- Agent works through the plan via `execute_change_plan`.
   Execution follows strict ordering: structural moves first, content changes
   second, then `syl` regeneration. Progress is tracked in the plan file.
5. **Review** -- Reviewer checks changes line by line via `review_change_plan`.
   Gaps are filed as new issues. The review result (passed/failed) is recorded.
6. **Close** -- `close_change_plan` moves the plan to `done/` and resolved
   issues to `issues/done/`.

The `status-tracking` skill provides a dashboard view of open issues, active
plans, and their current phase.

## Success Criteria

- All seven MCP tools are implemented and registered in the MCP server.
- Issues can be created, listed, and transition from `open` to `done`.
- Change plans can be created from open issues, approved, executed, reviewed,
  and closed.
- The approval gate blocks execution of unapproved plans.
- Execution ordering is enforced (structural, then content, then syl).
- Review can flag gaps as new issues without losing the review context.
- The `status-tracking` skill returns a structured summary of all open issues
  and active change plans.
- All existing tests continue to pass; new tests cover each tool and the full
  cycle end-to-end.

## Scope

### In Scope

- `create_issue` MCP tool -- creates numbered issue files in `.course/issues/open/`
- `list_issues` MCP tool -- lists issues filtered by status (open/done/all)
- `create_change_plan` MCP tool -- synthesizes open issues into a change plan
- `approve_change_plan` MCP tool -- records human approval in plan frontmatter
- `execute_change_plan` MCP tool -- tracks execution progress with ordering enforcement
- `review_change_plan` MCP tool -- records review result, files gap issues
- `close_change_plan` MCP tool -- moves plan and resolved issues to done directories
- `status-tracking` skill definition
- Issue file format (Markdown with YAML frontmatter)
- Change plan file format (Markdown with YAML frontmatter)
- Auto-incrementing issue and plan numbering
- Unit tests for each tool function
- Integration test for the full create-approve-execute-review-close cycle

### Out of Scope

- Lesson validation (Sprint 6)
- Quiz authoring or validation (Sprint 6)
- Agent definitions for the Reviewer role (Sprint 6 -- this sprint builds the
  tools the Reviewer will use)
- Automatic change detection or diff generation
- Git integration (commits, branches) within the change cycle -- this is
  file-based state only
- Notifications or webhooks

## Test Strategy

**Unit tests** for each of the seven tool functions in `tests/test_change_cycle.py`:
- `create_issue`: verifies file creation, auto-numbering, frontmatter format
- `list_issues`: verifies filtering by status, correct parsing of frontmatter
- `create_change_plan`: verifies plan creation from open issues, reference linking
- `approve_change_plan`: verifies approval gate sets timestamp, blocks re-approval
- `execute_change_plan`: verifies ordering enforcement, progress tracking
- `review_change_plan`: verifies review recording, gap issue creation
- `close_change_plan`: verifies file moves to done directories

**Integration test** for the full cycle: create issues, collect into plan,
approve, execute, review (with a gap), close, verify gap issue remains open.

**Error case tests**: attempt to execute unapproved plan, attempt to close
plan with unresolved issues, attempt to create plan with no open issues.

## Architecture Notes

- All state is file-based in `.course/` -- no database, consistent with the
  existing design in `project.py`.
- Issue files use auto-incrementing numbers: `001.md`, `002.md`, etc. The next
  number is derived by scanning the `open/` and `done/` directories.
- Change plan files also use auto-incrementing numbers in the same pattern.
- The approval gate is enforced by checking the `approved` field in plan
  frontmatter. `execute_change_plan` raises `CurikError` if the plan is not
  approved.
- Execution ordering is tracked via a `steps` list in plan frontmatter, each
  with a `type` (structural/content/syl) and `status` (pending/done). The tool
  enforces that all structural steps complete before content steps begin, and
  all content steps complete before syl steps.
- The new functions will be added to a new module `curik/change_cycle.py` and
  registered in both the CLI and MCP server.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
