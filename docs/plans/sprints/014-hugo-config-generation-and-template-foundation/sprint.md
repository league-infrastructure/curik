---
id: "014"
title: "Hugo Config Generation and Template Foundation"
status: planning
branch: sprint/014-hugo-config-generation-and-template-foundation
use-cases: [SUC-001, SUC-002, SUC-003]
---

# Sprint 014: Hugo Config Generation and Template Foundation

## Goals

Replace all MkDocs configuration generation with Hugo equivalents. After this
sprint, Curik generates Hugo projects instead of MkDocs projects.

## Problem

MkDocs 2.0 drops plugin support, breaks Material theme compatibility, and
MkDocs 1.x is unmaintained. Curik currently generates `mkdocs.yml` configs
and uses `docs/docs/` as the content directory. This must change to Hugo's
`hugo.toml` and `content/` conventions.

## Solution

1. Replace `get_mkdocs_yml()` with `get_hugo_config()` in `templates.py`.
2. Update `migrate.py` to detect Hugo (`hugo.toml`) and generate Hugo config.
3. Update `scaffolding.py` to use `content/` directory with `_index.md` files
   and simplify nav generation (Hugo uses directory order from `01-` prefixes).
4. Update `server.py` tool docstrings referencing MkDocs.
5. Add the brand guide as a packaged reference doc accessible via MCP.

## Success Criteria

- `get_hugo_config()` produces valid Hugo TOML config for all 4 tiers
- `inventory_course()` detects Hugo projects via `hugo.toml`
- `migrate_structure()` creates `hugo.toml` and `content/` directory
- `scaffold_structure()` creates `content/` with `_index.md` branch bundles
- Brand guide is accessible via MCP tool at runtime
- All existing tests updated and passing
- No remaining references to `mkdocs` in Python source files

## Scope

### In Scope

- `curik/templates.py`: replace `get_mkdocs_yml()` with `get_hugo_config()`
- `curik/migrate.py`: detect Hugo, generate Hugo config, update `migrate_structure()`
- `curik/scaffolding.py`: `content/` directory, `_index.md` files, simplify nav
- `curik/server.py`: update docstrings and tool descriptions
- `curik/references/`: new directory for packaged reference docs (brand guide)
- All affected test files
- Move consumed TODO to `done/`

### Out of Scope

- Content format changes (shortcodes) — next sprint
- Agent/skill markdown updates — later sprint
- League Hugo theme creation — later sprint
- Validation and README parsing changes — next sprint

## Test Strategy

Update all existing tests that reference MkDocs config, `mkdocs.yml`, or
`docs/docs/` paths. Key test files:
- `tests/test_scaffolding.py` — nav generation, scaffold structure
- `tests/test_migration.py` — inventory detection, migrate structure
- New tests for `get_hugo_config()` across all tiers
- New test for brand guide MCP tool

## Architecture Notes

- Hugo uses TOML config (`hugo.toml`) instead of YAML (`mkdocs.yml`)
- Content lives in `content/` (not `docs/docs/`)
- Branch bundles use `_index.md` (not `index.md`)
- Nav is auto-generated from directory structure — the `01-` prefix convention
  we already use provides correct ordering without explicit nav config
- `generate_nav()` can be simplified or removed since Hugo handles nav natively
- Reference docs (brand guide) go in `curik/references/` and ship with the
  package via `package_data` in `pyproject.toml`

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
