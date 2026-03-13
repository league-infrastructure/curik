---
name: lesson-writing-older
description: Lesson page format, notebook structure, inline instructor guide, and code example standards for Tier 3-4 lessons
---

# Lesson Writing — Older Learners (Tiers 3-4)

This skill covers how to write student-facing lesson pages and Jupyter
notebooks for grades 6-12. Students read the content directly. Instructor
guidance is embedded inline using a Hugo shortcode.

## Lesson Page Format

Markdown lesson pages follow this template:

```markdown
---
title: Lesson Title
lesson: 1
tier: 3
---

# Lesson Title

Brief introduction — why this topic matters and what we'll build.

## Concept Name

Explanation of the concept. Use analogies, then precise definitions.

### Example

\```python
# A short, runnable example
result = some_function()
print(result)  # Output: expected_output
\```

### Try It

Instructions for the student to practice the concept.

## Next Concept

Continue building...

## Summary

Key takeaways in 3-5 bullet points.

{{< instructor-guide >}}

## Instructor Guide

**Objectives**: ...
**Materials**: ...
**Timing**: ...
**Key Concepts**: ...
**Common Mistakes**: ...
**Assessment Cues**: ...
**Differentiation**: ...

{{< /instructor-guide >}}
```

## Jupyter Notebook Structure

Notebooks alternate between Markdown cells and code cells:

1. **Title cell** (Markdown): Lesson title, tier, and 1-2 sentence overview.
2. **Concept cells** (Markdown): Explain the concept before showing code.
3. **Example cells** (Code): Runnable, commented examples. Output should
   be included in the saved notebook.
4. **Practice cells** (Code): Contain a comment prompt and starter code.
   Students fill in the rest.
5. **Solution cells** (Code): Tagged with `# SOLUTION` in the first line.
   These are stripped from student-facing notebooks.
6. **Instructor guide cell** (Markdown): The last Markdown cell, containing
   the instructor guide shortcode.

### Notebook Rules

- The notebook must run top-to-bottom without errors (excluding practice
  cells with placeholder code).
- Each code cell should have a clear purpose stated in a preceding
  Markdown cell or in a comment.
- Avoid cells with more than 20 lines of code. Split into smaller cells.
- Import statements go in the first code cell.
- Do not use `!pip install` in notebooks — list dependencies in Materials.

## Inline Instructor Guide Sections

The instructor guide is embedded in a `{{< instructor-guide >}}` shortcode
block. This is rendered hidden for students but visible for instructors.

All 7 required fields must appear. See `instructor-guide-sections` for
detailed guidance on each field.

For lesson pages, the instructor guide goes at the end of the file,
after the summary. For notebooks, it goes in the final Markdown cell.

## Code Example Standards

### Correctness
- Every example must be syntactically valid and produce the stated output.
- Test examples before including them.

### Clarity
- One concept per example. Do not mix new ideas.
- Use meaningful variable names, not `x`, `y`, `temp`.
- Comment non-obvious lines. Do not comment obvious lines.

### Length
- Inline examples: under 15 lines.
- Full examples (in their own cell or section): under 30 lines.
- If an example needs more, split it into stages.

### Style
- Python: PEP 8. Use type hints for function signatures.
- JavaScript: standard style with semicolons.
- Other languages: follow the dominant community style guide.

### Output
- Show expected output in a comment (`# Output: ...`) for Markdown examples.
- Include cell output in saved notebooks.

## Lesson Type Guidelines

### Sequential Lessons
- Start with a "Prerequisites" note listing prior lessons.
- Begin with a brief review of the relevant concept from last time.
- End with a "Next time" teaser.

### Challenges
- State the problem clearly with success criteria.
- Provide starter code with `# TODO` markers.
- Include hints in `<details>` tags.
- Provide 1-2 extension tasks.

### Progressive Projects
- Define the milestone for this lesson at the top.
- Provide checkpoint code so students who missed the last session can
  catch up.
- Include a "Where we left off" section showing the state of the project.
- End with a working version of the project at the new milestone.

## Common Pitfalls

- **Wall of text.** Break explanations into short paragraphs. Use code
  examples every 2-3 paragraphs.
- **Assuming knowledge.** If a concept was taught in a prior lesson,
  link to it. Don't assume students remember.
- **Untested code.** Run every example. A syntax error destroys student
  trust.
- **Missing instructor guide.** The shortcode is easy to forget in notebooks.
  It is not optional.
