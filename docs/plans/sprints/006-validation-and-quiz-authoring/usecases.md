---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 006 Use Cases

## SUC-006-001: Reviewer Validates a Lesson
Parent: R7 (Validation)

- **Actor**: Reviewer agent
- **Preconditions**: A lesson file exists in the course directory structure.
  The lesson has been drafted by a Lesson Author agent. The course has been
  initialized and is in Phase 2 or later.
- **Main Flow**:
  1. Reviewer agent calls `validate_lesson(lesson_path)`.
  2. The tool reads the lesson file and checks for required instructor guide
     sections (Overview, Materials, Preparation, Lesson Plan, Assessment Notes,
     Differentiation) -- each must be present and non-empty.
  3. The tool checks that a learning objectives section exists with at least
     one objective listed.
  4. The tool reads `syllabus.yaml` and verifies the lesson file is referenced.
  5. The tool returns a validation result: `{"valid": true/false, "errors": [...], "warnings": [...]}`.
  6. If errors are found, the Reviewer creates issues in `.course/issues/open/`
     for each failure, referencing the lesson path and the specific missing element.
- **Postconditions**: The lesson's validation status is known. Any failures
  are recorded as issues that can be addressed through the change cycle.
- **Acceptance Criteria**:
  - [ ] `validate_lesson` returns `valid: true` for a lesson with all required sections present and non-empty
  - [ ] `validate_lesson` returns `valid: false` with specific error messages when instructor guide sections are missing
  - [ ] `validate_lesson` returns `valid: false` when learning objectives are missing or empty
  - [ ] `validate_lesson` returns `valid: false` when the lesson is not referenced in `syllabus.yaml`
  - [ ] Validation handles tier-specific requirements (Tier 1 lessons are instructor-guide-only; Tier 3+ lessons require student-facing content)

## SUC-006-002: Quiz Author Creates Quiz Configuration Aligned to Lesson Objectives
Parent: R7 (Validation), R5 (MCP Server with Enforcement Tools)

- **Actor**: Quiz Author agent
- **Preconditions**: A lesson exists with defined learning objectives. The
  lesson has passed `validate_lesson` (objectives are present and non-empty).
- **Main Flow**:
  1. Quiz Author agent calls `generate_quiz_stub(lesson_path)`.
  2. The tool reads the lesson's learning objectives.
  3. The tool generates a `quiz.yml` file in the lesson directory with:
     - `topics`: one entry per learning objective, derived from the objective text
     - `difficulty`: default "medium"
     - `question_types`: default `["multiple_choice", "short_answer"]`
     - `example_questions`: empty list (optional, to be filled by Quiz Author)
     - `status`: "draft"
  4. Quiz Author reviews the stub and edits `quiz.yml` to refine topics,
     adjust difficulty, add example questions if desired.
  5. Quiz Author calls `validate_quiz_alignment(lesson_path)` to verify that
     quiz topics cover all lesson objectives.
  6. The tool compares quiz topics against lesson objectives and reports any
     objectives not covered by a quiz topic.
  7. Once aligned, Quiz Author calls `set_quiz_status(lesson_path, "review")`
     to mark the quiz ready for review.
- **Postconditions**: A `quiz.yml` file exists for the lesson with topics
  aligned to learning objectives. The quiz status is set to "review".
- **Acceptance Criteria**:
  - [ ] `generate_quiz_stub` creates a valid `quiz.yml` file in the lesson directory
  - [ ] Generated topics correspond to the lesson's learning objectives
  - [ ] `quiz.yml` follows the defined schema (topics, difficulty, question_types, example_questions, status)
  - [ ] `validate_quiz_alignment` returns success when all objectives are covered by quiz topics
  - [ ] `validate_quiz_alignment` returns failure with specific messages when objectives are uncovered
  - [ ] `set_quiz_status` transitions the quiz status and writes it to `quiz.yml`
  - [ ] `generate_quiz_stub` fails with a clear error if the lesson has no learning objectives

## SUC-006-003: Full Course Validation Before Publication
Parent: R7 (Validation), R9 (Course Metadata and Registry Integration)

- **Actor**: Reviewer agent
- **Preconditions**: All modules and lessons have been drafted. Quiz
  configuration files exist for lessons that require them. The course has
  a `course.yml` and `syllabus.yaml`.
- **Main Flow**:
  1. Reviewer agent calls `get_validation_report(course_root)`.
  2. The tool runs `validate_course`, which internally:
     a. Iterates over all modules, calling `validate_module` for each.
     b. Each `validate_module` call iterates over lessons, calling
        `validate_lesson` for each.
     c. Checks that `course.yml` has no TBD placeholder values.
     d. Runs `mkdocs build --strict` and checks for build errors.
     e. Compares `syllabus.yaml` entries against the actual directory tree
        to detect orphaned files or missing references.
  3. The tool aggregates all results into a structured report:
     ```json
     {
       "valid": false,
       "course": {"valid": false, "errors": [...]},
       "modules": [
         {"path": "module-01", "valid": true, "errors": []},
         {"path": "module-02", "valid": false, "errors": [...]}
       ],
       "lessons": [
         {"path": "module-01/lesson-01", "valid": true, "errors": []},
         ...
       ],
       "quizzes": [
         {"path": "module-01/lesson-01/quiz.yml", "aligned": true, "status": "approved"},
         ...
       ]
     }
     ```
  4. Reviewer presents the report to the Curriculum Architect.
  5. If the report shows failures, the Curriculum Architect files issues
     through the change cycle (Sprint 5 tooling) and assigns them for
     remediation.
  6. After fixes, the Reviewer reruns validation until the course passes.
- **Postconditions**: The course is confirmed valid at all levels, or a
  clear list of failures exists as actionable issues.
- **Acceptance Criteria**:
  - [ ] `get_validation_report` produces a structured report covering course, module, lesson, and quiz levels
  - [ ] Report correctly aggregates pass/fail from all nested validations
  - [ ] Course validation fails when `course.yml` contains TBD values
  - [ ] Course validation fails when `syllabus.yaml` references files that do not exist
  - [ ] Course validation fails when directory tree contains lesson files not in `syllabus.yaml`
  - [ ] Course validation reports MkDocs build errors when `mkdocs build --strict` fails
  - [ ] A fully valid course produces a report with `valid: true` at all levels
