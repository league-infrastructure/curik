"""Change cycle and issue management for Curik projects."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from .project import CurikError, _course_dir


def _issues_dir(root: Path, status: str) -> Path:
    if status == "open":
        return _course_dir(root) / "issues" / "open"
    elif status == "done":
        return _course_dir(root) / "issues" / "done"
    raise CurikError(f"Unknown issue status directory: {status}")


def _plans_dir(root: Path, status: str) -> Path:
    if status == "active":
        return _course_dir(root) / "change-plan" / "active"
    elif status == "done":
        return _course_dir(root) / "change-plan" / "done"
    raise CurikError(f"Unknown plan status directory: {status}")


def _next_number(directory: Path) -> int:
    """Find the next available number from .md files in a directory."""
    existing = []
    if directory.is_dir():
        for f in directory.iterdir():
            if f.suffix == ".md":
                m = re.match(r"^(\d+)", f.stem)
                if m:
                    existing.append(int(m.group(1)))
    return max(existing, default=0) + 1


def _next_number_across(dirs: list[Path]) -> int:
    """Find the next available number across multiple directories."""
    existing = []
    for directory in dirs:
        if directory.is_dir():
            for f in directory.iterdir():
                if f.suffix == ".md":
                    m = re.match(r"^(\d+)", f.stem)
                    if m:
                        existing.append(int(m.group(1)))
    return max(existing, default=0) + 1


def _slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:50]


def _write_frontmatter_doc(path: Path, frontmatter: dict, body: str = "") -> None:
    lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    if body:
        lines.append("")
        lines.append(body)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter from a markdown file. Returns (frontmatter_dict, body)."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise CurikError(f"No frontmatter found in {path}")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise CurikError(f"Invalid frontmatter in {path}")
    fm_text = parts[1].strip()
    body = parts[2].strip()

    fm: dict = {}
    current_key = None
    current_list: list | None = None
    for line in fm_text.splitlines():
        list_match = re.match(r"^\s+-\s+(.+)$", line)
        if list_match and current_key:
            if current_list is None:
                current_list = []
            val = list_match.group(1).strip()
            # Try to convert to int
            try:
                val = int(val)
            except (ValueError, TypeError):
                pass
            current_list.append(val)
            fm[current_key] = current_list
            continue

        kv_match = re.match(r"^(\w+):\s*(.*)$", line)
        if kv_match:
            current_key = kv_match.group(1)
            value = kv_match.group(2).strip()
            current_list = None
            if value:
                fm[current_key] = value
            else:
                fm[current_key] = []
                current_list = []

    return fm, body


def _update_frontmatter_field(path: Path, key: str, value: str) -> None:
    """Update a single field in the frontmatter of a file."""
    fm, body = _parse_frontmatter(path)
    fm[key] = value
    _write_frontmatter_doc(path, fm, body)


def _find_plan(root: Path, plan_number: int) -> Path:
    """Find a change plan by number in the active directory."""
    active_dir = _plans_dir(root, "active")
    if active_dir.is_dir():
        for f in active_dir.iterdir():
            if f.suffix == ".md":
                m = re.match(r"^(\d+)", f.stem)
                if m and int(m.group(1)) == plan_number:
                    return f
    raise CurikError(f"Change plan #{plan_number} not found in active plans.")


# --- Public API ---


def create_issue(root: Path, title: str, content: str) -> dict:
    """Create a numbered issue file in CURIK_DIR/issues/open/."""
    root = root.resolve()
    open_dir = _issues_dir(root, "open")
    done_dir = _issues_dir(root, "done")
    if not open_dir.is_dir():
        raise CurikError("Course not initialized. Run 'curik init'.")

    number = _next_number_across([open_dir, done_dir])
    slug = _slugify(title)
    filename = f"{number:03d}-{slug}.md"
    path = open_dir / filename

    fm = {
        "title": title,
        "status": "open",
        "created": str(date.today()),
    }
    _write_frontmatter_doc(path, fm, content)

    return {"path": str(path), "number": number}


def list_issues(root: Path, status: str = "open") -> list[dict]:
    """List issues from the open/ or done/ directory."""
    root = root.resolve()
    directory = _issues_dir(root, status)
    if not directory.is_dir():
        return []

    results = []
    for f in sorted(directory.iterdir()):
        if f.suffix != ".md":
            continue
        m = re.match(r"^(\d+)", f.stem)
        if not m:
            continue
        fm, _ = _parse_frontmatter(f)
        results.append({
            "number": int(m.group(1)),
            "title": fm.get("title", ""),
            "status": fm.get("status", status),
            "path": str(f),
        })
    return results


def create_change_plan(root: Path, title: str, issue_numbers: list[int]) -> dict:
    """Create a numbered change plan in CURIK_DIR/change-plan/active/."""
    root = root.resolve()
    active_dir = _plans_dir(root, "active")
    done_dir = _plans_dir(root, "done")
    if not active_dir.is_dir():
        raise CurikError("Course not initialized. Run 'curik init'.")

    number = _next_number_across([active_dir, done_dir])
    slug = _slugify(title)
    filename = f"{number:03d}-{slug}.md"
    path = active_dir / filename

    fm = {
        "title": title,
        "status": "draft",
        "issues": issue_numbers,
    }
    _write_frontmatter_doc(path, fm)

    return {"path": str(path), "number": number}


def approve_change_plan(root: Path, plan_number: int) -> dict:
    """Set a change plan's status to 'approved'. Must be in 'draft' status."""
    root = root.resolve()
    path = _find_plan(root, plan_number)
    fm, _ = _parse_frontmatter(path)

    if fm.get("status") != "draft":
        raise CurikError(
            f"Cannot approve plan #{plan_number}: status is '{fm.get('status')}', expected 'draft'."
        )

    _update_frontmatter_field(path, "status", "approved")
    return {"path": str(path), "status": "approved"}


def execute_change_plan(root: Path, plan_number: int) -> dict:
    """Set a change plan's status to 'executed'. Must be in 'approved' status."""
    root = root.resolve()
    path = _find_plan(root, plan_number)
    fm, _ = _parse_frontmatter(path)

    if fm.get("status") != "approved":
        raise CurikError(
            f"Cannot execute plan #{plan_number}: status is '{fm.get('status')}', expected 'approved'."
        )

    _update_frontmatter_field(path, "status", "executed")
    return {"path": str(path), "status": "executed"}


def review_change_plan(root: Path, plan_number: int, gaps: list[str]) -> dict:
    """Set status to 'reviewed'. If gaps is non-empty, create new issues for each gap."""
    root = root.resolve()
    path = _find_plan(root, plan_number)
    fm, _ = _parse_frontmatter(path)

    if fm.get("status") != "executed":
        raise CurikError(
            f"Cannot review plan #{plan_number}: status is '{fm.get('status')}', expected 'executed'."
        )

    _update_frontmatter_field(path, "status", "reviewed")

    new_issues = []
    for gap in gaps:
        result = create_issue(root, gap, f"Gap identified during review of change plan #{plan_number}.")
        new_issues.append(result)

    return {"path": str(path), "new_issues": new_issues}


def close_change_plan(root: Path, plan_number: int) -> dict:
    """Move plan to done/, move referenced resolved issues to done/. Set status to 'closed'."""
    root = root.resolve()
    path = _find_plan(root, plan_number)
    fm, body = _parse_frontmatter(path)

    if fm.get("status") != "reviewed":
        raise CurikError(
            f"Cannot close plan #{plan_number}: status is '{fm.get('status')}', expected 'reviewed'."
        )

    # Update status to closed
    fm["status"] = "closed"

    # Move plan to done directory
    done_dir = _plans_dir(root, "done")
    new_plan_path = done_dir / path.name
    _write_frontmatter_doc(new_plan_path, fm, body)
    path.unlink()

    # Move referenced issues to done
    issue_numbers = fm.get("issues", [])
    if isinstance(issue_numbers, str):
        issue_numbers = [int(x.strip()) for x in issue_numbers.split(",") if x.strip()]

    open_dir = _issues_dir(root, "open")
    issues_done_dir = _issues_dir(root, "done")
    moved_issues = []

    for issue_num in issue_numbers:
        if not open_dir.is_dir():
            continue
        for f in open_dir.iterdir():
            if f.suffix != ".md":
                continue
            m = re.match(r"^(\d+)", f.stem)
            if m and int(m.group(1)) == issue_num:
                issue_fm, issue_body = _parse_frontmatter(f)
                issue_fm["status"] = "done"
                dest = issues_done_dir / f.name
                _write_frontmatter_doc(dest, issue_fm, issue_body)
                f.unlink()
                moved_issues.append(issue_num)
                break

    return {
        "path": str(new_plan_path),
        "status": "closed",
        "moved_issues": moved_issues,
    }
