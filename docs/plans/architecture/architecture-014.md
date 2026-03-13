---
status: done
---

# Architecture

## Architecture Overview

Curik is a Python MCP server that guides AI agents through curriculum
development. It generates project scaffolding including static site
generator configuration. This sprint replaces the MkDocs configuration
layer with Hugo equivalents.

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐
│ MCP Server   │────▶│ templates.py │────▶│ hugo.toml      │
│ (server.py)  │     │              │     │ (generated)    │
│              │────▶│ migrate.py   │     └────────────────┘
│              │     │              │     ┌────────────────┐
│              │────▶│ scaffolding  │────▶│ content/       │
│              │     │  .py         │     │  _index.md     │
│              │     └──────────────┘     │  01-module/    │
│              │                          │    _index.md   │
│              │     ┌──────────────┐     └────────────────┘
│              │────▶│ references/  │
│              │     │  brand-guide │
│              │     └──────────────┘
└─────────────┘
```

## Technology Stack

- **Python 3.10+** — existing project language
- **Hugo** — replaces MkDocs as static site generator (external binary, not
  invoked by Curik directly — Curik only generates config files)
- **TOML** — Hugo's native config format (Python stdlib `tomllib` for reading,
  manual string generation for writing since `tomli_w` is not in stdlib)

## Component Design

### Component: templates

**Purpose**: Generate configuration files for course scaffolding.

**Boundary**: Produces config strings (Hugo TOML, devcontainer JSON,
course.yml). Does not write files — callers handle I/O.

**Use Cases**: SUC-001

Changes:
- Remove `get_mkdocs_yml()` function
- Add `get_hugo_config(title, tier, theme_path)` function
- Output is TOML format string for `hugo.toml`
- Config references the League Hugo theme module
- Tier 1-2 includes `[params]` section with `instructorGuide = true`
- All tiers enable syntax highlighting, table of contents, code copy

### Component: migrate

**Purpose**: Inventory and migrate existing course repositories.

**Boundary**: Reads existing repo structure, creates Curik-standard structure.

**Use Cases**: SUC-002

Changes:
- `inventory_course()`: add detection of `hugo.toml` → `"hugo"` in
  `generator_guess`. Keep legacy `mkdocs.yml` detection.
- `migrate_structure()`: generate `hugo.toml` instead of `mkdocs.yml`,
  create `content/` instead of `docs/`, use `_index.md` instead of `index.md`
- Update import from `get_mkdocs_yml` to `get_hugo_config`

### Component: scaffolding

**Purpose**: Create directory trees and stub files for course structure.

**Boundary**: Creates directories and writes stub markdown files.

**Use Cases**: SUC-001

Changes:
- `scaffold_structure()`: no structural changes to module/lesson placement
  (modules already go under root or `resources/`). The MkDocs `docs/docs/`
  convention was only in `migrate_structure()`. However, `scaffold_structure()`
  must now create `_index.md` branch bundle files in each module directory
  (Hugo requires these for section pages). The lesson stubs already get
  created by `scaffold_structure()` — only the module-level index files change
  from `index.md` to `_index.md`.
- `generate_nav()`: remove MkDocs-specific output format. Hugo auto-generates
  navigation from directory structure using `01-` prefixes, so this function
  is no longer needed for nav config. Keep the function but change its output
  to return weight assignments (integer ordering values) that callers can
  inject into frontmatter. Update tests accordingly.

### Component: references (NEW)

**Purpose**: Package reference documents that ship with the curik package.

**Boundary**: Markdown files in `curik/references/` directory, read by MCP
server tools.

**Use Cases**: SUC-003

Implementation:
- Copy `docs/league-web-brand-guide.md` to `curik/references/league-web-brand-guide.md`
- Create `curik/references/__init__.py` (empty, required for package discovery)
- Add `"curik.references"` to the `packages` list in `pyproject.toml`
- Add `curik/references/*.md` to `package_data` in `pyproject.toml`
- Add `get_reference(name)` function in `curik/assets.py` (which already
  handles agents/skills loading via `importlib.resources`)

### Component: server

**Purpose**: MCP tool wrappers for all curik functions.

**Boundary**: Receives MCP tool calls, delegates to Python functions.

**Use Cases**: SUC-001, SUC-002, SUC-003

Changes:
- Update docstrings referencing MkDocs to reference Hugo
- Add `tool_get_reference(name)` MCP tool for brand guide access
- Update import from `get_mkdocs_yml` to `get_hugo_config`

## Dependency Map

```
server.py
  ├── templates.py  (get_hugo_config)
  ├── migrate.py    (inventory_course, migrate_structure)
  │     └── templates.py  (get_hugo_config)
  ├── scaffolding.py (scaffold_structure, generate_nav)
  └── assets.py     (get_reference — or new references.py)
```

## Data Model

No data model changes. State files (`.course/state.json`, `course.yml`)
are unaffected. The only file format change is the generated config:
`mkdocs.yml` (YAML) → `hugo.toml` (TOML).

## Security Considerations

None — this sprint changes generated config files and adds a read-only
reference document. No new inputs, no network access, no secrets.

## Design Rationale

**Why not abstract the SSG behind an interface?** The integration surface
is small (3 Python files generate SSG-specific output). An abstraction
layer would need to normalize config format, directory conventions, and
nav generation — essentially reimplementing each SSG. If Hugo ever needs
replacing, the same 3 files change. Abstraction cost exceeds benefit.

**Why TOML string generation instead of a TOML library?** Hugo configs
are simple key-value structures. Manual string building avoids adding a
dependency (`tomli_w`) for a trivial output format. The same pattern is
used for `get_mkdocs_yml()` today (manual YAML string building).

**Why keep `generate_nav()` as weight assignments?** Hugo handles nav
natively from directory structure, so the MkDocs nav-list output format is
no longer needed. However, the function is useful for generating `weight`
frontmatter values from a structure dict, giving explicit ordering control.
Decision: keep the function, change output to weight assignments.

## Sprint Changes

### Changed Components

- **templates.py**: `get_mkdocs_yml()` → `get_hugo_config()`, TOML output
- **migrate.py**: Hugo detection, Hugo config generation, `content/` directory
- **scaffolding.py**: `_index.md` files, simplified nav generation
- **server.py**: updated docstrings, new `tool_get_reference()` tool
- **references/** (NEW): brand guide markdown file, packaged with curik
- **pyproject.toml**: `packages` adds `curik.references`, `package_data`
  includes `curik/references/*.md`

### Migration Concerns

None — no existing curricula use MkDocs config generated by Curik.
The current curriculum sites (Python Apprentice, Motors) use Sphinx + Furo,
which is independent of Curik's scaffolding output.
