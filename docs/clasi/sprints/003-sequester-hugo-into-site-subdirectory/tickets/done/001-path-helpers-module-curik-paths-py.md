---
id: "001"
title: "Path helpers module (curik/paths.py)"
status: done
use-cases: [SUC-001, SUC-002, SUC-003, SUC-004]
depends-on: []
github-issue: ""
todo: "sequester-hugo-into-site-in-scaffolded-curriculum-projects.md"
completes_todo: false
---

# Path helpers module (curik/paths.py)

## Description

Create a new pure-utility module `curik/paths.py` that is the single source of
truth for all Hugo-related path construction within curriculum projects. This
module defines the `SITE_DIR` constant and five path-helper functions. Every
other curik module will import from this module instead of hardcoding path strings.

This is the foundational ticket for the sprint. All other path-migration tickets
depend on it.

## Acceptance Criteria

- [x] `curik/paths.py` exists and exports `SITE_DIR`, `site_root`, `hugo_toml_path`,
  `content_dir`, `themes_dir`, and `theme_dir`
- [x] `SITE_DIR = "site"` (string constant, no trailing slash)
- [x] `site_root(root)` returns `root / "site"` where `root` is a `Path`
- [x] `hugo_toml_path(root)` returns `root / "site" / "hugo.toml"`
- [x] `content_dir(root)` returns `root / "site" / "content"`
- [x] `themes_dir(root)` returns `root / "site" / "themes"`
- [x] `theme_dir(root)` returns `root / "site" / "themes" / "curriculum-hugo-theme"`
- [x] All helpers accept a `Path` and return a `Path`
- [x] Module has no side effects (no filesystem calls, no imports from other curik
  modules)
- [x] Module is importable: `from curik.paths import site_root, content_dir` works

## Implementation Plan

**Approach**: Create `curik/paths.py` as a new file. No existing files need
modification in this ticket — subsequent tickets import from it.

**Files to create**:
- `curik/paths.py` — module with `SITE_DIR` constant and five functions

**Structure** (do not implement yet — plan only):
```
SITE_DIR = "site"

def site_root(root: Path) -> Path: ...
def hugo_toml_path(root: Path) -> Path: ...
def content_dir(root: Path) -> Path: ...
def themes_dir(root: Path) -> Path: ...
def theme_dir(root: Path) -> Path: ...
```

Import only `from pathlib import Path` and `from .templates import THEME_NAME`
(for `theme_dir`). Do not import from any other curik module.

**Testing plan**:
- New `tests/test_paths.py` with parametrized tests for each helper
- Each test: given a `Path("/tmp/my-course")`, assert the helper returns the
  correct absolute path
- Test that all helpers return `Path` objects (not strings)
- Run `uv run pytest tests/test_paths.py -v`

**Documentation updates**: None required for this ticket — callers will be updated
in subsequent tickets.

## Testing

- **Existing tests to run**: `uv run pytest -q` (no existing tests should break;
  this ticket only adds a new module)
- **New tests to write**: `tests/test_paths.py` — unit tests for all six exports
- **Verification command**: `uv run pytest tests/test_paths.py -v && uv run pytest -q`
