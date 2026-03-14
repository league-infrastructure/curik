"""Implementation of Curik's init-time file installation.

Installs CLAUDE.md (with inline Curik section), a /curik skill stub,
VS Code MCP config, and MCP permissions into a target repository.
Follows the same pattern as CLASI's init_command.py.
"""

from __future__ import annotations

import importlib.resources
import json
from pathlib import Path

_SECTION_START = "<!-- CURIK:START -->"
_SECTION_END = "<!-- CURIK:END -->"

MCP_CONFIG = {
    "curik": {
        "command": "curik",
        "args": ["mcp"],
    }
}

VSCODE_MCP_CONFIG = {
    "curik": {
        "type": "stdio",
        "command": "curik",
        "args": ["mcp"],
    }
}


def _read_template(name: str) -> str:
    """Read a template file from the curik.init package."""
    ref = importlib.resources.files("curik.init").joinpath(name)
    return ref.read_text(encoding="utf-8")


def _update_claude_md(target: Path) -> str:
    """Create or update CLAUDE.md with the Curik section.

    Returns "created", "updated", or "unchanged".
    """
    claude_md = target / "CLAUDE.md"
    section = _read_template("claude-section.md").rstrip()

    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")

        if _SECTION_START in content and _SECTION_END in content:
            start_idx = content.index(_SECTION_START)
            end_idx = content.index(_SECTION_END) + len(_SECTION_END)
            new_content = content[:start_idx] + section + content[end_idx:]
        else:
            if not content.endswith("\n"):
                content += "\n"
            new_content = content + "\n" + section + "\n"

        if new_content == content:
            return "unchanged"

        claude_md.write_text(new_content, encoding="utf-8")
        return "updated"
    else:
        claude_md.write_text(section + "\n", encoding="utf-8")
        return "created"


def _write_curik_skill(target: Path) -> str:
    """Write the /curik skill stub to .claude/skills/curik/SKILL.md.

    Returns "created", "updated", or "unchanged".
    """
    source = _read_template("curik-skill.md")
    path = target / ".claude" / "skills" / "curik" / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        if path.read_text(encoding="utf-8") == source:
            return "unchanged"
        path.write_text(source, encoding="utf-8")
        return "updated"

    path.write_text(source, encoding="utf-8")
    return "created"


def _update_vscode_mcp_json(target: Path) -> str:
    """Merge curik server config into .vscode/mcp.json.

    Returns "created", "updated", or "unchanged".
    """
    vscode_dir = target / ".vscode"
    mcp_json_path = vscode_dir / "mcp.json"

    if mcp_json_path.exists():
        try:
            data = json.loads(mcp_json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            data = {}
    else:
        data = {}

    servers = data.setdefault("servers", {})

    if servers.get("curik") == VSCODE_MCP_CONFIG["curik"]:
        return "unchanged"

    vscode_dir.mkdir(parents=True, exist_ok=True)
    servers["curik"] = VSCODE_MCP_CONFIG["curik"]
    mcp_json_path.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    return "created" if len(servers) == 1 and len(data) == 1 else "updated"


_GITIGNORE_START = "# -- CURIK:START --"
_GITIGNORE_END = "# -- CURIK:END --"


def _write_gitignore(target: Path) -> str:
    """Create or update .gitignore with the Curik-managed section.

    Uses markers so user-added entries outside the markers are preserved.
    Returns "created", "updated", or "unchanged".
    """
    gitignore = target / ".gitignore"
    section = _read_template("gitignore").rstrip()

    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8")

        if _GITIGNORE_START in content and _GITIGNORE_END in content:
            start_idx = content.index(_GITIGNORE_START)
            end_idx = content.index(_GITIGNORE_END) + len(_GITIGNORE_END)
            new_content = content[:start_idx] + section + content[end_idx:]
        else:
            # Existing .gitignore without markers — prepend the managed section
            new_content = section + "\n\n" + content

        if new_content == content:
            return "unchanged"

        gitignore.write_text(new_content, encoding="utf-8")
        return "updated"
    else:
        gitignore.write_text(section + "\n", encoding="utf-8")
        return "created"


def _write_github_workflow(target: Path) -> str:
    """Create or update .github/workflows/deploy-pages.yml.

    This file is fully curik-owned — updates replace the entire file.
    Returns "created", "updated", or "unchanged".
    """
    source = _read_template("deploy-pages.yml")
    workflow = target / ".github" / "workflows" / "deploy-pages.yml"

    if workflow.exists():
        if workflow.read_text(encoding="utf-8") == source:
            return "unchanged"
        workflow.write_text(source, encoding="utf-8")
        return "updated"

    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text(source, encoding="utf-8")
    return "created"


def _update_settings_json(target: Path) -> str:
    """Add mcp__curik__* to the permissions allowlist.

    Returns "created", "updated", or "unchanged".
    """
    settings_path = target / ".claude" / "settings.local.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    if settings_path.exists():
        try:
            data = json.loads(settings_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            data = {}
    else:
        data = {}

    permissions = data.setdefault("permissions", {})
    allow = permissions.setdefault("allow", [])

    target_perm = "mcp__curik__*"
    if target_perm in allow:
        return "unchanged"

    allow.append(target_perm)
    settings_path.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    return "created" if len(allow) == 1 and len(data) == 1 else "updated"


def run_init(target: Path) -> dict[str, list[str]]:
    """Install Curik's CLAUDE.md section, skill, and MCP permissions.

    Returns dict with "created", "updated", and "unchanged" file lists.
    """
    result: dict[str, list[str]] = {
        "created": [],
        "updated": [],
        "unchanged": [],
    }

    actions = [
        ("CLAUDE.md", _update_claude_md(target)),
        (".claude/skills/curik/SKILL.md", _write_curik_skill(target)),
        (".vscode/mcp.json", _update_vscode_mcp_json(target)),
        (".claude/settings.local.json", _update_settings_json(target)),
        (".gitignore", _write_gitignore(target)),
        (".github/workflows/deploy-pages.yml", _write_github_workflow(target)),
    ]

    for path, status in actions:
        result[status].append(path)

    return result
