---
id: "019"
title: "Hugo Site Tools and MCP Guidance Enrichment"
status: planning
branch: sprint/019-hugo-site-tools-and-mcp-guidance-enrichment
use-cases: [SUC-001, SUC-002, SUC-003]
---

# Sprint 019: Hugo Site Tools and MCP Guidance Enrichment

## Goals

Add Tier 1 Hugo site management tools (list pages, create pages, update
frontmatter, build site) and enrich MCP server instructions and tool
docstrings so all agents (not just Claude Code) understand Hugo conventions.

## Problem

Curik can scaffold content and validate lessons, but agents have no tools
to list existing content pages, create arbitrary pages, update frontmatter,
or build the Hugo site. The MCP server instructions are also too sparse
for non-Claude-Code models that don't see CLAUDE.md.

## Solution

1. New `curik/hugo.py` module with functions for:
   - Listing content pages with frontmatter metadata
   - Creating arbitrary content pages (not just lesson stubs)
   - Updating YAML frontmatter on existing pages
   - Running `hugo build` and returning output

2. Expose these as MCP tools in server.py.

3. Enrich MCP server `instructions` with workflow guidance and shortcode
   examples. Improve tool docstrings across server.py.

## Success Criteria

- `tool_list_content_pages()` returns page list with frontmatter
- `tool_create_content_page()` creates pages with proper Hugo frontmatter
- `tool_update_frontmatter()` merges updates into existing page frontmatter
- `tool_hugo_build()` runs Hugo and returns build output (or actionable error)
- MCP instructions include workflow guidance and shortcode examples
- Tool docstrings mention Hugo context where relevant
- All tests pass (existing + new)

## Scope

### In Scope

- `curik/hugo.py` — new module with Tier 1 Hugo site functions
- `curik/server.py` — new MCP tools + enriched instructions/docstrings
- Tests for all new functions
- Move both TODOs to done

### Out of Scope

- Tier 2-4 Hugo tools (navigation, linking, theme introspection, section reorganization)
- Hugo binary installation/management
- MCP resources (deferred to future sprint)
- `tool_get_workflow_guide()` (instructions enrichment covers this for now)

## Test Strategy

Unit tests using tmp_path fixtures for:
- `list_content_pages()` with various content trees
- `create_content_page()` with frontmatter
- `update_frontmatter()` merge behavior
- `hugo_build()` when Hugo is not installed (graceful error)
- Integration test with `init_course()` + content creation

## Architecture Notes

- YAML frontmatter parsing uses a simple regex-based approach (split on
  `---` delimiters) rather than adding a PyYAML dependency — Curik already
  has this pattern in validation.py
- `hugo_build()` shells out to `hugo` binary; returns structured result
  with success/failure, output, and page count
- All functions take `root: Path` parameter for consistency with existing code

## Definition of Ready

- [x] Sprint planning documents are complete
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
