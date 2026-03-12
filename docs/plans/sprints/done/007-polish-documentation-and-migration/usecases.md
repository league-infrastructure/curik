---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 007 Use Cases

## SUC-001: End-to-end workflow test from init through validation
Parent: R1, R2, R3, R4, R7

- **Actor**: Automated test suite (simulating a Curriculum Architect agent)
- **Preconditions**: Curik is installed, no existing `.course/` directory in the test workspace
- **Main Flow**:
  1. Call `init_course()` on an empty directory
  2. Fill in all spec sections via `update_spec()` with realistic content
  3. Call `advance_phase()` to move from Phase 1 to Phase 2
  4. Call scaffolding functions to create the directory structure from the spec
  5. Create lesson stubs and instructor guide stubs in each module
  6. Run `regenerate_syllabus()` to produce `syllabus.yaml`
  7. Draft minimal lesson content in each stub (enough to pass validation)
  8. Run `validate_lesson()` on each lesson, `validate_module()` on each module, and `validate_course()` on the whole project
  9. Assert all validations pass with no errors
- **Alternate Flow** (validation failure):
  1. If any validation step fails, the test captures the error report
  2. Test fails with a clear message indicating which phase or artifact broke the chain
- **Postconditions**: A complete, valid course exists in the test directory with all phases completed, all validations passing, and `course.yml` fully populated
- **Acceptance Criteria**:
  - [ ] Test runs without manual intervention from empty directory to validated course
  - [ ] Every Curik phase transition (1 to 2) succeeds
  - [ ] Scaffolded structure matches the spec's module/lesson count
  - [ ] `validate_course()` returns no errors on the final state
  - [ ] `course.yml` contains no TBD values
  - [ ] `syllabus.yaml` is consistent with the directory structure

## SUC-002: Migrate an existing Sphinx/RST course to Curik format
Parent: R8, R9

- **Actor**: Curriculum designer (using CLI) or Curriculum Architect agent (using MCP)
- **Preconditions**: An existing course repo exists with Sphinx/RST content (`.rst` files, `conf.py`, possibly a `toctree`), Curik is installed, Pandoc is installed
- **Main Flow**:
  1. User runs `curik migrate <source-path>` (or agent calls `migrate_course` MCP tool)
  2. Curik inventories the source repo: counts `.rst` files, detects Sphinx `conf.py`, identifies `toctree` structure
  3. Curik maps the existing directory structure to Curik's module/lesson hierarchy based on `toctree` ordering
  4. Curik converts each `.rst` file to Markdown using Pandoc, preserving headings, code blocks, and images
  5. Curik copies converted files into the standard Curik directory structure (`modules/NN-name/lessons/NN-name/`)
  6. Curik generates `course.yml` from `conf.py` metadata (title, author, description) with tier and grades set to TBD for manual review
  7. Curik creates instructor guide stubs (`_instructor.md`) for each lesson
  8. Curik runs `curik init` to create the `.course/` directory and state files
  9. Curik produces a migration report listing: files converted, files skipped (binary, unknown format), fields requiring manual review
- **Alternate Flow** (Pandoc not installed):
  1. Curik detects Pandoc is unavailable
  2. Prints an error: "Pandoc is required for RST migration. Install with: brew install pandoc (macOS) or apt install pandoc (Linux)"
  3. Exits with non-zero status
- **Alternate Flow** (unrecognized repo format):
  1. Curik cannot find `conf.py` or any `.rst` files
  2. Prints a warning and falls back to a flat copy: all `.md` files are placed into a single module
  3. Migration report flags the repo as "unstructured — manual reorganization needed"
- **Postconditions**: A new directory contains the migrated course in Curik standard structure with `.course/`, `course.yml`, converted Markdown lessons, and instructor guide stubs
- **Acceptance Criteria**:
  - [ ] `.rst` files are converted to `.md` with headings, code blocks, and images intact
  - [ ] Directory structure follows `modules/NN-name/lessons/NN-name/` pattern
  - [ ] `course.yml` is generated with available metadata populated
  - [ ] Instructor guide stubs are created for every lesson
  - [ ] Migration report lists all converted, skipped, and flagged files
  - [ ] Migrated course passes `curik validate course` after TBD fields are filled in

## SUC-003: Generate and build project documentation
Parent: R1, R5, R6

- **Actor**: Developer or maintainer preparing Curik for release
- **Preconditions**: Curik source code is complete (all sprints merged), MkDocs and Material theme are installed
- **Main Flow**:
  1. Developer creates documentation source files in `docs/` covering: installation guide, quickstart tutorial, CLI reference (all subcommands), MCP tool reference (all tools with parameters and examples), agent and skill catalog, tier-specific workflow guides (tiers 1-4)
  2. Developer writes an `mkdocs.yml` configuration with navigation structure
  3. Developer runs `mkdocs build --strict` to generate the static site
  4. Build completes with no warnings or errors
  5. Developer reviews the generated site in `site/` for completeness
- **Postconditions**: A complete documentation site exists in `site/`, ready for deployment to GitHub Pages
- **Acceptance Criteria**:
  - [ ] `mkdocs build --strict` succeeds with zero warnings
  - [ ] Documentation covers: installation, quickstart, CLI reference, MCP tool reference, agent/skill catalog, tier guides
  - [ ] Every CLI subcommand is documented with usage, arguments, and examples
  - [ ] Every MCP tool is documented with parameters, return values, and error cases
  - [ ] Tier-specific guides describe the correct directory structure and workflow for each tier
  - [ ] Navigation structure is logical and complete
