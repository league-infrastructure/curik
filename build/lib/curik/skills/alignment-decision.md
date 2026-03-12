---
name: alignment-decision
description: Mapping research findings to alignment targets and topic lists
---

# Alignment Decision Skill (Phase 1d)

Guide the designer through choosing alignment targets based on research
findings from Phase 1c.

## Alignment Options

A course may align to one or more of:

- **Certification or exam** — AP CS A, PCEP, AWS Cloud Practitioner
- **External course** — Harvard CS50, freeCodeCamp curriculum
- **External tutorials/resources** — MakeCode tutorials, a Trinket course
- **Self-defined topic list** — our own judgment on what to cover
- **No alignment** — short-format classes, workshops

Alignment can be layered (e.g., Python Apprentice aligns to PCEP AND uses
specific sourced tutorials).

## Decision Process

1. Present research findings summary to the designer
2. For each alignment candidate, discuss:
   - Coverage: does this certification/course cover what we want to teach?
   - Fit: does the scope match our session count and format?
   - Value: will students/parents see value in this alignment?
3. Ask: "Which of these should this course align to, if any?"
4. If aligned: extract the specific topic list from the alignment target
5. If self-defined: work with the designer to create the topic list

## Recording

Format the alignment decision (what, why) plus the specific topic list
and call `record_alignment` with the content.

## Output

An alignment statement in the spec: what the course aligns to, why,
plus the topic list or syllabus.
