---
id: '002'
title: Phase 1 Agents and Skills
status: done
branch: sprint/002-phase-1-agents-and-skills
use-cases:
- SUC-001
- SUC-002
- SUC-003
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 002: Phase 1 Agents and Skills

## Goals

Deliver the agent definitions, Phase 1 skill files, and research MCP
tools so that the Curriculum Architect and Research Agent can drive the
full Phase 1 spec-development conversation. After this sprint, a
curriculum designer can start `curik` in a new repo and the agent has
everything it needs to guide the conversation from course concept
through spec synthesis, including web research.

## Problem

Sprint 001 delivers the MCP server with Phase 1 spec tools (init, phase
tracking, spec read/write, phase gating). But the server has no agent
definitions, no skill files, and no research tools. Without these, the
AI agent has no structured workflow to follow during the Phase 1
conversation: it does not know what questions to ask, what order to ask
them, how to conduct research, or how to synthesize findings into a
spec. The enforcement model requires behavioral scaffolding (skills) and
agent specialization (agent definitions) alongside mechanical
enforcement (MCP tools).

## Solution

1. **Agent definitions** -- Create markdown definition files for the
   Curriculum Architect and Research Agent, bundled inside the `curik`
   package at `curik/agents/`. Each definition specifies the agent's
   role, capabilities, boundaries, and which skills it uses.

2. **Phase 1 skill files** -- Create markdown skill files for the five
   Phase 1 skills (`course-concept`, `pedagogical-model`,
   `alignment-decision`, `spec-synthesis`, `structure-proposal`),
   bundled at `curik/skills/`. Each skill contains a step-by-step
   procedure the agent follows.

3. **Research MCP tools** -- Add three tools to the MCP server:
   `web_search`, `save_research_findings`, and `get_research_findings`.
   Research findings are persisted to `.course/research/` as numbered
   markdown files.

4. **Serving mechanism** -- Add MCP tools `get_agent_definition` and
   `get_skill_definition` that read the bundled markdown files from the
   package and return them to the agent. The `init_course` function
   writes agent and skill references into the project so the agent
   knows what is available.

## Success Criteria

- `get_agent_definition("curriculum-architect")` returns the full agent
  definition with role, capabilities, boundaries, and skill references
- `get_agent_definition("research-agent")` returns the research agent
  definition
- `get_skill_definition("course-concept")` returns the step-by-step
  skill procedure (and likewise for all five Phase 1 skills)
- `web_search` accepts a query and returns search results
- `save_research_findings` persists a structured finding to
  `.course/research/NNN-slug.md`
- `get_research_findings` returns all saved findings
- Agent and skill files are bundled inside the package (not loose files
  that must be installed separately)
- All existing Phase 1 MCP tools continue to work unchanged

## Scope

### In Scope

- Agent definition files: `curriculum-architect.md`, `research-agent.md`
  in `curik/agents/`
- Skill files: `course-concept.md`, `pedagogical-model.md`,
  `alignment-decision.md`, `spec-synthesis.md`, `structure-proposal.md`
  in `curik/skills/`
- MCP tools: `get_agent_definition`, `get_skill_definition`,
  `web_search`, `save_research_findings`, `get_research_findings`
- Research storage directory: `.course/research/`
- `pyproject.toml` update to include `package-data` for markdown assets
- Unit and integration tests for new tools and asset loading

### Out of Scope

- Phase 2 agents (Lesson Authors, Quiz Author, Reviewer)
- Phase 2 skills (lesson-writing, quiz-authoring, validation)
- Scaffolding tools (scaffold_structure, create_lesson_stub)
- Change cycle tools (issues, change plans)
- Actual web search API integration (the `web_search` tool delegates to
  the host environment's web search capability; it does not implement
  its own HTTP search client)

## Test Strategy

- **Unit tests**: Verify that agent and skill markdown files load
  correctly from the package via `importlib.resources` or
  `pkg_resources`. Test that `save_research_findings` creates numbered
  files in `.course/research/` and `get_research_findings` reads them
  back.
- **Integration tests**: Call `get_agent_definition` and
  `get_skill_definition` through the MCP server, verify non-empty
  markdown is returned. Call research tools through MCP and verify
  persistence round-trip.
- **Regression**: All Sprint 001 MCP tool tests continue to pass.
- **Content review**: Agent definitions and skill files are reviewed for
  completeness against the project plan (Sections 5 and 6).

## Architecture Notes

- Agent and skill files are static markdown bundled as package data.
  They are read-only at runtime -- the MCP server serves them but never
  modifies them.
- The `web_search` tool is a thin wrapper. In the MCP server context,
  the agent already has access to web search through Claude Code's
  built-in capabilities. The Curik `web_search` tool provides a
  domain-specific wrapper that constrains search to curriculum-relevant
  queries and returns structured results the agent can pass to
  `save_research_findings`.
- Research findings use numbered markdown files (`001-pcep-syllabus.md`,
  `002-existing-python-courses.md`) following the same numbered-artifact
  pattern as CLASI. The frontmatter records metadata (query, date,
  source URLs); the body contains the structured summary.
- `init_course` is updated to create `.course/research/` alongside the
  other directories.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [ ] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
