---
status: draft
---

# Architecture

## Architecture Overview

Curik is a Python MCP server for curriculum development. This sprint adds
5 instruction documents to `curik/references/`. No code changes — only
bundled markdown content.

## Sprint Changes

### New Components
- `curik/references/curriculum-process.md` — full process reference
- `curik/references/course-taxonomy.md` — delivery formats, structures, units
- `curik/references/hugo-conventions.md` — Hugo SSG conventions
- `curik/references/lesson-page-template.md` — lesson page structure
- `curik/references/instructor-guide-requirements.md` — instructor guide fields

### Changed Components
None — files are auto-discovered by existing `list_instructions()`.
