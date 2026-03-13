---
status: draft
---

# Sprint 015 Use Cases

## SUC-001: Generate lesson stubs with Hugo shortcodes
Parent: UC-002

- **Actor**: AI agent via MCP
- **Preconditions**: Project initialized, structure defined
- **Main Flow**:
  1. Agent calls scaffold_structure or create_lesson_stub
  2. System generates lesson stubs with Hugo shortcode syntax
  3. Instructor guide uses `{{</* instructor-guide */>}}` shortcode
- **Postconditions**: Lesson files contain Hugo shortcodes, not HTML divs
- **Acceptance Criteria**:
  - [ ] Tier 1-2 stubs use `{{</* instructor-guide */>}}` shortcode
  - [ ] Tier 3-4 stubs use shortcode with student content section
  - [ ] No `<div class="instructor-guide">` in generated content

## SUC-002: Validate lessons with Hugo shortcode patterns
Parent: UC-006

- **Actor**: AI agent via MCP
- **Preconditions**: Lessons exist with Hugo shortcodes
- **Main Flow**:
  1. Agent calls validate_lesson or validate_course
  2. System checks for Hugo shortcode presence
  3. Tier 3-4 checks for readme-shared shortcode
- **Postconditions**: Validation correctly identifies shortcode presence/absence
- **Acceptance Criteria**:
  - [ ] Validation detects `{{</* instructor-guide */>}}` shortcode
  - [ ] Validation detects `{{</* readme-shared */>}}` shortcode for tier 3-4
  - [ ] Quiz alignment works with shortcode-based content

## SUC-003: Parse readme guards from Hugo shortcodes
Parent: UC-005

- **Actor**: AI agent via MCP
- **Preconditions**: Lessons contain Hugo readme shortcodes
- **Main Flow**:
  1. Agent calls generate_readmes
  2. System parses `{{</* readme-shared */>}}` and `{{</* readme-only */>}}` blocks
  3. README.md files generated from extracted content
- **Postconditions**: README generation works with Hugo shortcode syntax
- **Acceptance Criteria**:
  - [ ] Shared guard regex matches `{{</* readme-shared */>}}`
  - [ ] Only guard regex matches `{{</* readme-only */>}}`
  - [ ] Default docs_dir is `content/` not `docs/docs/`
