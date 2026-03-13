# Course Taxonomy

This document defines the structural vocabulary for League courses:
delivery formats, pedagogical structures, tiers, and structural units.

## Tiers

Tiers define the target audience and shape everything — content
complexity, site structure, instructor guide style, and tooling.

| Tier | Grades | Programming Style | Key Characteristics |
|------|--------|-------------------|---------------------|
| 1 | K–2 | Unplugged, visual | Physical activities, no screens, instructor-led |
| 2 | 3–5 | Block-based, visual | Scratch/block programming, guided projects |
| 3 | 6–8 | Text-based, introductory | Python/JS basics, notebooks, scaffolded exercises |
| 4 | 9–12 | Text-based, advanced | Full applications, testing, version control |

### Tier Implications

| Feature | Tier 1–2 | Tier 3–4 |
|---------|----------|----------|
| Content layout | Instructor-guide-primary | Student content + inline instructor guide |
| Site generator | Hugo with instructor-guide layout | Hugo with standard layout |
| Notebook mirrors | No | Yes (.ipynb companion files) |
| Syllabus integration | No (course.yml only) | Yes (syllabus.yaml + jtl-syllabus) |
| README guards | No | Yes (readme-shared, readme-only shortcodes) |
| Lesson mirror dirs | No | Yes (lessons/, projects/) |

## Course Types

| Type | Description | Phase 1 Differences |
|------|-------------|---------------------|
| `course` | Full curriculum with pedagogical structure | All 5 sub-phases |
| `resource-collection` | Curated set of resources, guides, or references | Skips 1b (pedagogical model) and 1d (alignment) |

## Delivery Formats

The delivery format describes how content reaches students:

- **In-person class** — instructor-led, scheduled sessions
- **Self-paced online** — student works independently
- **Hybrid** — mix of in-person and online components
- **Workshop** — intensive single or multi-day session
- **Camp** — week-long immersive program (common at the League)

## Pedagogical Structures

How lessons are organized within modules:

- **Project-based** — each module builds toward a culminating project
- **Concept-based** — each module covers a concept cluster
- **Spiral** — concepts revisited at increasing depth
- **Problem-based** — lessons structured around problems to solve

## Structural Units

### Course

The top-level container. Has a `course.yml` with metadata:
- title, slug, uid
- tier, grade range, category
- topics list
- language (tier 3–4)

### Module

A thematic grouping of lessons. Named with numeric prefix: `01-intro/`.
Contains `_index.md` (branch bundle) with module title and weight.

### Lesson

A single learning session. Named with numeric prefix: `01-hello.md`.
Contains frontmatter (title, weight, draft) and content with
instructor guide shortcode.

### Exercise

An embedded or standalone practice activity within a lesson.

### Quiz

A `quiz.yml` configuration file associated with a lesson. Contains
questions aligned to lesson objectives.

## Naming Conventions

- **Directories**: lowercase, hyphenated, numeric prefix (e.g., `01-intro/`)
- **Files**: lowercase, hyphenated, numeric prefix (e.g., `01-variables.md`)
- **Branch bundles**: always `_index.md`
- **Course root**: always `content/` for Hugo content
