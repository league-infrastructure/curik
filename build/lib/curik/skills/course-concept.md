---
name: course-concept
description: Question sequence for Phase 1a — capturing the course concept
---

# Course Concept Skill (Phase 1a)

Guide the designer through capturing the course concept. Present each step
with structured formatting — status tables, clear questions, and a running
summary of what's been captured.

## Required Fields

Track these in a status table. Update it as fields are captured:

```
### Course Concept — Fields

| # | Field | Status |
|---|-------|--------|
| 1 | Target students | Captured |
| 2 | Educational goals | Captured |
| 3 | Student & parent goals | **Needs discussion** |
| 4 | Learning outcomes | **Needs discussion** |
| 5 | Format | Captured |
| 6 | Rough scope | **Needs discussion** |
```

### Field Details

1. **Target students**: Grade range, prerequisites, experience level
2. **Educational goals**: What students should be able to do after this course
3. **Student and parent goals**: What draws families to enroll? (excitement
   about tech, certification, college prep, portfolio pieces)
4. **Learning outcomes**: Specific, observable outcomes. Not "understand X"
   but "write a program that does X." (Some course types may not have formal
   learning outcomes.)
5. **Format**: One of these — present as a menu:

   ```
   What format fits this class?

   1. **Tech Club** — 90-minute sessions, fun and exploratory
   2. **Semester course** — 6-10 structured sessions with learning goals
   3. **Summer program** — multi-week intensive
   4. **Persistent / open-ended** — ongoing, students progress at own pace
   5. **Something else** — describe it
   ```

6. **Rough scope**: Number of sessions, session length, fixed endpoint or
   open-ended

## Question Flow

### Opening

Start with an open-ended question. Don't show the fields table yet —
let the designer talk first:

> **Tell me about the class you're imagining.** What are you trying to
> build? Who's it for? What should students walk away with?

Listen to the response and extract as many fields as you can.

### After the Opening

Show the fields table with what you've captured so far. For each
uncaptured field, ask a focused follow-up:

- Target students: "What grade range are you targeting? Any prerequisites?"
- Educational goals: "When a student finishes, what should they be able to do?"
- Student/parent goals: "What would make a parent excited about this class?"
- Learning outcomes: "Can you name 3-5 specific things a student should be
  able to demonstrate?"
- Format: Show the format menu above
- Scope: "How many sessions, and how long each? Does the class have a fixed
  endpoint?"

Ask one or two questions at a time, not all at once.

### Probing Questions

After the basics, probe for non-obvious information:

```
### A few more questions

- Is there a **certification or exam** this could prepare students for?
  (AP CS, PCEP, etc.)
- Are there specific **projects or artifacts** students should produce?
  (a game, a website, a portfolio piece)
- Are there things you explicitly **don't** want to include?
```

## Completion

When all fields are captured, show the complete summary:

```
---

## Phase 1a Summary: Course Concept

| Field | Value |
|-------|-------|
| Target students | Grades 6-8, no prior experience |
| Educational goals | Write Python programs using variables, loops, functions |
| Student/parent goals | Build confidence with technology, create portfolio pieces |
| Learning outcomes | See list below |
| Format | Semester course, 10 sessions x 90 min |
| Scope | 10 sessions, fixed endpoint |

### Learning Outcomes
1. Write a Python program with variables and user input
2. Use loops to process collections of data
3. Define and call functions with parameters
4. ...

---

**Does this capture your vision? Anything to add or change?**
```

When the designer confirms, call `record_course_concept` with the
formatted content and `tool_advance_sub_phase()` to move to Phase 1b.
