---
name: spec-synthesis
description: Assembling the complete course specification from prior phase outputs
---

# Spec Synthesis Skill (Phase 1e)

Assemble the full course specification from all prior sub-phase outputs.
This is the final Phase 1 step before advancing to Phase 2.

## Required Spec Sections

All must be present and non-placeholder before `advance_phase("phase2")`
will succeed:

1. **Course Concept** (from Phase 1a) — already recorded
2. **Pedagogical Model** (from Phase 1b) — already recorded
3. **Research Summary** (from Phase 1c) — synthesize from research findings
4. **Alignment Decision** (from Phase 1d) — already recorded
5. **Course Structure Outline** — NEW, assembled in this phase
6. **Assessment Plan** — NEW, assembled in this phase
7. **Technical Decisions** — NEW, assembled in this phase

## Course Structure Outline

Varies by pedagogical structure:
- **Sequential Lessons**: modules and lessons with title, topics, objectives
- **Activity courses**: activities with materials, timing, instructions
- **Challenge-Based**: challenges with problem summaries, objectives, difficulty
- **Progressive Project**: modules with concepts, sessions, what gets built
- **Hybrid**: combination with clear labeling

This is an outline, not content. Lesson pages are produced in Phase 2.

## Assessment Plan

- Quiz structure (if applicable)
- Project milestones
- Progress tracking approach
- How completion is measured

## Technical Decisions

- Tier (1-4)
- Delivery format
- Platform (MkDocs, Codespaces, Code Server, external)
- Content format (Markdown, notebooks, both)
- Lesson format (sequential, challenge, project, hybrid)
- Special requirements (hardware, accounts, software)

## Process

1. Read all existing spec sections
2. Draft Course Structure Outline from concept + pedagogical model + alignment
3. Draft Assessment Plan from pedagogical model + learning outcomes
4. Draft Technical Decisions from all prior phases
5. Use `update_spec` for each new section
6. Review the complete spec with the designer
7. When approved, call `advance_phase("phase2")`
