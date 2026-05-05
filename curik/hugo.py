"""Hugo content page operations — list, create, update frontmatter, build."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

import yaml

from .paths import site_root, content_dir as content_dir_fn
from .project import CurikError


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split markdown text into (frontmatter_dict, body).

    Expects YAML frontmatter delimited by ``---``.
    Returns empty dict if no frontmatter found.
    """
    if not text.startswith("---"):
        return {}, text

    end = text.find("---", 3)
    if end == -1:
        return {}, text

    fm_text = text[3:end].strip()
    body = text[end + 3:].lstrip("\n")

    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        return {}, text

    if not isinstance(data, dict):
        return {}, text

    return data, body


def render_frontmatter(data: dict[str, Any]) -> str:
    """Serialize a dict to YAML frontmatter with ``---`` delimiters."""
    fm = yaml.dump(data, default_flow_style=False, sort_keys=False).rstrip()
    return f"---\n{fm}\n---\n"


def list_content_pages(
    root: Path, section: str | None = None
) -> list[dict[str, Any]]:
    """Walk ``content/`` and return page metadata from frontmatter.

    Each entry has: ``path`` (relative to root), ``title``, ``weight``,
    ``draft``.  Optional *section* limits to a subdirectory of ``content/``.
    """
    _content_dir = content_dir_fn(root)
    if not _content_dir.is_dir():
        return []

    search_dir = _content_dir / section if section else _content_dir
    if not search_dir.is_dir():
        return []

    pages: list[dict[str, Any]] = []
    for md_file in sorted(search_dir.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        pages.append({
            "path": str(md_file.relative_to(_content_dir)),
            "title": fm.get("title", ""),
            "weight": fm.get("weight", 0),
            "draft": fm.get("draft", False),
        })

    return pages


def create_content_page(
    root: Path,
    page_path: str,
    title: str,
    content: str = "",
    extra_frontmatter: dict[str, Any] | None = None,
) -> str:
    """Create a content page at ``content/<page_path>``.

    Returns the relative path of the created file.
    Raises CurikError if the file already exists or path escapes content/.
    """
    _content_dir = content_dir_fn(root).resolve()
    full_path = (_content_dir / page_path).resolve()

    # Prevent path traversal
    if not str(full_path).startswith(str(_content_dir)):
        raise CurikError(f"Path escapes content directory: {page_path}")

    if full_path.exists():
        raise CurikError(f"Page already exists: {page_path}")

    fm: dict[str, Any] = {"title": title}
    if extra_frontmatter:
        fm.update(extra_frontmatter)

    full_path.parent.mkdir(parents=True, exist_ok=True)
    text = render_frontmatter(fm) + "\n" + content
    full_path.write_text(text, encoding="utf-8")

    return str(full_path.relative_to(_content_dir))


def update_frontmatter(
    root: Path, page_path: str, updates: dict[str, Any]
) -> dict[str, Any]:
    """Merge *updates* into an existing page's YAML frontmatter.

    Returns the merged frontmatter dict. Body content is preserved.
    Raises CurikError if the file doesn't exist.
    """
    full_path = content_dir_fn(root) / page_path
    if not full_path.is_file():
        raise CurikError(f"Page not found: {page_path}")

    text = full_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    fm.update(updates)

    new_text = render_frontmatter(fm) + "\n" + body
    full_path.write_text(new_text, encoding="utf-8")

    return fm


def hugo_build(root: Path) -> dict[str, Any]:
    """Run ``hugo`` in the project root and return build results.

    Returns ``{success: bool, output: str, error: str}``.
    If Hugo is not installed, returns an actionable error message.
    """
    if not shutil.which("hugo"):
        return {
            "success": False,
            "output": "",
            "error": (
                "Hugo is not installed. Install it from https://gohugo.io/ "
                "or via your package manager (e.g., 'brew install hugo')."
            ),
        }

    build_dir = site_root(root)
    if not build_dir.is_dir():
        return {
            "success": False,
            "output": "",
            "error": (
                f"Hugo site directory not found: {build_dir}. "
                "Run 'curik hugo setup' first."
            ),
        }

    try:
        result = subprocess.run(
            ["hugo"],
            cwd=str(build_dir),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Hugo build timed out after 60 seconds.",
        }
