"""Curik MCP server — thin wrapper over curik.project functions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from .assets import (
    get_agent_definition,
    get_skill_definition,
    list_agents,
    list_skills,
)
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
from .changes import (
    approve_change_plan,
    close_change_plan,
    create_change_plan,
    create_issue,
    execute_change_plan,
    list_issues,
    review_change_plan,
)
from .migrate import inventory_course, migrate_structure
from .quiz import generate_quiz_stub, set_quiz_status, validate_quiz_alignment
from .research import get_research_findings, save_research_findings
from .validation import (
    get_validation_report,
    save_validation_report,
    validate_course,
    validate_lesson,
    validate_module,
)
from .readme import generate_readmes
from .scaffolding import (
    approve_outline,
    create_lesson_stub,
    create_outline,
    generate_change_plan,
    generate_nav,
    get_outline,
    scaffold_structure,
)
from .syllabus import (
    get_syllabus,
    read_syllabus_entries,
    regenerate_syllabus,
    validate_syllabus_consistency,
    write_syllabus_url,
)

mcp = FastMCP("curik", instructions="Curik curriculum development tool")

# Resolved at server startup via run_server(path).
_project_root: Path = Path(".")


def _root() -> Path:
    return _project_root


@mcp.tool()
def tool_init_course(course_type: str = "course") -> str:
    """Initialize a new curriculum project with CURIK_DIR/ directory structure.

    *course_type* must be ``"course"`` (default) or ``"resource-collection"``.
    """
    try:
        result = init_course(_root(), course_type=course_type)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_phase() -> str:
    """Return the current course phase and what gates must be met to advance."""
    try:
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
        return json.dumps(get_course_status(_root()), indent=2)
    except CurikError as e:
        return f"Error: {e}"


# -- Asset tools --


@mcp.tool()
def tool_list_agents() -> str:
    """List all available agent definitions."""
    try:
        return json.dumps(list_agents())
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_agent_definition(name: str) -> str:
    """Get the full markdown content of a named agent definition."""
    try:
        return get_agent_definition(name)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_list_skills() -> str:
    """List all available skill definitions."""
    try:
        return json.dumps(list_skills())
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_skill_definition(name: str) -> str:
    """Get the full markdown content of a named skill definition."""
    try:
        return get_skill_definition(name)
    except CurikError as e:
        return f"Error: {e}"


# -- Research tools --


@mcp.tool()
def tool_save_research_findings(title: str, content: str) -> str:
    """Save structured research findings to CURIK_DIR/research/."""
    try:
        result = save_research_findings(_root(), title, content)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_research_findings() -> str:
    """List all saved research findings."""
    try:
        return json.dumps(get_research_findings(_root()), indent=2)
    except CurikError as e:
        return f"Error: {e}"


# -- Scaffolding tools --


@mcp.tool()
def tool_scaffold_structure(
    structure_json: str,
    course_type: str = "course",
    tier: int = 0,
    language: str = "python",
) -> str:
    """Create the directory tree and lesson stubs described by a JSON structure.

    *structure_json* must be a JSON string with format:
    {"modules": [{"name": "01-intro", "lessons": ["01-hello.md"]}]}

    *course_type* must be ``"course"`` (default) or ``"resource-collection"``.
    *tier* (1-4) enables tier-specific features; 0 means unset.
    *language* sets the devcontainer language for tier 3-4 projects.
    """
    try:
        structure = json.loads(structure_json)
        kwargs: dict[str, Any] = {"course_type": course_type}
        if tier > 0:
            kwargs["tier"] = tier
            kwargs["language"] = language
        result = scaffold_structure(_root(), structure, **kwargs)
        return json.dumps(result, indent=2)
    except (json.JSONDecodeError, CurikError) as e:
        return f"Error: {e}"


@mcp.tool()
def tool_create_lesson_stub(module: str, lesson: str, tier: int) -> str:
    """Create a single lesson stub file. Tier 1-2: instructor-guide-primary.
    Tier 3-4: student content + instructor guide (+ .ipynb companion if applicable)."""
    try:
        rel = create_lesson_stub(_root(), module, lesson, tier)
        return f"Created: {rel}"
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_create_outline(name: str, content: str) -> str:
    """Write an outline document to CURIK_DIR/outlines/."""
    try:
        rel = create_outline(_root(), name, content)
        return f"Created outline: {rel}"
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_approve_outline(name: str) -> str:
    """Mark an outline as approved by updating its frontmatter."""
    try:
        rel = approve_outline(_root(), name)
        return f"Approved outline: {rel}"
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_outline(name: str) -> str:
    """Read and return the content of an outline document."""
    try:
        return get_outline(_root(), name)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_generate_change_plan(title: str, items_json: str) -> str:
    """Create a numbered change plan. *items_json* is a JSON array of strings."""
    try:
        items = json.loads(items_json)
        rel = generate_change_plan(_root(), title, items)
        return f"Created change plan: {rel}"
    except (json.JSONDecodeError, CurikError) as e:
        return f"Error: {e}"


# -- Change cycle tools --


@mcp.tool()
def tool_create_issue(title: str, content: str) -> str:
    """Create a numbered issue in CURIK_DIR/issues/open/ with YAML frontmatter."""
    try:
        result = create_issue(_root(), title, content)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_list_issues(status: str = "open") -> str:
    """List issues from open/ or done/ directory."""
    try:
        return json.dumps(list_issues(_root(), status), indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_create_change_plan(title: str, issue_numbers_json: str) -> str:
    """Create a numbered change plan referencing issue numbers. issue_numbers_json is a JSON array of ints."""
    try:
        issue_numbers = json.loads(issue_numbers_json)
        result = create_change_plan(_root(), title, issue_numbers)
        return json.dumps(result, indent=2)
    except (json.JSONDecodeError, CurikError) as e:
        return f"Error: {e}"


@mcp.tool()
def tool_approve_change_plan(plan_number: int) -> str:
    """Set a change plan's status to 'approved'. Must be in 'draft' status."""
    try:
        result = approve_change_plan(_root(), plan_number)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_execute_change_plan(plan_number: int) -> str:
    """Set a change plan's status to 'executed'. Must be in 'approved' status."""
    try:
        result = execute_change_plan(_root(), plan_number)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_review_change_plan(plan_number: int, gaps_json: str = "[]") -> str:
    """Review a change plan. gaps_json is a JSON array of gap description strings."""
    try:
        gaps = json.loads(gaps_json)
        result = review_change_plan(_root(), plan_number, gaps)
        return json.dumps(result, indent=2)
    except (json.JSONDecodeError, CurikError) as e:
        return f"Error: {e}"


@mcp.tool()
def tool_close_change_plan(plan_number: int) -> str:
    """Close a change plan: move to done/, move referenced issues to done/."""
    try:
        result = close_change_plan(_root(), plan_number)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


# -- Migration tools --


@mcp.tool()
def tool_inventory_course(repo_path: str) -> str:
    """Analyze a course repository and return its current state as JSON."""
    try:
        result = inventory_course(repo_path)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_migrate_structure(tier: int, modules_json: str) -> str:
    """Create the standard Curik directory structure for a course.

    *modules_json* is a JSON array of module name strings (e.g. '["01-intro", "02-loops"]').
    """
    try:
        modules = json.loads(modules_json)
        result = migrate_structure(_root(), tier, modules)
        return json.dumps(result, indent=2)
    except (json.JSONDecodeError, CurikError) as e:
        return f"Error: {e}"


# -- Validation tools --


@mcp.tool()
def tool_validate_lesson(lesson_path: str, tier: int | None = None) -> str:
    """Validate a single lesson file for completeness (instructor guide, objectives).

    When *tier* is 3 or 4, also checks for readme-shared comment guards
    and verifies the lesson UID appears in syllabus.yaml.
    """
    try:
        result = validate_lesson(_root(), lesson_path, tier=tier)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_validate_module(module_path: str) -> str:
    """Validate a module directory — checks overview and all lesson files."""
    try:
        result = validate_module(_root(), module_path)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_validate_course(tier: int | None = None) -> str:
    """Validate the entire course — course.yml and all modules.

    When *tier* is 3 or 4, also checks syllabus consistency and
    README existence in lesson mirror directories.
    """
    try:
        result = validate_course(_root(), tier=tier)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_validation_report() -> str:
    """Read the last saved validation report."""
    try:
        result = get_validation_report(_root())
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_save_validation_report(report_json: str) -> str:
    """Save a validation report to CURIK_DIR/validation-report.json."""
    try:
        report = json.loads(report_json)
        result = save_validation_report(_root(), report)
        return json.dumps(result, indent=2)
    except (json.JSONDecodeError, CurikError) as e:
        return f"Error: {e}"


# -- Quiz tools --


@mcp.tool()
def tool_generate_quiz_stub(lesson_id: str, topics_json: str) -> str:
    """Create a quiz.yml stub for a lesson. topics_json is a JSON array of topic strings."""
    try:
        topics = json.loads(topics_json)
        result = generate_quiz_stub(_root(), lesson_id, topics)
        return json.dumps(result, indent=2)
    except (json.JSONDecodeError, CurikError) as e:
        return f"Error: {e}"


@mcp.tool()
def tool_validate_quiz_alignment(lesson_path: str, quiz_path: str) -> str:
    """Check that each lesson objective has at least one quiz topic covering it."""
    try:
        result = validate_quiz_alignment(_root(), lesson_path, quiz_path)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_set_quiz_status(quiz_path: str, status: str) -> str:
    """Update a quiz file's status. Valid statuses: drafted, reviewed, complete."""
    try:
        result = set_quiz_status(_root(), quiz_path, status)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


# -- Syllabus tools --


@mcp.tool()
def tool_read_syllabus_entries() -> str:
    """Read syllabus.yaml and return lesson entries with uid, name, lesson, exercise fields."""
    try:
        result = read_syllabus_entries(_root())
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_write_syllabus_url(uid: str, url: str) -> str:
    """Update the url field for a lesson entry identified by UID in syllabus.yaml."""
    try:
        result = write_syllabus_url(_root(), uid, url)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_regenerate_syllabus(lesson_dir: str = "lessons") -> str:
    """Compile syllabus from lesson directory using jtl-syllabus and write syllabus.yaml."""
    try:
        result = regenerate_syllabus(_root(), lesson_dir)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_syllabus() -> str:
    """Return the raw content of syllabus.yaml."""
    try:
        return get_syllabus(_root())
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_trigger_readme_generation(docs_dir: str = "docs/docs") -> str:
    """Generate README.md files from guarded sections in MkDocs lesson pages."""
    try:
        result = generate_readmes(_root(), docs_dir)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_validate_syllabus_consistency() -> str:
    """Check syllabus entries against MkDocs pages and report mismatches."""
    try:
        result = validate_syllabus_consistency(_root())
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


def run_server(root: Path) -> None:
    """Start the MCP server with the given project root."""
    global _project_root
    _project_root = root.resolve()
    mcp.run(transport="stdio")
