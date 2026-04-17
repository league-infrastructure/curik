---
status: done
sprint: '001'
---

# Plan: Remove quiz, research, assets, and trim syllabus

## Context

Before building the CLI replacement for the MCP server, we're pruning modules that don't need CLI equivalents. Four categories are being cut:

- **Quiz** — not used yet, remove entirely
- **Research** — just numbered file I/O, agent instructions can describe the convention
- **Assets** — Claude can read agent/skill/instruction markdown files directly from the filesystem
- **Syllabus** — 3 of 5 functions are trivial wrappers around `syl` CLI or file reads; keep only `write_syllabus_url` and `validate_syllabus_consistency`

This is a **deletion-focused** change. We're removing Python modules, MCP tool registrations, and tests. The domain modules that have real logic stay.

---

## Tools we're keeping (will become CLI commands later)

### Phase Management (5)
- `init_course` — initialize curriculum project
- `get_phase` — current phase and gate conditions
- `advance_phase` — gated phase transition
- `advance_sub_phase` — advance Phase 1 sub-phases
- `get_course_status` — project state summary

### Spec Management (5)
- `get_spec` — read spec document
- `update_spec` — update a spec section
- `record_course_concept` — Phase 1a shortcut
- `record_pedagogical_model` — Phase 1b shortcut
- `record_alignment` — Phase 1d shortcut

### Course Config (1)
- `update_course_yml` — selective YAML field updates

### Scaffolding (6)
- `scaffold_structure` — create Hugo content tree from structure dict
- `create_lesson_stub` — single lesson stub
- `create_outline` / `approve_outline` / `get_outline` — outline management
- `generate_change_plan` — create change plan from items

### Issues & Change Plans (8)
- `create_issue` / `list_issues`
- `create_change_plan` / `register_change_plan` / `approve_change_plan` / `execute_change_plan` / `review_change_plan` / `close_change_plan`

### Migration (3)
- `inventory_course` — read-only course repo analysis
- `sequester_content` — move non-Curik files to _old/
- `migrate_structure` — create standard directory structure

### Validation (5)
- `validate_lesson` / `validate_module` / `validate_course`
- `get_validation_report` / `save_validation_report`

### Syllabus (2 — trimmed from 5)
- `write_syllabus_url` — update URL field by UID in nested YAML
- `validate_syllabus_consistency` — cross-reference UIDs vs Hugo content pages

### Hugo (6)
- `list_content_pages` / `create_content_page` / `update_frontmatter`
- `hugo_setup` / `bump_curriculum_version` / `hugo_build`

### README (1)
- `generate_readmes` — generate from shortcodes

### Publishing (2)
- `get_publish_guide` — personalized checklist
- `check_publish_ready` — programmatic readiness check

**Total: ~44 tools kept** (down from ~59)

---

## Removed tools

### Quiz (3) — not used yet
- ~~`generate_quiz_stub`~~ / ~~`validate_quiz_alignment`~~ / ~~`set_quiz_status`~~

### Research (2) — just file I/O, describe convention in agent instructions
- ~~`save_research_findings`~~ / ~~`get_research_findings`~~

### Assets (10) — Claude reads these files directly from the filesystem
- ~~`list_agents`~~ / ~~`get_agent_definition`~~
- ~~`list_skills`~~ / ~~`get_skill_definition`~~
- ~~`list_instructions`~~ / ~~`get_instruction`~~ / ~~`list_references`~~ / ~~`get_reference`~~
- ~~`get_process_guide`~~ / ~~`get_activity_guide`~~

### Syllabus (3) — trivial wrappers around `syl` CLI or file reads
- ~~`get_syllabus`~~ / ~~`regenerate_syllabus`~~ / ~~`read_syllabus_entries`~~

---

## Step 1: Remove quiz module

- Delete [curik/quiz.py](curik/quiz.py)
- Remove all quiz tool registrations from [curik/server.py](curik/server.py) (`tool_generate_quiz_stub`, `tool_validate_quiz_alignment`, `tool_set_quiz_status`)
- Remove quiz imports from `server.py`
- Delete [tests/test_quiz.py](tests/test_quiz.py) if it exists
- Remove any quiz references from [curik/__init__.py](curik/__init__.py) if present

## Step 2: Remove research module

- Delete [curik/research.py](curik/research.py)
- Remove research tool registrations from [curik/server.py](curik/server.py) (`tool_save_research_findings`, `tool_get_research_findings`)
- Remove research imports from `server.py`
- Delete [tests/test_research.py](tests/test_research.py) if it exists
- Remove any research references from `curik/__init__.py` if present

## Step 3: Remove assets module

- Delete [curik/assets.py](curik/assets.py)
- Remove all asset tool registrations from [curik/server.py](curik/server.py): `tool_list_agents`, `tool_get_agent_definition`, `tool_list_skills`, `tool_get_skill_definition`, `tool_list_instructions`, `tool_get_instruction`, `tool_list_references`, `tool_get_reference`, `tool_get_process_guide`, `tool_get_activity_guide`
- Remove asset imports from `server.py` (the large import block at lines 11-23)
- Move `ACTIVITY_MAPPINGS` dict content into a new reference file [curik/references/activity-mappings.md](curik/references/activity-mappings.md) so the orchestration data is preserved as documentation
- Delete [tests/test_assets.py](tests/test_assets.py) if it exists
- Remove any assets references from `curik/__init__.py` if present

## Step 4: Trim syllabus module

- Remove 3 functions from [curik/syllabus.py](curik/syllabus.py): `get_syllabus()`, `regenerate_syllabus()`, `read_syllabus_entries()` (and the `_iter_lessons` helper if only used by `read_syllabus_entries`)
- Keep `write_syllabus_url()` and `validate_syllabus_consistency()` (these have real logic)
- Remove corresponding tool registrations from `server.py`: `tool_get_syllabus`, `tool_regenerate_syllabus`, `tool_read_syllabus_entries`
- Keep `tool_write_syllabus_url` and `tool_validate_syllabus_consistency` in server.py for now (they'll be migrated to CLI later)
- Update syllabus imports in `server.py` to only import the two kept functions
- Update tests if any exist for the removed functions

## Step 5: Clean up references in init templates

- Remove quiz, research, and asset tool references from [curik/init/claude-section.md](curik/init/claude-section.md)
- Remove quiz, research, and asset MCP call references from [curik/init/curik-skill.md](curik/init/curik-skill.md)
- Remove references to removed syllabus tools from both templates

## Step 6: Run tests and verify

- Run `uv run pytest` to confirm nothing is broken
- Verify `server.py` still imports and runs (the remaining MCP tools should work)
- Grep for any remaining references to deleted modules/functions

---

## Files to delete
- `curik/quiz.py`
- `curik/research.py`
- `curik/assets.py`
- `tests/test_quiz.py` (if exists)
- `tests/test_research.py` (if exists)
- `tests/test_assets.py` (if exists)

## Files to modify
- `curik/server.py` — remove imports and tool registrations for quiz, research, assets, and 3 syllabus tools
- `curik/syllabus.py` — remove `get_syllabus`, `regenerate_syllabus`, `read_syllabus_entries`, `_iter_lessons` (if orphaned)
- `curik/__init__.py` — remove any exports of deleted modules
- `curik/init/claude-section.md` — remove references to deleted tools
- `curik/init/curik-skill.md` — remove references to deleted tools

## Files to create
- `curik/references/activity-mappings.md` — preserve ACTIVITY_MAPPINGS data as a reference document

## Verification
1. `uv run pytest` — all remaining tests pass
2. `grep -r "quiz\|research\|assets\|get_syllabus\|regenerate_syllabus\|read_syllabus_entries" curik/server.py` — no references remain
3. The MCP server can still start (remaining tools work)
