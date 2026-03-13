---
title: Hugo Site Management Tools
priority: high
tags:
- hugo
- mcp-server
- website
- scaffolding
status: done
sprint: 019
---

# Hugo Site Management Tools

Curik generates Hugo content (lesson stubs, `_index.md` files, `hugo.toml`)
but has **no MCP tools for actually managing the Hugo site as a website**.
When an agent uses Curik via MCP, it can scaffold content and validate
lessons, but it cannot build the site, create arbitrary pages, manage
navigation, or link pages together. The agent has no awareness that the
curriculum is a Hugo website.

## Current State

### What Exists

- **`get_hugo_config()`** (templates.py) — generates `hugo.toml`
- **`scaffold_structure()`** (scaffolding.py) — creates module directories,
  `_index.md` branch bundles, and lesson stubs with Hugo shortcodes
- **`generate_nav()`** (scaffolding.py) — builds Hugo weight assignments
  for navigation ordering
- **`create_lesson_stub()`** (scaffolding.py) — writes lesson `.md` files
  with frontmatter and shortcode scaffolding
- **`migrate_structure()`** (migrate.py) — creates `hugo.toml` during
  migration
- **league-hugo-theme/** — a minimal theme with `baseof.html`, four
  shortcodes (`instructor-guide`, `callout`, `readme-shared`, `readme-only`),
  and basic CSS

### What Is Missing (No MCP Tools For)

1. **Building the site** — no tool to run `hugo build` or `hugo server`
   to preview the generated site
2. **Creating pages** — no general-purpose "create a content page" tool;
   only lesson stubs and `_index.md` are generated programmatically
3. **Managing frontmatter** — no tool to read or update Hugo frontmatter
   (title, weight, draft, layout, params) on existing pages
4. **Linking pages** — no tool to create cross-references between lessons,
   generate a table of contents, or produce `relref`/`ref` links
5. **Section management** — no tool to create, rename, or reorganize Hugo
   content sections (beyond the initial scaffold)
6. **Navigation control** — `generate_nav()` exists in Python but is not
   exposed as an MCP tool; agents cannot adjust page ordering
7. **Theme awareness** — no tool to list available shortcodes, layouts, or
   partials from the league-hugo-theme; agents don't know what the theme
   provides
8. **Site validation** — no tool to check that the Hugo site builds
   cleanly (no broken refs, missing layouts, invalid frontmatter)
9. **Content listing** — no tool to list all pages in the Hugo content
   tree with their frontmatter metadata

## Proposed Features

### Tier 1: Essential Site Operations

These are the minimum tools an agent needs to work with the Hugo site.

- **`tool_hugo_build()`** — Run `hugo` and return build output (errors,
  warnings, page count). Detect if Hugo is installed; provide actionable
  error if not.
- **`tool_list_content_pages(section: str | None)`** — Walk `content/`
  and return a list of pages with their frontmatter (title, weight, draft
  status, UID, section path).
- **`tool_create_content_page(path: str, title: str, frontmatter: dict)`**
  — Create an arbitrary content page at the given path under `content/`,
  with proper Hugo frontmatter. Not limited to lesson stubs.
- **`tool_update_frontmatter(page_path: str, updates: dict)`** — Read a
  content file, merge updates into its YAML frontmatter, and write it back.

### Tier 2: Navigation and Linking

- **`tool_generate_nav()`** — Expose the existing `generate_nav()` as an
  MCP tool so agents can retrieve weight assignments.
- **`tool_reorder_pages(section: str, order: list[str])`** — Update
  weights in `_index.md` or individual page frontmatter to match a
  specified ordering.
- **`tool_add_cross_reference(from_page: str, to_page: str)`** — Insert a
  Hugo `relref` link from one page to another.
- **`tool_generate_section_toc(section: str)`** — Produce a markdown table
  of contents for a section, suitable for inserting into `_index.md`.

### Tier 3: Theme and Build Awareness

- **`tool_list_shortcodes()`** — Enumerate available shortcodes from the
  league-hugo-theme with their usage documentation.
- **`tool_list_layouts()`** — List available layouts and partials in the
  theme.
- **`tool_validate_hugo_site()`** — Run `hugo` in a validation mode and
  report build errors, broken `relref` links, missing images, and pages
  with `draft: true`.
- **`tool_get_theme_info()`** — Return theme metadata, supported
  parameters, and brand guide essentials so the agent knows what's
  available.

### Tier 4: Advanced Site Management

- **`tool_reorganize_section(section: str, new_structure: dict)`** — Move
  pages within a section, updating weights and cross-references
  accordingly.
- **`tool_create_section(path: str, title: str)`** — Create a new Hugo
  content section with its `_index.md`.
- **`tool_set_page_draft(page_path: str, draft: bool)`** — Toggle draft
  status on a page.

## Implementation Notes

- Hugo binary availability is a prerequisite for build/serve tools.
  Consider shelling out to `hugo` and checking the exit code, or bundling
  `hugo` via a Python wrapper like `hugo-python`.
- Frontmatter parsing should handle both YAML (`---`) and TOML (`+++`)
  delimiters.
- The `content/` directory path should respect the project root
  (resolved via `_root()` in server.py).
- The league-hugo-theme shortcode documentation could be extracted
  automatically from the HTML comment headers in each shortcode file.

## Related

- [migrate-mkdocs-to-hugo](done/migrate-mkdocs-to-hugo.md) — completed
  migration (Sprint 014)
- league-hugo-theme/ — the theme that these tools would work with
