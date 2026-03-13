---
status: complete
---

# Sprint 016 Use Cases

## DUC-001: Agent Receives Correct Hugo Instructions

- **Actor**: AI agent (any LLM) using Curik MCP tools
- **Preconditions**: Agent loads a definition via `tool_get_agent_definition` or `tool_get_skill_definition`
- **Main Flow**:
  1. Agent requests a definition file (e.g., "start-curik")
  2. Definition references Hugo as the SSG, `content/` directory, `{{< shortcode >}}` syntax
  3. Agent uses this information to generate correct Hugo content
- **Postconditions**: Generated content uses Hugo conventions, not MkDocs
- **Acceptance Criteria**:
  - [x] All agent/skill definitions reference Hugo, not MkDocs

## DUC-002: No Stale MkDocs References in Agent Context

- **Actor**: AI agent performing curriculum development
- **Preconditions**: Agent has loaded multiple skill/agent definitions
- **Main Flow**:
  1. Agent loads repo-scaffolding skill — sees `content/` directory tree
  2. Agent loads readme-guards skill — sees `{{< readme-shared >}}` syntax
  3. Agent loads syllabus-integration skill — sees `content/` paths
  4. No conflicting MkDocs references exist across any loaded definitions
- **Postconditions**: Agent has a consistent view of Hugo-based tooling
- **Acceptance Criteria**:
  - [x] Zero MkDocs references in agent/skill files
