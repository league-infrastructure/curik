---
status: complete
---

# Sprint 019 Use Cases

## SUC-001: Agent lists content pages to understand site structure
Parent: UC-002

- **Actor**: AI agent (any model)
- **Preconditions**: Curik-initialized project with `content/` directory containing pages
- **Main Flow**:
  1. Agent calls `tool_list_content_pages()`
  2. Tool walks `content/` tree and parses frontmatter from each `.md` file
  3. Returns list of pages with path, title, weight, draft status
- **Postconditions**: Agent has a map of the content tree
- **Acceptance Criteria**:
  - [ ] Returns all `.md` files under `content/`
  - [ ] Each entry includes path, title, weight, draft status
  - [ ] Optional section filter narrows results

## SUC-002: Agent creates a new content page
Parent: UC-002

- **Actor**: AI agent (any model)
- **Preconditions**: Curik-initialized project with `content/` directory
- **Main Flow**:
  1. Agent calls `tool_create_content_page(path, title, content, frontmatter)`
  2. Tool creates the page under `content/` with YAML frontmatter
  3. Parent directories created if needed
- **Postconditions**: New page exists with proper Hugo frontmatter
- **Acceptance Criteria**:
  - [ ] Page created at specified path under `content/`
  - [ ] YAML frontmatter includes title and any extra fields
  - [ ] Parent directories auto-created
  - [ ] Error if page already exists

## SUC-003: Agent updates frontmatter on existing page
Parent: UC-002

- **Actor**: AI agent (any model)
- **Preconditions**: Content page exists with YAML frontmatter
- **Main Flow**:
  1. Agent calls `tool_update_frontmatter(page_path, updates)`
  2. Tool reads existing frontmatter, merges updates, writes back
  3. Body content preserved unchanged
- **Postconditions**: Frontmatter updated, body intact
- **Acceptance Criteria**:
  - [ ] Existing frontmatter fields preserved
  - [ ] New fields added, existing fields updated
  - [ ] Body content unchanged after update
