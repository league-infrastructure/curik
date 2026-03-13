---
id: '017'
title: League Hugo Theme
status: done
branch: sprint/017-league-hugo-theme
use-cases:
- TUC-001
- TUC-002
---

# Sprint 017: League Hugo Theme

## Goals

Create the `league-hugo-theme` subdirectory within the Curik repo
containing Hugo shortcodes, base layout, and CSS that all League
curricula will use. This ensures consistent rendering of instructor
guides, callouts, and README guards across all courses.

## Problem

The Python code and agent/skill docs now reference Hugo shortcodes
(`{{< instructor-guide >}}`, `{{< readme-shared >}}`, etc.) but no
theme exists to render them. Without a theme, `hugo server` on any
generated curriculum will fail to render these shortcodes.

## Solution

Create a Hugo theme directory (`league-hugo-theme/`) with:
- Shortcode templates for instructor-guide, callout, readme-shared,
  readme-only
- A base layout template
- Minimal CSS for instructor guide show/hide toggle
- A `theme.toml` manifest

This lives in-repo for now. It will be extracted to a separate repo
later when multiple curricula need to reference it.

## Success Criteria

- `league-hugo-theme/` directory exists with valid Hugo theme structure
- All 4 shortcode templates exist and contain valid Hugo template code
- Base layout template exists
- `theme.toml` has correct metadata
- CSS for instructor guide toggle exists

## Scope

### In Scope

- Theme scaffold: theme.toml, layouts, assets
- Instructor-guide shortcode (show/hide toggle)
- Callout shortcode (info/warning/tip)
- Readme-shared shortcode (renders normally)
- Readme-only shortcode (hidden from rendered site)
- Base layout template
- Minimal CSS

### Out of Scope

- Full visual design / branding
- Extracting to separate repo
- Hugo binary installation
- Integration testing with actual Hugo builds

## Test Strategy

No Python tests needed — this is HTML/CSS/Hugo template code. Verify
file structure exists and files are non-empty. The existing asset-loading
tests in the test suite will continue to pass since this sprint doesn't
modify Python code.

## Architecture Notes

Hugo theme directory structure follows Hugo conventions:
```
league-hugo-theme/
  theme.toml
  layouts/
    _default/
      baseof.html
    shortcodes/
      instructor-guide.html
      callout.html
      readme-shared.html
      readme-only.html
  assets/
    css/
      instructor-guide.css
```

Curricula reference the theme via `hugo.toml`:
```toml
theme = "league-hugo-theme"
```

## Definition of Ready

- [x] Sprint planning documents are complete
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

1. Theme scaffold — theme.toml, directory structure, base layout
2. Instructor-guide and callout shortcodes + CSS
3. Readme-shared and readme-only shortcodes
