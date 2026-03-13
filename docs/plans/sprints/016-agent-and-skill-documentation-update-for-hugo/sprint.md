---
id: "016"
title: "Agent and Skill Documentation Update for Hugo"
status: planning
branch: sprint/016-agent-and-skill-documentation-update-for-hugo
use-cases: [DUC-001, DUC-002]
---

# Sprint 016: Agent and Skill Documentation Update for Hugo

## Goals

Replace all MkDocs references in agent and skill markdown files with Hugo
equivalents so that AI agents using Curik's MCP tools receive correct
guidance about the site generator, shortcode syntax, and directory layout.

## Problem

Sprints 014-015 migrated the Python code (config generation, validation,
scaffolding, readme parsing) from MkDocs to Hugo. But the 12 agent and
skill definition files still reference MkDocs — HTML comment guards,
`<div>` instructor guides, `docs/docs/` paths, MkDocs nav config, and
MkDocs as the site generator. When other language models load these
definitions via the MCP server, they receive outdated instructions and
generate incorrect content.

## Solution

Update all 12 affected files (3 agents, 9 skills) to reference Hugo
shortcodes, `content/` directory, Hugo config, and Hugo as the SSG.
This is a documentation-only sprint — no Python code changes.

## Success Criteria

- Zero references to "MkDocs" in agent/skill files (except migrate.py
  detection which is intentional)
- Zero references to `docs/docs/` in agent/skill files
- Zero references to `<div class="instructor-guide">` or HTML comment guards
- All shortcode examples use `{{</* name */>}}` syntax
- All directory references use `content/` not `docs/docs/`
- Existing tests pass (229 tests)

## Scope

### In Scope

- 3 agent files: start-curik, curriculum-architect, lesson-author-older
- 9 skill files: pedagogical-model, spec-synthesis, structure-proposal,
  syllabus-integration, repo-scaffolding, readme-guards, validation-checklist,
  lesson-writing-older, lesson-writing-young

### Out of Scope

- Python code changes (done in Sprint 015)
- League Hugo theme (Sprint 017)
- migrate.py MkDocs detection logic (intentional — detects legacy repos)

## Test Strategy

Run full test suite to ensure no regressions. Asset loading tests verify
that all agent/skill files still load correctly after edits.

## Architecture Notes

No architectural changes. This is a content update to markdown files that
serve as AI agent instructions.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

1. Update agent definitions (start-curik, curriculum-architect, lesson-author-older)
2. Update scaffolding/structure skills (repo-scaffolding, structure-proposal)
3. Update content authoring skills (lesson-writing-young, lesson-writing-older,
   readme-guards, validation-checklist)
4. Update integration skills (syllabus-integration, spec-synthesis, pedagogical-model)
