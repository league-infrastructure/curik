---
id: "004"
title: "Integrate .devcontainer config generation into scaffolding flow"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Integrate .devcontainer config generation into scaffolding flow

## Description

The `templates.py` module already provides `get_devcontainer_json()` to generate
a `.devcontainer/devcontainer.json` configuration, but nothing in the
scaffolding flow calls it. Tier 3-4 courses need this file generated
automatically so students can open the repository in a VS Code dev container
without manual setup.

Modify `scaffold_structure` so that for Tier 3-4 courses it:

1. Reads the `language` field from `course.yml` (defaulting to `python` if
   absent).
2. Calls `get_devcontainer_json()` with the language value.
3. Creates the `.devcontainer/` directory at the repo root.
4. Writes `devcontainer.json` into that directory.

Tier 1-2 courses should not receive a `.devcontainer/` directory.

## Acceptance Criteria

- [ ] `scaffold_structure` calls `get_devcontainer_json()` for Tier 3 and Tier 4 courses
- [ ] `.devcontainer/devcontainer.json` is written at the repo root for Tier 3-4 courses
- [ ] The generated `devcontainer.json` is valid JSON
- [ ] The language passed to `get_devcontainer_json()` is read from the `language` field in `course.yml`
- [ ] When `course.yml` has no `language` field, `python` is used as the default
- [ ] Tier 1 and Tier 2 courses do not receive a `.devcontainer/` directory
- [ ] All existing scaffolding tests continue to pass

## Testing

- **Existing tests to run**: `uv run pytest tests/test_scaffolding.py` -- confirm no regressions
- **New tests to write**: In `tests/test_scaffolding.py` -- `scaffold_structure` with Tier 3 course verifies `.devcontainer/devcontainer.json` exists and is valid JSON; Tier 3 with explicit `language: java` verifies Java-specific devcontainer content; Tier 1 course verifies no `.devcontainer/` directory; Tier 3 with no `language` field verifies Python default is used
- **Verification command**: `uv run pytest tests/test_scaffolding.py -v`
