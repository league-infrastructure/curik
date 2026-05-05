---
id: "002"
title: "Update hugo.toml generation and theme install path"
status: done
use-cases: [SUC-001]
depends-on: ["001"]
github-issue: ""
todo: ""
completes_todo: false
---

# Update hugo.toml generation and theme install path

## Description

Update `curik/templates.py` to write `hugo.toml` and install the theme into
`site/` instead of the project root. Three functions change:

1. `get_hugo_config()` — change the `course.yml` data mount from
   `source = "course.yml"` to `source = "../course.yml"`. Since `hugo.toml` now
   lives at `site/hugo.toml`, Hugo resolves mounts relative to `hugo.toml`'s
   directory. The `content` mount stays `source = "content"` (= `site/content/`).

2. `hugo_setup()` — change `hugo_toml` to `hugo_toml_path(root)` and `theme_dest`
   to `theme_dir(root)`. Create `site/` parent directory before writing `hugo.toml`.

3. `bump_curriculum_version()` — change `hugo_toml = root / "hugo.toml"` to
   `hugo_toml = hugo_toml_path(root)`.

`hugo_setup_from_course()` delegates to `hugo_setup`; no change needed there.

## Acceptance Criteria

- [x] `curik hugo setup` writes `hugo.toml` to `site/hugo.toml`, not `hugo.toml`
- [x] `curik hugo setup` installs theme to `site/themes/curriculum-hugo-theme/`
- [x] Generated `hugo.toml` has `source = "../course.yml"` in the data mount
- [x] Generated `hugo.toml` has `source = "content"` in the content mount (unchanged)
- [x] `site/` directory is created if it does not exist before writing `hugo.toml`
- [x] `bump_curriculum_version()` reads and writes `site/hugo.toml`
- [x] Existing `[params]` preservation logic works with the new path
- [x] No `hugo.toml` is written at the project root

## Implementation Plan

**Files to modify**: `curik/templates.py`

**Specific changes**:
1. Add import: `from .paths import hugo_toml_path, theme_dir, site_root`
2. In `bump_curriculum_version()`: `hugo_toml = hugo_toml_path(root)`
3. In `get_hugo_config()`: change `'  source = "course.yml"'` to
   `'  source = "../course.yml"'`
4. In `hugo_setup()`:
   - `hugo_toml = hugo_toml_path(root)`
   - `theme_dest = theme_dir(root)`
   - Add `site_root(root).mkdir(parents=True, exist_ok=True)` before writing
   - `theme_dest.parent.mkdir(parents=True, exist_ok=True)` resolves to
     `site/themes/` (no logic change needed, just path changes)

**Testing plan**:
- Update `tests/test_hugo.py` `HugoSetupTest` fixture assertions:
  `root / "hugo.toml"` → `root / "site" / "hugo.toml"`,
  `root / "themes" / ...` → `root / "site" / "themes" / ...`
- Add test asserting generated config contains `source = "../course.yml"`
- Add test asserting `root / "hugo.toml"` does NOT exist after setup

## Testing

- **Existing tests to run**: `uv run pytest tests/test_hugo.py -v`
- **New tests to write**: Updated assertions in `HugoSetupTest`; new mount assertion
- **Verification command**: `uv run pytest tests/test_hugo.py -v && uv run pytest -q`
