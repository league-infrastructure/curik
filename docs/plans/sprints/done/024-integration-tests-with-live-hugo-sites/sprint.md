---
id: '024'
title: Integration Tests with Live Hugo Sites
status: done
branch: sprint/024-integration-tests-with-live-hugo-sites
use-cases:
- SUC-001
- SUC-002
- SUC-003
---

# Sprint 024: Integration Tests with Live Hugo Sites

## Goals

Build an integration test framework that operates on real curriculum
projects — copying fixture directories, running the MCP server as a
subprocess against them, and producing actual Hugo sites that can be
inspected visually.

## Problem

Current tests use `tempfile.TemporaryDirectory()` with inline string
fixtures and directly mutate `server._project_root`. This tests individual
functions but never validates the full pipeline: init → scaffold → generate
hugo.toml → copy theme → `hugo build`. TODO-001 documents that
`scaffold_structure()` doesn't produce a runnable Hugo site — there's no
integration test that would catch this.

We need tests that:
1. Start from realistic curriculum source material
2. Run operations through the actual MCP server interface
3. Produce Hugo sites that can be built and inspected
4. Persist output so developers can run `hugo server` on the result

## Solution

1. **Fixture directories** at `tests/content_source/` — complete curriculum
   projects (one per major curriculum type), checked into git, never modified.
2. **Scratch directory** at `tests/content_test/` — gitignored working area
   where fixtures are copied before each test run.
3. **Test harness** that copies a source to scratch, launches the MCP server
   as a subprocess pointed at the scratch copy, and sends operations to it.
4. **Fix scaffold_structure()** to produce content under `content/`, generate
   `hugo.toml`, and copy the theme — so the result is a runnable Hugo site.

## Success Criteria

- `tests/content_source/` contains at least two fixture curricula (Tier 2
  Python basics, Tier 3 web development)
- `tests/content_test/` is gitignored and populated by test runs
- A test can copy a fixture, run scaffold + hugo build, and assert success
- After running tests, `cd tests/content_test/python-basics && hugo server`
  shows a working site
- `scaffold_structure()` places content under `content/`, generates
  `hugo.toml`, and copies the curriculum-hugo-theme

## Scope

### In Scope

- Fixture curriculum directories in `tests/content_source/`
- Test harness: copy, server launch, operation execution
- Gitignore for `tests/content_test/`
- Fix `scaffold_structure()` to produce content under `content/`
- Generate `hugo.toml` during scaffolding
- Copy curriculum-hugo-theme into `themes/` during scaffolding
- Integration tests that build Hugo sites

### Out of Scope

- MCP protocol-level subprocess communication (tests can call Python
  functions directly with the scratch path — subprocess MCP is a future
  enhancement)
- Hugo theme development (Sprint 017, already done)
- Lesson content authoring
- CI/CD pipeline for running Hugo builds

## Test Strategy

Two layers:
1. **Unit tests**: Existing tests continue to use temp directories for
   fast, isolated function testing.
2. **Integration tests** (new): Copy fixtures from `content_source/` to
   `content_test/`, run full operations, assert on file structure and
   Hugo build success. These tests require Hugo to be installed.

Integration tests that require Hugo should be marked with
`@unittest.skipUnless(shutil.which("hugo"), "Hugo not installed")`.

## Architecture Notes

- `scaffold_structure()` currently places modules at repo root (line 57:
  `mod_dir = root / mod_name`). Must change to `root / "content" / mod_name`.
- Need to generate `hugo.toml` and copy theme during scaffolding or as a
  separate setup step.
- Fixture directories should include `course.yml` and `.course/` metadata
  so they look like real initialized projects.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

1. **001** — Fix scaffold_structure to place content under content/ and create content/_index.md
2. **002** — Add hugo_setup() to templates.py and tool_hugo_setup() to server.py (depends: 001)
3. **003** — Create test fixture directories in tests/content_source/
4. **004** — Integration test module tests/test_integration_hugo.py (depends: 001, 002, 003)
