# Lesson Page Template

This document defines the standard structure for lesson pages in Curik
curriculum projects. Lesson authors consult this reference.

## Tier 1–2 Lesson Structure

Tier 1–2 lessons are instructor-guide-primary: the instructor guide IS
the main content.

```markdown
---
title: "Sorting Race"
weight: 20
---

{{</* instructor-guide */>}}

**Objectives:**
- Sort a list of numbers from smallest to largest using a step-by-step method
- Explain why some sorting methods are faster than others

**Materials:**
- 1 set of number cards per pair (printed from appendix-a.pdf)
- Stopwatch or timer (1 per group)
- Whiteboard and markers

**Timing:**
- 5 min: Introduction — what does "sorted" mean?
- 10 min: Activity — sorting race with number cards
- 10 min: Discussion — which strategies were faster?
- 5 min: Wrap-up — preview of next lesson

**Key Concepts:**
- Sorting means arranging items in order (smallest to largest, A to Z)
- Different strategies (algorithms) take different amounts of time
- We can compare strategies by counting steps

**Common Mistakes:**
- Students may confuse "sorting" with "grouping" — clarify the difference
- Some students will try to sort all cards at once instead of comparing pairs

**Assessment Cues:**
- Can the student explain their sorting strategy in their own words?
- Can the student identify which strategy required fewer comparisons?

**Differentiation:**
- Struggling: Reduce to 5 cards instead of 10
- Advanced: Add a constraint — only compare adjacent cards

{{</* /instructor-guide */>}}
```

## Tier 3–4 Lesson Structure

Tier 3–4 lessons have student-facing content with an inline instructor
guide section.

```markdown
---
title: "Variables and Types"
weight: 10
---

{{</* readme-shared */>}}

# Variables and Types

In this lesson you'll learn how Python stores data in variables and
how different types affect what operations are available.

## Creating Variables

A variable is a name that refers to a value:

```python
name = "Alice"
age = 14
height = 5.6
```

{{</* callout type="tip" */>}}
Python figures out the type automatically — you don't need to declare it.
{{</* /callout */>}}

## Types

Python has several built-in types:

| Type | Example | Description |
|------|---------|-------------|
| `str` | `"hello"` | Text |
| `int` | `42` | Whole number |
| `float` | `3.14` | Decimal number |
| `bool` | `True` | True or False |

## Exercises

1. Create variables for your name, age, and favorite number
2. Use `type()` to check the type of each variable
3. What happens when you add an `int` and a `float`?

{{</* /readme-shared */>}}

{{</* instructor-guide */>}}

**Objectives:**
- Create variables with descriptive names
- Identify the type of a value using type()
- Predict the result of operations on different types

**Materials:**
- Starter notebook: lesson-01-starter.ipynb
- Solution notebook: lesson-01-solution.ipynb (instructor only)

**Timing:**
- 5 min: Review — what do students remember about print()?
- 15 min: Guided coding — variables and assignment
- 10 min: Type exploration — type() function, type mixing
- 15 min: Exercises — independent practice
- 5 min: Share out — volunteers show solutions

**Key Concepts:**
- Variables store values and can be reassigned
- Python is dynamically typed — type is inferred
- Operations depend on type (+ concatenates strings, adds numbers)

**Common Mistakes:**
- Using spaces in variable names (use underscores)
- Confusing = (assignment) with == (comparison)
- Expecting "14" + 1 to work (string + int TypeError)

**Assessment Cues:**
- Can the student create a variable and print its value?
- Can the student predict what type() returns for a given value?
- Can the student explain why "14" + 1 raises an error?

**Differentiation:**
- Struggling: Focus on str and int only, skip float
- Advanced: Explore type conversion (int(), str(), float())

{{</* /instructor-guide */>}}
```

## Required Elements

Every lesson page must include:

1. **YAML frontmatter** with `title` and `weight`
2. **Instructor guide shortcode** with all 7 required fields
3. **Student content** (Tier 3–4) with clear explanations and exercises

### The 7 Instructor Guide Fields

1. **Objectives** — 2-4 observable, testable learning objectives
2. **Materials** — everything needed, with specific quantities
3. **Timing** — minute-by-minute breakdown
4. **Key Concepts** — main ideas in plain language
5. **Common Mistakes** — specific errors students make and how to address them
6. **Assessment Cues** — observable indicators of understanding
7. **Differentiation** — adaptations for struggling and advanced students

## Content Markers

### Tier 3–4 README Guards

Every Tier 3–4 lesson must wrap student content in `{{</* readme-shared */>}}`
so it can be extracted to README.md files in mirror directories.

### Callouts

Use callouts for tips, warnings, and important information:
- `type="tip"` — helpful hints
- `type="warning"` — common pitfalls or important cautions
- `type="info"` — additional context or background

## Naming

- File: `NN-descriptive-name.md` (e.g., `01-variables-and-types.md`)
- Title: sentence case, matches the learning topic
- Weight: matches the numeric prefix × 10 (01 → 10, 02 → 20)
