---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 004 Use Cases

## SUC-001: Lesson Author Young Writes a Tier 1 Lesson with Instructor Guide

Parent: UC-R6 (Agent Specialization), UC-R8 (Curriculum Structure Support)

- **Actor**: Lesson Author Young agent
- **Preconditions**:
  - Course is in Phase 2 with an approved outline.
  - Lesson stub exists at the target path (created by Sprint 003 scaffolding).
  - The stub contains empty instructor guide `<div>` sections with all 7 field
    headings.
  - `course.yml` specifies `tier: 1` or `tier: 2`.
- **Main Flow**:
  1. Curriculum Architect invokes the Lesson Author Young agent for a specific
     lesson stub.
  2. Agent loads the `lesson-writing-young` skill definition.
  3. Agent reads the lesson stub and the approved outline for this lesson.
  4. Agent writes the instructor guide as the primary content — the instructor
     guide IS the lesson for Tier 1. Student-facing content is minimal or
     absent (students do not use computers at this tier).
  5. Agent fills all 7 required instructor guide fields inside the
     `<div class="instructor-guide" markdown>` section:
     - Objectives (what students will learn)
     - Materials (physical supplies needed)
     - Timing (minute-by-minute breakdown)
     - Key Concepts (core ideas to convey)
     - Common Mistakes (anticipated misconceptions)
     - Assessment Cues (how to check understanding without a quiz)
     - Differentiation (adjustments for different skill levels)
  6. Agent writes activity descriptions that are physical and hands-on (no
     screen-based activities for Tier 1).
  7. Agent saves the completed lesson file.
  8. Agent calls `validate_instructor_guide` on the saved file.
  9. Validation passes — all 7 fields present and non-empty.
- **Postconditions**:
  - Lesson file contains a complete instructor guide with all 7 fields filled.
  - Activities described are appropriate for grades 2-5 (physical, hands-on).
  - Validation returns no errors.
- **Acceptance Criteria**:
  - [ ] Lesson Author Young agent definition is loaded and used.
  - [ ] `lesson-writing-young` skill is followed during authoring.
  - [ ] All 7 instructor guide fields are present and non-empty.
  - [ ] No screen-based or coding activities appear in Tier 1 output.
  - [ ] `validate_instructor_guide` returns zero errors.

## SUC-002: Lesson Author Older Writes a Tier 3 Lesson with Notebook and Instructor Guide

Parent: UC-R6 (Agent Specialization), UC-R8 (Curriculum Structure Support)

- **Actor**: Lesson Author Older agent
- **Preconditions**:
  - Course is in Phase 2 with an approved outline.
  - Lesson stub (Markdown) and notebook stub (.ipynb) exist at the target path.
  - `course.yml` specifies `tier: 3` or `tier: 4`.
- **Main Flow**:
  1. Curriculum Architect invokes the Lesson Author Older agent for a specific
     lesson.
  2. Agent loads the `lesson-writing-older` skill definition.
  3. Agent reads the Markdown lesson stub, the notebook stub, and the approved
     outline for this lesson.
  4. Agent writes student-facing content in the Markdown lesson file — concept
     explanations, code examples, links to the notebook.
  5. Agent fills the inline instructor guide `<div class="instructor-guide" markdown>`
     section in the Markdown file with all 7 required fields. For Tiers 3-4 the
     instructor guide is supplementary (students read the main content directly).
  6. Agent populates the Jupyter notebook with:
     - Markdown cells for instructions and explanations.
     - Code cells with starter code or exercises.
     - An instructor guide cell (Markdown cell with `instructor-guide` tag in
       cell metadata) containing solution hints and teaching notes.
  7. Agent saves both the lesson Markdown and the notebook.
  8. Agent calls `validate_instructor_guide` on the Markdown file.
  9. Validation passes.
- **Postconditions**:
  - Markdown lesson has student-facing content and a complete inline instructor
    guide section.
  - Jupyter notebook is valid, contains instruction cells, code cells, and an
    instructor guide cell.
  - Validation returns no errors for the Markdown file.
- **Acceptance Criteria**:
  - [ ] Lesson Author Older agent definition is loaded and used.
  - [ ] `lesson-writing-older` skill is followed during authoring.
  - [ ] Markdown file contains `<div class="instructor-guide" markdown>` with
        all 7 fields.
  - [ ] Jupyter notebook is valid JSON and opens without error.
  - [ ] Notebook contains at least one instructor guide cell tagged in metadata.
  - [ ] `validate_instructor_guide` returns zero errors for the Markdown file.

## SUC-003: Validate That All Instructor Guide Fields Are Present

Parent: UC-R7 (Validation)

- **Actor**: Any agent (typically invoked by Lesson Author or Reviewer)
- **Preconditions**:
  - A lesson Markdown file exists with an instructor guide `<div>` section.
- **Main Flow**:
  1. Agent calls `validate_instructor_guide(file_path)`.
  2. Validator opens the file and locates all
     `<div class="instructor-guide" markdown>` sections.
  3. For each section, validator checks for the 7 required field headings:
     Objectives, Materials, Timing, Key Concepts, Common Mistakes, Assessment
     Cues, Differentiation.
  4. For each field heading found, validator checks that the content below it
     is non-empty (not blank, not "TBD", not placeholder text).
  5. Validator returns a result object:
     - `valid: true/false`
     - `errors: [list of {field, message} objects]`
     - `file: path`
- **Postconditions**:
  - Caller receives a structured validation result.
  - If errors exist, each error identifies the specific missing or empty field
    and its location.
- **Acceptance Criteria**:
  - [ ] Validation detects a missing field heading and returns an error naming
        that field.
  - [ ] Validation detects an empty field (heading present, no content) and
        returns an error.
  - [ ] Validation detects "TBD" placeholder content and returns an error.
  - [ ] Validation returns `valid: true` when all 7 fields are present and
        filled with real content.
  - [ ] Validation handles files with multiple instructor guide `<div>` sections
        (checks each independently).
