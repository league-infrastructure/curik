"""Load bundled agent definitions, skill files, and instruction docs from the package."""

from __future__ import annotations

import importlib.resources

from .project import CurikError


def _read_asset(package: str, name: str) -> str:
    """Read a markdown file from a subpackage."""
    filename = f"{name}.md"
    try:
        ref = importlib.resources.files(package).joinpath(filename)
        return ref.read_text(encoding="utf-8")
    except (FileNotFoundError, TypeError):
        raise CurikError(f"Asset not found: {package}/{filename}")


def get_agent_definition(name: str) -> str:
    """Return the markdown content of a named agent definition."""
    return _read_asset("curik.agents", name)


def get_skill_definition(name: str) -> str:
    """Return the markdown content of a named skill definition."""
    return _read_asset("curik.skills", name)


def list_agents() -> list[str]:
    """Return names of all bundled agent definitions."""
    agents_dir = importlib.resources.files("curik.agents")
    return sorted(
        f.name.removesuffix(".md")
        for f in agents_dir.iterdir()
        if f.name.endswith(".md")
    )


def list_skills() -> list[str]:
    """Return names of all bundled skill definitions."""
    skills_dir = importlib.resources.files("curik.skills")
    return sorted(
        f.name.removesuffix(".md")
        for f in skills_dir.iterdir()
        if f.name.endswith(".md")
    )


# -- Instructions (formerly "references") --


def get_instruction(name: str) -> str:
    """Return the markdown content of a named instruction document."""
    return _read_asset("curik.references", name)


def list_instructions() -> list[str]:
    """Return names of all bundled instruction documents."""
    refs_dir = importlib.resources.files("curik.references")
    return sorted(
        f.name.removesuffix(".md")
        for f in refs_dir.iterdir()
        if f.name.endswith(".md")
    )


# Backward-compatible aliases
get_reference = get_instruction
list_references = list_instructions


# -- Process guide --


def get_process_guide() -> str:
    """Return the full curriculum development process guide."""
    return _read_asset("curik.references", "process-guide")


# -- Activity guide --


# Maps activity name → (agent, [skills], [instructions])
ACTIVITY_MAPPINGS: dict[str, tuple[str, list[str], list[str]]] = {
    "spec-development": (
        "curriculum-architect",
        ["course-concept", "pedagogical-model", "alignment-decision", "spec-synthesis"],
        ["curriculum-process", "course-taxonomy"],
    ),
    "research": (
        "research-agent",
        [],
        ["curriculum-process"],
    ),
    "content-analysis": (
        "curriculum-architect",
        ["existing-content-analysis"],
        ["curriculum-process", "course-taxonomy"],
    ),
    "scaffolding": (
        "curriculum-architect",
        ["repo-scaffolding", "structure-proposal", "syllabus-integration"],
        ["hugo-conventions"],
    ),
    "lesson-writing-young": (
        "lesson-author-young",
        ["lesson-writing-young", "instructor-guide-sections"],
        ["lesson-page-template", "instructor-guide-requirements", "course-taxonomy"],
    ),
    "lesson-writing-older": (
        "lesson-author-older",
        ["lesson-writing-older", "instructor-guide-sections", "readme-guards"],
        ["lesson-page-template", "instructor-guide-requirements", "hugo-conventions"],
    ),
    "quiz-authoring": (
        "quiz-author",
        ["quiz-authoring"],
        ["curriculum-process"],
    ),
    "content-conversion": (
        "lesson-author-older",
        ["content-conversion", "instructor-guide-sections"],
        ["lesson-page-template", "hugo-conventions"],
    ),
    "change-management": (
        "curriculum-architect",
        ["status-tracking", "change-plan-execution"],
        ["curriculum-process"],
    ),
    "validation": (
        "reviewer",
        ["validation-checklist", "syllabus-integration"],
        ["hugo-conventions", "instructor-guide-requirements"],
    ),
}


def get_activity_guide(activity: str) -> str:
    """Return a composite document bundling agent + skills + instructions for an activity.

    Raises CurikError if the activity name is unknown.
    Missing skill or instruction files are noted with a placeholder.
    """
    if activity not in ACTIVITY_MAPPINGS:
        valid = ", ".join(sorted(ACTIVITY_MAPPINGS))
        raise CurikError(
            f"Unknown activity: {activity!r}. Valid activities: {valid}"
        )

    agent_name, skill_names, instruction_names = ACTIVITY_MAPPINGS[activity]

    sections: list[str] = []
    sections.append(f"# Activity Guide: {activity}\n")

    # Agent
    sections.append("## Agent\n")
    try:
        sections.append(get_agent_definition(agent_name))
    except CurikError:
        sections.append(f"*Agent `{agent_name}` not found.*\n")

    # Skills
    if skill_names:
        sections.append("## Skills\n")
        for skill_name in skill_names:
            try:
                sections.append(f"### Skill: {skill_name}\n")
                sections.append(get_skill_definition(skill_name))
            except CurikError:
                sections.append(f"*Skill `{skill_name}` not yet written.*\n")

    # Instructions
    if instruction_names:
        sections.append("## Instructions\n")
        for instr_name in instruction_names:
            try:
                sections.append(f"### Instruction: {instr_name}\n")
                sections.append(get_instruction(instr_name))
            except CurikError:
                sections.append(f"*Instruction `{instr_name}` not yet written.*\n")

    return "\n".join(sections)
