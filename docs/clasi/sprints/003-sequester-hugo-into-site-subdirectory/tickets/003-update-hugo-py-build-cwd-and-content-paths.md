---
id: "003"
title: "Update hugo.py — build cwd and content paths"
status: todo
use-cases: [SUC-003, SUC-004]
depends-on: ["001"]
github-issue: ""
todo: ""
completes_todo: false
---

# Update hugo.py — build cwd and content paths

## Description

Update `curik/hugo.py` so all content read/write operations use `content_dir(root)`
(= `root/site/content/`) and `hugo_build()` runs from `site_root(root)`.

Four functions require attention:

1. `hugo_build()` — `cwd` changes from `str(root)` to `str(site_root(root))`.

2. `list_content_pages()` — resolves content directory via `content_dir_fn(root)`.
   Returned `path` values remain relative to `content_dir` (e.g., `01-intro/01-hello.md`),
   not to `root`. Public API unchanged.

3. `create_content_page()` — `content_dir` local variable resolves via helper.
   Path-traversal guard uses the resolved helper path. Returned path is still
   relative to `content_dir`.

4. `update_frontmatter()` — currently resolves `full_path = root / page_path`.
   Verify that `page_path` callers pass paths relative to `content_dir`; if so,
   change to `content_dir_fn(root) / page_path`.

## Acceptance Criteria

- [ ] `hugo_build(root)` runs Hugo with `cwd = root/site/`
- [ ] `list_content_pages(root)` reads from `root/site/content/`
- [ ] Paths returned by `list_content_pages` are relative to `site/content/`,
  not to `root` (e.g., `01-intro/01-hello.md`, not `site/content/01-intro/01-hello.md`)
- [ ] `create_content_page(root, "mod/page.md", "Title")` creates
  `root/site/content/mod/page.md`
- [ ] `create_content_page` returns `"mod/page.md"` (not `"site/content/mod/page.md"`)
- [ ] Path traversal guard blocks paths escaping `site/content/`
- [ ] `update_frontmatter` resolves pages under `site/content/`

## Implementation Plan

**Files to modify**: `curik/hugo.py`

**Specific changes**:
1. Add import: `from .paths import site_root, content_dir as content_dir_fn`
   (alias because `content_dir` is used as a local variable in existing code)
2. `hugo_build()`: `cwd=str(site_root(root))`
3. `list_content_pages()`: `_content_dir = content_dir_fn(root)` — replace all
   references to `content_dir` local var with `_content_dir`
4. `create_content_page()`: `_content_dir = content_dir_fn(root).resolve()`
5. `update_frontmatter()`: trace `page_path` usage in CLI handlers; if callers
   pass content-dir-relative paths, resolve as `content_dir_fn(root) / page_path`

**Important**: The return values of `list_content_pages` and `create_content_page`
must remain relative to the `content_dir`, not to `root`. This is the key invariant
that keeps the CLI surface stable.

**Testing plan**:
- `tests/test_hugo.py`: update temp-dir fixtures to create files under
  `tmp/site/content/`
- Assert `create_content_page` returns `"mod/page.md"` (no `site/` prefix)
- Assert `hugo_build` subprocess call uses correct cwd (mock subprocess.run)

## Testing

- **Existing tests to run**: `uv run pytest tests/test_hugo.py tests/test_cli.py -v`
- **New tests to write**: Updated fixtures in `test_hugo.py`; cwd assertion for
  `hugo_build`
- **Verification command**: `uv run pytest tests/test_hugo.py -v && uv run pytest -q`
