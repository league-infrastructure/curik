---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 011 Use Cases

## SUC-001: Tier 3 Lesson Fails Validation When Comment Guards Are Missing

Parent: (none — new validation coverage)

- **Actor**: Course designer or CI pipeline invoking `validate_lesson()`
- **Preconditions**:
  - A Tier 3 or Tier 4 course repository exists with at least one lesson
    file under `modules/`.
  - The lesson file does not contain a `<!-- readme-shared -->` comment
    guard.
- **Main Flow**:
  1. The actor calls `validate_lesson(root, lesson_path, tier=3)`.
  2. The validator opens the lesson file and runs the standard checks
     (instructor guide fields, learning objectives section).
  3. Because `tier` is 3, the validator additionally scans the file
     content for the `<!-- readme-shared -->` comment guard.
  4. The guard is not found. The validator appends the error
     "Missing <!-- readme-shared --> comment guard (required for Tier 3-4)"
     to the error list.
  5. The validator returns `{"valid": False, "errors": [...]}` with the
     guard error included.
- **Postconditions**:
  - The validation result contains a clear error identifying the missing
    comment guard.
  - No file modifications are made.
- **Alternative Flow — Guard Present**:
  1. If the lesson file contains `<!-- readme-shared -->`, the guard check
     passes silently and does not add an error.
- **Alternative Flow — Tier 1-2**:
  1. If `tier` is 1, 2, or `None`, the guard check is skipped entirely.
     The function behaves identically to the pre-sprint implementation.
- **Acceptance Criteria**:
  - [ ] `validate_lesson(root, path, tier=3)` returns an error when the
        lesson lacks `<!-- readme-shared -->`
  - [ ] `validate_lesson(root, path, tier=3)` passes when the guard is
        present
  - [ ] `validate_lesson(root, path, tier=2)` does not check for the guard
  - [ ] `validate_lesson(root, path)` (no tier) does not check for the guard


## SUC-002: Tier 3 Course Fails Validation When Syllabus Entries Do Not Match MkDocs Pages

Parent: (none — new validation coverage)

- **Actor**: Course designer or CI pipeline invoking `validate_course()`
- **Preconditions**:
  - A Tier 3 or Tier 4 course repository exists with `course.yml`
    containing `tier: 3` (or `tier: 4`).
  - The repository has a `syllabus.yaml` file and an `mkdocs.yml` file.
  - At least one entry in `syllabus.yaml` references a lesson that does
    not appear in the `mkdocs.yml` `nav` section, or a nav entry has no
    corresponding syllabus record.
  - At least one module directory is missing its expected README in the
    repo-root mirror directory.
- **Main Flow**:
  1. The actor calls `validate_course(root)`.
  2. The validator reads `course.yml` and determines the tier is 3 or 4.
  3. The validator calls `validate_syllabus_consistency(root)` which:
     a. Parses `syllabus.yaml` to get the list of lesson UIDs and paths.
     b. Parses `mkdocs.yml` to get the nav page list.
     c. Compares the two lists and reports entries present in one but not
        the other.
  4. The validator checks that each module directory listed in the syllabus
     has a corresponding README file in the repo-root mirror directory
     structure.
  5. The validator returns `{"valid": False, "errors": [...]}` with errors
     for each mismatch and each missing README.
- **Postconditions**:
  - The validation result lists every syllabus/nav mismatch and every
    missing README.
  - No file modifications are made.
- **Alternative Flow — Everything Consistent**:
  1. If all syllabus entries match nav pages and all READMEs exist, the
     consistency checks pass and add no errors.
- **Alternative Flow — Tier 1-2 Course**:
  1. If `course.yml` has `tier: 1` or `tier: 2`, the syllabus consistency
     and README checks are skipped. The function behaves identically to
     the pre-sprint implementation.
- **Alternative Flow — No syllabus.yaml**:
  1. If `syllabus.yaml` does not exist for a Tier 3-4 course, the
     validator reports a single error: "syllabus.yaml not found (required
     for Tier 3-4 courses)".
- **Acceptance Criteria**:
  - [ ] `validate_course()` on a Tier 3 course with mismatched syllabus
        and nav entries reports each mismatch
  - [ ] `validate_course()` on a Tier 3 course with missing mirror-dir
        READMEs reports each missing file
  - [ ] `validate_course()` on a Tier 3 course with no syllabus.yaml
        reports the missing-file error
  - [ ] `validate_course()` on a Tier 1 course skips syllabus checks
  - [ ] `validate_course()` on a consistent Tier 3 course passes


## SUC-003: Agent Loads Infrastructure Skill to Understand Conventions

Parent: (none — new skill definitions)

- **Actor**: An AI agent operating within a Curik-managed course repository
- **Preconditions**:
  - The agent has access to the Curik MCP server.
  - The agent needs to understand one of: repository directory structure
    conventions, status-tracking file formats, or syllabus integration
    workflow.
- **Main Flow**:
  1. The agent calls `list_skills()` and sees `repo-scaffolding`,
     `status-tracking`, and `syllabus-integration` in the results.
  2. The agent calls `get_skill_definition("repo-scaffolding")` (or one
     of the other two).
  3. The MCP server reads the corresponding Markdown file from
     `curik/skills/` and returns its content.
  4. The agent parses the skill definition to learn the expected directory
     layout, file naming conventions, and tool usage patterns.
  5. The agent applies this knowledge when scaffolding a new repository,
     creating status-tracking files, or interacting with syllabus.yaml.
- **Postconditions**:
  - The agent has loaded a complete, actionable skill definition.
  - No files are modified by loading the skill.
- **Acceptance Criteria**:
  - [ ] `get_skill_definition("repo-scaffolding")` returns content
        documenting directory structure by tier/type, stub templates,
        mkdocs.yml generation, and .devcontainer config
  - [ ] `get_skill_definition("status-tracking")` returns content
        documenting .curik/ directory structure, issue and change plan
        formats, and state transitions
  - [ ] `get_skill_definition("syllabus-integration")` returns content
        documenting how Curik reads and writes syllabus.yaml, triggers
        syl compile, and coordinates with README generation
  - [ ] All three skills appear in the output of `list_skills()`
