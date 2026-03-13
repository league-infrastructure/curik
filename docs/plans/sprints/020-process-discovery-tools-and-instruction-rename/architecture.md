---
status: draft
---

# Architecture

## Architecture Overview

Curik is a Python MCP server that guides AI agents through curriculum
development for the League of Amazing Programmers. It uses Hugo as the
static site generator and manages a 3-phase lifecycle: project initiation,
first version, and ongoing changes.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────────┐
│ MCP Server   │────▶│ assets.py    │────▶│ Agent/Skill/Instr   │
│ (server.py)  │     │              │     │ markdown files       │
│              │     └──────────────┘     └─────────────────────┘
│              │     ┌──────────────┐     ┌─────────────────────┐
│              │────▶│ project.py   │────▶│ Phase state, spec   │
│              │     └──────────────┘     └─────────────────────┘
│              │     ┌──────────────┐     ┌─────────────────────┐
│              │────▶│ scaffolding  │────▶│ Hugo content stubs   │
│              │     └──────────────┘     └─────────────────────┘
│              │     ┌──────────────┐
│              │────▶│ validation   │
│              │     └──────────────┘
│              │     ┌──────────────┐
│              │────▶│ changes.py   │
│              │     └──────────────┘
│              │     ┌──────────────┐
│              │────▶│ hugo.py      │
│              │     └──────────────┘
└─────────────┘
```

## Technology Stack

- **Python 3.12+** — project language
- **FastMCP** — MCP server framework
- **Hugo** — static site generator (shortcode syntax)
- **importlib.resources** — bundled markdown file loading

## Component Design

### Component: Process Guide (new)

**Purpose**: Bundled markdown document describing the full 3-phase
curriculum development process as a decision tree.

**Location**: `curik/references/process-guide.md`

**Loaded by**: New `tool_get_process_guide()` in server.py via assets.py

The document is static content bundled with the package. It describes:
- 3 macro-phases and their sub-phases
- Which agent is active in each phase
- Which skills each agent uses
- Gate conditions for phase transitions

### Component: Activity Guide (new)

**Purpose**: Composite document builder that bundles agent + skills +
instructions for a named activity.

**Location**: New function in assets.py, exposed via server.py

**Activity mappings** (from spec):

| Activity | Agent | Skills | Instructions |
|----------|-------|--------|-------------|
| spec-development | curriculum-architect | course-concept, pedagogical-model, alignment-decision, spec-synthesis | curriculum-process, course-taxonomy |
| research | research-agent | (none) | curriculum-process |
| content-analysis | curriculum-architect | existing-content-analysis | curriculum-process, course-taxonomy |
| scaffolding | curriculum-architect | repo-scaffolding, structure-proposal, syllabus-integration | hugo-conventions |
| lesson-writing-young | lesson-author-young | lesson-writing-young, instructor-guide-sections | lesson-page-template, instructor-guide-requirements, course-taxonomy |
| lesson-writing-older | lesson-author-older | lesson-writing-older, instructor-guide-sections, readme-guards | lesson-page-template, instructor-guide-requirements, hugo-conventions |
| quiz-authoring | quiz-author | quiz-authoring | curriculum-process |
| content-conversion | lesson-author-older | content-conversion, instructor-guide-sections | lesson-page-template, hugo-conventions |
| change-management | curriculum-architect | status-tracking, change-plan-execution | curriculum-process |
| validation | reviewer | validation-checklist, syllabus-integration | hugo-conventions, instructor-guide-requirements |

At call time, the function reads each referenced file via assets.py and
concatenates them into a single markdown document with section headers.
Missing files (not yet written) are noted with a placeholder.

### Component: Instruction Rename

**Purpose**: Rename the public API from "references" to "instructions".

**Changes**:
- `assets.py`: Add `list_instructions()` and `get_instruction()` aliases
- `server.py`: Add `tool_list_instructions()` and `tool_get_instruction()` tools; keep old tools as aliases
- `pyproject.toml`: No change (package directory stays `curik.references`)

The underlying directory stays `curik/references/` to avoid package
restructuring. The API-level rename is sufficient.

## Dependency Map

```
server.py
  └── assets.py
        ├── curik/agents/*.md
        ├── curik/skills/*.md
        └── curik/references/*.md (includes process-guide.md)
```

## Data Model

No data model changes.

## Security Considerations

None — read-only tools returning bundled content.

## Sprint Changes

### New Components
- `curik/references/process-guide.md` — bundled process guide content
- `tool_get_process_guide()` — returns process guide
- `tool_get_activity_guide(activity)` — returns bundled context
- `tool_list_instructions()` / `tool_get_instruction()` — renamed API

### Changed Components
- `assets.py` — new functions for process guide and activity guide
- `server.py` — new tool registrations
- Test files — new tests + updated references to use "instructions"
