---
name: lesson-writing-young
description: Voice, format, activity structure, and instructor guide requirements for Tier 1-2 lessons
---

# Lesson Writing — Young Learners (Tiers 1-2)

This skill covers how to write instructor-guided lessons for grades 2-5.
The instructor guide is the lesson — there is no separate student-facing
document. The teacher reads from the guide and leads all activities.

## Voice Calibration

Write for a teacher who is reading the guide and speaking to the class.

**Do:**
- "Tell students to line up by height. Ask: 'How did you decide where to
  stand?'"
- "Hand out the sorting cards (printed from Appendix A). Each pair gets
  one set."
- "If a student says the answer is 5, say: 'Great — how did you figure
  that out?'"

**Don't:**
- "Students will explore sorting algorithms." (too abstract)
- "Facilitate a discussion." (too vague — what questions?)
- "The teacher should consider differentiation." (say what to do)

## Lesson Format

Every lesson is a single Markdown file with this structure:

```markdown
---
title: Lesson Title
lesson: 1
tier: 1
---

# Lesson Title

<div class="instructor-guide" markdown>

## Instructor Guide

**Objectives**: [2-3 bullet points]

**Materials**:
- [Item 1]
- [Item 2]

**Timing**:
| Segment | Minutes | Activity |
|---------|---------|----------|
| Warm-up | 5 | ... |
| Teach | 15 | ... |
| Activity | 25 | ... |
| Wrap-up | 5 | ... |

**Key Concepts**:
[Explain each concept at the teacher level, then provide the
student-friendly version the teacher can say aloud]

**Common Mistakes**:
- [Mistake]: [What the teacher should say or do]

**Assessment Cues**:
- [Observable behavior that shows understanding]

**Differentiation**:
- *Needs more support*: [Specific adjustment]
- *Ready for more*: [Specific extension]

</div>

## Welcome / Warm-up

[Teacher script and activity]

## Teach

[Explanation with teacher script, visuals, board work]

## Activity

[Step-by-step instructions for the hands-on activity]

## Wrap-up

[Reflection questions, share-out, exit ticket]
```

## Activity Design Rules

1. **One main activity per lesson.** Supporting activities (warm-up, wrap-up)
   are shorter and simpler.
2. **Hands-on first.** Start with a physical or unplugged version of the
   concept before moving to a screen.
3. **Concrete before abstract.** Use objects students can touch and move
   before introducing diagrams or code.
4. **Pairs or small groups.** Solo work is rare at this tier. Design
   activities for 2-4 students working together.
5. **Materials must be listed exactly.** "Craft supplies" is not acceptable.
   List "scissors, glue sticks, construction paper (5 colors), markers."

## Instructor Guide Requirements

Every lesson must include all 7 required fields. See the
`instructor-guide-sections` skill for detailed guidance on what good
looks like for each field.

The instructor guide div must appear near the top of the lesson, before
the first content section, so the teacher reads it first during prep.

## Common Pitfalls

- **Too much screen time.** Tiers 1-2 lessons should be at most 50%
  computer time. Many lessons can be fully unplugged.
- **Missing teacher script.** Don't just describe what happens — write
  what the teacher says.
- **Vague materials.** If the activity needs cards, specify how many,
  what's on them, and whether there's a printable.
- **Skipping differentiation.** Every class has a range. Always provide
  at least one "needs more support" and one "ready for more" adjustment.
