# Skill: README Shortcode Guards

## Purpose

Teach agents how to place Hugo shortcode guards in lesson pages so
that Curik can automatically generate README.md files for GitHub-visible
lesson directories. This applies to Tier 3-4 courses where students
browse lessons in the repository or Codespaces.

## Guard Types

### `{{</* readme-shared */>}}`

Content between `{{< readme-shared >}}` and `{{< /readme-shared >}}`
appears in **both** the rendered Hugo site page and the generated README.

Use this for:
- Lesson title and introduction
- Learning objectives
- Key concepts and summaries
- Prerequisites

Example:

```markdown
{{< readme-shared >}}
# Introduction to Variables

In this lesson you will learn how to create and use variables in Python.

## Objectives

- Define variables with meaningful names
- Understand variable types: str, int, float, bool
{{< /readme-shared >}}
```

### `{{</* readme-only */>}}`

Content between `{{< readme-only >}}` and `{{< /readme-only >}}` appears
**only** in the generated README. The Hugo shortcode renders this content
as hidden on the site.

Use this for:
- Getting-started instructions specific to the repo/Codespaces context
- File structure explanations
- Links to exercises or starter code in the repo
- Instructions that reference the local file system rather than the web

Example:

```markdown
{{< readme-only >}}
## Getting Started

Open `exercise.py` in this directory and follow the instructions in the
comments. Run your solution with:

```bash
python exercise.py
```
{{< /readme-only >}}
```

## Placement Guidelines

1. Place `{{< readme-shared >}}` guards around content that makes sense
   in both contexts (web page and repository README).
2. Place `{{< readme-only >}}` guards around content that only makes
   sense when reading the README in the repository (file references,
   local run commands, Codespaces setup).
3. Guards can appear multiple times in a single file. Each guarded
   section is extracted and concatenated in order.
4. Do not nest guards inside each other.
5. Always close guards with the matching closing shortcode
   (`{{< /readme-shared >}}` or `{{< /readme-only >}}`).
6. Place guards at the block level (around full paragraphs, headings,
   or sections), not inline within a sentence.

## When to Use Guards

- **Tier 3-4 courses**: Always add guards to lesson pages that have a
  corresponding directory in `lessons/`. These courses have student-facing
  repositories where READMEs are the primary discovery mechanism.
- **Tier 1-2 courses**: Do not add guards. These are instructor-guide-primary
  courses without student-facing repo directories.

## Workflow

1. Author writes or edits a Hugo lesson page in `content/`.
2. Author adds `{{< readme-shared >}}` and/or `{{< readme-only >}}`
   guards around appropriate content.
3. Run `tool_trigger_readme_generation` to generate READMEs from all
   guarded pages.
4. Generated READMEs appear in `lessons/<module>/<lesson>/README.md`.
5. Commit both the lesson page and the generated README.
