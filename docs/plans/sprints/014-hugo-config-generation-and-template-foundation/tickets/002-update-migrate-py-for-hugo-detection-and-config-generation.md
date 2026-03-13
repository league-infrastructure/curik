---
id: "002"
title: "Update migrate.py for Hugo detection and config generation"
status: todo
use-cases: [SUC-002]
depends-on: ["001"]
---

# Update migrate.py for Hugo detection and config generation

## Description

Update `inventory_course()` to detect Hugo projects via `hugo.toml` and
`migrate_structure()` to generate Hugo config and `content/` directory
with `_index.md` files instead of MkDocs config and `docs/`.

## Acceptance Criteria

- [ ] `inventory_course()` detects `hugo.toml` → `"hugo"`
- [ ] Legacy `mkdocs.yml` → `"mkdocs"` detection preserved
- [ ] `migrate_structure()` creates `hugo.toml` (not `mkdocs.yml`)
- [ ] `migrate_structure()` creates `content/` (not `docs/`)
- [ ] Module directories get `_index.md` (not `index.md`)
- [ ] Import updated from `get_mkdocs_yml` to `get_hugo_config`
- [ ] Tests updated and passing

## Testing

- **Existing tests to run**: `tests/test_migration.py`
- **New tests to write**: `test_detects_hugo_generator`,
  update `test_creates_tier3_structure` for Hugo
- **Verification command**: `uv run pytest tests/test_migration.py`
