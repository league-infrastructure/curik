"""Persist and retrieve structured research findings."""

from __future__ import annotations

import json
from pathlib import Path

from .project import CurikError, _course_dir


def _research_dir(root: Path) -> Path:
    d = _course_dir(root) / "research"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _next_number(directory: Path) -> int:
    existing = [
        int(f.stem.split("-")[0])
        for f in directory.iterdir()
        if f.suffix == ".md" and f.stem.split("-")[0].isdigit()
    ]
    return max(existing, default=0) + 1


def save_research_findings(root: Path, title: str, content: str) -> dict[str, str]:
    """Save a numbered research finding to CURIK_DIR/research/."""
    root = root.resolve()
    if not (_course_dir(root) / "state.json").exists():
        raise CurikError("Course not initialized. Run 'curik init'.")
    if not content or not content.strip():
        raise CurikError("Research content cannot be empty.")

    research = _research_dir(root)
    num = _next_number(research)
    slug = title.lower().replace(" ", "-")[:40]
    filename = f"{num:03d}-{slug}.md"
    filepath = research / filename

    doc = f"---\ntitle: {title}\nnumber: {num}\n---\n\n{content.strip()}\n"
    filepath.write_text(doc, encoding="utf-8")
    return {"path": str(filepath), "number": num}


def get_research_findings(root: Path) -> list[dict[str, str]]:
    """Return all research findings as a list of {number, title, path}."""
    root = root.resolve()
    if not (_course_dir(root) / "state.json").exists():
        raise CurikError("Course not initialized. Run 'curik init'.")

    research = _research_dir(root)
    findings = []
    for f in sorted(research.iterdir()):
        if f.suffix != ".md":
            continue
        text = f.read_text(encoding="utf-8")
        title = ""
        for line in text.splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
                break
        findings.append({"number": f.stem.split("-")[0], "title": title, "path": str(f)})
    return findings
