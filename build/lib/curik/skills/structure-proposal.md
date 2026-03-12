---
name: structure-proposal
description: Creating a concrete module/lesson skeleton from an approved spec
---

# Structure Proposal Skill

Convert an approved specification into a concrete module and lesson skeleton.
This is the bridge between Phase 1 (spec) and Phase 2 (scaffolding).

## Process

1. Read the complete spec, focusing on:
   - Course Structure Outline (section 5)
   - Pedagogical Model (section 2)
   - Technical Decisions (section 7)

2. Propose a directory structure:
   - For sequential/progressive: modules with numbered lessons
   - For challenge-based: challenge sets with numbered challenges
   - For activity: activity groups with numbered activities

3. For each lesson/challenge/activity, list:
   - Title
   - Brief description (1-2 sentences)
   - Key topics covered
   - Estimated duration

4. Present the structure to the designer for approval

5. When approved, this becomes the initial change plan that triggers
   Phase 2 scaffolding

## Naming Conventions

- Modules: `01-module-name/`, `02-module-name/`
- Lessons: `01-lesson-name.md`, `02-lesson-name.md`
- Exercises: `01-lesson-name-exercises.py` or `01-lesson-name-exercises.ipynb`
- Challenges: `01-challenge-name.md`

## Output

A change plan document listing every module, lesson, and stub description,
ready for scaffolding in Phase 2.
