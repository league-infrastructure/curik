"""Curik MCP server — thin wrapper over curik.project functions."""

from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .project import (
    CurikError,
    advance_phase,
    get_course_status,
    get_phase,
    get_spec,
    init_course,
    record_alignment,
    record_course_concept,
    record_pedagogical_model,
    update_spec,
)

mcp = FastMCP("curik", instructions="Curik curriculum development tool")

# Resolved at server startup via run_server(path).
_project_root: Path = Path(".")


def _root() -> Path:
    return _project_root


@mcp.tool()
def tool_init_course() -> str:
    """Initialize a new curriculum project with .course/ directory structure."""
    try:
        result = init_course(_root())
        import json

        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_phase() -> str:
    """Return the current course phase and what gates must be met to advance."""
    try:
        import json

        return json.dumps(get_phase(_root()), indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_advance_phase(target: str) -> str:
    """Advance to the target phase (e.g., 'phase2'). Fails if spec is incomplete."""
    try:
        advance_phase(_root(), target)
        return f"Advanced to {target}."
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_spec() -> str:
    """Read the current course specification document."""
    try:
        return get_spec(_root())
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_update_spec(section: str, content: str) -> str:
    """Update a named section of the spec document."""
    try:
        update_spec(_root(), section, content)
        return f"Updated section: {section}"
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_record_course_concept(content: str) -> str:
    """Record Phase 1a output: course concept details."""
    try:
        record_course_concept(_root(), content)
        return "Recorded course concept."
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_record_pedagogical_model(content: str) -> str:
    """Record Phase 1b output: pedagogical model choices."""
    try:
        record_pedagogical_model(_root(), content)
        return "Recorded pedagogical model."
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_record_alignment(content: str) -> str:
    """Record Phase 1d output: alignment decision and topic list."""
    try:
        record_alignment(_root(), content)
        return "Recorded alignment decision."
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_course_status() -> str:
    """Return a summary: current phase, open issues count, active change plans."""
    try:
        import json

        return json.dumps(get_course_status(_root()), indent=2)
    except CurikError as e:
        return f"Error: {e}"


def run_server(root: Path) -> None:
    """Start the MCP server with the given project root."""
    global _project_root
    _project_root = root.resolve()
    mcp.run(transport="stdio")
