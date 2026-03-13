---
name: content-conversion
description: Convert existing content from _old/ to standard Curik structure
---

# Content Conversion Skill

Convert existing curriculum content from `_old/` into the standard Curik
Hugo structure. Used by Lesson Authors when the designer chooses Path B
(convert existing content).

## When to Use

Use this skill after:
- Phase 1 spec is complete and approved
- Designer has chosen Path B (convert) for existing content
- Scaffolding has been run via `scaffold_structure()`

## Process

### Step 1: Review the Spec and Old Content

Read the approved spec and the `_old/` content inventory (from the
existing-content-analysis skill). Understand:
- What the new structure should look like
- What can be reused from old content
- What needs to be rewritten

### Step 2: Map Old Content to New Structure

Create a mapping table:

```
---

## Content Mapping

| Old File | New Location | Action |
|----------|-------------|--------|
| _old/lesson-01.md | content/01-intro/01-variables.md | Convert |
| _old/lesson-02.md | content/01-intro/02-loops.md | Convert |
| _old/advanced.md | (none) | Drop — out of scope |
| (none) | content/02-functions/01-basics.md | Write new |
```

### Step 3: Convert Each Lesson

For each lesson being converted:

1. **Read the old content** — understand what it teaches
2. **Create the new page** — use `create_lesson_stub()` for the scaffold
3. **Migrate the student content**:
   - Rewrite in the standard lesson page format
   - Add proper frontmatter (title, weight)
   - Wrap in `{{</* readme-shared */>}}` guards (Tier 3–4)
   - Convert any raw HTML to Hugo shortcodes
   - Update code examples if language/framework changed
4. **Write the instructor guide**:
   - All 7 required fields
   - Draw from old instructor notes if they exist
   - Write new sections for any gaps
5. **Validate** — run `validate_lesson()` on the new page

### Step 4: Post-Conversion Checks

After all lessons are converted:

1. Run `regenerate_syllabus()` (Tier 3–4)
2. Run `trigger_readme_generation()` (Tier 3–4)
3. Run `validate_course()` to check completeness
4. Present results to designer for review

### Step 5: Enter Phase 3

After designer reviews the conversion:
- File issues for anything that needs fixing via `create_issue()`
- The project enters Phase 3 (ongoing changes) for refinement

## Quality Standards

- Converted content should be **better** than the original, not just reformatted
- Every lesson must have all 7 instructor guide fields (even if old content didn't)
- Code examples must be tested and working
- No placeholder text — if old content is insufficient, write new material
