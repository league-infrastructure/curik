---
name: spec-synthesis
description: Assembling the complete course specification from prior phase outputs
---

# Spec Synthesis Skill (Phase 1e)

Assemble the full course specification from all prior sub-phase outputs.
This is the final Phase 1 step before advancing to Phase 2.

## Opening

Show the section checklist:

```
---

## Phase 1e: Spec Synthesis

### Specification Sections

| # | Section | Status | Source |
|---|---------|--------|--------|
| 1 | Course Concept | Done | Phase 1a |
| 2 | Pedagogical Model | Done | Phase 1b |
| 3 | Research Summary | Done | Phase 1c |
| 4 | Alignment Decision | Done | Phase 1d |
| 5 | Course Structure Outline | **To draft** | This phase |
| 6 | Assessment Plan | **To draft** | This phase |
| 7 | Technical Decisions | **To draft** | This phase |

I need to draft sections 5-7 based on everything we've decided so far.

---
```

## Section 5: Course Structure Outline

Draft the outline based on pedagogical model and alignment. Present it
in the appropriate format:

### For Sequential Lessons / Progressive Project:

```
---

### Proposed Course Structure

| Module | Lessons | Topics | Sessions |
|--------|---------|--------|----------|
| **Module 1: Getting Started** | | | |
| | 01 - Hello Python | Variables, print, input | 1 |
| | 02 - Data Types | Strings, ints, floats, type conversion | 1 |
| **Module 2: Control Flow** | | | |
| | 03 - Decisions | if/elif/else, boolean logic | 1 |
| | 04 - Loops | for loops, while loops, range | 1-2 |
| **Module 3: Functions** | | | |
| | 05 - Writing Functions | def, parameters, return | 1 |
| | 06 - Function Practice | Scope, multiple functions | 1 |
| ... | | | |

**Total**: 10 lessons across 4 modules, 10 sessions

---

**Does this structure work? Anything to add, move, or remove?**
```

### For Activity / Have Fun courses:

```
---

### Proposed Activity Sequence

| # | Activity | Materials | Duration | Key Concept |
|---|----------|-----------|----------|-------------|
| 1 | Binary Bracelets | Beads, string | 30 min | Binary encoding |
| 2 | Robot Maze | Grid mat, cards | 45 min | Sequencing |
| ... | | | | |

---
```

### For Challenge-Based:

```
---

### Proposed Challenge Sequence

| # | Challenge | Difficulty | Concepts | Est. Time |
|---|-----------|-----------|----------|-----------|
| 1 | Number Guessing Game | Starter | Variables, input, loops | 1 session |
| 2 | Password Validator | Intermediate | Strings, conditions | 1 session |
| ... | | | | |

---
```

## Section 6: Assessment Plan

```
---

### Assessment Plan

| Component | Description | When |
|-----------|-------------|------|
| Lesson quizzes | 5-question quiz per lesson | End of each lesson |
| Exercises | Coding exercises with auto-check | During lab time |
| Module projects | Mini-project per module | End of each module |
| Final project | Student-chosen project | Sessions 9-10 |

### Completion Criteria

- [ ] 80% of quizzes passed (7/10 correct)
- [ ] All required exercises submitted
- [ ] Final project demonstrates 3+ learning outcomes

---

**Does this assessment approach work?**
```

## Section 7: Technical Decisions

```
---

### Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Tier | 3 | Grades 6-10, code-based |
| Delivery | MkDocs site + GitHub repo | Standard League stack |
| Platform | GitHub Codespaces | No local setup needed |
| Content format | Markdown + .py exercises | Simple, version-controlled |
| Lesson format | Sequential with progressive project | Matches pedagogical model |
| Special requirements | None | Browser-only |

---
```

## Final Review

After drafting all three sections, present the complete spec summary:

```
---

## Complete Specification — Review

### Section Checklist

| # | Section | Status |
|---|---------|--------|
| 1 | Course Concept | Done |
| 2 | Pedagogical Model | Done |
| 3 | Research Summary | Done |
| 4 | Alignment Decision | Done |
| 5 | Course Structure Outline | Done |
| 6 | Assessment Plan | Done |
| 7 | Technical Decisions | Done |

### Quick Summary

| Property | Value |
|----------|-------|
| Title | (from concept) |
| Target | (grades, prerequisites) |
| Format | (sessions, duration) |
| Tier | (1-4) |
| Alignment | (certification/standard) |
| Modules | (count) |
| Lessons | (count) |
| Assessment | (approach) |

---

**The spec is complete. Ready to approve and move to Phase 2?**

Phase 2 will scaffold the directory structure, create lesson stubs,
and begin content authoring.
```

When the designer approves, use `update_spec` for each drafted section,
then call `advance_phase("phase2")`.
