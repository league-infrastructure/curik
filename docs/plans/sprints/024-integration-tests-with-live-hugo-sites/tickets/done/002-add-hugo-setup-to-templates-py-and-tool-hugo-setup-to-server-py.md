---
id: '002'
title: Add hugo_setup() to templates.py and tool_hugo_setup() to server.py
status: done
use-cases:
- SUC-001
depends-on:
- '001'
---

# Add hugo_setup() to templates.py and tool_hugo_setup() to server.py

## Description

Create `hugo_setup(root, title, tier)` in `curik/templates.py` that:
1. Calls `get_hugo_config(title, tier)` and writes `hugo.toml` to root
2. Copies `curriculum-hugo-theme/` from curik's bundled copy
   (`get_theme_source()`) to `root / "themes" / "curriculum-hugo-theme"`

Expose as `tool_hugo_setup()` MCP tool in `curik/server.py`.

Wire `scaffold_structure()` to call `hugo_setup()` — read title and tier
from `course.yml` in the project root.

## Acceptance Criteria

- [ ] `hugo_setup()` function exists in templates.py
- [ ] `hugo_setup()` generates valid `hugo.toml` at project root
- [ ] `hugo_setup()` copies theme to `themes/curriculum-hugo-theme/`
- [ ] `scaffold_structure()` calls `hugo_setup()` automatically
- [ ] `tool_hugo_setup()` MCP tool registered in server.py
- [ ] Unit tests for `hugo_setup()` standalone behavior

## Testing

- **Existing tests to run**: `tests/test_scaffolding.py`, `tests/test_hugo.py`
- **New tests to write**: Test hugo_setup creates hugo.toml and copies theme
- **Verification command**: `python3 -m pytest tests/test_scaffolding.py tests/test_hugo.py -v`
