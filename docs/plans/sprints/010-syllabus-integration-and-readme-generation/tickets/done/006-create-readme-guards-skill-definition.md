---
id: "006"
title: "Create readme-guards skill definition"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Create readme-guards skill definition

## Description

Create a `curik/skills/readme-guards.md` skill definition file that teaches agents when and how to place `<!-- readme-shared -->` and `<!-- readme-only -->` comment guards in MkDocs lesson pages. The skill should explain the guard syntax (opening and closing tags), when to use `readme-shared` vs `readme-only`, placement guidelines relative to page structure (e.g., after frontmatter, around summaries and objectives), and examples of correctly guarded content. The skill must be loadable via `get_skill_definition("readme-guards")`. This is needed because agents writing or editing lesson content must know how to mark sections for README extraction without being told each time.

## Acceptance Criteria

- [ ] `curik/skills/readme-guards.md` file exists
- [ ] Skill definition explains the `<!-- readme-shared -->` / `<!-- /readme-shared -->` guard syntax
- [ ] Skill definition explains the `<!-- readme-only -->` / `<!-- /readme-only -->` guard syntax
- [ ] Skill definition describes when to use `readme-shared` (content for both MkDocs and README) vs `readme-only` (README-exclusive content)
- [ ] Skill definition includes placement guidelines (where in a lesson page guards should go)
- [ ] Skill definition includes at least one concrete example of a correctly guarded lesson page
- [ ] Skill is loadable via `get_skill_definition("readme-guards")` (registered in skill index or discovery mechanism)

## Testing

- **Existing tests to run**: `uv run pytest tests/` to verify no regressions
- **New tests to write**: No unit tests needed for a skill definition file; verify manually that `get_skill_definition("readme-guards")` returns the content
- **Verification command**: Manually invoke `get_skill_definition("readme-guards")` via the MCP server
