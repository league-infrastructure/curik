---
title: Migrate from MkDocs to Hugo
priority: high
tags: [architecture, breaking-change]
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
- Theme lives in a **separate repo** (`league-hugo-theme`), imported via Hugo module

## Content Format Changes

Instructor guide: `<div class="instructor-guide" markdown>` → `{{</* instructor-guide */>}}`
README guards: `<!-- readme-shared -->` → `{{</* readme-shared */>}}`
New capability: `{{</* callout type="tip" */>}}` for callouts

Directory: `docs/docs/` → `content/`, `index.md` → `_index.md`, `mkdocs.yml` → `hugo.toml`

## Sprint 014: Hugo Config Generation and Template Foundation

Replace MkDocs config generation with Hugo config generation.

Files: `curik/templates.py`, `curik/migrate.py`, `curik/scaffolding.py`, `curik/server.py`, tests

- [ ] Replace `get_mkdocs_yml()` with `get_hugo_config()` in templates.py + tests
- [ ] Update migrate.py to detect/generate Hugo config + tests
- [ ] Update scaffolding.py: `content/` dir, `_index.md` files, simplify nav + tests
- [ ] Update server.py tool docstrings and default paths
- [ ] Integration test pass

## Sprint 015: Content Format Migration (Shortcodes)

Replace HTML divs and comment guards with Hugo shortcodes.

Files: `curik/scaffolding.py`, `curik/validation.py`, `curik/readme.py`, `curik/syllabus.py`, tests

- [ ] Update lesson stub generation to emit shortcodes in scaffolding.py + tests
- [ ] Update instructor guide validation regex in validation.py + tests
- [ ] Update README guard parsing regex in readme.py + tests
- [ ] Update syllabus consistency paths (`content/` not `docs/docs/`) in syllabus.py + tests
- [ ] Comprehensive regression test pass

## Sprint 016: Agent and Skill Documentation Update

Update all agent/skill markdown files to reference Hugo, shortcodes, and new directory structure.

Files: 12+ files in `curik/agents/` and `curik/skills/`

- [ ] Update agent definitions (start-curik, curriculum-architect, lesson-authors)
- [ ] Update scaffolding/structure skills (repo-scaffolding, structure-proposal)
- [ ] Update content authoring skills (lesson-writing-*, readme-guards, instructor-guide-sections, validation-checklist)
- [ ] Update integration skills (syllabus-integration, spec-synthesis, pedagogical-model)

## Sprint 017: League Hugo Theme (Separate Repo)

Create `league-hugo-theme` with shortcodes, layouts, and CSS.

- [ ] Theme scaffold: `theme.toml`, base layout, CSS framework
- [ ] Instructor-guide and callout shortcodes + CSS
- [ ] Readme-shared and readme-only shortcodes
- [ ] Theme docs and integration test with sample site

## Sprint Dependencies

```
014 (Config) → 015 (Content Format) → 016 (Skill Docs)
                       ↘ 017 (Theme, parallel with 016)
```

## Verification

- Full test suite passes after each sprint
- `curik init` creates correct Hugo project structure
- Generated `hugo.toml` is valid Hugo config
- No remaining references to "mkdocs" in Python code (after 015)
- No remaining references to "mkdocs" in skill/agent files (after 016)

## Open Question

- Hugo binary management: Should Curik install Hugo automatically (e.g., `hugo-bin` pip package) or document it as a prerequisite?
