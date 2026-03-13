---
name: change-plan-execution
description: Step-by-step workflow for executing an approved change plan
---

# Change Plan Execution Skill

Execute an approved change plan through a structured sequence: branch,
structural moves, content edits, validation. Used by the Curriculum
Architect in Phase 3 (ongoing changes).

## When to Use

Use this skill when:
- A change plan has been approved via `approve_change_plan()`
- The plan is in `change-plan/active/` with status "approved"

## Process

### Step 1: Read the Plan

Read the approved change plan. Identify:
- Which issues it addresses
- What structural changes are needed (file moves, renames, new files)
- What content changes are needed (edits, additions, deletions)

### Step 2: Create a Branch

Create a git branch for the change set:
```
git checkout -b change/NNN-short-description
```

### Step 3: Execute Structural Changes First

Structural changes MUST come before content changes:

1. **Create new directories** if needed
2. **Move/rename files** as specified in the plan
3. **Create new stub files** via `create_lesson_stub()` if adding lessons
4. **Delete files** marked for removal (with designer confirmation)

After structural changes:
- Run `regenerate_syllabus()` to update syllabus.yaml (Tier 3–4)
- Verify the directory structure is correct

### Step 4: Execute Content Changes

For each content change in the plan:

1. Read the current file
2. Make the specified edits
3. Ensure instructor guide is complete (all 7 fields)
4. Ensure shortcode syntax is correct
5. Save the file

### Step 5: Update Supporting Files

After all content changes:

1. **Syllabus** — `regenerate_syllabus()` if any lessons were added/moved
2. **Syllabus URLs** — `write_syllabus_url()` for new pages (Tier 3–4)
3. **READMEs** — `trigger_readme_generation()` for affected modules
4. **Frontmatter** — update weights if lesson order changed

### Step 6: Validate

Run validation on affected areas:

- `validate_module(module_path)` for each changed module
- `validate_syllabus_consistency()` for Tier 3–4
- `validate_course()` if changes span multiple modules

Report any validation failures.

### Step 7: Mark as Executed

Call `execute_change_plan(plan_number)` to update the plan's status
to "executed".

### Step 8: Request Review

The reviewer agent should check the changes:
- Load `get_agent("reviewer")` + `get_skill("validation-checklist")`
- Review each item in the change plan against the actual changes
- File new issues for any gaps found

### Step 9: Close

After review:
- Call `close_change_plan(plan_number)` — moves plan and issues to done/
- Merge the branch (with designer approval)

## Execution Order Summary

```
1. Read plan
2. Branch
3. Structural moves (create, move, rename, delete)
4. regenerate_syllabus()
5. Content edits
6. write_syllabus_url() for new pages
7. trigger_readme_generation()
8. validate_module() / validate_course()
9. execute_change_plan()
10. Review
11. close_change_plan()
12. Merge branch
```

## Rules

- **Structural before content** — always
- **Validate after every batch** — don't wait until the end
- **One plan at a time** — don't interleave change plans
- **Branch per plan** — each change plan gets its own branch
