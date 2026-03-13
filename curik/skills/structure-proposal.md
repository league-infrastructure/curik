---
name: structure-proposal
description: Creating a concrete module/lesson skeleton from an approved spec
---

# Structure Proposal Skill

Convert an approved specification into a concrete module and lesson skeleton.
This is the bridge between Phase 1 (spec) and Phase 2 (scaffolding).

## Process

### Step 1: Read the Spec

Read all spec sections. Summarize what drives the structure:

```
---

## Structure Proposal

### Design Inputs

| Source | Key decisions |
|--------|--------------|
| Course Structure Outline | 4 modules, 10 lessons |
| Pedagogical Model | Sequential + progressive project |
| Technical Decisions | Tier 3, Hugo + Codespaces |
| Alignment | PCEP topics in order |

---
```

### Step 2: Propose Directory Structure

**Write the structure proposal to a file** — either as a change plan
document or directly into `.course/spec.md` as an appendix. Include the
full directory tree and lesson detail table.

Then show a brief summary in chat:

---

### Structure Proposal — Written

I've written the proposed directory structure to `[file path]`.
It includes N modules with M lessons total.

**Please open the file and review the proposed structure.** You can
edit module names, lesson order, and topics directly.

### When you're done reviewing:

1. **Looks good — scaffold it** — proceed to create the directory structure
2. **I made changes** — I edited the file, take a look
3. **Let's discuss** — I have questions about the structure
4. **Start over** — rethink the structure from scratch

---

### Step 3: Finalize

When approved, present the action plan briefly in chat, then proceed
with scaffolding.

## Naming Conventions

- Modules: `01-module-name/`, `02-module-name/`
- Lessons: `01-lesson-name.md`, `02-lesson-name.md`
- Exercises: `01-lesson-name-exercises.py` or `.ipynb`
- Challenges: `01-challenge-name.md`

## Output

A change plan document listing every module, lesson, and stub description,
ready for scaffolding in Phase 2.
