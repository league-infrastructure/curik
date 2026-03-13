---
name: validation-checklist
description: Defines what "complete" looks like at lesson, module, and course level
---

# Validation Checklist

Use this checklist to determine completeness at each level of the
curriculum hierarchy.

## Lesson Level

A lesson is **complete** when all of the following are true:

- [ ] File exists as a `.md` file in its module directory
- [ ] Contains an instructor guide shortcode (`{{< instructor-guide >}}`)
- [ ] Instructor guide has all 7 required fields, each non-empty:
  1. **Objectives** — what the lesson aims to teach
  2. **Materials** — supplies, software, or resources needed
  3. **Timing** — suggested time allocation for sections
  4. **Key concepts** — the core ideas students must grasp
  5. **Common mistakes** — frequent errors and how to address them
  6. **Assessment cues** — signals that a student has understood
  7. **Differentiation** — adaptations for different skill levels
- [ ] Has a Learning Objectives section outside the instructor guide
- [ ] Learning objectives are specific and observable (not "understand X")

## Module Level

A module is **complete** when:

- [ ] Module directory exists under `modules/`
- [ ] Contains `README.md` or `overview.md` with module description
- [ ] All `.md` lesson files in the directory pass lesson-level validation
- [ ] Lessons are ordered logically (numbered or sequenced)

## Course Level

A course is **complete** when:

- [ ] `course.yml` exists at the project root
- [ ] No field in `course.yml` has the value `TBD`
- [ ] All required fields are populated: title, slug, tier, grades,
  category, topics, prerequisites, lessons, estimated_weeks,
  curriculum_url, repo_url, description
- [ ] All module directories pass module-level validation

## Running Validation

Use these MCP tools to check completeness:

- `validate_lesson(root, lesson_path)` — check a single lesson
- `validate_module(root, module_path)` — check a module and its lessons
- `validate_course(root)` — check the entire course
- `save_validation_report(root, report)` — persist results
- `get_validation_report(root)` — retrieve the last report
