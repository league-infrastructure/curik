---
title: Curik scaffold_structure does not produce a runnable Hugo site
status: open
created: 2026-03-13
---

## Problem

When `tool_scaffold_structure()` creates the directory tree for a course, the result is not a runnable Hugo site. Several pieces are missing, and one structural issue means Hugo can't even find the content.

## Issues Found

### 1. Modules scaffolded at repo root, not under `content/`

`tool_scaffold_structure()` creates module directories (e.g., `01-getting-started/`) at the repository root. Hugo expects them under `content/`. The `repo-scaffolding` skill and `hugo-conventions` instruction both document that content lives under `content/`, but the scaffold tool doesn't follow this convention.

**Fix**: `tool_scaffold_structure()` should create all module/lesson directories under `content/`, not at the repo root. It should also create `content/_index.md` as the course landing page.

### 2. No `hugo.toml` created

The scaffold does not generate a `hugo.toml` configuration file. Without it, `hugo server` has no config to work with. The `hugo-conventions` instruction documents the expected config format.

**Fix**: `tool_scaffold_structure()` (or a separate setup step) should generate `hugo.toml` with at minimum:
```toml
baseURL = "/"
title = "<course title from course.yml>"
theme = "league-hugo-theme"

[markup]
  [markup.highlight]
    codeFences = true
    guessSyntax = true
    lineNos = false
  [markup.tableOfContents]
    startLevel = 2
    endLevel = 3

[params]
  instructorGuide = true  # for Tier 1-2
```

### 3. No `league-hugo-theme` available

The `hugo-conventions` instruction references `league-hugo-theme` as the theme, and lesson stubs use its shortcodes (`instructor-guide`, `callout`). But the theme doesn't exist as a published repo or Hugo module. The agent has no way to install it.

**Fix options**:
- Publish `league-hugo-theme` as a GitHub repo (e.g., `league-curriculum/league-hugo-theme`) and have the scaffold add it as a git submodule under `themes/`
- Or bundle it as a Hugo module and configure `hugo.toml` to fetch it
- Or at minimum, have the scaffold create stub shortcode templates in `layouts/shortcodes/` so Hugo can render pages without the theme

### 4. Lesson stubs use shortcodes that require the theme

The `tool_scaffold_structure()` creates lesson stubs containing `{{</* instructor-guide */>}}` shortcodes. If the theme isn't installed, Hugo fails to build with: `template for shortcode "instructor-guide" not found`.

**Fix**: Either ensure the theme is always installed during scaffolding, or don't include shortcodes in stubs until the theme is confirmed available.

### 5. `tool_hugo_build()` doesn't check for prerequisites

`tool_hugo_build()` checks if Hugo is installed but doesn't check for `hugo.toml`, `content/` directory, or theme availability. It should validate these before attempting a build and return actionable error messages.

## Expected Behavior

After running `tool_scaffold_structure()` on a fresh course, an agent should be able to immediately run `hugo server` and see a working site with stub pages. The current flow requires manual intervention to:
1. Move directories into `content/`
2. Create `hugo.toml`
3. Create `content/_index.md`
4. Install or stub out the theme and shortcodes

## Environment
- Curik version: 0.20260313.5
- Hugo version: 0.157.0+extended
- Course tier: 2
