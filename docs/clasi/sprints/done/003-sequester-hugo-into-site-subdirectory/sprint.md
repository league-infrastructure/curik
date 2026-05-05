---
id: '003'
title: Sequester Hugo into site/ Subdirectory
status: done
branch: sprint/003-sequester-hugo-into-site-subdirectory
use-cases:
- SUC-001
- SUC-002
- SUC-003
- SUC-004
todo: sequester-hugo-into-site-in-scaffolded-curriculum-projects.md
---

# Sprint 003: Sequester Hugo into site/ Subdirectory

## Goals

Move all Hugo files from the curriculum project root into a `site/` subdirectory.
Add a path-helper module so every code path goes through a single source of truth.
Add a legacy-layout detector that warns on every CLI invocation.
Add a `curik migrate hugo-layout` command for one-shot opt-in migration of existing
projects.

## Problem

When `curik` scaffolds a curriculum project, Hugo files (`hugo.toml`, `themes/`,
`content/`, `public/`, `resources/_gen/`, `.hugo_build.lock`) are written to the
project root, mixing them with curik's own files (`course.yml`, `.course/`, `.claude/`,
`CLAUDE.md`, `README.md`). Authors cannot tell at a glance what is "the curriculum
source" vs "the Hugo site that renders it." Root-level clutter also makes it harder for
agents and tooling to reason about project structure.

## Solution

Introduce a `site/` subdirectory that contains everything Hugo-related. A new
`curik/paths.py` module provides path-helper functions (`site_root`, `hugo_toml_path`,
`content_dir`, `themes_dir`, `theme_dir`) so no caller hardcodes `"content"`,
`"hugo.toml"`, or `"themes"` relative to the project root. Every existing code path
is updated to use these helpers.

The `hugo.toml` mount for `course.yml` changes from `source = "course.yml"` to
`source = "../course.yml"` because hugo.toml now lives one level below the project root.

A new `curik/layout_check.py` module detects the legacy layout (Hugo files at root, no
`site/hugo.toml`) and emits a stderr warning on every CLI invocation. A new
`curik/layout_migrate.py` module and `curik migrate hugo-layout` subcommand perform the
one-shot opt-in migration using `git mv` to preserve history.

Existing scaffolded projects keep working as-is until the stakeholder runs
`curik migrate hugo-layout`. No auto-migration ever occurs.

## Success Criteria

- `curik init` then `curik hugo setup` on a fresh repo creates `site/hugo.toml`,
  `site/themes/curriculum-hugo-theme/`, and `site/content/` — no Hugo files at root.
- `curik hugo build` runs Hugo from `site/` and produces `site/public/`.
- `curik hugo create-page mod/intro.md "Intro"` creates `site/content/mod/intro.md`
  and returns `mod/intro.md` (no `site/` prefix in the public API).
- Running any curik command in a legacy-layout project emits a warning to stderr.
  `CURIK_NO_LAYOUT_WARNING=1` suppresses it.
- `curik migrate hugo-layout --dry-run` prints the plan; without `--dry-run` it moves
  files using `git mv`, rewrites hugo.toml mounts, and updates `.gitignore`.
- `curik migrate hugo-layout` is idempotent: running it twice on an already-migrated
  repo exits 0 with nothing to do.
- `pytest -q` is green.

## Scope

### In Scope

- New `curik/paths.py` — `SITE_DIR` constant and five path-helper functions
- `curik/templates.py` — hugo.toml generation (`../course.yml` mount), theme install
  path, `bump_curriculum_version` path
- `curik/hugo.py` — `hugo_build` cwd, all content read/write paths
- `curik/scaffolding.py` — content/ creation, module dirs, lesson stubs
- `curik/migrate.py` — `migrate_structure` content paths, `_PROTECTED_NAMES` update
  (add `"site"`, remove `"hugo.toml"` and `"themes"`)
- `curik/syllabus.py` — content scan path
- `curik/readme.py` — `docs_dir` default parameter
- `curik/publish.py` — `has_hugo_toml`, `has_theme`, content scan, baseURL read,
  build call, `has_local_baseof`
- `curik/cli.py` — `--docs-dir` default, new `migrate hugo-layout` subcommand, legacy
  warning hook near top of `main()`
- `curik/init/gitignore` — `site/public/`, `site/resources/_gen/`,
  `site/.hugo_build.lock`
- `curik/init/deploy-pages.yml` — `hugo --minify --source site`, `./site/public`
- `curik/init/claude-section.md` — Hugo Theme section path, Hugo Site command
  descriptions
- `curik/references/hugo-conventions.md` — all path references
- `curik/skills/repo-scaffolding.md` — scaffolded layout example
- `curik/agents/start-curik.md` — paths table
- New `curik/layout_check.py` — legacy-layout detector
- New `curik/layout_migrate.py` — hugo-layout migration logic
- Tests: `test_hugo.py`, `test_scaffolding.py`, `test_migration.py`, `test_cli.py`,
  `test_publish.py` updated; `test_layout_check.py` and `test_layout_migrate.py` new

### Out of Scope

- Changes to the curik package's own `curriculum-hugo-theme/` directory (git subtree
  source, separate concern)
- Versioning or breaking-change comms beyond the in-CLI warning
- Hugo theme changes (theme is layout-agnostic)

## Test Strategy

Unit tests cover each module in isolation — paths helpers, layout detection, migration
logic, and all updated domain functions. Integration tests (`test_hugo.py`,
`test_scaffolding.py`) spin up a temp project dir to exercise end-to-end scaffold and
build flows. Migration tests cover: fresh project (no-op), legacy project (full
migration), dirty-tree refusal, idempotency (run twice). CLI tests verify the
`--docs-dir` default and the new `migrate hugo-layout` subcommand.

End-to-end manual verification checklist is in the TODO (steps 1-7 in the Verification
section).

## Architecture Notes

- `curik/paths.py` is a pure utility module — no imports from other curik modules,
  no side effects. Everything else imports from it.
- The public CLI surface for `curik hugo create-page <page-path>` is unchanged:
  `<page-path>` is relative to `content/`, not `site/content/`. Helpers prepend
  `site/content/` internally.
- Migration uses `git mv` when in a git repo to preserve `git log --follow` history.
- The legacy-layout warning fires on every CLI invocation unless suppressed by
  `--quiet` or `CURIK_NO_LAYOUT_WARNING=1`.
- `layout_migrate.py` refuses to run on a dirty tree unless `--force` is passed.

## TODO Reference

- `docs/clasi/todo/sequester-hugo-into-site-in-scaffolded-curriculum-projects.md`

## Tickets

| # | Title | Depends On | Group |
|---|-------|------------|-------|
| 001 | Path helpers module (curik/paths.py) | — | 1 |
| 002 | Update hugo.toml generation + theme install path | 001 | 2 |
| 003 | Update hugo.py (build cwd + content paths) | 001 | 2 |
| 004 | Update scaffolding.py, migrate.py, syllabus.py, readme.py, publish.py | 001 | 2 |
| 005 | Update gitignore, deploy-pages.yml, and agent-facing docs | — | 1 |
| 006 | Legacy-layout detector (layout_check.py) wired into CLI | 001 | 2 |
| 007 | curik migrate hugo-layout command (layout_migrate.py + CLI) | 001, 003 | 3 |
| 008 | Update and add tests | 002, 003, 004, 006, 007 | 4 |
