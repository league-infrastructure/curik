---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 008 Use Cases

## SUC-001: Initialize a Resource Collection Project
Parent: N/A

- **Actor**: Curriculum designer (via Claude agent or CLI)
- **Preconditions**: The designer has an empty or new directory for the project. Curik is installed.
- **Main Flow**:
  1. The designer calls `init_course` with `course_type="resource-collection"`.
  2. Curik creates the `.curik/` directory structure (same as a standard course).
  3. Curik writes `state.json` with `{"phase": "phase1", "type": "resource-collection"}`.
  4. Curik writes `course.yml` with a `type: resource-collection` field included alongside the standard metadata fields.
  5. Curik writes `spec.md` with the standard section headings (all seven sections are present in the template, but only five are required for advancement).
  6. Curik writes `.mcp.json` for agent connectivity.
  7. Curik returns the lists of created and existing files.
- **Postconditions**: The project directory contains a fully initialized Curik project with type `resource-collection` in both `state.json` and `course.yml`. The designer can begin the abbreviated Phase 1 process.
- **Acceptance Criteria**:
  - [x] `state.json` contains `"type": "resource-collection"`
  - [x] `course.yml` contains `type: resource-collection`
  - [x] All standard `.curik/` directories are created
  - [x] Calling `init_course` without `course_type` produces `"type": "course"` (backward compatibility)
  - [x] Calling `init_course` with an invalid type raises `CurikError`

## SUC-002: Abbreviated Phase 1 for Resource Collection
Parent: N/A

- **Actor**: Curriculum designer (via Claude agent)
- **Preconditions**: A resource collection project has been initialized (SUC-001 completed). The project is in phase1.
- **Main Flow**:
  1. The designer loads the `resource-collection-spec` skill definition to understand the abbreviated workflow.
  2. The designer completes the course-concept section (Phase 1a) using `record_course_concept`.
  3. The designer completes the research-summary section (Phase 1c) using `update_spec`.
  4. The designer completes the course-structure-outline section (Phase 1e) using `update_spec`.
  5. The designer completes the assessment-plan section (Phase 1e) using `update_spec`.
  6. The designer completes the technical-decisions section (Phase 1e) using `update_spec`.
  7. The designer calls `advance_phase("phase2")`.
  8. `advance_phase` reads the course type from `state.json`, determines that `pedagogical-model` and `alignment-decision` are not required, and checks only the five required sections.
  9. All five sections have non-placeholder content. The phase advances to phase2.
- **Postconditions**: `state.json` phase is `"phase2"`. The designer did not need to fill in pedagogical-model or alignment-decision sections.
- **Acceptance Criteria**:
  - [x] `advance_phase("phase2")` succeeds when the five required sections are filled and the two skipped sections remain "TBD"
  - [x] `advance_phase("phase2")` fails if any of the five required sections is still "TBD"
  - [x] `advance_phase("phase2")` for a standard `course` type still requires all seven sections
  - [x] The `resource-collection-spec` skill definition documents exactly which phases are included and which are skipped

## SUC-003: Scaffold Resource Collection Directory Layout
Parent: N/A

- **Actor**: Curriculum designer (via Claude agent or CLI)
- **Preconditions**: A resource collection project is in phase2. The designer has a structure definition describing the resource categories and pages.
- **Main Flow**:
  1. The designer calls `scaffold_structure` with a structure JSON that describes resource categories and pages. The structure format uses `categories` instead of `modules` and `pages` instead of `lessons`:
     ```json
     {"categories": [
       {"name": "01-getting-started", "pages": ["overview.md", "setup-guide.md"]},
       {"name": "02-activities", "pages": ["activity-01.md", "activity-02.md"]}
     ]}
     ```
  2. `scaffold_structure` reads the course type from `state.json`.
  3. For a resource collection, it creates directories under the project root using the category names directly (same top-level placement as modules for standard courses).
  4. For each page, it creates a stub file with a title derived from the filename and a simple content placeholder (no instructor guide div, since resource pages are reference material).
  5. The function returns lists of created and existing paths.
- **Postconditions**: The project directory contains the resource collection directory tree with stub pages. The stubs use a simpler format than lesson stubs (no instructor guide section).
- **Acceptance Criteria**:
  - [x] `scaffold_structure` creates category directories and page stub files for resource collections
  - [x] Resource page stubs contain a title heading and a content placeholder but no instructor guide div
  - [x] Standard course scaffolding (modules/lessons) is unchanged
  - [x] The function returns accurate created/existing lists
