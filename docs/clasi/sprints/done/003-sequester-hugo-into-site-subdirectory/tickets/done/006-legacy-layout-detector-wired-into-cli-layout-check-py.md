---
id: "006"
title: "Legacy-layout detector wired into CLI (layout_check.py)"
status: done
use-cases: [SUC-002]
depends-on: ["001"]
github-issue: ""
todo: ""
completes_todo: false
---

# Legacy-layout detector wired into CLI (layout_check.py)

## Description

Create `curik/layout_check.py` with a single function `check_legacy_hugo_layout`
that returns a warning string when a project uses the old root-level Hugo layout,
and wire it into `curik/cli.py`'s `main()` so it fires on every CLI invocation.

**Detection rule**: Return a warning string if ANY of the following exist:
- `root/hugo.toml`
- `root/themes/curriculum-hugo-theme/`
- `root/content/_index.md`

AND `root/site/hugo.toml` does NOT exist.

Return `None` if layout is correct or no Hugo presence detected.

**Warning message** (printed to stderr):
```
WARNING: This project uses the legacy Hugo layout (hugo.toml at root).
Run `curik migrate hugo-layout` to move Hugo files into site/.
The legacy layout will stop working in a future release.
```

**Suppression**: Do not emit the warning when `CURIK_NO_LAYOUT_WARNING=1` environment
variable is set.

**CLI wiring**: In `main()`, after `--path` is resolved to `root`, call
`check_legacy_hugo_layout(root)` and print any non-None result to `sys.stderr`.
This must happen before the handler dispatch so it fires on every command. Exception:
skip the check if the command is `migrate` with subcommand `hugo-layout` (the migrate
command is the resolution action, no need to warn during it).

## Acceptance Criteria

- [x] `curik/layout_check.py` exists with `check_legacy_hugo_layout(root) -> str | None`
- [x] Returns a warning string when `root/hugo.toml` exists and `root/site/hugo.toml`
  does not
- [x] Returns a warning string when `root/themes/curriculum-hugo-theme/` exists and
  `root/site/hugo.toml` does not
- [x] Returns `None` when `root/site/hugo.toml` exists (new layout)
- [x] Returns `None` when no Hugo files detected at all (non-Hugo project)
- [x] Warning fires to stderr before command output on every `curik` command
- [x] `CURIK_NO_LAYOUT_WARNING=1 curik <command>` suppresses the warning
- [x] Warning does NOT fire when running `curik migrate hugo-layout`
- [x] No existing commands break

## Implementation Plan

**Files to create**: `curik/layout_check.py`

**Files to modify**: `curik/cli.py`

**layout_check.py structure**:
```python
import os
from pathlib import Path
from .paths import hugo_toml_path, themes_dir, content_dir

_WARNING = (
    "WARNING: This project uses the legacy Hugo layout (hugo.toml at root).\n"
    "Run `curik migrate hugo-layout` to move Hugo files into site/.\n"
    "The legacy layout will stop working in a future release."
)

def check_legacy_hugo_layout(root: Path) -> str | None:
    if os.environ.get("CURIK_NO_LAYOUT_WARNING"):
        return None
    if hugo_toml_path(root).exists():
        return None  # already on new layout
    legacy_indicators = [
        root / "hugo.toml",
        root / "themes" / "curriculum-hugo-theme",
        root / "content" / "_index.md",
    ]
    if any(p.exists() for p in legacy_indicators):
        return _WARNING
    return None
```

**cli.py wiring**: Near the top of `main()`, after `args = parser.parse_args(argv)`,
resolve `root = Path(getattr(args, "path", ".")).resolve()`, then:
```python
# Skip warning during migration (that's the fix action)
if not (args.command == "migrate" and getattr(args, "migrate_command", None) == "hugo-layout"):
    warn = check_legacy_hugo_layout(root)
    if warn:
        print(warn, file=sys.stderr)
```

Add `from .layout_check import check_legacy_hugo_layout` to cli.py imports.

## Testing

- **Existing tests to run**: `uv run pytest tests/test_cli.py -v`
- **New tests to write**: `tests/test_layout_check.py`:
  - `test_legacy_detected_hugo_toml_at_root`: temp dir with `hugo.toml` at root,
    no `site/hugo.toml` → returns warning string
  - `test_new_layout_no_warning`: temp dir with `site/hugo.toml` → returns None
  - `test_no_hugo_no_warning`: empty temp dir → returns None
  - `test_env_var_suppresses`: legacy layout + `CURIK_NO_LAYOUT_WARNING=1` → None
  - `test_warning_fires_on_cli`: test that `curik status` on a legacy temp project
    emits warning to stderr
  - `test_no_warning_during_migrate`: `curik migrate hugo-layout` does not emit warning
- **Verification command**: `uv run pytest tests/test_layout_check.py tests/test_cli.py -v`
