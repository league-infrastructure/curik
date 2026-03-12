---
id: "007"
title: "Polish Documentation and Migration"
status: planning
branch: sprint/007-polish-documentation-and-migration
use-cases:
  - SUC-001
  - SUC-002
  - SUC-003
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 007: Polish Documentation and Migration

## Goals

This is the final sprint. It accomplishes three things: (1) end-to-end
testing of the full Curik workflow from `curik init` through validation,
proving the entire system works as a cohesive pipeline; (2) generating
project documentation so that curriculum designers can use Curik without
reading the source code; (3) building migration tooling and tier-specific
template repos so that existing League courses can be converted to the
Curik-standard structure.

## Problem

Curik now has all its core features — init, spec development, scaffolding,
content authoring, change cycles, validation, and quiz authoring — but
three gaps remain before it is production-ready:

1. **No end-to-end proof.** Individual sprints tested their own features,
   but nobody has run the full workflow from a blank repo to a validated
   course. Integration seams between phases may have hidden failures.
2. **No user-facing documentation.** Curriculum designers need a getting-
   started guide, CLI reference, MCP tool catalog, and tier-specific
   workflow descriptions.
3. **No migration path.** The League has existing courses in Sphinx/Furo,
   VuePress, and bare GitHub repos. Without migration tooling, those
   courses will never move to the standard structure, and the registry
   will remain incomplete.

## Solution

- **End-to-end test suite**: A scripted integration test that walks through
  every phase — init, spec filling, phase advance, scaffolding, content
  stubs, outline approval, lesson drafting, validation — and asserts the
  final state is a complete, valid course.
- **Documentation generation**: Write user-facing docs in `docs/` using
  MkDocs with Material theme, covering installation, quickstart, CLI
  reference, MCP tool reference, agent/skill catalog, and tier-specific
  guides.
- **Migration CLI command** (`curik migrate`): Inventory an existing course
  repo, detect its current format (Sphinx RST, VuePress Markdown, bare
  repo), convert content to the Curik standard structure, generate
  `course.yml`, add instructor guide stubs, and produce a migration report.
- **Template repos**: One Cookiecutter-style template per tier (1-4) that
  `curik init --tier N` can use to scaffold a correctly-structured project.
- **Registry integration validation**: Confirm that a migrated course has
  a valid `course.yml` and that the GitHub Action for registry posting
  would succeed.

## Success Criteria

- End-to-end test passes: blank directory to validated course with no
  manual intervention
- `curik migrate <path>` converts a Sphinx RST course to Curik structure
  and passes `curik validate course`
- `curik init --tier 2` scaffolds a project using the Tier 2 template
- User documentation builds with `mkdocs build` and covers all commands
- `course.yml` produced by migration passes schema validation
- All existing tests continue to pass

## Scope

### In Scope

- End-to-end integration test (init through course validation)
- `curik migrate` CLI command with RST-to-Markdown conversion
- Migration report generation (inventory of what was converted, what needs
  manual attention)
- Tier-specific template directories (tiers 1-4) bundled in the package
- `curik init --tier N` flag to select a template
- User-facing documentation: installation, quickstart, CLI reference, MCP
  tool reference, agent and skill catalog, tier workflow guides
- Registry integration smoke test (validate `course.yml` schema)
- DNS/GitHub Pages deployment documentation (instructions, not automation)

### Out of Scope

- Building the curriculum registry service itself (separate infrastructure)
- Automated DNS configuration or GitHub Pages deployment automation
- VuePress migration (RST/Sphinx is the priority; VuePress courses are
  already Markdown and need only restructuring, which can be a follow-up)
- Converting quiz content from existing formats (quiz authoring is manual)
- MkDocs theme customization beyond what Material provides
- CI/CD pipeline setup (documented but not implemented)

## Test Strategy

- **End-to-end integration test**: `tests/test_e2e_workflow.py` — creates
  a temp directory, runs the full workflow programmatically (init, fill
  spec, advance phase, scaffold, create stubs, validate), asserts final
  state. This is the primary deliverable of the sprint's testing effort.
- **Migration unit tests**: `tests/test_migrate.py` — test RST-to-Markdown
  conversion, directory restructuring, `course.yml` generation, and error
  handling for malformed source repos.
- **Template tests**: `tests/test_templates.py` — verify each tier
  template produces a valid project that passes init-time validation.
- **Documentation build test**: `mkdocs build --strict` must succeed with
  no warnings.
- **Regression**: all existing unit and integration tests must pass.

## Architecture Notes

- The `curik migrate` command is a new subcommand in `curik.cli` that
  delegates to a new `curik.migrate` module.
- RST-to-Markdown conversion uses `pypandoc` (wrapping Pandoc) for
  reliable conversion. If Pandoc is not installed, the command prints
  an error with installation instructions rather than attempting a
  fragile regex-based conversion.
- Template repos are stored as directories under `curik/templates/tier_N/`
  and copied by `init_course()` when `--tier` is specified.
- The migration module follows a pipeline pattern: inventory, detect
  format, convert content, restructure directories, generate metadata,
  produce report.
- Documentation lives in `docs/` and uses MkDocs with Material theme,
  consistent with League curriculum sites.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
