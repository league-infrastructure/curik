---
status: complete
---

# Sprint 012 Use Cases

## SUC-001: Initialize new course project

- **Actor**: Curriculum developer
- **Preconditions**: Empty or existing git repository cloned locally
- **Main Flow**:
  1. Developer runs `curik init` in the repo root
  2. System creates `.course/` directory with state, spec, and subdirectories
  3. System creates `course.yml` and `.mcp.json`
  4. System prints friendly message: "Open Claude Code and say: Start Curik"
- **Postconditions**: `.course/` directory exists, developer knows next step
- **Acceptance Criteria**:
  - [x] `.course/` is the hidden directory name (not `.curik/`)
  - [x] CLI prints human-readable init message

## SUC-002: Sequester existing content

- **Actor**: Agent (on behalf of curriculum developer)
- **Preconditions**: Repository has non-Curik files, `.course/` exists
- **Main Flow**:
  1. Agent calls `sequester_content()` tool
  2. System moves all non-Curik files into `_old/` preserving directory structure
  3. System returns list of moved files
- **Postconditions**: Original files in `_old/`, root is clean for rebuilding
- **Acceptance Criteria**:
  - [x] Files moved to `_old/`, not deleted
  - [x] `.course/`, `.git/`, `.mcp.json`, `course.yml` are NOT moved
  - [x] Returns inventory of moved files

## SUC-003: Track Phase 1 sub-phases

- **Actor**: Agent
- **Preconditions**: Course initialized, in phase1
- **Main Flow**:
  1. Agent queries current sub-phase via `get_phase()`
  2. Agent advances sub-phase after completing a sub-phase's work
  3. State tracks progression: 1a → 1b → 1c → 1d → 1e → phase2
- **Postconditions**: State reflects current sub-phase
- **Acceptance Criteria**:
  - [x] `get_phase()` returns sub_phase field
  - [x] `advance_sub_phase()` moves to next sub-phase
  - [x] Cannot skip sub-phases

## SUC-004: Start Curik agent flow

- **Actor**: Curriculum developer (via Claude Code)
- **Preconditions**: `curik init` completed, Claude Code open
- **Main Flow**:
  1. Developer says "Start Curik"
  2. Agent verifies MCP server connectivity and `.course/` existence
  3. Agent detects empty vs existing-content repo
  4. For existing content: asks about sequestering
  5. Begins Phase 1a conversation
- **Postconditions**: Phase 1 conversation underway
- **Acceptance Criteria**:
  - [x] Agent definition exists with startup instructions
  - [x] Handles both empty and existing-content repos
