---
id: "008"
title: "Update and add tests for site/ layout"
status: todo
use-cases: [SUC-001, SUC-002, SUC-003, SUC-004]
depends-on: ["002", "003", "004", "006", "007"]
github-issue: ""
todo: "sequester-hugo-into-site-in-scaffolded-curriculum-projects.md"
completes_todo: true
---

# Update and add tests for site/ layout

## Description

Update all existing test files that assert on Hugo-related paths to use the new
`site/` layout. Create two new test files for `layout_check.py` and
`layout_migrate.py`. This ticket runs after all implementation tickets are done
and verifies the entire sprint with a green test suite.

**Note**: Individual implementation tickets (T002–T007) already specify the fixture
and assertion changes needed in their respective test files. This ticket consolidates
the remaining cross-cutting test work and ensures the full suite passes.

## Acceptance Criteria

- [ ] `uv run pytest -q` passes with zero failures
- [ ] `tests/test_hugo.py` — all fixtures use `site/content/` layout; all Hugo
  setup assertions use `site/hugo.toml` and `site/themes/`
- [ ] `tests/test_scaffolding.py` — module and lesson stub assertions use
  `site/content/...`
- [ ] `tests/test_migration.py` — `migrate_structure` output paths use `site/`
  prefix; `_PROTECTED_NAMES` tests verify `"site"` is in the set and `"hugo.toml"`
  and `"themes"` are not
- [ ] `tests/test_cli.py` — Hugo CLI handler fixtures use `site/` layout;
  `--docs-dir` default tests expect `"site/content"` not `"content"`
- [ ] `tests/test_publish.py` — readiness check fixtures place Hugo files under
  `site/`
- [ ] `tests/test_layout_check.py` (new) — see T006 testing plan for required cases
- [ ] `tests/test_layout_migrate.py` (new) — see T007 testing plan for required cases
- [ ] `tests/test_paths.py` (new) — see T001 testing plan for required cases

## Implementation Plan

**Systematic approach**: Run `uv run pytest -q` after T001-T007 are done. Identify
any remaining failures. For each failure:
1. Identify whether the fixture creates a Hugo project (needs `site/` subdirs)
2. Update `setUp` or fixture helper to create `site/content/`, `site/hugo.toml`,
   `site/themes/curriculum-hugo-theme/`
3. Update assertions from `root / "hugo.toml"` to `root / "site" / "hugo.toml"` etc.

**Common fixture pattern** (before):
```python
(tmp_path / "hugo.toml").write_text(...)
(tmp_path / "content").mkdir()
```

**Common fixture pattern** (after):
```python
(tmp_path / "site").mkdir()
(tmp_path / "site" / "hugo.toml").write_text(...)
(tmp_path / "site" / "content").mkdir()
```

**Files to modify**:
- `tests/test_hugo.py`
- `tests/test_scaffolding.py`
- `tests/test_migration.py`
- `tests/test_cli.py`
- `tests/test_publish.py`

**Files to create**:
- `tests/test_paths.py`
- `tests/test_layout_check.py`
- `tests/test_layout_migrate.py`

Note: `tests/test_paths.py`, `tests/test_layout_check.py`, and
`tests/test_layout_migrate.py` may already be created by T001, T006, and T007
respectively. If so, this ticket only needs to verify they exist and pass.

## Testing

- **Existing tests to run**: Full suite — `uv run pytest -q`
- **New tests to write**: New test files as listed; fixture updates in existing files
- **Verification command**: `uv run pytest -q` — must show zero failures
