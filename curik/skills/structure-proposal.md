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

Present the full tree with descriptions:

```
---

### Proposed Directory Tree

```
content/
  _index.md
  01-getting-started/
    _index.md
    01-hello-python.md        # Variables, print, input
    02-data-types.md          # Strings, ints, floats
  02-control-flow/
    _index.md
    03-decisions.md           # if/elif/else
    04-loops.md               # for, while, range
  03-functions/
    _index.md
    05-writing-functions.md   # def, parameters, return
    06-function-practice.md   # Scope, composition
  04-data-and-projects/
    _index.md
    07-lists.md               # Lists, iteration
    08-dictionaries.md        # Dicts, key-value
    09-file-io.md             # Reading/writing files
    10-final-project.md       # Student project
```

### Lesson Detail

| # | Lesson | Module | Topics | Est. Duration |
|---|--------|--------|--------|---------------|
| 01 | Hello Python | Getting Started | Variables, print, input | 1 session |
| 02 | Data Types | Getting Started | Strings, ints, type conversion | 1 session |
| 03 | Decisions | Control Flow | if/elif/else, booleans | 1 session |
| 04 | Loops | Control Flow | for, while, range | 1.5 sessions |
| ... | | | | |

---

**Does this structure look right? Any lessons to add, remove, split, or
reorder?**
```

### Step 3: Finalize

When approved, present the action plan:

```
---

### Ready to Scaffold

When you approve, I will:

- [ ] Create 4 module directories
- [ ] Create 10 lesson stub files with frontmatter
- [ ] Generate Hugo nav weights
- [ ] Set up .devcontainer (Tier 3)
- [ ] Create mirror directories in lessons/ and projects/

**Approve to proceed?**

---
```

## Naming Conventions

- Modules: `01-module-name/`, `02-module-name/`
- Lessons: `01-lesson-name.md`, `02-lesson-name.md`
- Exercises: `01-lesson-name-exercises.py` or `.ipynb`
- Challenges: `01-challenge-name.md`

## Output

A change plan document listing every module, lesson, and stub description,
ready for scaffolding in Phase 2.
