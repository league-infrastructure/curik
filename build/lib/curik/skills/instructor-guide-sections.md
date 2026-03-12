---
name: instructor-guide-sections
description: Defines the 7 required instructor guide fields and what good looks like for each
---

# Instructor Guide Sections

Every lesson — regardless of tier — must include an instructor guide with
all 7 fields below. This skill defines each field and provides criteria
for what makes a good entry.

## 1. Objectives

**What it is:** 2-4 specific, observable learning objectives for the lesson.

**What good looks like:**
- Uses action verbs: "write", "identify", "explain", "debug", "build"
- Is testable: you can observe whether the student achieved it
- Matches the lesson content — not aspirational goals from the course level

**Bad example:** "Understand loops"
**Good example:** "Write a for-loop that iterates over a list and prints
each element"

## 2. Materials

**What it is:** A complete list of everything the instructor needs to
prepare before the lesson starts.

**What good looks like:**
- Specific quantities and descriptions ("20 index cards, each with a
  number 1-20 written on it")
- Includes digital resources (links to starter code, slides, handouts)
- Includes physical materials for unplugged activities
- Notes anything that needs to be printed, cut, or set up in advance
- Includes required software, packages, or accounts

**Bad example:** "Cards, markers"
**Good example:**
- "1 deck of number cards per pair (printed from appendix-a.pdf, cut
  into individual cards)"
- "Markers (1 per student, any color)"
- "Projector displaying the starter notebook from lesson-03-starter.ipynb"

## 3. Timing

**What it is:** A minute-by-minute breakdown of how the lesson time is
spent.

**What good looks like:**
- Accounts for the full session length (e.g., 50 min or 90 min)
- Includes transitions ("2 min — students return to seats")
- Realistic — does not cram 60 minutes of content into 45 minutes
- Identifies which segments can be shortened if time runs out
- Uses a table format for easy scanning

**Bad example:** "Introduction, main activity, wrap-up"
**Good example:**

| Segment | Minutes | Activity |
|---------|---------|----------|
| Warm-up | 5 | Review question on board; students discuss in pairs |
| Teach | 12 | Teacher explains for-loops with live demo |
| Activity | 25 | Students complete the loop challenges worksheet |
| Share-out | 5 | 2-3 students show their solutions |
| Wrap-up | 3 | Exit ticket: "Write a loop that prints 1-10" |

## 4. Key Concepts

**What it is:** The core ideas of the lesson, explained at the teacher's
level of understanding. For young-learner guides, also includes the
student-friendly version the teacher can say aloud.

**What good looks like:**
- Explains the concept accurately, not just names it
- Distinguishes this concept from related ones students may confuse
- For Tiers 1-2: provides exact phrasing the teacher can use
- For Tiers 3-4: provides the precise technical definition plus a
  plain-language restatement

**Bad example:** "Key concept: loops"
**Good example:** "A for-loop repeats a block of code once for each item
in a sequence. Students often confuse this with a while-loop, which
repeats until a condition is false. For this lesson, we only use for-loops.
Tell students: 'A for-loop is like going through a line of people and
saying hello to each one.'"

## 5. Common Mistakes

**What it is:** Errors students frequently make with this lesson's
content, along with how to diagnose and address each one.

**What good looks like:**
- Specific and grounded ("students write `for i in range(10)` but expect
  it to include 10")
- Includes what the teacher should look for (the symptom)
- Includes what to say or do (the intervention)
- Covers both conceptual mistakes and mechanical errors

**Bad example:** "Students may have trouble with syntax"
**Good example:**
- "Off-by-one in range(): students expect `range(5)` to produce 1-5.
  Show them `list(range(5))` and count the elements together."
- "Indentation errors: students forget to indent the loop body. If their
  code runs but only executes once, check indentation first."

## 6. Assessment Cues

**What it is:** Observable behaviors or artifacts that tell the instructor
whether students are understanding the material.

**What good looks like:**
- Describes something the teacher can see, hear, or read
- Covers a range from "not yet" to "got it" to "exceeding"
- Practical — the teacher can check these during the activity, not only
  after grading

**Bad example:** "Check for understanding"
**Good example:**
- "Students who get it: loop runs correctly on first or second try, they
  can explain why range stops before the end number"
- "Students who need help: loop body is not indented, or they are copying
  the example without changing the variable"
- "Students exceeding: they modify the loop to count backwards or skip
  every other number without being asked"

## 7. Differentiation

**What it is:** Concrete adjustments for students who need more support
and students who are ready for more challenge.

**What good looks like:**
- At least one adjustment for "needs more support"
- At least one adjustment for "ready for more"
- Specific actions, not general advice
- Does not require separate materials (ideally) — small tweaks to the
  same activity

**Bad example:** "Differentiate as needed"
**Good example:**
- *Needs more support*: "Provide a printed reference card showing loop
  syntax. Pair the student with a stronger partner for the activity."
- *Ready for more*: "Challenge them to write a nested loop that prints a
  multiplication table. They can also try using `enumerate()` instead of
  `range()`."
