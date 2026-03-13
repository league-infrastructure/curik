---
status: draft
---

# Sprint 024 Use Cases

## SUC-001: Scaffold produces a runnable Hugo site
Parent: TODO-001

- **Actor**: Curik MCP server (called by curriculum agent)
- **Preconditions**: Course initialized with `tool_init_course()`, structure
  defined via outline
- **Main Flow**:
  1. Agent calls `tool_scaffold_structure()` with module/lesson structure
  2. Curik creates `content/` directory with modules and lesson stubs
  3. Curik generates `hugo.toml` with course title and tier config
  4. Curik copies `curriculum-hugo-theme` into `themes/`
  5. Agent (or developer) runs `hugo build` or `hugo server`
  6. Hugo builds successfully and serves a working site
- **Postconditions**: Complete Hugo project at repo root with `content/`,
  `hugo.toml`, and `themes/curriculum-hugo-theme/`
- **Acceptance Criteria**:
  - [ ] `content/` contains `_index.md` and module subdirectories
  - [ ] `hugo.toml` exists with correct title and theme reference
  - [ ] `themes/curriculum-hugo-theme/` exists with shortcode templates
  - [ ] `hugo build` succeeds with zero errors

## SUC-002: Integration test copies fixture and runs operations
Parent: (new)

- **Actor**: Developer running `pytest`
- **Preconditions**: `tests/content_source/python-basics/` exists with
  a complete curriculum fixture
- **Main Flow**:
  1. Test copies `content_source/python-basics/` to `content_test/python-basics/`
  2. Test sets project root to the scratch copy
  3. Test calls `scaffold_structure()` with a predefined structure
  4. Test calls `hugo_build()` and asserts success
  5. Scratch directory persists for manual inspection
- **Postconditions**: `tests/content_test/python-basics/` contains a
  complete, buildable Hugo site
- **Acceptance Criteria**:
  - [ ] Fixture is never modified by tests
  - [ ] Scratch copy is gitignored
  - [ ] Test passes when Hugo is installed
  - [ ] Test skips gracefully when Hugo is not installed

## SUC-003: Multiple curriculum types have fixtures
Parent: (new)

- **Actor**: Developer writing or running tests
- **Preconditions**: Test framework supports multiple source directories
- **Main Flow**:
  1. Developer creates a new fixture in `content_source/` for a different
     curriculum type (e.g., web-dev, tier 3)
  2. Tests parameterize over available fixtures
  3. Each fixture produces a working Hugo site with type-appropriate content
- **Postconditions**: Multiple fixture directories exist, each representing
  a distinct curriculum type
- **Acceptance Criteria**:
  - [ ] At least two fixtures: `python-basics` (tier 2) and `web-dev` (tier 3)
  - [ ] Both produce buildable Hugo sites
  - [ ] Fixtures contain realistic course.yml and .course/ metadata
