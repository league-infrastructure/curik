"""README generation from MkDocs comment guards."""

from __future__ import annotations

import re
from pathlib import Path

from .project import CurikError

_SHARED_RE = re.compile(
    r"<!-- readme-shared -->\s*\n(.*?)<!-- /readme-shared -->",
    re.DOTALL,
)
_ONLY_RE = re.compile(
    r"<!-- readme-only -->\s*\n(.*?)<!-- /readme-only -->",
    re.DOTALL,
)


def parse_guards(content: str) -> dict[str, list[str]]:
    """Parse <!-- readme-shared --> and <!-- readme-only --> guards from markdown.

    Returns {"shared": [...sections...], "only": [...sections...]}.
    """
    shared = [m.group(1).strip() for m in _SHARED_RE.finditer(content)]
    only = [m.group(1).strip() for m in _ONLY_RE.finditer(content)]
    return {"shared": shared, "only": only}


def generate_readme(content: str) -> str | None:
    """Generate README content from guarded sections. Returns None if no guards found."""
    guards = parse_guards(content)
    if not guards["shared"] and not guards["only"]:
        return None
    parts = guards["shared"] + guards["only"]
    return "\n\n".join(parts).strip() + "\n"


def generate_readmes(root: Path, docs_dir: str = "docs/docs") -> dict:
    """Generate READMEs for all lessons in docs_dir that have guards.

    Writes README.md files to corresponding paths under root/lessons/.
    Returns {"generated": [...paths...], "skipped": [...paths...]}.
    """
    source = root / docs_dir
    if not source.is_dir():
        raise CurikError(f"Docs directory not found: {source}")

    generated: list[str] = []
    skipped: list[str] = []

    for md_file in sorted(source.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        readme_content = generate_readme(content)

        rel = md_file.relative_to(source)

        if readme_content is None:
            skipped.append(str(rel))
            continue

        # Map docs/docs/module/lesson.md -> lessons/module/lesson/README.md
        # The lesson dir is the stem of the md file
        lesson_dir = root / "lessons" / rel.parent / rel.stem
        lesson_dir.mkdir(parents=True, exist_ok=True)
        readme_path = lesson_dir / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")
        generated.append(str(readme_path.relative_to(root)))

    return {"generated": generated, "skipped": skipped}
