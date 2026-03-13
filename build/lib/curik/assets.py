"""Load bundled agent definitions, skill files, and reference docs from the package."""

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


def get_reference(name: str) -> str:
    """Return the markdown content of a named reference document."""
    return _read_asset("curik.references", name)


def list_references() -> list[str]:
    """Return names of all bundled reference documents."""
    refs_dir = importlib.resources.files("curik.references")
    return sorted(
        f.name.removesuffix(".md")
        for f in refs_dir.iterdir()
        if f.name.endswith(".md")
    )
