---
name: pedagogical-model
description: Delivery format and pedagogical structure decisions for Phase 1b
---

# Pedagogical Model Skill (Phase 1b)

Guide the designer through choosing how the class runs before deciding
what to teach. The model shapes everything downstream.

## Delivery Format Options

- **Website with lessons** — student reads MkDocs pages, exercises separate
- **Website with interactive lessons** — embedded Pyodide for in-browser execution
- **Website linking to third-party platform** — MakeCode Arcade, Trinket, etc.
- **Repository with code** — students clone into Codespaces/Code Server
- **Activity / instructor-delivered** — hands-on, physical, exploratory

## Pedagogical Structure Options

- **Activity** — structured hands-on tasks (build this circuit, follow steps)
- **Have Fun** — inspiration and exposure, loose structure, engagement focus
- **Sequential Lessons** — topics build on each other, each lesson distinct
- **Challenge-Based** — problems with multiple valid solutions
- **Single Project** — one substantial project, learning happens ad hoc
- **Progressive Project** — one project built over the course, adding complexity

Most courses are hybrids. Help the designer combine structures as needed.

## Session Structure Questions

1. "How does a single session run? Explain-demonstrate-practice? Present
   challenge-explore-debrief? Something else?"
2. "What does assessment look like? Quizzes? Completed exercises? Working
   project? No formal assessment?"
3. "How do you handle students who are ahead or behind?"
4. "Which structural units does this course use?" (modules, lessons,
   assignments, challenges, projects)

## Tier Determination

Based on grade range (from Phase 1a) and delivery format:
- Tier 1 (grades 2-3): No student computers, instructor guide primary
- Tier 2 (grades 3-5): Website links to external platforms
- Tier 3 (grades 6-10): Repo with code, notebooks, Codespaces
- Tier 4 (grades 10-12): Reference docs, independent work

## Recording

Format choices into a structured description and call
`record_pedagogical_model` with the content.
