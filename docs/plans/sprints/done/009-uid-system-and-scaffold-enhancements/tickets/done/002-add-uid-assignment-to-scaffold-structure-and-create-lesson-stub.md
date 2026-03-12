---
id: "002"
title: "Add UID assignment to scaffold_structure and create_lesson_stub"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Add UID assignment to scaffold_structure and create_lesson_stub

## Description

Integrate UID generation into the scaffolding pipeline so that every scaffolded
artifact receives a stable unique identifier. Without UIDs, courses and their
units have no identity beyond file paths, which break when content is
reorganized.

Changes required:

- **`scaffold_structure`**: After creating each lesson stub, call
  `generate_unit_uid()` and pass the result to `create_lesson_stub` so the
  stub's YAML frontmatter includes a `uid` field.
- **`create_lesson_stub`**: Accept an optional `uid` parameter. When provided,
  write YAML frontmatter (`---\nuid: <value>\n---\n`) at the top of the stub
  file before the lesson content. When omitted, generate the stub without
  frontmatter (backward compatible).
- **`course.yml`**: Add a `uid` field to the course YAML template in
  `templates.py`. In `init_course` (`project.py`), call `generate_course_uid()`
  and inject the value into the template context so the generated `course.yml`
  contains a UUID4 `uid` field.

## Acceptance Criteria

- [ ] `create_lesson_stub` accepts an optional `uid` keyword parameter
- [ ] When `uid` is provided, the generated stub file begins with YAML frontmatter containing `uid: <value>`
- [ ] When `uid` is omitted, the generated stub has no frontmatter (backward compatible)
- [ ] `scaffold_structure` calls `generate_unit_uid()` for each lesson and passes the result to `create_lesson_stub`
- [ ] The `course.yml` template in `templates.py` includes a `uid` placeholder
- [ ] `init_course` in `project.py` calls `generate_course_uid()` and writes the result into `course.yml`
- [ ] Generated `course.yml` contains a `uid` field with a valid UUID4 value
- [ ] All existing scaffolding tests continue to pass without modification

## Testing

- **Existing tests to run**: `uv run pytest tests/test_scaffolding.py` -- confirm backward compatibility
- **New tests to write**: In `tests/test_scaffolding.py` -- `create_lesson_stub` with `uid` param verifies frontmatter contains `uid:` field; `create_lesson_stub` without `uid` verifies no frontmatter; `scaffold_structure` end-to-end verifies stubs contain `uid:` in frontmatter; `init_course` verifies `course.yml` contains a UUID4 `uid` field
- **Verification command**: `uv run pytest tests/test_scaffolding.py -v`
