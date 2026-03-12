---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 004 Use Cases

## SUC-001: Lesson Author Young Writes a Tier 1 Lesson with Instructor Guide
Parent: UC-R6 (Agent Specialization), UC-R8 (Curriculum Structure Support)

- **Actor**: Lesson Author Young agent (invoked by Curriculum Architect)
- **Preconditions**:
  - Course is in Phase 2 (scaffolding complete).
  - A lesson stub exists for the target lesson (created by `create_lesson_stub`
    with tier=1).
  - The course spec and module outline are approved.
- **Main Flow**:
  1. Curriculum Architect delegates a lesson to the Lesson Author Young agent
     by invoking the `lesson-writing-young` skill with the lesson path and
     module outline.
  2. The agent reads the lesson stub, which contains instructor guide
     placeholders for all seven required fields.
  3. The agent writes the instructor guide as the primary content: Objectives,
     Materials (physical manipulatives, printed handouts), Timing (activity
     breakdown), Key Concepts, Common Mistakes, Assessment Cues (observable
     behaviors), and Differentiation (scaffolding and extension).
  4. The agent writes student-facing activity descriptions (brief, since Tier 1
     students do not use computers -- the instructor guide drives the lesson).
  5. The agent invokes the `instructor-guide-sections` skill to self-validate
     that all seven fields are present and non-empty.
  6. If validation fails, the agent fills in missing fields and re-validates.
  7. The agent saves the completed lesson file.
- **Postconditions**:
  - The lesson file contains all seven instructor guide fields with real
    content (no "TBD" or empty sections).
  - The lesson file follows the Tier 1 template structure (instructor guide
    primary, minimal student-facing content).
- **Acceptance Criteria**:
  - [ ] Lesson Author Young agent definition exists and loads via MCP
  - [ ] `lesson-writing-young` skill definition exists and loads via MCP
  - [ ] Generated Tier 1 lesson has instructor guide as primary content
  - [ ] All seven instructor guide fields are present and non-empty
  - [ ] Student-facing section contains activity descriptions only (no code)
  - [ ] Validation function confirms all fields pass

## SUC-002: Lesson Author Older Writes a Tier 3 Lesson with Notebook and Instructor Guide
Parent: UC-R6 (Agent Specialization), UC-R8 (Curriculum Structure Support)

- **Actor**: Lesson Author Older agent (invoked by Curriculum Architect)
- **Preconditions**:
  - Course is in Phase 2 (scaffolding complete).
  - Lesson stubs exist for both the Markdown lesson and the Jupyter notebook
    (created by `create_lesson_stub` with tier=3).
  - The course spec and module outline are approved.
- **Main Flow**:
  1. Curriculum Architect delegates a lesson to the Lesson Author Older agent
     by invoking the `lesson-writing-older` skill with the lesson path, notebook
     path, and module outline.
  2. The agent reads the Markdown lesson stub, which contains inline
     `<div class="instructor-guide" markdown>` sections with placeholders.
  3. The agent writes the student-facing lesson content: explanations, code
     examples, and references to the companion notebook.
  4. The agent fills in all seven instructor guide fields within the inline
     `<div class="instructor-guide" markdown>` wrappers, covering: Objectives,
     Materials (software, accounts, repos), Timing, Key Concepts, Common
     Mistakes (code errors, misconceptions), Assessment Cues (code review
     checkpoints), and Differentiation.
  5. The agent creates or updates the companion Jupyter notebook with:
     - Markdown cells for instructions and explanations.
     - Code cells with starter code or exercises.
     - An instructor guide cell (tagged with metadata) containing answer keys
       or solution hints.
  6. The agent invokes the `instructor-guide-sections` skill to validate both
     the Markdown lesson and the notebook.
  7. If validation fails, the agent fills in missing fields and re-validates.
  8. The agent saves both files.
- **Postconditions**:
  - The Markdown lesson contains inline instructor guide sections with all
    seven fields populated.
  - The Jupyter notebook is valid nbformat v4 JSON with instruction cells,
    code cells, and an instructor guide cell.
  - Both files follow the Tier 3 template structure.
- **Acceptance Criteria**:
  - [ ] Lesson Author Older agent definition exists and loads via MCP
  - [ ] `lesson-writing-older` skill definition exists and loads via MCP
  - [ ] Generated Tier 3 Markdown lesson uses `<div class="instructor-guide" markdown>` sections
  - [ ] All seven instructor guide fields are present in the Markdown lesson
  - [ ] Companion Jupyter notebook is valid nbformat v4 JSON
  - [ ] Notebook contains instructor guide cell with metadata tag
  - [ ] Validation function confirms all fields pass for both files

## SUC-003: Agent Validates Instructor Guide Completeness
Parent: UC-R7 (Validation)

- **Actor**: Any Lesson Author agent (Young or Older)
- **Preconditions**:
  - A lesson file exists (Markdown or Jupyter notebook).
  - The lesson file contains instructor guide sections (inline or primary).
- **Main Flow**:
  1. The agent invokes the `instructor-guide-sections` skill, passing the
     lesson file path.
  2. The skill calls the instructor guide validation function, which parses
     the lesson file and checks for the presence and content of all seven
     required fields:
     - **Objectives** -- learning goals for the lesson
     - **Materials** -- what the instructor and students need
     - **Timing** -- time allocation per activity or section
     - **Key Concepts** -- core ideas the lesson teaches
     - **Common Mistakes** -- errors students typically make
     - **Assessment Cues** -- how to tell if students understand
     - **Differentiation** -- how to adjust for different ability levels
  3. For each field, the validator checks:
     - The field heading or marker is present in the file.
     - The content below the heading is non-empty.
     - The content is not a placeholder string ("TBD", "TODO", "FIXME").
  4. The validator returns a result object listing any missing or invalid
     fields with actionable messages (e.g., "Materials section is empty --
     list physical items needed for the activity").
  5. If all fields pass, the skill confirms the instructor guide is complete.
  6. If any fields fail, the agent uses the error messages to fill in the
     missing content, then re-invokes validation.
- **Postconditions**:
  - The validation result accurately reflects the state of all seven fields.
  - If the agent acts on the result, the lesson ends with all fields valid.
- **Acceptance Criteria**:
  - [ ] `instructor-guide-sections` skill definition exists and loads via MCP
  - [ ] Validation function checks all seven required fields
  - [ ] Validation detects missing field headings
  - [ ] Validation detects empty field content
  - [ ] Validation detects placeholder strings ("TBD", "TODO", "FIXME")
  - [ ] Validation returns actionable error messages per field
  - [ ] Validation works on Markdown lessons (inline div format)
  - [ ] Validation works on Jupyter notebooks (metadata-tagged cells)
  - [ ] All-pass case returns a clean result with no errors
