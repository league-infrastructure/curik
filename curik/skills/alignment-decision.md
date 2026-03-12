---
name: alignment-decision
description: Mapping research findings to alignment targets and topic lists
---

# Alignment Decision Skill (Phase 1d)

Guide the designer through choosing alignment targets based on research
findings from Phase 1c. Present options as structured menus and comparisons.

## Step 1: Research Summary

First, present a summary of what research found:

```
---

## Phase 1d: Alignment Decision

### Research Findings Summary

| Source | What it covers | Fit |
|--------|---------------|-----|
| PCEP certification | Python basics through functions | Strong — matches our scope |
| freeCodeCamp Python | Variables through OOP | Partial — broader than we need |
| CS50 Python | Full intro CS curriculum | Too broad for our format |
| AP CS Principles | Computational thinking focus | Different language focus |

---
```

After presenting the research summary:

```
---

### What would you like to do with these findings?

1. **Choose an alignment** — let's pick what this course should align to
2. **Tell me more** — explain what alignment means and why it matters
3. **Research more** — I want to look at specific areas in more detail
4. **Skip alignment** — this course doesn't need to align to anything external

---
```

## Step 2: Alignment Options

If the user wants to choose an alignment, present the menu:

```
---

### What should this course align to?

You can pick more than one — alignment can be layered.

1. **Certification or exam** — build toward a specific credential
   - *Examples: PCEP, AP CS A, AWS Cloud Practitioner*
2. **External course** — follow another course's structure
   - *Examples: CS50, freeCodeCamp*
3. **External tutorials/resources** — use specific materials as a base
   - *Examples: MakeCode tutorials, a specific Trinket course*
4. **Self-defined topic list** — we decide what to cover ourselves
5. **No alignment** — short-format, exploratory, no external standard

Pick one or more numbers, or describe what you're thinking.

---
```

After the user picks alignment options, confirm and offer evaluation:

```
---

You're considering **[chosen options]**.

### What next?

1. **Evaluate these** — let me show you how each one fits your course
2. **I already know** — just go with [option], skip the comparison
3. **Go back** — I want to reconsider my options

---
```

## Step 3: Evaluation (if aligning)

For each alignment candidate the designer is considering, present a
comparison:

```
---

### Evaluating: PCEP Certification

| Criterion | Assessment |
|-----------|-----------|
| **Coverage** | Covers variables, operators, loops, functions, data structures — matches our scope well |
| **Fit** | 35 topics across our 10 sessions = 3-4 topics per session, manageable |
| **Value** | Industry-recognized Python cert, looks good on student portfolio |
| **Gap** | Doesn't cover file I/O or classes, which we might want |

**Recommendation**: Strong fit as primary alignment. We can add our own
topics beyond what PCEP requires.

---
```

After evaluation, present the decision point:

```
---

### Based on the evaluation:

**[recommendation summary]**

### What would you like to do?

1. **Go with this recommendation** — use [recommended alignment]
2. **Pick a different one** — I prefer [other option]
3. **Combine them** — use multiple alignment targets
4. **Evaluate another option** — show me the comparison for [another candidate]

---
```

## Step 4: Topic List

Once alignment is decided, extract or build the topic list:

```
---

### Course Topic List

Aligned to: **PCEP** + custom additions

| # | Topic | Source | Sessions |
|---|-------|--------|----------|
| 1 | Variables and data types | PCEP | 1-2 |
| 2 | Operators and expressions | PCEP | 2 |
| 3 | Control flow (if/else) | PCEP | 3 |
| 4 | Loops (for, while) | PCEP | 4-5 |
| 5 | Functions | PCEP | 6-7 |
| 6 | Data structures (lists, dicts) | PCEP | 8 |
| 7 | File I/O | Custom | 9 |
| 8 | Final project | Custom | 10 |

---

**Does this topic sequence work?**

### What would you like to do?

1. **Looks good** — lock in this topic list
2. **Reorder** — I want to change the sequence
3. **Add topics** — there's something missing
4. **Remove topics** — this is too much for the course
5. **Change alignment** — go back and pick a different alignment target

---
```

## Completion

Show the final alignment decision:

```
---

## Phase 1d Summary: Alignment Decision

| Decision | Value |
|----------|-------|
| Primary alignment | PCEP certification |
| Secondary alignment | None |
| Custom additions | File I/O, final project |
| Total topics | 8 |
| Rationale | Industry-recognized credential, scope matches our session count |

---

**Ready to move on?**

### What would you like to do?

1. **Looks good — move on** — save this and proceed to Phase 1e
   (Spec Synthesis)
2. **Change something** — I want to adjust the alignment or topic list
3. **Go back to research** — I want more research before deciding
4. **Start over** — rethink alignment from scratch

---
```

When confirmed, call `record_alignment` with the formatted content and
`tool_advance_sub_phase()` to move to Phase 1e.

## Guided Mode Rule

**In guided mode, EVERY response must end with a numbered choice menu.**
After each step, after confirming a choice, after showing a table —
always end with "What next?" and numbered options. The user should never
face a blank prompt.
