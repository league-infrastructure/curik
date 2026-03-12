# Repo Scaffolding

## Purpose

Document the conventions for repository directory structures used by
Curik so that agents can create, navigate, and validate course
repositories consistently.

## Directory Structures

### MkDocs Content Tree (`docs/docs/`)

All rendered course content lives under `docs/docs/`. This is the
MkDocs source directory and contains the `mkdocs.yml` configuration
alongside the Markdown pages:

```
docs/
  docs/
    mkdocs.yml
    index.md
    01-module-name/
      index.md
      01-lesson-name.md
      02-lesson-name.md
    02-module-name/
      index.md
      01-lesson-name.md
```

Module and lesson directories use numbered prefixes (`01-`, `02-`) for
ordering. Each module directory has an `index.md` that serves as the
module overview page.

### Repo-Root Lessons and Projects (Tier 3-4)

Tier 3-4 courses have student-facing repositories where students browse
files directly in GitHub or Codespaces. These courses mirror the content
into repo-root directories:

```
lessons/
  01-module-name/
    README.md
    01-lesson-name/
      README.md
      exercise.py
    02-lesson-name/
      README.md
      exercise.py
  02-module-name/
    README.md
    ...
projects/
  01-project-name/
    README.md
    starter/
    solution/
```

Each lesson directory contains a `README.md` generated from guarded
sections in the corresponding MkDocs page (see the `readme-guards`
skill). Exercise and starter code files live alongside the README.

### DevContainer Setup

Tier 3-4 courses include a `.devcontainer/` directory for GitHub
Codespaces:

```
.devcontainer/
  devcontainer.json
  Dockerfile        (optional, for custom images)
```

The `devcontainer.json` specifies the language runtime, extensions, and
any setup commands needed for the course exercises.

### Modules vs Resources

- **`modules/`** is used for structured courses (Tier 1-4) where
  content is organized into sequential modules containing lessons.
- **`resources/`** is used for resource collections (non-sequential
  reference material) where items are grouped by topic rather than
  learning order.

### Course Metadata

Every course repository has a `course.yml` at the root containing
metadata fields (title, slug, tier, grades, category, topics, etc.)
and a `CURIK_DIR/` directory (default `.curik/`) for internal state.

## File Naming Conventions

- Use numbered prefixes for ordering: `01-`, `02-`, `03-`, etc.
- Use lowercase kebab-case for directory and file names:
  `01-intro-to-variables.md`, not `01_IntroToVariables.md`.
- Module directories: `01-module-name/`
- Lesson files: `01-lesson-name.md`
- Overview files: `index.md` (MkDocs) or `README.md` (repo-root)
- Exercise files: `exercise.py`, `exercise.java`, etc. (language
  appropriate, no numbered prefix)

## Scaffolding Workflow

1. Define the course structure in the spec or outline.
2. Use `tool_scaffold_structure` to create the directory tree and
   lesson stubs from a JSON structure description.
3. Use `tool_create_lesson_stub` to add individual lessons as needed.
4. For Tier 3-4, the scaffold automatically creates `.devcontainer/`
   and the repo-root `lessons/` mirror directories.
