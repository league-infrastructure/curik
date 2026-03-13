---
name: existing-content-analysis
description: Analyze sequestered existing content and produce a structured analysis report
---

# Existing Content Analysis Skill

When a repository has existing content that has been sequestered to `_old/`,
this skill guides the analysis. Used by the Curriculum Architect before
beginning Phase 1 spec development.

## When to Use

Use this skill when `get_course_status()` reports `has_existing_content: true`
and the content has been sequestered via `sequester_content()`.

## Process

### Step 1: Inventory the Content

Read through `_old/` and catalog what exists:

```
---

## Existing Content Analysis

### Content Inventory

| # | Item | Type | Description |
|---|------|------|-------------|
| 1 | lesson-01.md | Lesson | Introduction to variables |
| 2 | lesson-02.md | Lesson | Loops and iteration |
| 3 | README.md | Documentation | Course overview |
| 4 | slides/ | Directory | Presentation files |

**Total**: X lessons, Y supporting files
```

### Step 2: Analyze Structure

Describe how the content is organized:
- What directory structure is used?
- How are lessons numbered and ordered?
- Is there a table of contents, nav file, or syllabus?
- What file formats are used (.md, .ipynb, .pptx, .pdf)?

### Step 3: Analyze Pedagogy

Examine the content for pedagogical patterns:
- What topics are covered and in what order?
- What's the target audience / difficulty level?
- What pedagogical approach is used (project-based, concept-based, etc.)?
- Are there exercises, quizzes, or assessments?
- Are there instructor guides or teacher notes?

### Step 4: Identify Strengths and Gaps

```
---

### Strengths
- (What the existing content does well)

### Gaps
- (What's missing or weak)

### Assumptions
- (What the content assumes about students)

### Prerequisites
- (What students need to know before starting)
```

### Step 5: Present to Designer

Present the analysis and ask:
1. "Is this analysis accurate? Anything I'm missing or misreading?"
2. "Do you want to keep this scope, expand it, or narrow it?"
3. "Should we convert this content (Path B) or start fresh informed by it (Path C)?"

### Step 6: Proceed to Phase 1

After designer confirms:
- Proceed through Phase 1 sub-phases as normal
- Each sub-phase question is informed by the analysis
- Example: "The existing curriculum covers X. Do you want to keep this scope?"

## Output

The analysis report should be written directly into `.course/spec.md` as a
preamble section, or saved as a research finding via `save_research_findings()`.
