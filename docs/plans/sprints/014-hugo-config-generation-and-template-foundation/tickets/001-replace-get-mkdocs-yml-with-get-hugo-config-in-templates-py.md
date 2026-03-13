---
id: "001"
title: "Replace get_mkdocs_yml with get_hugo_config in templates.py"
status: todo
use-cases: [SUC-001]
depends-on: []
---

# Replace get_mkdocs_yml with get_hugo_config in templates.py

## Description

Remove `get_mkdocs_yml()` and add `get_hugo_config(title, tier, theme_path)`
that returns a valid Hugo TOML config string. Tier 1-2 includes
`instructorGuide = true` param. All tiers reference `league-hugo-theme` and
enable syntax highlighting and code copy.

## Acceptance Criteria

- [ ] `get_mkdocs_yml()` removed from `templates.py`
- [ ] `get_hugo_config()` returns valid TOML for tiers 1-4
- [ ] Tier 1-2 config includes `instructorGuide = true` in `[params]`
- [ ] Tier 3-4 config omits `instructorGuide`
- [ ] All tiers reference `league-hugo-theme`
- [ ] Tests updated and passing

## Testing

- **Existing tests to run**: `tests/test_scaffolding.py` (MkdocsNavTest)
- **New tests to write**: `test_hugo_config_tier1`, `test_hugo_config_tier3`,
  `test_hugo_config_with_theme_path`
- **Verification command**: `uv run pytest tests/test_scaffolding.py`
