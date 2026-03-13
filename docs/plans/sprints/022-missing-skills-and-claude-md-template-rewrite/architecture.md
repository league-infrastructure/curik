---
status: draft
---

# Architecture

## Architecture Overview

Curik is a Python MCP server for curriculum development. This sprint adds
3 missing skill files and rewrites the CLAUDE.md init template.

## Sprint Changes

### New Components
- `curik/skills/existing-content-analysis.md` — analyze sequestered content
- `curik/skills/content-conversion.md` — convert old content to Curik format
- `curik/skills/change-plan-execution.md` — execute an approved change plan

### Changed Components
- `curik/init/claude-section.md` — rewritten from Hugo tutorial to process-routing doc
