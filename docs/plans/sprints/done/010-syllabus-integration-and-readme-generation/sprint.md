---
id: '010'
title: Syllabus Integration and README Generation
status: done
branch: sprint/010-syllabus-integration-and-readme-generation
use-cases:
- SUC-001
- SUC-002
- SUC-003
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 010: Syllabus Integration and README Generation

## Goals

Implement bidirectional syllabus.yaml integration so Curik can read lesson
entries, create MkDocs pages with matching UIDs, and write url fields back
into syllabus.yaml. Implement the README generation pipeline for Tier 3-4
courses that extracts guarded content from MkDocs lesson pages and produces
README files in repo-root lesson directories.

## Problem

Curik currently scaffolds directory structures and creates lesson stubs, but
has no way to read or update syllabus.yaml. After scaffolding, the url fields
in syllabus.yaml must be manually populated. There is also no mechanism to
generate README files for GitHub-visible lesson directories from MkDocs page
content. Tier 3-4 courses need READMEs in the repo-root lesson directories
so that students browsing the repository on GitHub or in Codespaces can see
lesson summaries, but maintaining these separately from MkDocs pages creates
duplication and drift.

## Solution

Add a `curik/syllabus.py` module that reads and writes syllabus.yaml using
PyYAML, parses lesson entries with their UIDs, paths, and url fields, and
can invoke `syl compile` to regenerate the file from directory structure. Add
a `curik/readme.py` module that parses `<!-- readme-shared -->` and
`<!-- readme-only -->` comment guards from MkDocs lesson pages, assembles
README content from guarded sections, and writes README.md files to the
corresponding repo-root lesson directories. Expose six new MCP tools in
server.py: `read_syllabus_entries`, `write_syllabus_url`,
`regenerate_syllabus`, `get_syllabus`, `trigger_readme_generation`, and
`validate_syllabus_consistency`. Add a `readme-guards` skill definition that
teaches agents when and how to place comment guards in lesson content.

## Success Criteria

- `read_syllabus_entries` returns a list of lesson entries from syllabus.yaml
  with uid, path, title, and url fields parsed correctly.
- `write_syllabus_url` updates the url field for a specific lesson entry
  identified by UID and preserves the rest of the YAML file.
- `regenerate_syllabus` invokes `syl compile` and returns success/failure.
- `trigger_readme_generation` produces README.md files in repo-root lesson
  directories with content extracted from guarded sections of MkDocs pages.
- `validate_syllabus_consistency` identifies entries without corresponding
  MkDocs pages, pages without syllabus entries, and UID mismatches.
- All new tools are accessible via the MCP server.
- The `readme-guards` skill definition is loadable via `get_skill_definition`.
- All new functionality has unit test coverage.

## Scope

### In Scope

- Reading syllabus.yaml and parsing entries into structured data
- Writing url fields back to syllabus.yaml for individual entries by UID
- Invoking `syl compile` as a subprocess to regenerate syllabus.yaml
- Returning raw syllabus.yaml content via `get_syllabus`
- Parsing `<!-- readme-shared -->` and `<!-- readme-only -->` comment guards
  from MkDocs Markdown files
- Generating README.md files from guarded content
- Consistency validation between syllabus.yaml entries and MkDocs pages
- MCP tool wrappers for all new functions
- Skill definition for README comment guard placement
- Unit tests for syllabus parsing, URL writing, guard parsing, and README
  generation

### Out of Scope

- Modifying the `syl` tool itself
- Building or deploying MkDocs sites
- Tier 1-2 README generation (instructor-guide-primary courses do not have
  student-facing repo directories)
- Automatic placement of comment guards in existing lesson content (agents
  place guards manually using the skill definition)
- syllabus.yaml schema changes or format migration

## Test Strategy

Unit tests in `tests/test_syllabus.py` covering:
- Parsing syllabus.yaml with various entry structures (with/without url,
  with/without uid)
- Writing url fields and verifying YAML round-trip integrity
- Handling missing syllabus.yaml gracefully
- Subprocess invocation mocking for `syl compile`

Unit tests in `tests/test_readme.py` covering:
- Comment guard regex parsing with nested content, multiple guards per file,
  and edge cases (empty guards, unclosed guards)
- README generation from parsed sections
- File I/O for writing README.md to correct directories
- Handling pages with no guards (no README generated)

Integration-level tests verifying:
- MCP tool wrappers return correct JSON responses
- Consistency validation catches mismatches between syllabus entries and pages

## Architecture Notes

- syllabus.yaml is owned by the `syl` tool. Curik reads it and writes only
  the `url` field per entry. All structural changes go through
  `syl compile`.
- UID matching depends on Sprint 009's UID system. Each syllabus entry and
  each MkDocs page frontmatter share a `uid` field. This sprint assumes UIDs
  are already present and does not generate them.
- Comment guards use HTML comments so they are invisible in rendered MkDocs
  output but parseable from the Markdown source. `<!-- readme-shared -->`
  marks content that appears in both the MkDocs page and the README.
  `<!-- readme-only -->` marks content that appears only in the README.
  Both guards are closed with `<!-- /readme-shared -->` and
  `<!-- /readme-only -->` respectively.
- PyYAML is already a transitive dependency via MkDocs. No new dependencies
  are required.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

1. Implement `read_syllabus_entries` tool -- reads lesson entries from
   syllabus.yaml with UIDs, paths, url fields
2. Implement `write_syllabus_url` tool -- writes url field for a specific
   lesson entry after Curik creates the MkDocs page
3. Implement `regenerate_syllabus` tool -- runs `syl compile` subprocess to
   rebuild syllabus.yaml
4. Implement README generation from comment guards -- parse
   `<!-- readme-shared -->` and `<!-- readme-only -->` markers from MkDocs
   pages, generate READMEs in repo-root lesson dirs
5. Implement `trigger_readme_generation` and
   `validate_syllabus_consistency` tools
6. Create `readme-guards` skill definition (when and how to place guards)
7. Tests for syllabus integration and README generation
