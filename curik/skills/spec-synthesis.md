---
name: spec-synthesis
description: Assembling the complete course specification from prior phase outputs
---

# Spec Synthesis Skill (Phase 1e)

Assemble the full course specification from all prior sub-phase outputs.
This is the final Phase 1 step before advancing to Phase 2.

## Opening

Show the section checklist as rendered markdown:

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

I need to draft sections 5–7 based on everything we've decided so far.
I'll write each section directly to `.course/spec.md`.

### How would you like to proceed?

1. **Draft all three** — I'll draft sections 5, 6, and 7 and write them to the spec
2. **One at a time** — walk me through each section separately
3. **Review first** — let me open `.course/spec.md` and see what's in sections 1–4

---

## Sections 5–7: Drafting

Draft all three sections (Course Structure Outline, Assessment Plan,
Technical Decisions) based on the prior phase outputs. **Write each
section directly to `.course/spec.md`** using `update_spec` as you
draft it — do not paste full drafts into chat.

For each section, briefly describe in chat what you're about to write
(2–3 sentences), then write it to the file. After writing all three,
present the review prompt.

### Section 5: Course Structure Outline

Draft the module/lesson outline based on pedagogical model and alignment.
Write it to the spec file. Adapt the format to the course type:
- **Sequential / Progressive Project**: modules with numbered lessons
- **Activity / Have Fun**: activity sequence with materials and durations
- **Challenge-Based**: challenge sequence with difficulty levels

### Section 6: Assessment Plan

Draft assessment components, timing, and completion criteria. Write to
the spec file.

### Section 7: Technical Decisions

Draft tier, delivery platform, content format, and any special
requirements. Write to the spec file.

## Final Review

After writing all three sections to the spec file, present a brief
status in chat and point the user to the file:

---

## Phase 1e: Spec Synthesis — Written

I've drafted sections 5–7 and written them to `.course/spec.md`.
The full specification is now complete:

| # | Section | Status |
|---|---------|--------|
| 1 | Course Concept | Done (Phase 1a) |
| 2 | Pedagogical Model | Done (Phase 1b) |
| 3 | Research Summary | Done (Phase 1c) |
| 4 | Alignment Decision | Done (Phase 1d) |
| 5 | Course Structure Outline | Done (just written) |
| 6 | Assessment Plan | Done (just written) |
| 7 | Technical Decisions | Done (just written) |

**Please open `.course/spec.md` and review the complete specification.**
Focus on sections 5–7 which are new. Edit anything directly in the file.

### When you're done reviewing:

1. **Approve and move to Phase 2** — lock in the spec and start scaffolding
2. **I made changes** — I edited the file, take a look
3. **Let's discuss** — I have questions about specific sections
4. **Go back** — revisit an earlier phase before finalizing

---

When the designer approves, call `advance_phase("phase2")`.

## Guided Mode Rule

**In guided mode, EVERY response must end with a numbered choice menu.**
After drafting a section, after showing a table, after any interaction —
always end with "What next?" and numbered options. The user should never
face a blank prompt.
