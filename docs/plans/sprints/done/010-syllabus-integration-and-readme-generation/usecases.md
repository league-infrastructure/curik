---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 010 Use Cases

## SUC-001: Syllabus-Driven Page Creation with URL Writeback
Parent: R3 (Phase 2 -- Scaffold and Draft), R5 (MCP Server with Enforcement Tools)

- **Actor**: Curriculum Architect agent
- **Preconditions**:
  - Course repository has been scaffolded (directory structure exists)
  - `syl compile` has been run, producing a valid syllabus.yaml
  - Lesson entries in syllabus.yaml have `uid` fields (from Sprint 009 UID system)
  - MkDocs pages have been created with matching `uid` fields in frontmatter
- **Main Flow**:
  1. Agent calls `read_syllabus_entries` to retrieve the list of lesson entries from syllabus.yaml, receiving structured data with uid, path, title, and url fields for each entry.
  2. Agent iterates through entries, identifying entries where the `url` field is empty or missing.
  3. For each entry that now has a corresponding MkDocs page, agent calls `write_syllabus_url` with the entry's UID and the page URL.
  4. `write_syllabus_url` locates the entry in syllabus.yaml by UID, writes the url field, and preserves the rest of the YAML structure.
  5. Agent calls `read_syllabus_entries` again to verify the url fields are populated.
- **Postconditions**:
  - syllabus.yaml contains url fields for all entries that have corresponding MkDocs pages.
  - The YAML file is well-formed and parseable by the `syl` tool.
  - No other fields in syllabus.yaml have been modified.
- **Acceptance Criteria**:
  - [ ] `read_syllabus_entries` returns a JSON array of entry objects with uid, path, title, and url keys
  - [ ] Entries without a url field return url as null in the response
  - [ ] `write_syllabus_url` updates exactly one entry identified by UID
  - [ ] `write_syllabus_url` returns an error if the UID is not found in syllabus.yaml
  - [ ] After writing, syllabus.yaml is valid YAML and preservable by `syl compile`
  - [ ] Round-trip test: read entries, write urls, read again -- urls match what was written

## SUC-002: README Generation from MkDocs Page Guards
Parent: R3 (Phase 2 -- Scaffold and Draft), R8 (Curriculum Structure Support)

- **Actor**: Lesson Author (Older, Tiers 3-4) agent
- **Preconditions**:
  - MkDocs lesson pages exist with content authored
  - Lesson pages contain `<!-- readme-shared -->` and/or `<!-- readme-only -->` comment guards wrapping content sections
  - Repo-root lesson directories exist (the directories students see on GitHub)
- **Main Flow**:
  1. Agent finishes writing a lesson's MkDocs page, including placing comment guards around sections appropriate for the README (introductions, setup instructions, exercise descriptions).
  2. Agent calls `trigger_readme_generation` with the path to the MkDocs page (or a module/course-wide scope).
  3. The tool reads the MkDocs Markdown source and extracts content within `<!-- readme-shared -->...<!-- /readme-shared -->` blocks (shared between MkDocs and README) and `<!-- readme-only -->...<!-- /readme-only -->` blocks (README-exclusive content like "view the full lesson at [url]" links).
  4. The tool assembles the extracted sections in document order into a README.md file.
  5. The tool writes README.md to the corresponding repo-root lesson directory, determined by matching the MkDocs page path to the repository directory structure.
  6. The tool returns a summary of generated READMEs with their file paths.
- **Postconditions**:
  - README.md files exist in repo-root lesson directories for all processed pages.
  - README content matches the guarded sections from the MkDocs source, in order.
  - Pages with no comment guards produce no README (no empty files).
- **Acceptance Criteria**:
  - [ ] `<!-- readme-shared -->` content appears in both the MkDocs rendered page and the README
  - [ ] `<!-- readme-only -->` content appears only in the README, not rendered by MkDocs
  - [ ] Multiple guard blocks per page are concatenated in document order
  - [ ] Guard blocks can contain any valid Markdown (headings, code blocks, lists, images)
  - [ ] Pages with no guards are skipped -- no README.md is created or overwritten
  - [ ] Existing README.md files are overwritten with fresh content on regeneration
  - [ ] The tool reports which READMEs were generated and their paths

## SUC-003: Syllabus Consistency Validation
Parent: R7 (Validation)

- **Actor**: Reviewer agent
- **Preconditions**:
  - syllabus.yaml exists and contains lesson entries with uid fields
  - MkDocs lesson pages exist with uid fields in frontmatter
  - Course scaffolding is complete
- **Main Flow**:
  1. Agent calls `validate_syllabus_consistency` to check the alignment between syllabus.yaml entries and MkDocs pages.
  2. The tool reads all entries from syllabus.yaml and all MkDocs page frontmatter.
  3. The tool checks for: (a) syllabus entries with no corresponding MkDocs page (by UID), (b) MkDocs pages with no corresponding syllabus entry (by UID), (c) UID mismatches where path suggests a match but UIDs differ, (d) entries with empty url fields that have corresponding pages.
  4. The tool returns a structured report with lists of issues found in each category.
  5. If all checks pass, the tool returns a clean report indicating full consistency.
- **Postconditions**:
  - Agent has a clear list of inconsistencies to resolve, or confirmation that syllabus and pages are aligned.
- **Acceptance Criteria**:
  - [ ] Orphaned syllabus entries (no matching page) are reported with entry path and UID
  - [ ] Orphaned MkDocs pages (no matching syllabus entry) are reported with file path and UID
  - [ ] UID mismatches between path-matched entries and pages are flagged
  - [ ] Entries with missing url fields are listed separately as warnings
  - [ ] A fully consistent course produces a clean report with zero issues
  - [ ] The report is returned as structured JSON suitable for programmatic processing
