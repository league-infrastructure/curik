---
description: Curik curriculum development tool dispatcher
---

# /curik

Dispatch to the Curik curriculum development tool. Parse the argument
after `/curik` and call the matching MCP tool from the table below.

If `/curik` is called with **no arguments**, display this help listing
to the user and stop — do not execute any tool.

## Available commands

| Command | Description | MCP call |
|---------|-------------|----------|
| `/curik status` | Show current project phase, open issues, active plans | `tool_get_course_status(path=".")` |
| `/curik spec` | Display the current course specification | `tool_get_spec(path=".")` |
| `/curik phase` | Show the current development phase | `tool_get_phase(path=".")` |
| `/curik validate <path>` | Validate a lesson file | `tool_validate_lesson(lesson_path=<path>)` |
| `/curik agents` | List available curriculum agents | `list_agents()` |
| `/curik skills` | List available curriculum skills | `list_skills()` |
| `/curik refs` | List available reference documents | `list_references()` |
| `/curik publish` | Show publishing guide with pre/post checklists | `tool_get_publish_guide()` |
| `/curik publish check` | Quick readiness check for publishing | `tool_check_publish_ready()` |

Pass any remaining text after the subcommand as the argument to the
tool (e.g., `/curik validate content/01-intro/01-hello.md`).

For general guidance, call `list_agents()` and load the `start-curik`
agent definition to begin the curriculum development workflow.
