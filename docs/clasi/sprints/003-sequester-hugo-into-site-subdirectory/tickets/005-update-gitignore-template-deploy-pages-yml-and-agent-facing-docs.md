---
id: "005"
title: "Update gitignore template, deploy-pages.yml, and agent-facing docs"
status: todo
use-cases: [SUC-001, SUC-002]
depends-on: []
github-issue: ""
todo: ""
completes_todo: false
---

# Update gitignore template, deploy-pages.yml, and agent-facing docs

## Description

Update static template files and agent-facing documentation to reflect the new
`site/` layout. These are text/config changes with no Python logic.

This ticket is independent of the Python path-helper work (no dependency on T001)
and can be done in parallel with Group 2 tickets.

**curik/init/gitignore** — Replace the Hugo section in the CURIK block:
```
# Hugo build output (now under site/)
site/public/
site/resources/_gen/

# Hugo lock file
site/.hugo_build.lock
```
(Remove the old `public/`, `resources/_gen/`, `.hugo_build.lock` lines.)

**curik/init/deploy-pages.yml** — Two changes:
- Build step: `run: hugo --minify` → `run: hugo --minify --source site`
- Upload path: `path: ./public` → `path: ./site/public`

**curik/init/claude-section.md** — "Hugo Theme" section:
- `themes/curriculum-hugo-theme/` → `site/themes/curriculum-hugo-theme/`
- `hugo.toml` at project root → `site/hugo.toml`

**curik/references/hugo-conventions.md** — All root-relative Hugo paths:
- `hugo.toml` → `site/hugo.toml`
- `content/` → `site/content/`
- `themes/curriculum-hugo-theme/` → `site/themes/curriculum-hugo-theme/`
- `run hugo` in project root → `run hugo` from `site/` or via `curik hugo build`
- Build output `public/` → `site/public/`

**curik/skills/repo-scaffolding.md** — Scaffolded layout example:
- Update the directory tree to show `site/` subdirectory structure matching the
  new layout (see TODO for the exact tree).

**curik/agents/start-curik.md** — Paths table (line 104 area):
- Update `hugo.toml | File |` row to `site/hugo.toml | File |`
- Update any `content/` or `themes/` references in the paths table

## Acceptance Criteria

- [ ] `curik/init/gitignore` CURIK block uses `site/public/`, `site/resources/_gen/`,
  `site/.hugo_build.lock`; old root-level paths removed
- [ ] `curik/init/deploy-pages.yml` build step runs `hugo --minify --source site`
- [ ] `curik/init/deploy-pages.yml` upload artifact path is `./site/public`
- [ ] `curik/init/claude-section.md` "Hugo Theme" section references `site/themes/`
  and `site/hugo.toml`
- [ ] `curik/references/hugo-conventions.md` has no root-relative Hugo paths (all
  updated with `site/` prefix)
- [ ] `curik/skills/repo-scaffolding.md` layout example shows `site/` directory tree
- [ ] `curik/agents/start-curik.md` paths table reflects new layout

## Implementation Plan

**Files to modify** (all text edits):
- `curik/init/gitignore`
- `curik/init/deploy-pages.yml`
- `curik/init/claude-section.md`
- `curik/references/hugo-conventions.md`
- `curik/skills/repo-scaffolding.md`
- `curik/agents/start-curik.md`

No Python changes in this ticket.

**Testing plan**: No automated tests for template content. Manual check:
- After `curik init` on a test project, verify the written `.gitignore` and
  `deploy-pages.yml` contain the new paths
- Verify `CLAUDE.md` written to a test project references `site/` paths

## Testing

- **Existing tests to run**: `uv run pytest tests/test_init_command.py -v` (verify
  init still writes templates correctly)
- **New tests to write**: Optionally add assertions in `test_init_command.py` that
  written `.gitignore` contains `site/public/`
- **Verification command**: `uv run pytest tests/test_init_command.py -v`
