"""Curik MCP server — thin wrapper over curik.project functions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from .assets import (
    ACTIVITY_MAPPINGS,
    get_activity_guide,
    get_agent_definition,
    get_instruction,
    get_process_guide,
    get_reference,
    get_skill_definition,
    list_agents,
    list_instructions,
    list_references,
    list_skills,
)
from .project import (
    CurikError,
    advance_phase,
    advance_sub_phase,
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
    register_change_plan,
    review_change_plan,
)
from .hugo import (
    create_content_page,
    hugo_build,
    list_content_pages,
    update_frontmatter,
)
from .migrate import inventory_course, migrate_structure, sequester_content
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
from .templates import hugo_setup
from .syllabus import (
    get_syllabus,
    read_syllabus_entries,
    regenerate_syllabus,
    validate_syllabus_consistency,
    write_syllabus_url,
)

mcp = FastMCP(
    "curik",
    instructions=(
        "Curik is a curriculum development tool for the League of Amazing "
        "Programmers.\n\n"
        "GETTING STARTED: Call tool_get_course_status() to see current phase, "
        "then tool_get_phase() for what to do next. Load the start-curik agent "
        "via tool_get_agent_definition('start-curik') for guided workflow.\n\n"
        "HUGO SSG: Content lives in content/ with _index.md branch bundles. "
        "Navigation order from numeric prefixes (01-, 02-). Config in hugo.toml. "
        "The Curriculum Hugo Theme provides branding and shortcodes.\n\n"
        "SHORTCODES (use these, NEVER raw HTML divs or comment guards):\n"
        "- {{< instructor-guide >}}...{{< /instructor-guide >}} — instructor-only content\n"
        "- {{< callout type=\"tip\" >}}...{{< /callout >}} — info/warning/tip boxes\n"
        "- {{< readme-shared >}}...{{< /readme-shared >}} — appears on site AND in README\n"
        "- {{< readme-only >}}...{{< /readme-only >}} — README only, hidden from site\n\n"
        "WORKFLOW: Phase 1 (course design) → Phase 2 (content authoring). "
        "In Phase 1, use tool_update_spec() to fill spec sections and "
        "tool_advance_sub_phase() to progress. In Phase 2, use "
        "tool_scaffold_structure() for layout, tool_create_lesson_stub() for "
        "lessons, tool_validate_lesson() to check work.\n\n"
        "DISCOVERY: Use tool_get_process_guide() for the full process decision "
        "tree. Use tool_get_activity_guide(activity) to load bundled context "
        "for a named activity. Use tool_list_agents(), tool_list_skills(), "
        "tool_list_instructions() to find curriculum development resources."
    ),
)

# Resolved at server startup via run_server(path).
_project_root: Path = Path(".")


def _root() -> Path:
    return _project_root


@mcp.tool()
def tool_init_course(course_type: str = "course") -> str:
    """Initialize a new curriculum project.

    Creates .course/ directory, course.yml, .mcp.json, CLAUDE.md with Hugo
    conventions, /curik skill, and MCP permissions.
    *course_type*: ``"course"`` (default) or ``"resource-collection"``.
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
def tool_advance_sub_phase() -> str:
    """Advance to the next Phase 1 sub-phase (1a→1b→1c→1d→1e).

    Resource-collection projects skip 1b and 1d.
    Raises an error if already at 1e — use advance_phase('phase2') instead.
    """
    try:
        result = advance_sub_phase(_root())
        return json.dumps(result, indent=2)
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


@mcp.tool()
def tool_update_course_yml(updates_json: str) -> str:
    """Update fields in course.yml.

    *updates_json* is a JSON object of field names to new values, e.g.:
    ``{"title": "Python Basics", "slug": "python-basics", "tier": 3}``

    Only updates the specified fields; leaves other fields unchanged.
    Returns the full updated course.yml content.

    IMPORTANT: After updating slug or title, run ``tool_hugo_setup()`` to
    regenerate ``hugo.toml`` with the correct baseURL.
    """
    import yaml

    root = _root()
    course_yml = root / "course.yml"
    if not course_yml.exists():
        return "Error: course.yml not found. Run tool_init_course() first."

    try:
        updates = json.loads(updates_json)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON: {e}"

    if not isinstance(updates, dict):
        return "Error: updates_json must be a JSON object"

    try:
        data = yaml.safe_load(course_yml.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            data = {}
    except yaml.YAMLError as e:
        return f"Error: Failed to parse course.yml: {e}"

    data.update(updates)

    # Write back preserving simple key: value format
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}: {json.dumps(value)}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("")

    content = "\n".join(lines)
    course_yml.write_text(content, encoding="utf-8")

    # Report what changed and what's still TBD
    still_tbd = [f for f in COURSE_YML_REQUIRED_FIELDS if _is_tbd(data.get(f))]

    result = {
        "updated_fields": list(updates.keys()),
        "content": content,
    }
    if still_tbd:
        result["still_tbd"] = still_tbd
        result["message"] = (
            f"{len(still_tbd)} required field(s) still need values: "
            + ", ".join(still_tbd)
        )
    else:
        result["message"] = "All required fields are set."

    return json.dumps(result, indent=2)


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


@mcp.tool()
def tool_list_instructions() -> str:
    """List all available instruction documents (process refs, conventions, templates)."""
    try:
        return json.dumps(list_instructions())
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_instruction(name: str) -> str:
    """Get the full markdown content of a named instruction document."""
    try:
        return get_instruction(name)
    except CurikError as e:
        return f"Error: {e}"


# Backward-compatible aliases
@mcp.tool()
def tool_list_references() -> str:
    """List all available reference documents. Alias for tool_list_instructions."""
    return tool_list_instructions()


@mcp.tool()
def tool_get_reference(name: str) -> str:
    """Get a reference document by name. Alias for tool_get_instruction."""
    return tool_get_instruction(name)


# -- Process discovery tools --


@mcp.tool()
def tool_get_process_guide() -> str:
    """Get the full curriculum development process guide.

    Returns a decision-tree document describing all 3 macro-phases,
    which agents to use at each stage, which skills apply, and gate
    conditions. Call this at session start and whenever uncertain about
    what to do next.
    """
    try:
        return get_process_guide()
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_get_activity_guide(activity: str) -> str:
    """Get bundled context for a named activity: agent + skills + instructions.

    Combines the agent definition, all applicable skills, and all applicable
    instructions into a single document. Valid activities:
    spec-development, research, content-analysis, scaffolding,
    lesson-writing-young, lesson-writing-older, quiz-authoring,
    content-conversion, change-management, validation.
    """
    try:
        return get_activity_guide(activity)
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
    """Create the Hugo content/ directory tree and lesson stubs.

    Generates module directories with _index.md branch bundles and lesson
    stub files containing Hugo shortcodes (instructor-guide, readme guards).

    *structure_json*: ``{"modules": [{"name": "01-intro", "lessons": ["01-hello.md"]}]}``
    *course_type*: ``"course"`` (default) or ``"resource-collection"``.
    *tier* (1-4): enables tier-specific features; 0 means unset.
    *language*: devcontainer language for tier 3-4 projects.
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
    """Create a single Hugo lesson stub in content/<module>/<lesson>.

    Generated stubs include {{< instructor-guide >}} shortcode blocks.
    Tier 1-2: instructor-guide-primary layout.
    Tier 3-4: student content + instructor guide (+ .ipynb companion)."""
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
def tool_register_change_plan(plan_number: int) -> str:
    """Register an agent-written change plan file.

    Validates that the plan file exists in change-plan/active/ and has
    correct frontmatter (title, status). Use this after writing a change
    plan document directly, rather than using tool_create_change_plan.
    """
    try:
        result = register_change_plan(_root(), plan_number)
        return json.dumps(result, indent=2)
    except CurikError as e:
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
def tool_sequester_content() -> str:
    """Move all non-Curik files in the project root into _old/.

    Protected paths (.course/, .git/, .mcp.json, course.yml, _old/) are
    never moved.  Returns {"moved": [...], "protected": [...]}.
    """
    try:
        result = sequester_content(_root())
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

    When *tier* is 3 or 4, also checks for ``{{</* readme-shared */>}}`` shortcode guards
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
def tool_trigger_readme_generation(docs_dir: str = "content") -> str:
    """Generate README.md files from {{< readme-shared >}} and {{< readme-only >}} shortcode guards in Hugo lesson pages."""
    try:
        result = generate_readmes(_root(), docs_dir)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_validate_syllabus_consistency() -> str:
    """Check syllabus entries against Hugo content pages and report mismatches."""
    try:
        result = validate_syllabus_consistency(_root())
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


# -- Hugo site tools --


@mcp.tool()
def tool_list_content_pages(section: str | None = None) -> str:
    """List all content pages under content/ with frontmatter metadata.

    Returns path, title, weight, and draft status for each .md file.
    Optional *section* (e.g. "01-intro") limits to a subdirectory.
    """
    try:
        result = list_content_pages(_root(), section=section)
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


@mcp.tool()
def tool_create_content_page(
    page_path: str,
    title: str,
    content: str = "",
    extra_frontmatter_json: str = "{}",
) -> str:
    """Create a new Hugo content page at content/<page_path>.

    Use this for arbitrary pages (landing pages, resources, etc.) —
    for lesson stubs with shortcode scaffolding, use tool_create_lesson_stub.
    *extra_frontmatter_json*: JSON dict of additional frontmatter fields.
    """
    try:
        extra = json.loads(extra_frontmatter_json)
        rel = create_content_page(
            _root(), page_path, title, content, extra_frontmatter=extra
        )
        return f"Created: {rel}"
    except (json.JSONDecodeError, CurikError) as e:
        return f"Error: {e}"


@mcp.tool()
def tool_update_frontmatter(page_path: str, updates_json: str) -> str:
    """Update YAML frontmatter on an existing content page.

    Merges *updates_json* (a JSON dict) into the page's frontmatter.
    Existing fields are preserved; matching keys are overwritten.
    Body content is not modified.
    """
    try:
        updates = json.loads(updates_json)
        result = update_frontmatter(_root(), page_path, updates)
        return json.dumps(result, indent=2)
    except (json.JSONDecodeError, CurikError) as e:
        return f"Error: {e}"


@mcp.tool()
def tool_hugo_setup(title: str = "", tier: int = 2) -> str:
    """Generate hugo.toml and copy the curriculum theme into this course repo.

    Creates ``hugo.toml`` with the given title and tier settings, and copies
    the curriculum-hugo-theme into ``themes/curriculum-hugo-theme/``.

    If *title* is empty, reads it from ``course.yml``. If *tier* is not
    provided, defaults to 2 (or reads from ``course.yml``).

    This is called automatically by ``tool_scaffold_structure()``, but can
    also be used standalone to regenerate the Hugo config or re-copy the theme.
    """
    import yaml

    root = _root()
    effective_title = title
    effective_tier = tier

    slug = ""
    if not effective_title:
        course_yml = root / "course.yml"
        if course_yml.is_file():
            try:
                data = yaml.safe_load(course_yml.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    effective_title = data.get("title", "Course")
                    slug = data.get("slug", "")
                    effective_tier = data.get("tier", tier)
            except yaml.YAMLError:
                pass
        if not effective_title:
            effective_title = "Course"

    try:
        result = hugo_setup(root, effective_title, effective_tier, slug=slug)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def tool_hugo_build() -> str:
    """Build the Hugo site and return the result.

    Returns success status, build output, and any errors.
    If Hugo is not installed, returns an actionable error message.
    """
    try:
        result = hugo_build(_root())
        return json.dumps(result, indent=2)
    except CurikError as e:
        return f"Error: {e}"


# Fields in course.yml that must be set (not TBD/empty) before publishing.
# These are the fields that affect the published site or are required metadata.
COURSE_YML_REQUIRED_FIELDS = [
    "title",        # course title — appears in site header and browser tab
    "slug",         # URL path segment — determines the published URL
    "tier",         # tier number — controls theme behavior (instructor guide, etc.)
    "grades",       # grade range — displayed in course metadata
    "category",     # course category — used for index page grouping
    "description",  # one-line description — used in index listing and meta tags
    "curriculum_url",  # published URL — set to https://curriculum.jointheleague.org/<slug>/
    "repo_url",     # GitHub repo URL — appears in site footer
]


def _is_tbd(value: object) -> bool:
    """Return True if a course.yml value is unset / placeholder."""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() in ("", "TBD", "0")
    if isinstance(value, (int, float)):
        return value == 0
    if isinstance(value, list):
        return len(value) == 0
    return False


def _read_publish_state(root: Path) -> dict:
    """Read course metadata and check publish-readiness indicators."""
    import yaml

    state: dict = {
        "slug": "",
        "title": "this course",
        "tier": 0,
        "has_course_yml": False,
        "course_yml_data": {},
        "course_yml_tbd_fields": [],
        "has_workflow": (root / ".github" / "workflows" / "deploy-pages.yml").exists(),
        "has_gitignore": (root / ".gitignore").exists(),
        "has_hugo_toml": (root / "hugo.toml").exists(),
        "base_url_ok": False,
        "has_content": False,
        "content_sections": 0,
        "content_pages": 0,
        "has_theme": (root / "themes" / "curriculum-hugo-theme").exists()
            or (root / "themes" / "curriculum-hugo-theme").is_symlink(),
        "hugo_builds": False,
    }

    course_yml = root / "course.yml"
    if course_yml.is_file():
        state["has_course_yml"] = True
        try:
            data = yaml.safe_load(course_yml.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                state["course_yml_data"] = data
                state["slug"] = data.get("slug", "")
                state["title"] = data.get("title", state["title"])
                state["tier"] = data.get("tier", 0)
                # Check required fields for TBD/empty values
                tbd = []
                for field in COURSE_YML_REQUIRED_FIELDS:
                    if _is_tbd(data.get(field)):
                        tbd.append(field)
                state["course_yml_tbd_fields"] = tbd
        except yaml.YAMLError:
            pass

    if state["has_hugo_toml"]:
        content = (root / "hugo.toml").read_text(encoding="utf-8")
        state["base_url_ok"] = "curriculum.jointheleague.org" in content

    content_dir = root / "content"
    if content_dir.is_dir():
        sections = [
            d for d in content_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]
        state["content_sections"] = len(sections)
        pages = list(content_dir.rglob("*.md"))
        state["content_pages"] = len(pages)
        state["has_content"] = len(pages) > 1  # more than just _index.md

    # Try a Hugo build to check for errors
    if state["has_hugo_toml"] and state["has_theme"]:
        try:
            result = hugo_build(root)
            state["hugo_builds"] = result.get("success", False)
            state["build_errors"] = result.get("stderr", "")
        except Exception as e:
            state["hugo_builds"] = False
            state["build_errors"] = str(e)

    return state


@mcp.tool()
def tool_get_publish_guide() -> str:
    """Return the publishing guide with pre-publish and post-publish checklists.

    Reads the course state and returns a personalized guide with:
    - Setup instructions for GitHub Pages
    - Pre-publish checklist (is everything ready?)
    - Post-publish checklist (verify the deployment)
    """
    root = _root()
    s = _read_publish_state(root)

    slug = s["slug"]
    title = s["title"]
    has_slug = slug and slug != "TBD"

    if has_slug:
        url = f"https://curriculum.jointheleague.org/{slug}/"
        repo = f"league-curriculum/{slug}"
    else:
        url = "https://curriculum.jointheleague.org/<slug>/"
        repo = "league-curriculum/<slug>"

    lines = [
        f"# Publishing Guide: {title}",
        "",
        f"**Target URL:** {url}",
        f"**GitHub repo:** {repo}",
        "",
        "## Hosting Architecture",
        "",
        "All League curricula are published to GitHub Pages under the",
        "`league-curriculum` GitHub organization with a shared custom domain:",
        "",
        "- **Index:** https://curriculum.jointheleague.org/ (from league-curriculum/league-curriculum)",
        f"- **This course:** {url}",
        "",
        "GitHub Pages automatically routes project repos as subpaths of",
        "the org custom domain.",
        "",

        # ── Pre-publish checklist ──────────────────────────────────
        "## Pre-Publish Checklist",
        "",
        "Everything here must pass before deploying.",
        "",
        "### Configuration",
        "",
    ]

    def check(ok: bool, yes: str, no: str) -> str:
        return f"- [x] {yes}" if ok else f"- [ ] {no}"

    # ── course.yml metadata ────────────────────────────────────
    tbd_fields = s["course_yml_tbd_fields"]
    course_data = s["course_yml_data"]
    course_yml_ok = s["has_course_yml"] and len(tbd_fields) == 0

    lines.append(check(
        s["has_course_yml"],
        "`course.yml` exists",
        "**Create `course.yml`** — run `curik init`",
    ))

    if s["has_course_yml"]:
        lines.append(check(
            course_yml_ok,
            "All required `course.yml` fields are set",
            f"**{len(tbd_fields)} field(s) still TBD** in `course.yml` (see below)",
        ))

        if tbd_fields:
            lines.extend([
                "",
                "#### course.yml Fields to Complete",
                "",
                "The following fields are required for publishing. Set them in",
                "`course.yml` based on the course content, or ask the stakeholder",
                "if unsure. For `curriculum_url` and `repo_url`, use the values",
                "shown in the Target URL and GitHub repo at the top of this guide.",
                "",
                "| Field | Current | Required |",
                "|-------|---------|----------|",
            ])
            field_hints = {
                "title": "Human-readable course title",
                "slug": "URL path segment (lowercase, hyphenated)",
                "tier": "1 (K-2), 2 (3-5), 3 (6-8), or 4 (9-12)",
                "grades": "Grade range, e.g. 'K-2', '6-8'",
                "category": "unplugged, block-programming, text-programming, or advanced",
                "description": "One-line course description",
                "curriculum_url": f"{url}",
                "repo_url": f"https://github.com/{repo}",
            }
            for field in tbd_fields:
                current = course_data.get(field, "missing")
                hint = field_hints.get(field, "Required value")
                lines.append(f"| `{field}` | `{current}` | {hint} |")

            lines.extend([
                "",
                "**Agent instruction:** If you can infer the correct values from",
                "the course content and structure, update `course.yml` with your",
                "best values and present them to the stakeholder for review.",
                "If you cannot determine a value, ask the stakeholder.",
                "",
            ])

    # ── Infrastructure files ───────────────────────────────────
    lines.extend(["", "### Infrastructure", ""])

    lines.append(check(
        s["has_hugo_toml"],
        "`hugo.toml` exists",
        "**Generate `hugo.toml`** — run `tool_hugo_setup()`",
    ))
    lines.append(check(
        s["base_url_ok"],
        f"`baseURL` set to `{url}`",
        "**Fix `baseURL`** in `hugo.toml` — run `tool_hugo_setup()` to regenerate",
    ))
    lines.append(check(
        s["has_theme"],
        "Hugo theme installed",
        "**Install theme** — run `tool_hugo_setup()`",
    ))
    lines.append(check(
        s["has_gitignore"],
        "`.gitignore` installed",
        "**Run `curik init`** to install `.gitignore`",
    ))
    lines.append(check(
        s["has_workflow"],
        "GitHub Actions workflow installed",
        "**Run `curik init`** to install `.github/workflows/deploy-pages.yml`",
    ))

    lines.extend(["", "### Content", ""])

    lines.append(check(
        s["has_content"],
        f"{s['content_sections']} modules, {s['content_pages']} pages",
        "**No content found** — scaffold or create content before publishing",
    ))
    lines.append(check(
        s["hugo_builds"],
        "Hugo builds successfully",
        "**Hugo build fails** — fix build errors before publishing",
    ))
    if not s["hugo_builds"] and s.get("build_errors"):
        # Include first few lines of build error
        err_lines = s["build_errors"].strip().splitlines()[:5]
        for err in err_lines:
            lines.append(f"  > {err}")

    # Summarize readiness
    course_yml_ok = s["has_course_yml"] and len(s["course_yml_tbd_fields"]) == 0
    config_ready = all([
        course_yml_ok, s["has_hugo_toml"], s["base_url_ok"],
        s["has_theme"], s["has_gitignore"], s["has_workflow"],
    ])
    content_ready = s["has_content"] and s["hugo_builds"]
    all_ready = config_ready and content_ready

    lines.extend([
        "",
        f"### Status: {'READY TO PUBLISH' if all_ready else 'NOT READY'}",
        "",
    ])

    if not all_ready:
        lines.append("Fix the unchecked items above before publishing.")
        lines.append("")

    # ── GitHub setup ───────────────────────────────────────────
    lines.extend([
        "## GitHub Repo Setup (one-time, manual)",
        "",
        f"1. Push this repo to `https://github.com/{repo}`",
        "2. Go to **Settings → Pages**",
        "3. Under **Build and deployment → Source**, select **GitHub Actions**",
        "4. Push to `main` to trigger the first deploy",
        "",
        "## DNS (one-time, org-level)",
        "",
        "If not already configured:",
        "",
        "1. Add a CNAME record: `curriculum.jointheleague.org` → `league-curriculum.github.io`",
        "2. In the `league-curriculum` org GitHub settings, configure",
        "   `curriculum.jointheleague.org` as the verified custom domain",
        "",

        # ── Post-publish checklist ─────────────────────────────────
        "## Post-Publish Checklist",
        "",
        "After the first deploy, verify everything works:",
        "",
        f"- [ ] Site loads at {url}",
        "- [ ] All sidebar navigation links work",
        "- [ ] Images and code blocks render correctly",
        "- [ ] Previous/Next navigation works through all lessons",
        f"- [ ] GitHub repo link in footer points to `https://github.com/{repo}`",
    ])
    if s.get("tier") in (1, 2):
        lines.append("- [ ] Instructor guide toggle appears and works")

    lines.extend([
        "- [ ] Site works on mobile (sidebar collapses correctly)",
        f"- [ ] Course added to index at `league-curriculum/league-curriculum`",
        "",
        "## How Deployment Works",
        "",
        "1. You push to `main`",
        "2. GitHub Actions: checkout → Hugo build (minified) → upload → deploy",
        "3. Site is live at the target URL within ~60 seconds",
    ])

    return "\n".join(lines)


@mcp.tool()
def tool_check_publish_ready() -> str:
    """Check if this course is ready to publish to GitHub Pages.

    Returns a JSON object with pass/fail status for each requirement
    and an overall ready boolean. Use this for quick programmatic checks.
    """
    root = _root()
    s = _read_publish_state(root)
    has_slug = bool(s["slug"]) and s["slug"] != "TBD"

    course_yml_complete = s["has_course_yml"] and len(s["course_yml_tbd_fields"]) == 0

    checks = {
        "course_yml_exists": s["has_course_yml"],
        "course_yml_complete": course_yml_complete,
        "hugo_toml_exists": s["has_hugo_toml"],
        "base_url_configured": s["base_url_ok"],
        "theme_installed": s["has_theme"],
        "gitignore_installed": s["has_gitignore"],
        "workflow_installed": s["has_workflow"],
        "has_content": s["has_content"],
        "hugo_builds": s["hugo_builds"],
    }

    url = ""
    if has_slug:
        url = f"https://curriculum.jointheleague.org/{s['slug']}/"

    result: dict = {
        "ready": all(checks.values()),
        "checks": checks,
        "slug": s["slug"],
        "title": s["title"],
        "url": url,
        "content_sections": s["content_sections"],
        "content_pages": s["content_pages"],
    }

    if s["course_yml_tbd_fields"]:
        result["course_yml_tbd_fields"] = s["course_yml_tbd_fields"]

    return json.dumps(result, indent=2)


def run_server(root: Path) -> None:
    """Start the MCP server with the given project root."""
    global _project_root
    _project_root = root.resolve()
    mcp.run(transport="stdio")
