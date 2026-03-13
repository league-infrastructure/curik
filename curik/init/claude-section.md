<!-- CURIK:START -->
# Curik Curriculum Project

This repository is a Curik-managed curriculum project for the League of Amazing Programmers.

## Before You Do Anything

1. Call `get_course_status()` to determine where this project stands.
2. Call `get_process_guide()` to understand what to do next.
3. Follow the process guide's instructions for the current phase.

Do not write curriculum content, modify course structure, scaffold files, or make any substantive changes without first consulting the MCP server for the current phase and the applicable agent.

## Rules

- **MCP-first**: For any operation that Curik has a tool for (creating issues, managing change plans, scaffolding, validation, syllabus operations), use the Curik MCP tool. Do not perform these operations by directly editing files.
- **Agent boundaries**: When you load an agent definition via `get_agent()`, respect its boundaries. The Curriculum Architect does not write lesson content. The Lesson Author does not modify course structure.
- **Skills are workflows**: When you load a skill via `get_skill()`, follow its steps in order. Do not skip steps.
- **Gates are gates**: When `advance_phase()` fails, do not work around it. Address the unmet conditions.
- **Designer approval**: Change plans, outlines, and phase transitions require designer approval. Do not self-approve.

## Available MCP Tools

### Process Discovery
- `get_process_guide()` — full process overview and decision tree
- `get_course_status()` — current project state
- `get_phase()` — current phase and gate conditions
- `advance_phase()` — gated phase transition
- `get_activity_guide(activity)` — bundled agent + skills + instructions

### Agent and Skill Loading
- `list_agents()` / `get_agent(name)` — agent definitions
- `list_skills()` / `get_skill(name)` — skill workflows
- `list_instructions()` / `get_instruction(name)` — reference documents

### State Management
- Spec state: `record_course_concept`, `record_pedagogical_model`, `record_alignment`
- Scaffolding: `scaffold_structure`, `create_lesson_stub`
- Syllabus: `regenerate_syllabus`, `get_syllabus`, `write_syllabus_url`, `trigger_readme_generation`, `validate_syllabus_consistency`
- Outlines: `approve_outline`
- Issues and change plans: `create_issue`, `list_issues`, `approve_change_plan`, `close_change_plan`
- Validation: `validate_lesson`, `validate_module`, `validate_course`, `get_validation_report`
- Quiz: `generate_quiz_stub`, `validate_quiz_alignment`, `set_quiz_status`
- Hugo: `list_content_pages`, `create_content_page`, `update_frontmatter`, `hugo_build`
<!-- CURIK:END -->
