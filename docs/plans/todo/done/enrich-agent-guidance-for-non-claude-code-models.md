---
title: 'Curik Init: Enrich CLAUDE.md and Skill for Non-Claude-Code Models'
priority: medium
tags:
- init
- mcp-server
- agent-guidance
- hugo
status: done
sprint: 019
---

# Curik Init: Enrich CLAUDE.md and Skill for Non-Claude-Code Models

Sprint 018 added `init_command.py` which installs a CLAUDE.md section, a
`/curik` skill stub, and MCP permission configuration. This works well for
Claude Code, but agents running on other models (Gemini, GPT, etc.) or via
VS Code / Cursor MCP integration **do not see the CLAUDE.md file**. They
only receive:

1. The MCP server `instructions` string (currently ~80 words)
2. Tool names and their docstrings
3. Tool return values

The result is that non-Claude-Code agents have no awareness of Hugo
conventions, shortcodes, content structure, the League theme, or the
curriculum development workflow. They can call tools but don't know
*when* or *why* to call them.

## Current State

### What CLAUDE.md Provides (Claude Code only)

The installed `claude-section.md` covers:
- Hugo as the SSG, with `content/` directory layout
- All four shortcodes with usage examples
- Content directory tree structure
- MCP tool listing by name
- Workflow overview (Phase 1 → Phase 2)

### What the MCP Server Instructions Provide (all models)

```python
"Curik is a curriculum development tool for the League of Amazing "
"Programmers. Curricula use Hugo as the static site generator with "
"content in the content/ directory. Lessons use Hugo shortcodes: "
"{{< instructor-guide >}}, {{< callout type=\"tip\" >}}, "
"{{< readme-shared >}}, and {{< readme-only >}}. "
"Do NOT use raw HTML divs or HTML comment guards in lesson files. "
"Use list_agents(), list_skills(), and list_references() to discover "
"available curriculum development agents, skills, and reference docs."
```

This is the *only guidance* non-Claude-Code models get. It's minimal —
shortcodes are named but not explained, the workflow isn't mentioned,
and there's no indication of what tools to call first or in what order.

### What the `/curik` Skill Provides (Claude Code only)

A dispatch table mapping `/curik status`, `/curik spec`, etc. to MCP
tool calls. Not available to other models at all.

## Gap Analysis

| Guidance topic                 | CLAUDE.md | MCP instructions | Tool docstrings |
|-------------------------------|-----------|-----------------|-----------------|
| Hugo is the SSG               | Yes       | Brief           | —               |
| Content directory structure   | Yes       | "content/ dir"  | —               |
| Shortcode syntax & usage      | Yes       | Names only      | —               |
| When NOT to use HTML          | Yes       | Yes             | —               |
| Workflow phases                | Yes       | —               | —               |
| Which tool to call first      | Yes       | —               | —               |
| Tool purpose & sequencing     | Yes       | —               | Partial         |
| Agent/skill discovery         | Yes       | Yes             | —               |
| League theme awareness        | Yes       | —               | —               |
| Building / previewing site    | —         | —               | —               |
| Page linking (relref)         | —         | —               | —               |

## Proposed Improvements

### 1. Richer MCP Server Instructions

Expand the `instructions` string on `FastMCP()` to cover the essentials
that non-Claude-Code agents need. This is the single most impactful
change because it reaches every model. Should include:

- Hugo SSG with shortcode syntax examples (not just names)
- Content directory layout with `_index.md` explanation
- Workflow: call `tool_get_phase()` first, then follow the phase workflow
- Tool grouping: "start with `tool_get_course_status`, use
  `tool_scaffold_structure` for layout, `tool_create_lesson_stub` for
  lessons, `tool_validate_*` tools to check work"
- The `start-curik` agent entry point: "load `start-curik` agent
  definition to begin"

### 2. Better Tool Docstrings

Several tool docstrings are terse or don't explain Hugo context:

- `tool_scaffold_structure` — doesn't mention Hugo's `content/` directory
  or that the result is a Hugo section tree
- `tool_create_lesson_stub` — doesn't show what shortcodes will be
  included in the generated stub
- `tool_init_course` — doesn't mention CLAUDE.md or skill installation
- `tool_trigger_readme_generation` — doesn't explain the readme-shared /
  readme-only shortcode relationship

Improving these docstrings helps all models, since docstrings are always
visible.

### 3. MCP Resource for Hugo Conventions

Consider exposing a `curik://conventions` MCP resource (or a tool like
`tool_get_hugo_conventions()`) that returns the full Hugo/shortcode/
workflow documentation. This mirrors how `list_references()` works for
brand guide content, but for Hugo conventions specifically. Any model
could call this tool to learn the conventions.

### 4. Tool Discovery Tool

Add a `tool_get_workflow_guide()` or similar that returns a structured
overview of what tools are available and when to call them — essentially
the workflow section of CLAUDE.md but as a callable tool. This gives
non-Claude-Code agents the same "here's how to get started" guidance.

## Implementation Notes

- Changes to MCP server `instructions` and tool docstrings require no
  new modules — just edits to `server.py`
- An MCP resource or conventions tool would need a new template file
  (like `curik/init/hugo-conventions.md`) and a new tool registration
- Consider whether the `instructions` string has a practical length limit
  for various MCP clients; if so, keep it concise and direct agents to
  call `tool_get_workflow_guide()` for details

## Related

- Sprint 018 (done) — installed CLAUDE.md section and /curik skill
- [hugo-site-management-tools](hugo-site-management-tools.md) — the
  broader gap of missing Hugo build/serve/page management tools
