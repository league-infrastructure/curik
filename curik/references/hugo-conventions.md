# Hugo Conventions

This document describes how Curik projects use Hugo as the static site
generator. Lesson authors and reviewers consult this reference.

## Configuration

The `hugo.toml` file in the project root configures Hugo:

```toml
baseURL = "/"
title = "Course Title"
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
  instructorGuide = true  # Tier 1-2 only
```

Tiers 3–4 add `[params.syllabus]` for syllabus integration.

## Content Directory Structure

```
content/
  _index.md                  # Course landing page
  01-module-name/
    _index.md                # Module overview (branch bundle)
    01-lesson-name.md        # Lesson page
    02-lesson-name.md        # Lesson page
  02-module-name/
    _index.md
    01-lesson-name.md
```

- **`_index.md`** files are Hugo branch bundles — they define section pages
- **Numeric prefixes** (`01-`, `02-`) control navigation order
- **No explicit nav file** — Hugo builds navigation from directory structure

## Frontmatter

Every content page has YAML frontmatter:

```yaml
---
title: "Variables and Types"
weight: 10
draft: false
---
```

- `title`: Page title (used in nav and headings)
- `weight`: Sort order within the section (lower = earlier)
- `draft: true`: Hides page from published site

## Shortcodes

**NEVER use raw HTML in content pages.** Always use Hugo shortcodes:

### Instructor Guide

```markdown
{{</* instructor-guide */>}}

**Objectives:**
- Write a for-loop that iterates over a list

**Materials:**
- Projector with starter notebook displayed

{{</* /instructor-guide */>}}
```

Wraps instructor-only content. Tier 1–2: displayed prominently (primary
layout). Tier 3–4: collapsible section.

### Callout

```markdown
{{</* callout type="tip" */>}}
Remember to save before running!
{{</* /callout */>}}
```

Valid types: `tip`, `warning`, `info`. Renders as a styled box.

### README Guards (Tier 3–4 only)

```markdown
{{</* readme-shared */>}}
# Getting Started
This content appears on the site AND in the generated README.
{{</* /readme-shared */>}}

{{</* readme-only */>}}
This content appears ONLY in the generated README, not on the site.
{{</* /readme-only */>}}
```

Used for generating `README.md` files in lesson mirror directories
(`lessons/`, `projects/`).

## League Hugo Theme

The `league-hugo-theme` provides:
- Base layout with League branding (orange/black/white)
- Shortcode implementations (instructor-guide, callout, readme guards)
- CSS for consistent styling across all curricula
- Code syntax highlighting
- Search functionality
- Responsive navigation

Referenced in `hugo.toml` via the `theme` field. Distributed as a git
submodule or Hugo module.

## Building

Run `hugo` in the project root to build. The Curik MCP server provides
`hugo_build()` which runs this and returns success/failure status.

For local development: `hugo server` starts a live-reload dev server.

## Tier-Specific Conventions

### Tier 1–2

- `instructorGuide = true` in hugo.toml params
- Instructor guide is the primary content (takes most of the page)
- No README guards, no syllabus integration
- Simpler page structure

### Tier 3–4

- Student content is primary, instructor guide is supplementary
- README guards required for lesson pages
- Syllabus integration via `syllabus.yaml`
- Notebook companion files (`.ipynb`) alongside `.md` pages
- Mirror directories: `lessons/` and `projects/` with generated READMEs
