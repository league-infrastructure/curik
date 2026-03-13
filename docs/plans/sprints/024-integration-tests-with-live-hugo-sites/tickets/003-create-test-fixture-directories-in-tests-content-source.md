---
id: "003"
title: "Create test fixture directories in tests/content_source/"
status: todo
use-cases: [SUC-002, SUC-003]
depends-on: []
---

# Create test fixture directories in tests/content_source/

## Description

Create two realistic curriculum fixture directories under
`tests/content_source/`, plus add `tests/content_test/` to `.gitignore`.

**python-basics/** (Tier 2):
- `course.yml` with title "Python Basics", tier 2, slug, etc.
- `.course/state.json` with phase set to "phase2"
- `.course/spec.md` with minimal spec content
- Structure: 2 modules (variables, control-flow), 2-3 lessons each

**web-dev/** (Tier 3):
- `course.yml` with title "Web Development", tier 3, slug, etc.
- `.course/state.json` with phase set to "phase2"
- `.course/spec.md` with minimal spec content
- Structure: 2 modules (html-basics, css-styling), 2-3 lessons each

Fixtures contain ONLY initialization metadata. No `content/`, `hugo.toml`,
or `themes/` — those are created by the operations under test.

## Acceptance Criteria

- [ ] `tests/content_source/python-basics/` exists with course.yml and .course/
- [ ] `tests/content_source/web-dev/` exists with course.yml and .course/
- [ ] `tests/content_test/` is in .gitignore
- [ ] Fixtures contain valid course.yml with appropriate tier settings
- [ ] Fixtures contain .course/state.json at phase2

## Testing

- **Existing tests to run**: Full suite to verify no regressions
- **New tests to write**: None (fixtures are consumed by ticket 004)
- **Verification command**: `python3 -m pytest -v`
