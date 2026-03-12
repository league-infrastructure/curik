# Syllabus Integration

## Purpose

Document the conventions for working with `syllabus.yaml` and the
`syl` tool so that agents can read, update, and validate syllabus
data consistently.

## syllabus.yaml Format

The `syllabus.yaml` file at the repository root describes the course
structure using a three-level hierarchy:

```yaml
title: "Introduction to Python"
modules:
  - name: "Variables and Types"
    lessons:
      - uid: "py-101-vars"
        name: "Introduction to Variables"
        lesson: "docs/docs/01-variables/01-intro.md"
        exercise: "lessons/01-variables/01-intro/exercise.py"
      - uid: "py-101-types"
        name: "Data Types"
        lesson: "docs/docs/01-variables/02-types.md"
        exercise: "lessons/01-variables/02-types/exercise.py"
  - name: "Control Flow"
    lessons:
      - uid: "py-102-if"
        name: "Conditionals"
        lesson: "docs/docs/02-control-flow/01-if.md"
```

### Structure

- **Course**: Top level with `title` and `modules` list.
- **Module**: Named group containing a `lessons` list. Modules may
  also contain nested `LessonSet` groups for sub-sections.
- **Lesson**: Individual entry with:
  - `uid` — Unique identifier for cross-referencing
  - `name` — Display name
  - `lesson` — Path to the MkDocs lesson page
  - `exercise` — Path to the exercise file (optional)
  - `url` — External URL (optional, set via `write_syllabus_url`)

## UID-Based Lookups

Every lesson has a unique `uid` field that serves as the primary key
for cross-referencing between systems:

- **Syllabus to MkDocs**: Match syllabus UIDs to frontmatter `uid:`
  fields in MkDocs pages under `docs/docs/`.
- **Syllabus to Lesson Files**: The `lesson` path field points to the
  source Markdown file.
- **Validation**: `validate_lesson` (tier 3-4) checks that the lesson
  file's frontmatter UID appears in the syllabus.
- **Consistency Check**: `validate_syllabus_consistency` cross-references
  all syllabus UIDs against all MkDocs page UIDs and reports mismatches.

## syl Compile Workflow

The `syl` tool (from the `jtl-syllabus` package) can regenerate
`syllabus.yaml` from the lesson directory structure:

1. Run `tool_regenerate_syllabus(lesson_dir="lessons")` to scan the
   lesson directory and produce a fresh `syllabus.yaml`.
2. The compile step reads lesson metadata from file frontmatter and
   directory structure to build the Course model.
3. The resulting YAML is written to `syllabus.yaml` at the repo root.

Use this when the file structure has changed significantly and the
syllabus needs to be rebuilt from scratch.

## Bidirectional Sync

The syllabus and MkDocs pages must stay in sync. Drift between them
causes broken navigation, missing lessons, and validation failures.

### Syllabus to MkDocs Direction

- Each syllabus lesson entry should have a corresponding MkDocs page
  with a matching `uid` in its YAML frontmatter.
- `validate_syllabus_consistency` reports `entries_without_pages` for
  syllabus UIDs that have no matching MkDocs page.

### MkDocs to Syllabus Direction

- Each MkDocs page with a `uid` frontmatter field should have a
  corresponding syllabus entry.
- `validate_syllabus_consistency` reports `pages_without_entries` for
  MkDocs page UIDs that have no matching syllabus entry.

### Pages Without UIDs

MkDocs pages that lack a `uid` frontmatter field are reported as
`pages_without_uid`. These pages cannot be cross-referenced and should
have UIDs added.

## MCP Tools Reference

- `tool_read_syllabus_entries` — Read all lesson entries from syllabus
- `tool_write_syllabus_url(uid, url)` — Set the URL for a lesson by UID
- `tool_regenerate_syllabus(lesson_dir)` — Rebuild syllabus from files
- `tool_get_syllabus` — Return raw syllabus.yaml content
- `tool_validate_syllabus_consistency` — Check syllabus vs MkDocs sync
