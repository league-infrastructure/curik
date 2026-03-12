---
id: "005"
title: "Implement mkdocs.yml explicit nav generation from course structure"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Implement mkdocs.yml explicit nav generation from course structure

## Description

Currently `get_mkdocs_yml()` generates a config without a `nav` section,
relying on MkDocs auto-discovery to determine page ordering. This produces
unpredictable navigation and prevents intentional lesson sequencing. The nav
should be generated from the course structure so lesson order matches the spec.

Changes required:

- **New `generate_nav()` function** in `scaffolding.py`: Takes the course
  structure (modules and lessons) and builds a `nav` list matching the MkDocs
  nav schema -- a list of dicts like
  `[{"Module Name": ["lessons/01-hello.md"]}]`.
- **Modify `get_mkdocs_yml()`**: Add an optional `nav` parameter. When
  provided, serialize it into the `mkdocs.yml` output as a top-level `nav:`
  key. When omitted, produce the same output as before (no `nav` section),
  preserving backward compatibility.

## Acceptance Criteria

- [ ] A `generate_nav()` function exists in `scaffolding.py`
- [ ] `generate_nav()` accepts a course structure and returns a nav list matching the MkDocs nav schema
- [ ] The returned nav list is a list of dicts where keys are module names and values are lists of lesson paths
- [ ] `get_mkdocs_yml()` accepts an optional `nav` keyword parameter
- [ ] When `nav` is provided, the generated `mkdocs.yml` string contains a `nav:` section with the supplied structure
- [ ] When `nav` is omitted, the generated `mkdocs.yml` contains no `nav:` section (backward compatible)
- [ ] The nav ordering matches the module/lesson order from the course structure

## Testing

- **Existing tests to run**: `uv run pytest tests/test_scaffolding.py` -- confirm `get_mkdocs_yml` without `nav` is unchanged
- **New tests to write**: In `tests/test_scaffolding.py` -- `generate_nav` with a sample structure returns expected nested list; `get_mkdocs_yml` with `nav` param includes `nav:` section that round-trips through YAML parse; `get_mkdocs_yml` without `nav` omits `nav:` key; verify nav order matches input structure order
- **Verification command**: `uv run pytest tests/test_scaffolding.py -v`
