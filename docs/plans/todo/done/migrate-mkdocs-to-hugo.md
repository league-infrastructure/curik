---
title: Migrate from MkDocs to Hugo
priority: high
tags:
- architecture
- breaking-change
status: done
sprint: '014'
---

# Migrate from MkDocs to Hugo

MkDocs 2.0 drops plugin support, breaks Material theme compatibility, and
MkDocs 1.x is unmaintained. Replace with Hugo across the entire Curik codebase.

No existing curricula to migrate — this is purely a tool-side change.

## Decision: Hugo

- Shortcodes (`{{</* name */>}}`) are purpose-built for clean custom syntax in markdown
- Theme components are composable modules — perfect for a shared League theme
- No plugin API to break; features built into the binary
- Fast builds (milliseconds), active ecosystem
- Theme lives as a subdirectory (`league-hugo-theme/`) with its own git repo inside
  this project. Will be moved to a standalone repo later when mature.
- Brand guide (`docs/league-web-brand-guide.md`) must be available at MCP runtime —
  copy to `curik/references/` (or similar) so it ships with the package and can be
  served to agents. All instructions, skills, and reference docs are separate markdown
  files, never inlined in Python.

## Content Format Changes

Instructor guide: `<div class="instructor-guide" markdown>` → `{{</* instructor-guide */>}}`
README guards: `<!-- readme-shared -->` → `{{</* readme-shared */>}}`
New capability: `{{</* callout type="tip" */>}}` for callouts

Directory: `docs/docs/` → `content/`, `index.md` → `_index.md`, `mkdocs.yml` → `hugo.toml`

## Phase 1: Hugo Config Generation and Template Foundation

Replace MkDocs config generation with Hugo config generation.

Files: `curik/templates.py`, `curik/migrate.py`, `curik/scaffolding.py`, `curik/server.py`, tests

- [ ] Replace `get_mkdocs_yml()` with `get_hugo_config()` in templates.py + tests
- [ ] Update migrate.py to detect/generate Hugo config + tests
- [ ] Update scaffolding.py: `content/` dir, `_index.md` files, simplify nav + tests
- [ ] Update server.py tool docstrings and default paths
- [ ] Add brand guide as a runtime MCP resource (`curik/references/league-web-brand-guide.md`)
      with an MCP tool to retrieve it. Wire up in server.py.
- [ ] Integration test pass

## Phase 2: Content Format Migration (Shortcodes)

Replace HTML divs and comment guards with Hugo shortcodes.

Files: `curik/scaffolding.py`, `curik/validation.py`, `curik/readme.py`, `curik/syllabus.py`, tests

- [ ] Update lesson stub generation to emit shortcodes in scaffolding.py + tests
- [ ] Update instructor guide validation regex in validation.py + tests
- [ ] Update README guard parsing regex in readme.py + tests
- [ ] Update syllabus consistency paths (`content/` not `docs/docs/`) in syllabus.py + tests
- [ ] Comprehensive regression test pass

## Phase 3: Agent and Skill Documentation Update

Update all agent/skill markdown files to reference Hugo, shortcodes, and new directory structure.

Files: 12+ files in `curik/agents/` and `curik/skills/`

- [ ] Update agent definitions (start-curik, curriculum-architect, lesson-authors)
- [ ] Update scaffolding/structure skills (repo-scaffolding, structure-proposal)
- [ ] Update content authoring skills (lesson-writing-*, readme-guards, instructor-guide-sections, validation-checklist)
- [ ] Update integration skills (syllabus-integration, spec-synthesis, pedagogical-model)

## Phase 4: League Hugo Theme (Subdirectory)

Create `league-hugo-theme/` as a subdirectory with its own `git init`.
Incorporate `docs/league-web-brand-guide.md` into the theme's CSS and layouts.
Will be moved to a standalone repo when mature.

### Existing Theme Reference (Sphinx + Furo)

The current curriculum sites (Python Apprentice, Motors Clinic) use Sphinx + Furo
theme. The Hugo theme should replicate this look and feel, not invent something new.

**Layout structure to replicate:**
- Left sidebar: collapsible navigation with nested module/lesson hierarchy
- Right sidebar: table of contents for current page
- Center: main content area
- Header: League logo (`logo4.png` from images.jointheleague.org) + course title
- Footer: copyright, license (CC BY-NC 4.0), last-updated timestamp
- Light/dark/auto theme toggle

**UI components to replicate as Hugo shortcodes:**
- Warning/note/tip admonition boxes (Sphinx `.. warning::`, `.. note::`)
- Toggle/collapsible hint sections ("Click to show/hide")
- Code blocks with syntax highlighting
- Next/previous lesson navigation links
- Image embedding from `images.jointheleague.org`

**Brand guide integration:**
- Colors: League Orange `#F37121`, cream backgrounds `#FEF7F0`, dark footer `#1A1A2E`
- Typography: Arial/Helvetica Neue stack
- Buttons: rounded orange primary, white secondary
- Logo rules: clear space, no colored backgrounds except black/white
- CSS custom properties from `docs/league-web-brand-guide.md`

### Work items

- [ ] `git init league-hugo-theme/`, theme scaffold: `theme.toml`, base layout
- [ ] Base layout: sidebar nav, TOC sidebar, header with logo, dark footer,
      light/dark/auto toggle — matching existing Furo-based sites
- [ ] CSS framework implementing the League web brand guide (colors, typography,
      buttons, page layout patterns from `docs/league-web-brand-guide.md`)
- [ ] Shortcodes: `instructor-guide`, `callout` (warning/note/tip), `toggle-hint`,
      `readme-shared`, `readme-only`
- [ ] Next/previous lesson nav partial (auto-generated from content order)
- [ ] Theme docs and integration test with sample site

## Phase Dependencies

```
Phase 1 (Config) → Phase 2 (Content Format) → Phase 3 (Skill Docs)
                          ↘ Phase 4 (Theme, parallel with Phase 3)
```

## Verification

- Full test suite passes after each phase
- `curik init` creates correct Hugo project structure
- Generated `hugo.toml` is valid Hugo config
- No remaining references to "mkdocs" in Python code (after Phase 2)
- No remaining references to "mkdocs" in skill/agent files (after Phase 3)

## Open Question

- Hugo binary management: Should Curik install Hugo automatically (e.g., `hugo-bin` pip package) or document it as a prerequisite?
