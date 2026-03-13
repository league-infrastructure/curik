<!-- CURIK:START -->
## Curik Curriculum Development

This project uses **Curik**, a curriculum development tool for the
League of Amazing Programmers. Curik provides an MCP server that guides
you through curriculum design and content authoring.

### Static Site Generator: Hugo

This curriculum uses **Hugo** as its static site generator.

- Content lives in the `content/` directory
- Section indexes use `_index.md` (Hugo branch bundles)
- Navigation order comes from numeric prefixes (`01-`, `02-`, etc.)
- Configuration is in `hugo.toml`
- The **League Hugo Theme** provides consistent branding and shortcodes

### Hugo Shortcodes

Use these shortcodes in lesson markdown files. Do NOT use raw HTML divs
or HTML comment guards.

**Instructor guide** — content visible only to instructors (collapsed by default):
```
{{</* instructor-guide */>}}
**Objectives**: Students will learn...
**Common mistakes**: Watch for...
{{</* /instructor-guide */>}}
```

**Callout boxes** — info, warning, or tip highlights:
```
{{</* callout type="tip" */>}}
Remember to save your work before running tests!
{{</* /callout */>}}
```

**README guards** — control what appears in generated README files:
```
{{</* readme-shared */>}}
This content appears on the site AND in the README.
{{</* /readme-shared */>}}

{{</* readme-only */>}}
This content appears ONLY in the README, not on the site.
{{</* /readme-only */>}}
```

### Content Structure

```
content/
  _index.md                  # Course landing page
  01-module-name/
    _index.md                # Module landing page
    01-lesson-name.md        # Individual lesson
    02-lesson-name.md
  02-module-name/
    _index.md
    ...
```

### Curik MCP Tools

Curik provides these MCP tools for curriculum development:

- `tool_init_course` — Initialize a new curriculum project
- `tool_get_phase` / `tool_advance_phase` — Track development phases
- `tool_get_spec` / `tool_update_spec` — Read and update the course spec
- `tool_advance_sub_phase` — Move through Phase 1 sub-phases
- `tool_get_course_status` — Check project status
- `tool_scaffold_structure` — Generate module/lesson file structure
- `tool_create_lesson_stub` — Create a new lesson file with shortcodes
- `tool_validate_lesson` — Validate lesson content and structure
- `tool_validate_instructor_guide` — Check instructor guide sections
- `tool_trigger_readme_generation` — Generate README files from guards
- `tool_validate_syllabus_consistency` — Check syllabus vs content pages

Use `list_agents()`, `list_skills()`, and `list_references()` to discover
available curriculum development agents, skills, and reference documents.

### Workflow

1. **Phase 1** — Course design: concept, pedagogical model, research,
   alignment, structure outline, assessment plan, technical decisions
2. **Phase 2** — Content authoring: scaffold structure, write lessons,
   add instructor guides, generate READMEs, validate content
<!-- CURIK:END -->
