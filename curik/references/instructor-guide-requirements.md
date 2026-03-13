# Instructor Guide Requirements

This document defines the required fields and quality standards for
instructor guide sections. Lesson authors and reviewers consult this
reference.

## The 7 Required Fields

Every instructor guide must include ALL 7 fields. Missing fields cause
validation failures.

### 1. Objectives

2–4 specific, observable learning objectives for the lesson.

**Requirements:**
- Uses action verbs (write, identify, explain, debug, build, predict)
- Each objective is testable — you can observe whether achieved
- Matches the actual lesson content, not aspirational course goals
- Avoids vague verbs (understand, learn, know, appreciate)

**Validation check:** At least 2 objectives present, each starting with
an action verb.

### 2. Materials

Complete list of everything needed before the lesson starts.

**Requirements:**
- Specific quantities ("20 index cards" not "cards")
- Digital resources with filenames or links
- Physical materials for unplugged activities
- Anything that needs printing, cutting, or setup
- Required software, packages, or accounts

**Validation check:** Non-empty, contains at least one specific item.

### 3. Timing

Minute-by-minute breakdown of how lesson time is spent.

**Requirements:**
- Every segment has a duration in minutes
- Total should match the expected lesson length
- Includes transitions between activities
- Format: `X min: Activity description`

**Validation check:** Contains at least 3 timed segments.

### 4. Key Concepts

Main ideas in plain language — what the instructor should emphasize.

**Requirements:**
- 2–5 key concepts per lesson
- Written as complete statements, not single words
- Matches the lesson objectives — concepts support the objectives
- Age-appropriate language for the tier

**Validation check:** At least 2 concepts present.

### 5. Common Mistakes

Specific errors students make and how to address them.

**Requirements:**
- Real, observed mistakes (not hypothetical)
- Includes the mistake AND the correction/response
- Tier-appropriate — matches what students at this level actually do
- At least 2 mistakes per lesson

**Validation check:** At least 2 mistakes listed.

### 6. Assessment Cues

Observable indicators that tell the instructor whether students understand.

**Requirements:**
- Phrased as questions the instructor can check during class
- Focus on observable behavior, not internal understanding
- Cover the main objectives (at least one cue per objective)
- Format: "Can the student [observable action]?"

**Validation check:** At least 2 assessment cues present.

### 7. Differentiation

Adaptations for students at different levels.

**Requirements:**
- At least one adaptation for struggling students
- At least one adaptation for advanced students
- Specific and actionable (not "give extra help")
- Format: "Struggling: [specific adaptation]" and "Advanced: [specific adaptation]"

**Validation check:** Contains both "struggling" and "advanced" adaptations.

## Formatting in Shortcodes

The instructor guide is wrapped in a Hugo shortcode:

```markdown
{{</* instructor-guide */>}}

**Objectives:**
- First objective
- Second objective

**Materials:**
- Item 1
- Item 2

**Timing:**
- 5 min: Introduction
- 15 min: Main activity
- 10 min: Practice

**Key Concepts:**
- Concept 1
- Concept 2

**Common Mistakes:**
- Mistake 1 — how to address it
- Mistake 2 — how to address it

**Assessment Cues:**
- Can the student do X?
- Can the student explain Y?

**Differentiation:**
- Struggling: Simplify to X
- Advanced: Extend with Y

{{</* /instructor-guide */>}}
```

## Tier Differences

### Tier 1–2 (Instructor-Guide-Primary)

The instructor guide IS the main content. The page is essentially all
instructor guide with minimal student-facing text. The guide should be
detailed enough that a substitute instructor could teach from it.

### Tier 3–4 (Student Content + Inline Guide)

Student content comes first, instructor guide follows. The guide
supplements the student content — it doesn't need to repeat what
students can read, but should add instructor-specific context (timing,
common mistakes, how to facilitate discussions).

## Quality Benchmarks

A complete, high-quality instructor guide:
- Could be used by a substitute instructor who has never seen the lesson
- Contains no placeholder text ("TBD", "TODO", "fill in later")
- Is specific to THIS lesson (not generic advice)
- Timing adds up to the expected lesson duration
- Assessment cues map to objectives
