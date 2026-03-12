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
    generate_nav,
    get_outline,
    scaffold_structure,
)
from .uid import generate_course_uid, generate_unit_uid

__all__ = [
    "CurikError",
    "advance_phase",
    "approve_outline",
    "create_lesson_stub",
    "create_outline",
    "generate_change_plan",
    "generate_course_uid",
    "generate_nav",
    "generate_unit_uid",
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
