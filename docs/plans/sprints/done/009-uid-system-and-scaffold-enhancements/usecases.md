---
status: draft
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 009 Use Cases

## SUC-009-001: Scaffolding a Tier 3 Course Creates Mirror Directories with UIDs
Parent: R4 (Scaffolding and Structure Generation)

- **Actor**: Curriculum Architect agent (via MCP tools)
- **Preconditions**: A course has been initialized with `init_course`. The
  `course.yml` file exists with `tier: 3` and a language field (e.g.,
  `language: python`). The course spec is complete and the project is in
  Phase 2. A structure dict has been prepared with modules and lessons.
- **Main Flow**:
  1. The agent calls `scaffold_structure(root, structure)` with a structure
     containing modules and lessons.
  2. `scaffold_structure` reads `course.yml` to determine the tier (3) and
     language (`python`).
  3. For each module, the function creates `docs/docs/<module>/` with lesson
     stub Markdown files, each containing YAML frontmatter with a generated
     8-character base62 UID.
  4. Because the tier is 3, the function also creates repo-root mirror
     directories: `lessons/<module>/` with placeholder files corresponding
     to each lesson.
  5. The function creates `projects/` as an empty directory for student
     project work.
  6. The function calls `get_devcontainer_json("python")` and writes the
     result to `.devcontainer/devcontainer.json` in the repo root.
  7. The function calls `generate_nav(structure)` to build an explicit nav
     list and passes it to `get_mkdocs_yml(title, tier, nav=nav)`. The
     resulting `mkdocs.yml` is written to `docs/mkdocs.yml`.
  8. The function returns `{"created": [...], "existing": [...]}` listing
     all created and pre-existing paths.
- **Postconditions**: The repo contains both `docs/docs/` lesson stubs (with
  UIDs in frontmatter) and repo-root `lessons/` mirror directories. A
  `.devcontainer/devcontainer.json` exists. `mkdocs.yml` contains an explicit
  `nav` section reflecting the module/lesson structure.
- **Acceptance Criteria**:
  - [x] `scaffold_structure` creates `docs/docs/<module>/` directories with lesson stubs
  - [ ] `scaffold_structure` creates repo-root `lessons/<module>/` mirror directories for Tier 3
  - [ ] `scaffold_structure` creates a `projects/` directory for Tier 3-4
  - [ ] Each lesson stub contains YAML frontmatter with a `uid:` field
  - [ ] The `uid` values are 8-character base62 strings
  - [ ] `.devcontainer/devcontainer.json` is written with the correct language config
  - [ ] `mkdocs.yml` contains a `nav:` section matching the module/lesson structure
  - [ ] For Tier 1-2, no mirror directories or `.devcontainer/` are created

## SUC-009-002: Lesson Stubs Receive Unique UIDs in Frontmatter
Parent: R4 (Scaffolding and Structure Generation)

- **Actor**: Curriculum Architect agent (via MCP tools)
- **Preconditions**: A course is initialized and in Phase 2. The agent is
  creating individual lesson stubs using `create_lesson_stub`.
- **Main Flow**:
  1. The agent calls `create_lesson_stub(root, module, lesson, tier)` to
     create a single lesson file.
  2. `create_lesson_stub` calls `generate_unit_uid()` to produce an
     8-character base62 identifier.
  3. The function writes the lesson file with YAML frontmatter at the top:
     ```
     ---
     uid: Ab3kQ9xZ
     ---
     ```
     followed by the tier-appropriate lesson content (instructor-guide-only
     for Tier 1-2, student content + instructor guide for Tier 3-4).
  4. The function returns the relative path of the created file.
- **Postconditions**: The lesson file exists with a unique UID in its YAML
  frontmatter. The UID is stable for the lifetime of the file (it is written
  once and not regenerated on subsequent operations).
- **Acceptance Criteria**:
  - [ ] `create_lesson_stub` generates a UID and writes it into frontmatter
  - [ ] The frontmatter is valid YAML between `---` delimiters
  - [ ] The UID is an 8-character base62 string
  - [ ] The rest of the lesson content is unchanged from the existing tier-appropriate template
  - [ ] If `create_lesson_stub` is called with an explicit `uid` parameter, that value is used instead of generating a new one

## SUC-009-003: mkdocs.yml Gets Explicit Nav from Course Structure
Parent: R4 (Scaffolding and Structure Generation)

- **Actor**: Curriculum Architect agent (via MCP tools)
- **Preconditions**: A course structure dict exists with modules and lessons.
  The course has been initialized and is in Phase 2.
- **Main Flow**:
  1. The agent calls `scaffold_structure(root, structure)` which internally
     calls `generate_nav(structure)`.
  2. `generate_nav` iterates over the structure's modules and lessons,
     building a list of nav entries in MkDocs format:
     ```yaml
     nav:
       - Home: index.md
       - "Module: Intro":
         - Hello: 01-intro/01-hello.md
         - Variables: 01-intro/02-variables.md
       - "Module: Data Types":
         - Strings: 02-data-types/01-strings.md
     ```
  3. The nav list is passed to `get_mkdocs_yml(title, tier, nav=nav)`.
  4. `get_mkdocs_yml` serializes the nav into the YAML config string,
     producing a complete `mkdocs.yml` with explicit navigation.
  5. The file is written to `docs/mkdocs.yml`.
- **Postconditions**: `mkdocs.yml` contains a `nav:` section that explicitly
  lists all modules and lessons in the order defined by the course structure.
  MkDocs will render navigation matching this order instead of using
  auto-discovery.
- **Acceptance Criteria**:
  - [ ] `generate_nav` produces a nav list from a structure dict
  - [ ] Nav entries use human-readable titles derived from filenames
  - [ ] Nav entries reference the correct relative paths under `docs/`
  - [ ] `get_mkdocs_yml` with a `nav` parameter includes the nav in the output
  - [ ] `get_mkdocs_yml` without a `nav` parameter omits nav (backward compatible)
  - [ ] The generated nav preserves module and lesson ordering from the structure
