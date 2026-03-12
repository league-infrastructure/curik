"""Quiz authoring tools — stub generation, alignment, and status management."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from .project import CurikError

DEFAULT_QUESTION_TYPES = [
    "multiple-choice",
    "short-answer",
    "true-false",
    "fill-in-the-blank",
]


def generate_quiz_stub(root: Path, lesson_id: str, topics: list[str]) -> dict:
    """Create a quiz.yml stub for a lesson with pre-filled topics.

    Returns {"path": <str>}.
    """
    root = root.resolve()
    quiz_dir = root / "quizzes"
    quiz_dir.mkdir(parents=True, exist_ok=True)

    quiz_path = quiz_dir / f"{lesson_id}-quiz.yml"
    quiz_data = {
        "lesson_id": lesson_id,
        "status": "drafted",
        "difficulty": "beginner",
        "question_types": DEFAULT_QUESTION_TYPES,
        "topics": topics,
        "questions": [],
    }
    quiz_path.write_text(
        yaml.dump(quiz_data, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )
    return {"path": str(quiz_path)}


def _extract_lesson_objectives(text: str) -> list[str]:
    """Extract learning objectives from lesson markdown text."""
    # Remove instructor guide block
    text_no_guide = re.sub(
        r'<div\s+class=["\']instructor-guide["\']\s*>.*?</div>',
        "",
        text,
        flags=re.DOTALL,
    )
    # Find the learning objectives section
    m = re.search(
        r'(?i)#+\s*learning\s+objectives?\s*\n(.*?)(?=\n#+\s|\Z)',
        text_no_guide,
        re.DOTALL,
    )
    if not m:
        return []
    block = m.group(1)
    objectives = []
    for line in block.splitlines():
        line = line.strip()
        # Match list items: - item or * item or 1. item
        lm = re.match(r'^[-*]\s+(.+)$', line) or re.match(r'^\d+\.\s+(.+)$', line)
        if lm:
            objectives.append(lm.group(1).strip())
    return objectives


def validate_quiz_alignment(root: Path, lesson_path: str, quiz_path: str) -> dict:
    """Check that each lesson objective has at least one quiz topic covering it.

    Returns {"aligned": bool, "uncovered_objectives": [str]}.
    """
    root = root.resolve()
    lesson_file = root / lesson_path
    quiz_file = root / quiz_path

    if not lesson_file.exists():
        raise CurikError(f"Lesson file not found: {lesson_path}")
    if not quiz_file.exists():
        raise CurikError(f"Quiz file not found: {quiz_path}")

    lesson_text = lesson_file.read_text(encoding="utf-8")
    objectives = _extract_lesson_objectives(lesson_text)

    quiz_data = yaml.safe_load(quiz_file.read_text(encoding="utf-8"))
    topics = [t.lower() for t in (quiz_data.get("topics") or [])]

    uncovered: list[str] = []
    for obj in objectives:
        obj_lower = obj.lower()
        # Check if any topic word appears in the objective or vice versa
        covered = any(
            topic in obj_lower or obj_lower in topic
            for topic in topics
        )
        if not covered:
            uncovered.append(obj)

    return {
        "aligned": len(uncovered) == 0,
        "uncovered_objectives": uncovered,
    }


VALID_STATUSES = {"drafted", "reviewed", "complete"}


def set_quiz_status(root: Path, quiz_path: str, status: str) -> dict:
    """Update the status field in a quiz.yml file.

    Valid statuses: drafted, reviewed, complete.
    """
    if status not in VALID_STATUSES:
        raise CurikError(
            f"Invalid quiz status '{status}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}"
        )
    root = root.resolve()
    full_path = root / quiz_path
    if not full_path.exists():
        raise CurikError(f"Quiz file not found: {quiz_path}")

    quiz_data = yaml.safe_load(full_path.read_text(encoding="utf-8"))
    quiz_data["status"] = status
    full_path.write_text(
        yaml.dump(quiz_data, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )
    return {"path": str(full_path), "status": status}
