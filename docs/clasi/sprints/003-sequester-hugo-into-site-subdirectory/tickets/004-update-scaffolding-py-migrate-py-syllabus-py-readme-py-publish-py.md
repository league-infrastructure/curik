---
id: "004"
title: "Update scaffolding.py, migrate.py, syllabus.py, readme.py, publish.py"
status: todo
use-cases: [SUC-001, SUC-002]
depends-on: ["001"]
github-issue: ""
todo: ""
completes_todo: false
---

# Update scaffolding.py, migrate.py, syllabus.py, readme.py, publish.py

## Description

Route all remaining content and Hugo-path references through `curik/paths.py` helpers
in five domain modules. Each module currently hardcodes `"content"`, `"hugo.toml"`,
or `"themes"` relative to the project root.

**scaffolding.py**:
- `scaffold_structure()`: `content_dir = root / "content"` → `content_dir_fn(root)`.
  Module dir creation and lesson stubs route through the helper.
- `create_lesson_stub()`: `mod_dir = root / "content" / module` → `content_dir_fn(root) / module`.

**migrate.py**:
- `migrate_structure()`: content dir, theme dest, and hugo.toml path via helpers.
- `_PROTECTED_NAMES`: add `"site"`, remove `"hugo.toml"` and `"themes"` (they no
  longer live at root in new-layout projects).
- `inventory_course()`: Hugo generator detection: check both `root / "hugo.toml"`
  (legacy) and `hugo_toml_path(root)` (new layout).

**syllabus.py**:
- `validate_syllabus_consistency()`: `docs_dir = root / "content"` →
  `content_dir_fn(root)`.

**readme.py**:
- `generate_readmes(root, docs_dir="content")`: the `docs_dir` default is used as
  a string passed to `root / docs_dir`. Change the default to `"site/content"` so
  callers that omit `docs_dir` get the correct path. Callers that pass an explicit
  `docs_dir` are unaffected.
- Also update `curik/cli.py` line 1009: `default="content"` → `default="site/content"`.

**publish.py**:
- `has_hugo_toml`: `(root / "hugo.toml").exists()` → `hugo_toml_path(root).exists()`
- `has_theme`: `root / "themes" / "curriculum-hugo-theme"` → `theme_dir(root)`
- `has_local_baseof`: `root / "layouts" / ...` → `site_root(root) / "layouts" / ...`
- Content dir scan: `root / "content"` → `content_dir_fn(root)`
- `base_url` read: `root / "hugo.toml"` → `hugo_toml_path(root)`

## Acceptance Criteria

- [ ] `scaffold_structure()` creates `site/content/_index.md` and module dirs under
  `site/content/`
- [ ] `create_lesson_stub()` creates lesson files under `site/content/<module>/`
- [ ] `migrate_structure()` creates `site/content/`, `site/themes/`, `site/hugo.toml`
- [ ] `_PROTECTED_NAMES` contains `"site"` and does NOT contain `"hugo.toml"` or
  `"themes"`
- [ ] `inventory_course()` correctly detects Hugo presence in both legacy and new
  layout projects
- [ ] `validate_syllabus_consistency()` scans `site/content/` for UID frontmatter
- [ ] `generate_readmes()` default `docs_dir` is `"site/content"`
- [ ] `curik readme generate` (no `--docs-dir`) reads from `site/content/`
- [ ] `publish.py` readiness checks detect Hugo presence via new-layout paths
- [ ] `check_publish_ready()` returns correct result for a new-layout project

## Implementation Plan

**Files to modify**:
- `curik/scaffolding.py`
- `curik/migrate.py`
- `curik/syllabus.py`
- `curik/readme.py`
- `curik/publish.py`
- `curik/cli.py` (one line: `--docs-dir` default in readme subparser)

**Imports to add** in each file:
```python
from .paths import content_dir as content_dir_fn  # scaffolding, syllabus, readme, publish
from .paths import hugo_toml_path, theme_dir, site_root  # migrate, publish
```

**Note on migrate.py `_PROTECTED_NAMES`**: This is a `frozenset`. The change is:
```python
_PROTECTED_NAMES = frozenset({
    CURIK_DIR, ".git", ".github", ".gitignore", ".mcp.json",
    ".claude", ".vscode", "CLAUDE.md", "course.yml",
    "site",   # NEW: protect new-layout Hugo dir
    "_old",
    # "hugo.toml" and "themes" removed — they're under site/ now
})
```

**Note on publish.py `has_local_baseof`**: Legacy layout had `root/layouts/`. New
layout has `site/layouts/`. Use `site_root(root) / "layouts" / "_default" / "baseof.html"`.

## Testing

- **Existing tests to run**: `uv run pytest tests/test_scaffolding.py tests/test_migration.py tests/test_publish.py tests/test_sequester.py -v`
- **New tests to write**: Update fixtures in each test file to use `site/` paths;
  update assertions on `_PROTECTED_NAMES` content in `test_migration.py`
- **Verification command**: `uv run pytest tests/test_scaffolding.py tests/test_migration.py tests/test_publish.py -v`
