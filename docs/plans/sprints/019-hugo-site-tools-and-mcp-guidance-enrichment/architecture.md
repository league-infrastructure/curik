---
status: complete
---

# Architecture

## Architecture Overview

Curik is a Python MCP server that guides AI agents through curriculum
development using Hugo as the static site generator. Sprints 014–018
completed the MkDocs-to-Hugo migration and added CLAUDE.md installation.

This sprint adds Tier 1 Hugo site management tools and enriches MCP
guidance for all agents.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────────┐
│ MCP Server   │────▶│ hugo.py      │────▶│ List/create/update  │
│ (server.py)  │     │ (NEW)        │     │ content pages       │
│              │     └──────────────┘     └─────────────────────┘
│              │     ┌──────────────┐     ┌─────────────────────┐
│              │────▶│ scaffolding  │────▶│ Lesson stubs        │
│              │     │  .py         │     │                     │
│              │     └──────────────┘     └─────────────────────┘
│              │     ┌──────────────┐     ┌─────────────────────┐
│              │────▶│ validation   │◀────│ Shortcode regex     │
│              │     │  .py         │     │ patterns            │
│              │     └──────────────┘     └─────────────────────┘
│              │     ┌──────────────┐
│              │────▶│ readme.py    │
│              │     └──────────────┘
│              │     ┌──────────────┐
│              │────▶│ syllabus.py  │
│              │     └──────────────┘
│              │     ┌──────────────┐
│              │────▶│ init_command │
│              │     │  .py         │
│              │     └──────────────┘
└─────────────┘
```

## Technology Stack

- **Python 3.12+** — existing project language
- **subprocess** — for `hugo build` execution
- **PyYAML** — for frontmatter parsing (already indirect dep via jtl-syllabus)

## Component Design

### Component: hugo.py (NEW)

**Purpose**: Hugo content page management — list, create, update, build.

**Use Cases**: SUC-001, SUC-002, SUC-003

New module `curik/hugo.py` with these functions:

- `parse_frontmatter(text: str) -> tuple[dict, str]`
  Split a markdown file into (frontmatter_dict, body_text).
  Uses `---` delimiters and `yaml.safe_load()`.

- `render_frontmatter(data: dict) -> str`
  Serialize a dict back to YAML frontmatter with `---` delimiters.

- `list_content_pages(root: Path, section: str | None = None) -> list[dict]`
  Walk `content/` directory, parse each `.md` file's frontmatter.
  Return list of `{path, title, weight, draft}` dicts.
  Optional `section` filter limits to a subdirectory.

- `create_content_page(root: Path, path: str, title: str, content: str = "", **extra_fm) -> str`
  Create a page at `content/<path>` with YAML frontmatter.
  Creates parent dirs. Raises CurikError if file already exists.

- `update_frontmatter(root: Path, page_path: str, updates: dict) -> dict`
  Read page, merge updates into frontmatter, write back.
  Returns merged frontmatter. Body content preserved.

- `hugo_build(root: Path) -> dict`
  Run `hugo` in the project root. Return `{success, output, error}`.
  If Hugo is not installed, return actionable error message.

### Component: server.py (MODIFIED)

**Purpose**: Expose new Hugo tools and enrich MCP guidance.

Changes:
- Import and register 4 new MCP tools from hugo.py
- Expand `instructions` string with workflow guidance, shortcode examples,
  tool grouping, and recommended sequence
- Improve docstrings on existing tools:
  - `tool_scaffold_structure` — mention Hugo content/ and section tree
  - `tool_create_lesson_stub` — mention shortcodes in generated stub
  - `tool_init_course` — mention CLAUDE.md and skill installation
  - `tool_trigger_readme_generation` — explain shortcode relationship

## Dependency Map

```
server.py
  ├── hugo.py          (NEW — content page operations)
  ├── scaffolding.py   (existing — lesson stubs)
  ├── validation.py    (existing — content validation)
  ├── readme.py        (existing — README generation)
  ├── syllabus.py      (existing — syllabus validation)
  └── init_command.py  (existing — init-time setup)
```

## Data Model

No new persistent state. Content pages use standard Hugo YAML frontmatter:
```yaml
---
title: "Page Title"
weight: 10
draft: false
---
```

## Security Considerations

- `hugo_build()` shells out to `hugo` binary — uses `subprocess.run` with
  no shell interpolation, fixed args only
- `create_content_page()` validates path is under `content/` to prevent
  path traversal
- `update_frontmatter()` uses `yaml.safe_load()` (no arbitrary code execution)

## Sprint Changes

### Changed Components

- **hugo.py**: NEW — content page list, create, update, build functions
- **server.py**: 4 new MCP tools + enriched instructions + improved docstrings

### Migration Concerns

None — additive changes only. No existing behavior modified.
