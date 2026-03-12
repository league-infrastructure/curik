"""UID generation utilities for course and unit identifiers."""

from __future__ import annotations

import secrets
import string
import uuid


def generate_course_uid() -> str:
    """Return a UUID4 string for course-level identity."""
    return str(uuid.uuid4())


def generate_unit_uid() -> str:
    """Return an 8-character base62 string for modules/lessons/exercises."""
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(8))
