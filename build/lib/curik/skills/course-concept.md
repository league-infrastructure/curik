---
name: course-concept
description: Question sequence for Phase 1a — capturing the course concept
---

# Course Concept Skill (Phase 1a)

Guide the designer through capturing the course concept. Ask these questions
in order, recording answers into the spec's Course Concept section.

## Required Fields

1. **Target students**: Grade range, prerequisites, experience level
2. **Educational goals**: What students should be able to do after this course
3. **Student and parent goals**: What draws families to enroll? (excitement
   about tech, certification, college prep, portfolio pieces)
4. **Learning outcomes**: Specific, observable outcomes. Not "understand X"
   but "write a program that does X." (Some course types may not have formal
   learning outcomes.)
5. **Format**: Tech Club (90 min, fun), semester course (6-10 sessions),
   summer program (multi-week intensive), persistent/open-ended
6. **Rough scope**: Number of sessions, session length, fixed endpoint or
   open-ended

## Question Sequence

1. "Tell me about the class you're imagining."
   → Let the designer talk freely. Extract initial answers to fields above.

2. For each missing field, ask a focused question:
   - "What grade range are you targeting?"
   - "What should students be able to do when they finish?"
   - "What would make a parent excited about this class?"
   - "How is the class structured — weekly sessions, intensive, or open-ended?"
   - "How many sessions are you thinking, and how long each?"

3. Probe for non-obvious goals:
   - "Is there a certification or exam this could prepare students for?"
   - "Are there specific projects or artifacts students should produce?"

## Recording

When all fields are captured, format them into a structured summary and
call `record_course_concept` with the content.

## Output

A written course concept — a few paragraphs plus structured summary in
the spec's Course Concept section.
