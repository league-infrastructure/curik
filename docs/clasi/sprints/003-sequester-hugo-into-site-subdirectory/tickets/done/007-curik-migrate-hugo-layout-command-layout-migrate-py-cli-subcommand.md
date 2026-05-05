---
id: "007"
title: "curik migrate hugo-layout command (layout_migrate.py + CLI subcommand)"
status: done
use-cases: [SUC-002]
depends-on: ["001", "003"]
github-issue: ""
todo: ""
completes_todo: false
---

# curik migrate hugo-layout command (layout_migrate.py + CLI subcommand)

## Description

Create `curik/layout_migrate.py` with `migrate_hugo_layout()` and wire it into
`curik/cli.py` as `curik migrate hugo-layout`.

The function performs a one-shot opt-in migration from the legacy root layout to
the `site/` layout. It uses `git mv` when inside a git repo to preserve history.

**Migration steps**:
1. **Check idempotency**: if `site/hugo.toml` exists, return immediately (nothing
   to do). Exit 0.
2. **Check dirty tree**: run `git status --porcelain` in `root`; abort if there are
   uncommitted changes unless `--force` is passed.
3. **Dry-run mode**: if `--dry-run`, print the planned moves and exit 0 without
   writing.
4. **Create `site/`**.
5. **Move files** using `git mv` (fall back to `shutil.move` if not in a git repo):
   - `hugo.toml` → `site/hugo.toml`
   - `themes/` → `site/themes/`
   - `content/` → `site/content/`
   - `layouts/` → `site/layouts/` (only if exists)
   - `static/`, `data/`, `assets/` → `site/<name>/` (only if exist)
6. **Rewrite `site/hugo.toml`** mounts: change `source = "course.yml"` to
   `source = "../course.yml"`. Reuse `_replace_params_section` / `_extract_params_section`
   logic from `templates.py` to keep user `[params]` edits intact.
7. **Update `.gitignore`**: rewrite the `# -- CURIK:START --` block to use
   `site/public/`, `site/resources/_gen/`, `site/.hugo_build.lock`. If no CURIK
   block exists, append the new block.
8. **Verify** (optional, `--verify` flag): run `hugo --source site` to check the
   migrated project builds.
9. **Return summary** dict: `{"moved": [...], "rewritten": [...], "verify_success": bool | None}`.

**CLI subcommand**: `curik migrate hugo-layout [--dry-run] [--force] [--verify]`
Add this as a new subcommand under the existing `migrate` group in `cli.py`.

## Acceptance Criteria

- [x] `curik/layout_migrate.py` exists with `migrate_hugo_layout(root, *, dry_run, force, verify)`
- [x] On an already-migrated project (`site/hugo.toml` exists): exits 0, prints
  "Already on new layout — nothing to do."
- [x] On a dirty git tree without `--force`: exits non-zero with error message
- [x] With `--dry-run`: prints planned moves, makes no filesystem changes
- [x] Moves `hugo.toml`, `themes/`, `content/` to `site/` using `git mv` when in git
- [x] Falls back to `shutil.move` when not in a git repo
- [x] `layouts/`, `static/`, `data/`, `assets/` are moved only if they exist
- [x] `site/hugo.toml` data mount rewritten to `../course.yml`
- [x] `[params]` section from original `hugo.toml` preserved in `site/hugo.toml`
- [x] `.gitignore` CURIK block updated to `site/public/` etc.
- [x] `curik migrate hugo-layout` is idempotent: second run reports nothing to do
- [x] `--verify` flag runs `hugo --source site` and reports success/failure
- [x] `curik migrate hugo-layout` is available as a CLI subcommand

## Implementation Plan

**Files to create**: `curik/layout_migrate.py`

**Files to modify**: `curik/cli.py`

**layout_migrate.py imports**:
```python
import os, shutil, subprocess
from pathlib import Path
from .paths import site_root, hugo_toml_path
from .templates import _extract_params_section, _replace_params_section
```

**Gitignore rewrite**: Read the file, find the `# -- CURIK:START --` / `# -- CURIK:END --`
block, replace its contents with the new `site/` paths. If no such block, append it.
Pattern: same logic used in `init_command.py` for writing the gitignore block.

**Git detection**: `(root / ".git").exists()` → use `git mv`; else `shutil.move`.

**CLI wiring in cli.py**:
1. Add `from .layout_migrate import migrate_hugo_layout` to imports
2. Under the `migrate` subparser, add `hugo-layout` subcommand with
   `--dry-run`, `--force`, `--verify` flags
3. Add `elif sub == "hugo-layout":` branch in `_handle_migrate()`

**Note on `_extract_params_section` / `_replace_params_section`**: These are private
functions in `templates.py`. Either make them importable (rename without leading `_`)
or duplicate the minimal logic needed in `layout_migrate.py`. Prefer making them
importable by removing the underscore prefix — they are stable utilities, not
implementation details.

## Testing

- **Existing tests to run**: `uv run pytest tests/test_migration.py tests/test_cli.py -v`
- **New tests to write**: `tests/test_layout_migrate.py`:
  - `test_fresh_project_no_op`: new-layout project → nothing to do, returns empty moved list
  - `test_legacy_migration`: temp dir with `hugo.toml`, `themes/`, `content/` at root
    (non-git) → all moved to `site/`; `site/hugo.toml` mount is `../course.yml`
  - `test_dirty_tree_refusal`: dirty git repo without `--force` → raises or returns error
  - `test_idempotency`: run migration twice → second run is no-op
  - `test_dry_run_no_writes`: `--dry-run` returns plan dict but no files created
  - `test_gitignore_rewritten`: `.gitignore` CURIK block updated to `site/` paths
  - `test_layouts_moved_if_exists`: `layouts/` at root is moved
  - `test_layouts_skipped_if_absent`: no error if `layouts/` does not exist
- **Verification command**: `uv run pytest tests/test_layout_migrate.py -v && uv run pytest -q`
