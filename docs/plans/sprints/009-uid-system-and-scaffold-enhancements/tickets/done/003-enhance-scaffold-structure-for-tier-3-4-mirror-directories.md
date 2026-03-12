---
id: "003"
title: "Enhance scaffold_structure for Tier 3-4 mirror directories"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Enhance scaffold_structure for Tier 3-4 mirror directories

## Description

Tier 3-4 courses include student-facing code (exercises, projects) that must
live outside the MkDocs `docs/` tree so it can be opened, edited, and run
directly. Currently `scaffold_structure` only creates directories under
`docs/docs/`, leaving Tier 3-4 courses without a proper code workspace.

Modify `scaffold_structure` to detect the course tier from `course.yml`. For
Tier 3-4 courses, create repo-root `lessons/` and `projects/` directories that
mirror the module structure under `docs/docs/`. For example, if `docs/docs/`
contains `01-intro/01-hello/`, then `lessons/01-intro/01-hello/` should also
be created. Tier 1-2 courses remain unchanged -- no mirror directories are
created.

## Acceptance Criteria

- [ ] `scaffold_structure` reads the `tier` field from `course.yml` to determine course tier
- [ ] For Tier 3 and Tier 4 courses, a repo-root `lessons/` directory is created
- [ ] For Tier 3 and Tier 4 courses, a repo-root `projects/` directory is created
- [ ] Mirror directories under `lessons/` replicate the module/lesson directory structure from `docs/docs/`
- [ ] For Tier 1 and Tier 2 courses, no `lessons/` or `projects/` directories are created
- [ ] Existing `docs/docs/` directory creation is unaffected for all tiers
- [ ] All existing scaffolding tests continue to pass

## Testing

- **Existing tests to run**: `uv run pytest tests/test_scaffolding.py` -- confirm Tier 1-2 behavior unchanged
- **New tests to write**: In `tests/test_scaffolding.py` -- `scaffold_structure` with Tier 3 course verifies `lessons/` and `projects/` dirs exist with correct subdirectory structure; `scaffold_structure` with Tier 1 course verifies no `lessons/` or `projects/` dirs; verify mirror directory names match `docs/docs/` module/lesson names
- **Verification command**: `uv run pytest tests/test_scaffolding.py -v`
