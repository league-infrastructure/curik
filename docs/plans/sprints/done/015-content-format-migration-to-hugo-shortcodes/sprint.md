---
id: '015'
title: Content Format Migration to Hugo Shortcodes
status: done
branch: sprint/015-content-format-migration-to-hugo-shortcodes
use-cases:
- SUC-001
- SUC-002
- SUC-003
---

# Sprint 015: Content Format Migration to Hugo Shortcodes

## Goals

Replace HTML divs and comment guards with Hugo shortcodes in all generated
content, validation, and parsing. After this sprint, no Python code or tests
reference the old MkDocs HTML patterns.

## Problem

Sprint 014 replaced MkDocs config generation with Hugo, but the content
format still uses MkDocs-era patterns:
- `<div class="instructor-guide">` HTML divs in lesson stubs
- `<!-- readme-shared -->` / `<!-- readme-only -->` HTML comment guards
- `docs/docs/` path references in syllabus consistency checking
- Validation regexes that match HTML div patterns

These patterns are incompatible with Hugo shortcodes and confuse agents
reading the generated content.

## Solution

Update all Python modules that generate or parse content to use Hugo
shortcode syntax:
- `{{</* instructor-guide */>}}...{{</* /instructor-guide */>}}`
- `{{</* readme-shared */>}}...{{</* /readme-shared */>}}`
- `{{</* readme-only */>}}...{{</* /readme-only */>}}`
- `content/` instead of `docs/docs/`

## Success Criteria

- No references to `<div class="instructor-guide"` in Python source
- No references to `<!-- readme-shared -->` in Python source
- No references to `docs/docs` path in Python source
- All tests pass with new shortcode patterns
- Validation correctly detects Hugo shortcode presence/absence

## Scope

### In Scope

- scaffolding.py: lesson stub generation (3 locations)
- validation.py: instructor guide regex (4 patterns), readme guard check
- readme.py: guard parsing regex (2 patterns), default path
- quiz.py: instructor guide removal regex (1 pattern)
- syllabus.py: docs/docs path reference, comment
- server.py: docstring update for readme guards
- All corresponding tests

### Out of Scope

- Agent/skill markdown files (Sprint 016)
- Hugo theme creation (Sprint 017)
- Actual Hugo shortcode template implementations (theme work)

## Test Strategy

Update existing test fixtures and assertions to use Hugo shortcode syntax.
No new test files needed — the existing test coverage is comprehensive.
Run full suite after each ticket.

## Architecture Notes

Hugo shortcode syntax: `{{</* name */>}}` for opening, `{{</* /name */>}}` for
closing. Content between shortcode tags is processed by Hugo. The shortcodes
themselves are defined in the Hugo theme's `layouts/shortcodes/` directory —
Curik only generates the markdown that references them.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
