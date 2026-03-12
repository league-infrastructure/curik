"""Curik package."""

from .project import (
    CurikError,
    advance_phase,
    get_course_status,
    get_phase,
    get_spec,
    init_course,
    record_alignment,
    record_course_concept,
    record_pedagogical_model,
    update_spec,
)
from .scaffolding import (
    approve_outline,
    create_lesson_stub,
    create_outline,
    generate_change_plan,
    get_outline,
    scaffold_structure,
)

__all__ = [
    "CurikError",
    "advance_phase",
    "approve_outline",
    "create_lesson_stub",
    "create_outline",
    "generate_change_plan",
    "get_course_status",
    "get_outline",
    "get_phase",
    "get_spec",
    "init_course",
    "record_alignment",
    "record_course_concept",
    "record_pedagogical_model",
    "scaffold_structure",
    "update_spec",
]
