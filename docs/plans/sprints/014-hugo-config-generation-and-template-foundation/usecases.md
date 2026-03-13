---
status: draft
---

# Sprint 014 Use Cases

## SUC-001: Generate Hugo config for a new course
Parent: UC-002

- **Actor**: Curik agent (via `migrate_structure()` or `scaffold_structure()`)
- **Preconditions**: Course directory exists, tier is known (1-4)
- **Main Flow**:
  1. Agent calls `migrate_structure()` or scaffolding creates a new course
  2. System generates `hugo.toml` with tier-appropriate settings
  3. System creates `content/` directory with `_index.md` root page
  4. For tier 1-2: config references instructor guide CSS/JS
  5. For tier 3-4: config uses standard student-facing layout
- **Postconditions**: `hugo.toml` exists at project root, `content/` directory
  has `_index.md`, Hugo can process the project
- **Acceptance Criteria**:
  - [ ] `get_hugo_config()` returns valid TOML for tiers 1-4
  - [ ] Tier 1-2 config includes instructor guide asset references
  - [ ] Tier 3-4 config uses standard layout
  - [ ] `hugo.toml` is created (not `mkdocs.yml`)

## SUC-002: Detect existing site generator during inventory
Parent: UC-003

- **Actor**: Curik agent (via `inventory_course()`)
- **Preconditions**: Course repository exists with unknown structure
- **Main Flow**:
  1. Agent calls `inventory_course()` on a repository
  2. System checks for `hugo.toml` (Hugo), `conf.py` (Sphinx), `mkdocs.yml`
     (legacy MkDocs), and `.vuepress/` (VuePress)
  3. System returns `generator_guess` field with detected SSG
- **Postconditions**: Inventory result includes correct `generator_guess`
- **Acceptance Criteria**:
  - [ ] Detects `hugo.toml` → `"hugo"`
  - [ ] Still detects legacy `mkdocs.yml` → `"mkdocs"`
  - [ ] Still detects `conf.py` → `"sphinx"`

## SUC-003: Access brand guide during course creation
Parent: UC-001

- **Actor**: Curik agent (during Phase 1 or scaffolding)
- **Preconditions**: MCP server is running
- **Main Flow**:
  1. Agent needs brand guide info for site styling decisions
  2. Agent calls `get_reference()` MCP tool with name `"league-web-brand-guide"`
  3. System reads `curik/references/league-web-brand-guide.md` from package
  4. Returns full markdown content
- **Postconditions**: Agent has brand guide content for decision-making
- **Acceptance Criteria**:
  - [ ] Brand guide file ships with the curik package
  - [ ] MCP tool returns full content of the brand guide
  - [ ] File is a separate markdown file, not inlined in Python
