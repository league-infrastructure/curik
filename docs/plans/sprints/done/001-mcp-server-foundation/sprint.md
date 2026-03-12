---
id: '001'
title: MCP Server Foundation
status: done
branch: sprint/001-mcp-server-foundation
use-cases:
- SUC-001
- SUC-002
- SUC-003
---

# Sprint 001: MCP Server Foundation

## Goals

Stand up the Curik MCP server so that the existing Phase 1 functionality
(init, phase tracking, spec management) is accessible to AI agents through
Claude Code. This is the foundational infrastructure that all subsequent
sprints depend on.

## Problem

Curik has a working CLI with init, phase tracking, spec management, and
Phase 1→2 gating — but it only works from the command line. AI agents in
Claude Code interact through MCP tools, not CLI commands. Without an MCP
server, agents cannot use Curik's enforcement model.

## Solution

Implement a Python MCP server using the MCP SDK that wraps the existing
`curik.project` module functions as MCP tools. The server runs locally via
`curik mcp` and is configured in `.mcp.json`. Each existing CLI command
becomes an MCP tool with the same semantics.

## Success Criteria

- `curik mcp` starts a working MCP server
- All Phase 1 tools are callable from Claude Code
- Phase gating works identically through MCP as through CLI
- Existing tests continue to pass
- New tests cover MCP tool invocations

## Scope

### In Scope

- MCP server implementation using Python MCP SDK
- MCP tools: `init_course`, `get_phase`, `advance_phase`, `get_spec`,
  `update_spec`, `record_course_concept`, `record_pedagogical_model`,
  `record_alignment`, `get_course_status`
- `.mcp.json` configuration pointing to `curik mcp`
- Integration tests for MCP tool calls
- `pyproject.toml` dependency on MCP SDK

### Out of Scope

- Phase 2 tools (scaffolding, outlines, lesson stubs)
- Agent or skill definitions (Sprint 2)
- Research tools (Sprint 2)
- Change cycle tools (Sprint 5)
- Validation tools (Sprint 6)

## Test Strategy

- Unit tests: existing tests in `test_project.py` must continue to pass
- Integration tests: new test file `test_mcp_server.py` that starts the
  MCP server and calls each tool, verifying correct responses and error
  handling
- Phase gating test: verify that `advance_phase` rejects incomplete specs
  through MCP just as it does through the Python API

## Architecture Notes

- The MCP server is a thin wrapper around `curik.project` functions
- No new business logic in the MCP layer — it delegates entirely to
  the existing project module
- Server uses stdio transport (standard for Claude Code MCP servers)
- Tool names match the project plan's MCP tool names (Section 7)
- Error responses use CurikError messages as MCP error content

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [ ] Architecture review passed
- [ ] Stakeholder has approved the sprint plan

## Tickets

(To be created after sprint approval.)
