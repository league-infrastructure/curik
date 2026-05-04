---
sprint: "001"
status: draft
---

# Use Cases — Sprint 001: Prune Unused Modules for CLI Migration

## SUC-001: Developer removes quiz module without breaking the package

- **Actor**: Developer
- **Preconditions**: curik/quiz.py exists and is imported by server.py.
- **Main Flow**:
  1. Delete curik/quiz.py.
  2. Remove quiz imports and @mcp.tool() registrations from server.py.
  3. Remove associated test files.
  4. Run `uv run pytest`.
- **Postconditions**: Package imports cleanly; no test references quiz.py.
- **Acceptance Criteria**:
  - [ ] curik/quiz.py does not exist
  - [ ] server.py has no import or registration for quiz functions
  - [ ] `uv run pytest` passes

---

## SUC-002: Developer removes research module without breaking the package

- **Actor**: Developer
- **Preconditions**: curik/research.py exists and is imported by server.py.
- **Main Flow**:
  1. Delete curik/research.py.
  2. Remove research imports and tool registrations from server.py.
  3. Remove ResearchTest class or delete tests/test_assets_research.py.
  4. Run `uv run pytest`.
- **Postconditions**: Package imports cleanly; no test references research.py.
- **Acceptance Criteria**:
  - [ ] curik/research.py does not exist
  - [ ] server.py has no import or registration for research functions
  - [ ] `uv run pytest` passes

---

## SUC-003: Developer removes assets module and preserves ACTIVITY_MAPPINGS

- **Actor**: Developer
- **Preconditions**: curik/assets.py exists with ACTIVITY_MAPPINGS dict and
  asset-loading functions. server.py imports from assets.py.
- **Main Flow**:
  1. Extract ACTIVITY_MAPPINGS from assets.py into curik/references/activity-mappings.md
     as a markdown table.
  2. Delete curik/assets.py.
  3. Remove all assets imports and tool registrations from server.py:
     tool_list_agents, tool_get_agent_definition, tool_list_skills,
     tool_get_skill_definition, tool_list_instructions, tool_get_instruction,
     tool_list_references, tool_get_reference, tool_get_process_guide,
     tool_get_activity_guide.
  4. Delete tests/test_assets_research.py.
  5. Run `uv run pytest`.
- **Postconditions**: ACTIVITY_MAPPINGS preserved as reference doc; assets.py gone;
  server imports cleanly.
- **Acceptance Criteria**:
  - [ ] curik/references/activity-mappings.md exists and contains ACTIVITY_MAPPINGS data
  - [ ] curik/assets.py does not exist
  - [ ] server.py has no import or registration for any asset function
  - [ ] tests/test_assets_research.py does not exist
  - [ ] `uv run pytest` passes

---

## SUC-004: Developer trims syllabus.py and cleans up all remaining references

- **Actor**: Developer
- **Preconditions**: curik/syllabus.py has five functions. server.py registers
  five syllabus tools. Test file covers all five. Init templates list removed tools.
- **Main Flow**:
  1. Remove get_syllabus, regenerate_syllabus, and read_syllabus_entries from
     syllabus.py. Retain _iter_lessons (used by validate_syllabus_consistency).
  2. Remove tool_read_syllabus_entries, tool_regenerate_syllabus, and tool_get_syllabus
     from server.py; update syllabus import to only import the two kept functions.
  3. Remove ReadSyllabusEntriesTest, GetSyllabusTest, and MCP wrapper tests for
     removed tools from tests/test_syllabus.py.
  4. Remove references to deleted tools from curik/init/claude-section.md and
     curik/init/curik-skill.md.
  5. Run `uv run pytest`.
- **Postconditions**: syllabus.py has exactly two public functions; tests pass;
  init templates are accurate.
- **Acceptance Criteria**:
  - [ ] curik/syllabus.py contains only write_syllabus_url, validate_syllabus_consistency,
        and _iter_lessons helper
  - [ ] server.py syllabus import lists only write_syllabus_url and
        validate_syllabus_consistency
  - [ ] tests/test_syllabus.py has no classes referencing removed functions
  - [ ] WriteSyllabusUrlTest and ValidateSyllabusConsistencyTest still pass
  - [ ] curik/init/claude-section.md and curik/init/curik-skill.md do not
        reference get_syllabus, regenerate_syllabus, read_syllabus_entries,
        generate_quiz_stub, validate_quiz_alignment, set_quiz_status,
        save_research_findings, or get_research_findings
  - [ ] `uv run pytest` passes
