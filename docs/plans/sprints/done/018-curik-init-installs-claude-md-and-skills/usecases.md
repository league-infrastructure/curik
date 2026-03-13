---
status: complete
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 018 Use Cases

## SUC-001: Fresh project initialization
Parent: UC-001

- **Actor**: Curriculum developer
- **Preconditions**: Empty or new repository with no CLAUDE.md or `.claude/` directory
- **Main Flow**:
  1. Developer runs `curik init` in the repository root
  2. Curik creates `.course/` structure, `course.yml`, `.mcp.json` (existing behavior)
  3. Curik creates `CLAUDE.md` with the `<!-- CURIK:START -->`/`<!-- CURIK:END -->` section
  4. Curik writes `/curik` skill to `.claude/skills/curik/SKILL.md`
  5. Curik adds `mcp__curik__*` to `.claude/settings.local.json` permissions
  6. Curik creates `.vscode/mcp.json` with curik server config
- **Postconditions**: Repository has full Curik configuration; agents opening the project see Hugo conventions and workflow guidance in CLAUDE.md
- **Acceptance Criteria**:
  - [x] CLAUDE.md exists with `<!-- CURIK:START -->` and `<!-- CURIK:END -->` markers
  - [x] `.claude/skills/curik/SKILL.md` exists
  - [x] `.claude/settings.local.json` has `mcp__curik__*` in allow list
  - [x] `.vscode/mcp.json` has curik server entry

## SUC-002: Re-initialization (idempotent update)
Parent: UC-001

- **Actor**: Curriculum developer
- **Preconditions**: Repository already initialized with Curik (CLAUDE.md has CURIK section)
- **Main Flow**:
  1. Developer upgrades Curik package (new version with updated templates)
  2. Developer runs `curik init` again
  3. Curik replaces the `<!-- CURIK:START -->`/`<!-- CURIK:END -->` section in place
  4. Curik overwrites the skill file if changed
  5. Curik merges MCP config (does not duplicate entries)
- **Postconditions**: All Curik-managed files updated to latest templates; user content outside markers preserved
- **Acceptance Criteria**:
  - [x] Existing content outside `<!-- CURIK:START -->`/`<!-- CURIK:END -->` is preserved
  - [x] Skill file updated if source changed, reported as "Unchanged" if identical
  - [x] Settings JSON merged without duplicating permissions

## SUC-003: Initialization alongside CLASI
Parent: UC-001

- **Actor**: Curriculum developer working in a CLASI-managed project
- **Preconditions**: Repository has existing CLAUDE.md with `<!-- CLASI:START -->`/`<!-- CLASI:END -->` section
- **Main Flow**:
  1. Developer runs `curik init` in a CLASI-managed repo
  2. Curik appends `<!-- CURIK:START -->`/`<!-- CURIK:END -->` section after existing content
  3. Curik merges its MCP server config alongside CLASI's in `.mcp.json`
  4. Curik adds its permissions alongside CLASI's in settings
- **Postconditions**: Both CLASI and CURIK sections coexist in CLAUDE.md; both MCP servers configured
- **Acceptance Criteria**:
  - [x] CLASI section untouched
  - [x] CURIK section appended
  - [x] `.mcp.json` has both `clasi` and `curik` server entries
  - [x] Settings has both `mcp__clasi__*` and `mcp__curik__*` permissions
