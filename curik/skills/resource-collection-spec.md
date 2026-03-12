---
name: resource-collection-spec
description: Abbreviated Phase 1 workflow for resource collection projects
---

# Resource Collection Spec

Resource collections are sets of reference pages, activity descriptions, and
supporting materials rather than sequential lesson plans. They follow an
abbreviated Phase 1 process that skips the pedagogical model and alignment
decision sub-phases, since those concepts do not apply to reference material.

## Required Sections (5)

Resource collections require only these five spec sections to advance to
Phase 2:

1. **course-concept** — What the collection covers, target audience, and goals
2. **research-summary** — Research findings that inform the collection content
3. **course-structure-outline** — How the resources are organized (categories,
   topics, navigation structure)
4. **assessment-plan** — How usage or comprehension is assessed, if applicable
5. **technical-decisions** — Technology choices, hosting, format decisions

## Skipped Sections

The following sections are **not required** for resource collections:

- **pedagogical-model** — Resource collections are not sequential instructional
  material, so pedagogical model selection does not apply.
- **alignment-decision** — Resource collections typically do not align to
  specific standards frameworks.

## Workflow

1. Initialize the project with `course_type="resource-collection"`:
   ```
   init_course(root, course_type="resource-collection")
   ```
2. Fill in the five required spec sections using `update_spec()`.
3. Advance to Phase 2 with `advance_phase(root, "phase2")` — the gate check
   will only require the five sections listed above.
4. Scaffold the resource directory structure with:
   ```
   scaffold_structure(root, structure, course_type="resource-collection")
   ```
   This creates directories under `resources/` instead of at the project root.

## Output

A resource collection project ready for Phase 2 content authoring, with the
abbreviated spec complete and the `resources/` directory tree in place.
