# Curik — Project Plan

*Draft: March 2026*

---

## 1. Project Overview

### 1.1 What Curik Is

Curik is a curriculum development tool for the League of Amazing Programmers. It is a Python package with a CLI entry point and an MCP server that runs locally inside Claude Code. A curriculum designer — who may be an instructor with subject-matter expertise but limited technical-writing or site-building experience — works interactively with an AI agent through a defined process, from course concept to fully authored, structured curriculum.

The tool enforces a lifecycle: the agent cannot skip steps because the tooling prevents it. This is the same design philosophy as CLASI (Claude Agent Skills Instructions), the software engineering process from which Curik descends: AI agents know the rules and violate them anyway, so enforcement must be mechanical, not instructional.

### 1.2 The Problem

The League teaches students from 2nd grade through 12th grade across Python, Java, robotics, and technology courses. Curriculum is currently spread across multiple site generators (Sphinx with Furo, VuePress, bare GitHub repos) with inconsistent structure. There is no standard repository layout, no shared metadata format, no automated catalog, and no process for ensuring that a new course is complete before it ships.

An AI agent told to "follow the curriculum template" will produce a lesson page that looks right but is missing the instructor guide. Or it will skip the quiz configuration. Or it will generate a `course.yml` with placeholder values that never get updated. Curik prevents these failures through gated progression: you cannot move from planning to drafting until every lesson outline has objectives; you cannot publish until all validation checks pass.

### 1.3 Relationship to CLASI

Curik is a standalone Python package, separate from CLASI, with its own CLI entry point. It draws on CLASI's patterns — MCP server, file-based state, numbered artifacts, human-approval gates — but is purpose-built for curriculum rather than software engineering. The following CLASI concepts carry over directly:

- Mechanical enforcement via MCP tools that gate phase transitions
- File-based state (no database; the filesystem is the source of truth)
- Agent specialization with hard boundaries on what each agent can do
- Human-approval gates that block progression until the designer confirms
- Numbered artifacts with defined lifecycle (active → done)

Curik does not reuse CLASI code. It is a new implementation of the same philosophy applied to a different domain.

### 1.4 Relationship to the Syllabus Tool

The existing `syl` program (`league-infrastructure/syllabus`) generates `syllabus.yaml` from the directory structure on disk. Curik does not write `syllabus.yaml` directly. It creates and manages the directory structure; `syl` is called to regenerate `syllabus.yaml` from what's on disk. `syllabus.yaml` is a derived artifact, not a primary one.

### 1.5 What Curik Does Not Do

- Write to `syllabus.yaml` directly
- Manage student identity, passphrases, or enrollment
- Build or deploy the MkDocs site (it calls `make docs` or equivalent, but does not own that process)
- Replace the `syl` tool — it depends on it
- Handle quiz execution or student assessment — quiz configuration is an authoring artifact; the quiz runtime is a separate system

---

## 2. The League's Curriculum Landscape

### 2.1 Curriculum Tiers

The League's courses span four tiers based on student age and the role of technology in delivery.

| Tier | Grades | Examples | Technology Role |
|------|--------|----------|-----------------|
| 1 | 2–3 | Robotics Explorers (Edison robots) | No student computers. Repo contains only `docs/` for instructor guide. |
| 2 | 3–5 | MakeCode Arcade, Robot Riot, Intro Python via Trinket | Website links to external platforms. Some repos include starter code. |
| 3 | 6–10 | Python Apprentice, Python Games, Java Levels 0–5 | Curriculum lives in the repo (Jupyter notebooks, code files). Students clone into Codespaces/Code Server. Website is navigation aid only. |
| 4 | 10–12 | Advanced Java, AP Prep, Portfolio, Projects, Internships | Reference documentation, project specs. Students work independently. |

### 2.2 Course Taxonomy

Every course has two independent dimensions: delivery format and pedagogical structure.

**Delivery Formats:**

- **Website with lessons** — student reads MkDocs pages and does exercises separately
- **Website with interactive lessons** — embedded Pyodide or similar for in-browser execution
- **Website linking to third-party platform** — instructions and context on our site, work happens on MakeCode Arcade, Trinket, etc.
- **Repository with code** — student clones repo into Codespaces/Code Server, works through notebooks or code files; website is orientation only
- **Activity / instructor-delivered** — hands-on, physical, exploratory; the curriculum artifact is primarily an instructor guide

**Pedagogical Structures:**

- **Activity** — structured hands-on task (build this circuit, follow these steps)
- **Have Fun** — inspiration and exposure, not formal skill-building; loose structure, no formal learning objectives beyond engagement
- **Sequential Lessons** — each lesson covers a distinct topic, lessons build on each other
- **Challenge-Based** — problems to solve with multiple valid solutions and embedded learning objectives
- **Single Project** — one substantial project, not broken into guided steps; learning happens ad hoc with instructor support
- **Progressive Project** — one project built over the course, adding complexity each session; organized into modules

Most real courses are hybrids. The taxonomy provides the vocabulary; the course design combines structures as needed.

**Structural Units:**

- **Module** — a group of related lessons forming a coherent chunk
- **Lesson** — a single session's worth of work
- **Assignment/Exercise** — work within or after a lesson with a defined correct outcome
- **Challenge** — an open-ended problem, possibly spanning multiple sessions
- **Project** — substantial open-ended work, potentially spanning many sessions

### 2.3 Standard Repository Structure

Every course is a GitHub repository. Every repo contains a `docs/` directory that builds to a website with MkDocs Material. Code-based courses also include student working files.

**Tier 1–2 (website only):**

```
robotics-explorers/
├── docs/
│   ├── mkdocs.yml
│   ├── docs/
│   │   ├── index.md
│   │   ├── instructor.md       # sets cookie, enables guide sections
│   │   ├── lessons/
│   │   │   ├── 01-meet-your-robot.md
│   │   │   └── ...
│   │   └── assets/
│   │       ├── instructor.js   # cookie check, show/hide logic
│   │       └── instructor.css  # .instructor-guide { display: none }
│   └── overrides/
├── course.yml
└── README.md
```

**Tier 3–4 (website + student code):**

```
python-apprentice/
├── docs/
│   ├── mkdocs.yml
│   ├── docs/
│   │   ├── index.md
│   │   ├── instructor.md
│   │   ├── lessons/
│   │   └── assets/
│   └── overrides/
├── lessons/
│   ├── 01-variables/
│   │   ├── lesson.ipynb
│   │   └── exercises.ipynb
│   └── 02-loops/
├── .devcontainer/              # Codespaces / Code Server config
├── course.yml
└── README.md
```

The `syl` tool reads the lesson directory structure and generates `syllabus.yaml`. The canonical structure that `syl` expects:

```
CourseRepo/
  ModuleName/
    README.md                     # Module overview
    01_LessonName.md              # Lesson text
    01_LessonName.py              # Exercise file
    02_LessonName.ipynb           # Notebook
  course.yml
  syllabus.yaml                   # Generated by syl
  docs/
  .course/
```

### 2.4 Instructor Guide: Inline, Not Separate

The instructor guide is embedded directly in lesson pages inside a marked section hidden by default and revealed when the instructor enables "instructor mode."

```markdown
# Lesson 1: Variables

Student-facing content here...

<div class="instructor-guide" markdown>

**Objectives**: Students can assign variables and identify types.

**Timing**: 30 minutes — 10 on explanation, 20 on exercises.

**Common mistakes**: Using = vs ==. Forgetting quotes on strings.

**If students are ahead**: Have them explore input().

</div>
```

The `markdown` attribute tells MkDocs Material to process Markdown inside the div. CSS hides `.instructor-guide` by default. A JavaScript file checks for a browser cookie; if present, it adds a class to the body that makes instructor sections visible.

The instructor enables this by visiting `/instructor` on the site, which sets the cookie. There is no login or authentication — the guide content is teaching notes, not sensitive material.

Required instructor guide fields per lesson:

- **Objectives** — what students should be able to do after this lesson
- **Materials** — what to have ready (hardware, accounts, printed handouts)
- **Timing** — estimated duration and suggested pacing
- **Key concepts** — what to explain verbally, with suggested language
- **Common mistakes** — what students typically get wrong
- **Assessment cues** — how to tell if students understood
- **Differentiation** — suggestions for students who are ahead or behind

For Tier 1 (youngest students), the instructor guide sections are the primary content — student-facing parts may be minimal or empty. For Tiers 3–4, the guide is supplementary.

### 2.5 Course Metadata

Every repo has a `course.yml` at the root:

```yaml
title: Python Apprentice
slug: python-apprentice
tier: 3
grades: "6-10"
category: python
topics:
  - programming
  - python
  - certification
prerequisites:
  - intro-python
lessons: 12
estimated_weeks: 24
curriculum_url: https://python-apprentice.jointheleague.org
repo_url: https://github.com/league-curriculum/Python-Apprentice
description: >
  The first course in Python, covering the basics of the language
  and preparing students for PCEP certification.
```

This file is read by the curriculum registry, used by Curik to validate course completeness, and consumed by the main website build to generate catalog pages.

### 2.6 Website Framework

All curriculum sites use MkDocs with the Material theme.

Rationale: Markdown-native (no templates or build tooling for the designer to learn), Python-based (consistent with the League's primary language), good defaults (admonitions, code highlighting, tabs, search, responsive layout), AI-friendly (plain Markdown with YAML frontmatter is the easiest format for an LLM to generate and validate).

Deployment is via GitHub Pages using a GitHub Action on push to main.

---

## 3. The Curriculum Development Process

This is the process model that Curik implements. A content developer works interactively with an AI agent through each phase, from "I have an idea for a class" to a complete course specification. The specification is the input to a second phase — content production — where individual lessons, the website, and the repository are created.

### 3.1 Phase 1: Spec Development

The Curriculum Architect agent drives a structured conversation through five sub-phases. The agent edits `.course/spec.md` live throughout.

#### 1a. Course Concept

The content developer describes the idea. The agent helps clarify and document:

- **Target students** — grade range, prerequisites, experience level
- **Educational goals** — what students should be able to do after this course
- **Student and parent goals** — the League charges tuition; educational goals are necessary but not sufficient. What do students want? What do parents expect? For younger kids, "my child is excited about technology" matters as much as "my child can write a for loop." For older students, certification, college prep, or portfolio pieces may be the draw.
- **Learning outcomes** — specific, observable outcomes where applicable. Not "understand loops" but "write a program that uses a for loop to iterate over a list." Some course types (activity / have fun) may not have formal learning outcomes.
- **Format** — Tech Club (90 min, fun/exploratory), semester course (6–10 sessions, after school), summer program (multi-week intensive), persistent/open-ended (own pace)
- **Rough scope** — how many sessions, how long each, fixed endpoint or open-ended

Output: a written course concept — a few paragraphs plus structured summary.

#### 1b. Pedagogical Model

Before deciding *what* to teach, decide *how* the class runs. The model shapes everything downstream.

The content developer and agent choose delivery format and pedagogical structure(s) from the taxonomy. Decisions include:

- How is a single session structured? (Explain → demonstrate → practice? Present challenge → explore → debrief?)
- What does assessment look like? (Quizzes? Completed exercises? Working project? No formal assessment?)
- How do we handle students who are ahead or behind?
- What structural units does this course use?

Output: description of chosen format, structure, and reasoning.

#### 1c. Research

The Research Agent investigates what exists in the space. Research serves several purposes: discover alignment candidates (standards, certifications, external syllabi), validate scope and sequencing, find usable resources (tutorials, exercises, project ideas), identify pedagogical patterns, and spot gaps.

Types of resources:

- Standards documents and certification syllabi
- Existing tutorials and courses (free and commercial)
- Textbooks and reference materials
- Exercise and problem sets
- Project ideas and starter code

Resources fall into two categories: **linked resources** (external content we point students at directly) and **adapted resources** (external content we use as inspiration but rewrite into our own format).

Research may happen in multiple rounds — an initial broad survey, then more targeted research after the alignment decision.

Output: research summary — what was found, what's relevant, what we recommend using and how. Includes candidate alignments.

#### 1d. Alignment Decision

Based on research, the content developer decides whether and how to align the course. A course may align to:

- **Certification or exam** — AP CS A, PCEP, AWS Cloud Practitioner
- **External course** — Harvard CS50, freeCodeCamp web dev curriculum
- **External tutorials or resources** — MakeCode Arcade built-in tutorials, a Trinket course
- **Self-defined topic list** — we decide what topics to cover based on our own judgment
- **No alignment** — some short-format classes (Tech Clubs, one-off workshops)

Alignment can be layered. A Python Apprentice course aligns to PCEP *and* uses specific sourced tutorials.

Output: alignment statement — what the course aligns to, why, plus the specific topic list or syllabus.

#### 1e. Spec Synthesis

Assembles the full course specification from prior sub-phase outputs. Sections:

1. **Course Overview** — concept, goals, target students, format, duration
2. **Pedagogical Approach** — delivery format, structure, session format, assessment
3. **Alignment and Standards** — alignment targets, topic list, mapping
4. **Research and Resources** — key findings, external resources to link or adapt
5. **Course Structure Outline** — varies by pedagogical structure (see below)
6. **Assessment Plan** — quiz structure, project milestones, progress tracking
7. **Technical Decisions** — tier, delivery format, platform, content format, lesson format, special requirements

The course structure outline section varies by pedagogical structure:

- **Activity courses**: the set of activities with materials, timing, instructions, student output
- **Have Fun courses**: loosely structured sessions with engagement focus
- **Sequential Lessons**: modules and lessons, each with title, topics, objectives, description, resources, duration
- **Challenge-Based**: sequence of challenges with problem summaries, embedded objectives, difficulty, solution approaches
- **Single Project**: project description, prerequisites, difficulty points, instructor interventions
- **Progressive Project**: project description, then modules with concepts, sessions, and what gets built
- **Hybrid**: combination with clear indication of which parts use which structure

This is an outline, not content. Actual lesson pages are produced in Phase 2.

**Gate:** The agent cannot proceed to Phase 2 until all required spec sections are present and non-empty.

### 3.2 Phase 1 → Phase 2 Handoff: Initial Change Plan

When the spec is approved, the agent produces `change-plan/active/001-initial-build.md`. This document lists every module, every lesson, and a stub description of what each lesson contains. The designer reviews and approves this plan. Approval triggers Phase 2 scaffolding.

### 3.3 Phase 2: Scaffold and Draft

**Scaffold:** The agent creates the directory structure and stub files from the approved change plan. `syl` runs and generates `syllabus.yaml`. The MkDocs development server starts. The site is navigable from this point, even with stub content.

**Outline:** Before writing full lesson content, the agent produces outline documents in `.course/outlines/` — one per module or one for the whole course, depending on size. Each outline describes what each lesson covers, key concepts, learning objectives, and how lessons connect. The designer reviews and approves outlines before drafting begins.

**Draft:** The appropriate Lesson Author writes lessons module by module, in order. The designer can review as lessons arrive or batch-review a module at a time.

### 3.4 Ongoing: The Change Cycle

After the initial draft, the process enters a steady-state cycle:

1. **Comment** — the designer reads lessons, uses the site, works through coursework. Change requests are filed as numbered issues in `.course/issues/open/`.
2. **Collect** — at intervals, the designer asks the agent to collect open issues into a change plan. The agent reads all open issues and synthesizes them into a numbered document in `.course/change-plan/active/`. Structural moves are listed first, per-lesson content changes second.
3. **Approve** — the designer reviews the change plan. Approval is recorded in the document. The agent cannot execute without approval.
4. **Execute** — the agent works through the change plan in order: file moves and renaming first, then content changes, then `syl` regenerates `syllabus.yaml`.
5. **Review** — the Reviewer checks the change plan line by line and confirms each item is complete. Gaps are flagged as new issues.
6. **Close** — the change plan moves to `change-plan/done/`, resolved issues move to `issues/done/`. The cycle restarts.

---

## 4. Architecture

### 4.1 Package Structure

Curik is a standalone Python package, pip-installable, with a CLI entry point (`curik`) and an MCP server. It follows the same structural pattern as CLASI: content assets (agent definitions, skill definitions, templates) are bundled inside the package and served via the MCP server.

### 4.2 Runtime Environment

Curik runs locally inside Claude Code. The MCP server is configured at init time and runs in the Claude Code sidebar. The curriculum designer interacts with the agent in the Claude Code chat; the agent uses Curik's MCP tools to enforce process and edit files.

### 4.3 State Model

There is no database. State is entirely file-based. The `.course/` directory inside the curriculum repo is the state container. The filesystem is the source of truth.

This is a deliberate departure from CLASI, which uses a SQLite state database. CLASI's experience showed that the database's graceful degradation (all enforcement disappears silently when the DB is unavailable) undermined the enforcement model. A file-based state model is simpler: state is always visible, always inspectable, and never silently absent.

Phase tracking, issue status, and change plan status are all determined by reading the filesystem — which directory a file lives in, what frontmatter values are set, whether required sections exist and are non-empty.

### 4.4 `.course/` Directory Structure

```
.course/
  spec.md                   # Live spec document, edited throughout Phase 1
  overview.md               # Course overview, maintained alongside spec
  outlines/                 # Module and lesson outlines, produced before drafting
  change-plan/
    active/                 # Change plans currently in progress
    done/                   # Completed change plans (archived, not deleted)
  issues/
    open/                   # Numbered issue files, one per comment or change request
    done/                   # Resolved issues
```

### 4.5 Initialization: `curik init`

Running `curik init` in a new directory:

1. Creates the GitHub repository
2. Scaffolds the `.course/` directory with initial state files
3. Writes agent instruction files and skill files for Claude Code
4. Configures `.mcp.json` to point at the Curik MCP server
5. Creates a stub `course.yml` with placeholder metadata
6. Starts Phase 1 — the agent immediately begins the course concept conversation

From this point the designer is working in the real repo. There is no separate planning environment that later gets migrated.

---

## 5. Agents

Curik uses six specialized agents, adapted from CLASI's agent specialization model. Each agent has hard boundaries on what it can and cannot do, reducing cognitive load at each decision point and limiting the blast radius of a single agent's process violation.

### 5.1 Curriculum Architect

Orchestrates the full process. Drives Phases 1a, 1b, 1d, and 1e — course concept conversation, pedagogical model decisions, alignment decisions, and spec synthesis. The human talks to this agent. It edits `.course/spec.md` and `.course/overview.md` live as the conversation progresses.

**Can:** orchestrate the process, edit spec and overview documents, create change plans, delegate to other agents.

**Cannot:** write lesson content directly, write quiz configuration, run validation.

### 5.2 Research Agent

Phase 1c only. Web-search heavy. Finds certification syllabi, existing courses, tutorials, pedagogical patterns, and alignment candidates. Invoked by the Curriculum Architect, produces a structured research summary, and returns. Stateless between invocations.

**Can:** search the web, summarize findings, recommend resources and alignments.

**Cannot:** edit spec documents, write lesson content, make alignment decisions.

### 5.3 Lesson Author — Young (Tiers 1–2)

Writes for grades 2–5. Knows that the instructor guide is often the primary content. Student-facing text is minimal or absent for Tier 1. Activities are physical and hands-on. Voice and structure are calibrated for a teacher reading from a guide in front of a classroom, not a student reading a screen.

**Can:** write lesson pages, write instructor guide sections, create activity descriptions.

**Cannot:** edit the spec, create change plans, modify course structure.

### 5.4 Lesson Author — Older (Tiers 3–4)

Writes for grades 6–12. Produces Markdown lesson pages and Jupyter notebooks. Knows the inline instructor guide section format. Handles sequential lessons, challenge problems, and progressive project structures. Can produce working code examples and exercises.

**Can:** write lesson pages, write notebooks, write instructor guide sections, write code examples.

**Cannot:** edit the spec, create change plans, modify course structure.

### 5.5 Quiz Author

Creates `quiz.yml` for each lesson. Aligns question topics to lesson objectives. Knows the question type taxonomy: multiple choice, code output, code write, code fix. Validates alignment against the lesson before marking a quiz done.

**Can:** create quiz configuration, validate quiz-to-lesson alignment.

**Cannot:** write lesson content, edit the spec, modify course structure.

### 5.6 Reviewer

Runs validation. Checks structural completeness: instructor guide sections present and non-empty, lesson objectives exist, quiz config covers lesson topics, MkDocs builds clean, `syllabus.yaml` is consistent with the directory structure. Produces a validation report. Approves or blocks publication.

**Can:** run validation checks, produce reports, flag issues.

**Cannot:** write content, edit the spec, fix issues (only identifies them).

---

## 6. Skills

Skills are structured workflows — step-by-step procedures that agents follow. They are the primary mechanism for ensuring consistent execution.

### 6.1 Phase 1 Skills (Curriculum Architect)

| Skill | Purpose |
|-------|---------|
| `course-concept` | Question sequence for Phase 1a: required fields, document format, how to probe for student/parent goals |
| `pedagogical-model` | Delivery format taxonomy, pedagogical structure taxonomy, session structure decisions |
| `alignment-decision` | How to map research findings to a topic list; layered alignment patterns |
| `spec-synthesis` | How to assemble the complete Phase 5 document from prior phase outputs |
| `structure-proposal` | How to go from an approved spec to a concrete module/lesson skeleton |

### 6.2 Content Skills

| Skill | Purpose |
|-------|---------|
| `lesson-writing-young` | Voice, format, activity structure, instructor guide requirements for Tiers 1–2 |
| `lesson-writing-older` | Lesson page format, notebook structure, inline instructor guide sections, code example standards for Tiers 3–4 |
| `instructor-guide-sections` | Required fields (objectives, materials, timing, key concepts, common mistakes, assessment cues, differentiation) and what good looks like in each |
| `quiz-authoring` | Schema, question types, alignment checking procedure |

### 6.3 Infrastructure Skills

| Skill | Purpose |
|-------|---------|
| `repo-scaffolding` | Directory structure by tier, stub file templates, `mkdocs.yml` generation |
| `status-tracking` | `.course/` directory structure, issue and change plan file formats, state transitions |

### 6.4 Validation Skill

| Skill | Purpose |
|-------|---------|
| `validation-checklist` | What "complete" looks like at lesson, module, and course level |

---

## 7. MCP Tools

The MCP server exposes the following tools. All tools that modify state do so by editing files in the repo or `.course/` directory.

### 7.1 Initialization

| Tool | Description |
|------|-------------|
| `init_course` | Creates `.course/` directory, seeds spec files, configures MCP, writes agent and skill files |
| `get_course_status` | Top-level summary: current phase, open issues count, active change plans |

### 7.2 Phase 1: Spec

| Tool | Description |
|------|-------------|
| `get_phase` | Returns current phase and what gates must be met to advance |
| `advance_phase` | Gated phase transition; fails with a reason if requirements are not met |
| `update_spec` | Write or update a named section of the spec document |
| `get_spec` | Read the current spec, optionally a specific section |
| `record_course_concept` | Structured save of Phase 1a output: tier, grade range, format, goals, scope |
| `record_pedagogical_model` | Saves delivery format and structural choices from Phase 1b |
| `record_alignment` | Saves alignment decision and topic list from Phase 1d |

`advance_phase` is the enforcement mechanism. It checks that all required sections of `spec.md` are present and non-empty before allowing the transition from Phase 1 to Phase 2. The check is not "does the file exist" but "does the section contain real content" — the same pattern as CLASI's template-placeholder detection, where ≥3 placeholder markers indicate an unfilled template.

### 7.3 Research

| Tool | Description |
|------|-------------|
| `web_search` | Searches for syllabi, certifications, existing courses, tutorials |
| `save_research_findings` | Persists structured research output: sources, alignment candidates, resource list |
| `get_research_findings` | Read back findings for use in alignment decisions |

### 7.4 Scaffolding

| Tool | Description |
|------|-------------|
| `scaffold_structure` | Creates the module/lesson directory tree from an approved change plan |
| `create_lesson_stub` | Creates stub `.md` and/or exercise file for a specific lesson |
| `regenerate_syllabus` | Runs `syl` to rebuild `syllabus.yaml` from the current directory state |
| `get_syllabus` | Reads `syllabus.yaml` (read-only from Curik's perspective) |

### 7.5 Outlines

| Tool | Description |
|------|-------------|
| `create_outline` | Writes a module or course outline to `.course/outlines/` |
| `approve_outline` | Human-gated; records outline approval, enables drafting |

### 7.6 Issue and Change Plan Management

| Tool | Description |
|------|-------------|
| `create_issue` | Writes a numbered file to `issues/open/` |
| `list_issues` | Returns all open issues, optionally filtered by module or lesson |
| `create_change_plan` | Synthesizes open issues into a change plan document in `change-plan/active/` |
| `approve_change_plan` | Records approval in the change plan document; enables execution |
| `execute_change_plan` | Agent works through the plan: moves first, then content edits, then `syl` |
| `review_change_plan` | Reviewer checks completion line by line, flags gaps as new issues |
| `close_change_plan` | Moves change plan to `done/`, moves resolved issues to `done/` |

### 7.7 Validation

| Tool | Description |
|------|-------------|
| `validate_lesson` | Checks instructor guide section present and non-empty, objectives present, file referenced in `syllabus.yaml` |
| `validate_module` | Checks all lessons pass `validate_lesson`, module overview exists |
| `validate_course` | Full pre-publication check: all modules valid, `course.yml` complete, MkDocs builds, `syllabus.yaml` consistent |
| `get_validation_report` | Reads the last saved validation run |

### 7.8 Quiz

| Tool | Description |
|------|-------------|
| `generate_quiz_stub` | Creates a `quiz.yml` skeleton pre-populated with lesson topics |
| `validate_quiz_alignment` | Checks quiz topics cover lesson objectives; flags gaps |
| `set_quiz_status` | Marks quiz config as `drafted`, `reviewed`, or `complete` |

---

## 8. Enforcement Model

### 8.1 Design Philosophy

CLASI's core finding across 15 sprints and 8 formal reflections: every single process failure was categorized as `ignored-instruction`. The agent knew the rules and violated them anyway. CLASI responded with three interlocking strategies that Curik adopts:

1. **Mechanical enforcement (process-as-code)** — MCP tools gate phase transitions and validate preconditions. The agent cannot advance past Phase 1 until the spec is complete. The agent cannot execute a change plan without recorded approval.

2. **Behavioral scaffolding (process-as-instructions)** — Agent definitions and skill files contain explicit decision trees, not vague guidelines. Binary decision points rather than judgment calls.

3. **Agent specialization (divide and conquer)** — Six agents with hard boundaries. The Curriculum Architect cannot write lesson content. The Lesson Author cannot modify course structure. This limits the blast radius of any single agent's process violation.

### 8.2 Enforcement Points

| Enforcement Point | What It Prevents | Type |
|--------------------|-----------------|------|
| `advance_phase` spec completeness check | Proceeding to content production with an incomplete spec | Mechanical |
| `approve_change_plan` gate | Executing changes without designer approval | Mechanical |
| `approve_outline` gate | Drafting lessons without approved outlines | Mechanical |
| `validate_lesson` instructor guide check | Publishing lessons without instructor guide sections | Mechanical |
| `validate_course` pre-publication check | Publishing an incomplete course | Mechanical |
| Agent role boundaries | Curriculum Architect writing lessons, Lesson Author modifying structure | Behavioral |
| Skill step sequences | Skipping intermediate steps in a workflow | Behavioral |

### 8.3 What Is Not Mechanically Enforced

Some CLASI enforcement gaps are instructive. CLASI's "Definition of Done" for tickets — a 6-point checklist — was entirely behavioral and was the most frequently violated rule in the process. Curik should learn from this:

- Lesson completeness (instructor guide present, objectives present) is mechanically checked by `validate_lesson`. This is the equivalent of making the Definition of Done a blocking gate rather than an advisory check.
- Change plan execution order (moves first, then content, then `syl`) is behavioral. The tool does not physically prevent the agent from editing content before completing file moves. But the consequence of violation is lower than in CLASI's case — a file in the wrong directory is less damaging than a merged branch with untested code.

---

## 9. Quiz System Interface

The quiz system is a separate application developed independently. Curik handles only the authoring-side interface: the `quiz.yml` configuration that lives in the curriculum repo.

### 9.1 Quiz Configuration Schema

```yaml
course: python-apprentice
version: 1

lessons:
  - id: 01-variables
    topics:
      - variable assignment
      - data types (int, str, float, bool)
      - type() function
    difficulty: beginner
    question_types:
      - multiple_choice
      - code_output     # "What does this code print?"
      - code_write      # "Write code that does X"
      - code_fix        # "Fix the bug in this code"
    example_questions:
      - type: code_output
        code: |
          x = 5
          y = "hello"
          print(type(x), type(y))
        answer: "<class 'int'> <class 'str'>"
    code_execution:
      language: python
      timeout_seconds: 10
      allowed_imports: []
```

The configuration specifies which topics each lesson covers, expected difficulty, question types, optional example questions, and code execution constraints. The quiz application uses this configuration plus lesson content to generate questions dynamically — quizzes are never identical across attempts.

### 9.2 Curik's Role

Curik's Quiz Author agent creates and maintains `quiz.yml`. The `validate_quiz_alignment` tool checks that quiz topics cover lesson objectives. Curik does not execute quizzes, grade students, or interact with the quiz runtime.

---

## 10. Student Identity and External Systems

Curik does not manage student identity, but the curriculum it produces must work within the League's identity model.

**Under 13:** Students are identified by passphrase, not name or PII. Younger students (grades 2–5) get playful passphrases ("Four Green Frogs"). Older students (grades 6–8, under 13) get CS-themed passphrases. The passphrase is the student's identity across all League systems.

**13 and over:** Students are identified by their GitHub account, which they need for Codespaces and Code Server.

**Parent engagement:** Parents view progress by entering the child's passphrase (under 13) or through the GitHub-linked dashboard (13+).

These are not implementation concerns for Curik. They are context for understanding why the curriculum sites do not have login walls and why the instructor guide uses a cookie-based reveal rather than authentication.

---

## 11. Curriculum Registry

The curriculum registry is a lightweight service that keeps track of all League curriculum repos and their metadata.

1. Each curriculum repo has a `course.yml` with metadata.
2. A GitHub Action fires on push to main, reads `course.yml`, and posts metadata to the registry.
3. The registry stores the metadata. The simplest implementation is a JSON file in a dedicated GitHub repo; a more capable version is a small API service.
4. The main League website queries the registry at build time and generates curriculum catalog pages — replacing the manually maintained list at `curriculum.jointheleague.org`.

From the user's perspective: browse classes on `jointheleague.org` → click on Python Apprentice → see description, schedule, enrollment → also see a "Curriculum" link → click through to `python-apprentice.jointheleague.org`.

Curik's `validate_course` checks that `course.yml` is complete and well-formed. The registry and GitHub Action are separate infrastructure.

---

## 12. Codespaces and Code Server

Tier 3 and Tier 4 courses expect students to work in a cloud development environment.

- **GitHub Codespaces** — standard offering. `.devcontainer/` configures the environment.
- **Code Server** — the League's own VS Code Online deployment on Docker Swarm, for students under 13 or when Codespaces quotas are a concern.

Curriculum repos must work in both environments. The `.devcontainer/` configuration should be sufficient for Codespaces, and Code Server should use the same repo structure without modification.

Curik's `repo-scaffolding` skill generates the appropriate `.devcontainer/` configuration based on the course tier and platform choices recorded in the spec.

---

## 13. Open Design Questions

These are decisions that need to be made during or before implementation. They are recorded here rather than resolved, because each involves tradeoffs that benefit from implementation experience.

1. **Does the initial change plan go through the full comment → collect → approve cycle, or is it a direct output of Phase 1 approval?** Probably direct output, to avoid the bootstrapping awkwardness of filing issues before any content exists.

2. **How does the Reviewer agent get invoked — explicitly by the designer, or automatically at close time?** An explicit invocation is simpler and more predictable.

3. **What is the right granularity for outlines — one per module, or one document for the whole course?** Probably per module for larger courses, whole-course for short ones. The agent should propose based on lesson count.

4. **Where do projects and challenges fit in the lesson numbering scheme?** Challenges can map naturally to exercises. Projects that span multiple lessons may need a different structural unit in the directory layout.

5. **MkDocs nav structure: auto-generated or explicitly defined in `mkdocs.yml`?** Explicit is more reliable but requires maintenance. Auto-generated is lower friction but can produce surprising ordering.

6. **Subdomain vs. path for course sites**: `course-name.jointheleague.org` (current pattern, easier with GitHub Pages) vs. `jointheleague.org/curriculum/course-name` (requires monorepo or reverse proxy).

7. **Code Server integration**: Is the `.devcontainer/` config sufficient for Code Server, or does it need its own config?

---

## 14. Migration Plan

Existing curriculum needs to be consolidated from multiple generators and inconsistent structures into the standard Curik-managed format.

1. **Inventory** — catalog every existing course repo, its current generator, tier, and content completeness.
2. **Template** — create a template repo for each tier with the standard structure, MkDocs config, GitHub Actions for deployment, and `course.yml`.
3. **Migrate content** — for each existing course, copy lesson content into the standard structure, convert RST to Markdown where needed, add stub instructor guide sections.
4. **Deploy** — point DNS or GitHub Pages to the new MkDocs sites. Retire old Sphinx/VuePress builds.
5. **Registry** — set up the GitHub Action and registry. Update the main website to pull from the registry.

This should be phased — start with one course per tier as proof of concept, then migrate the rest.

---

## 15. Artifact Checklist

At the end of the spec development process (Phase 1), the content developer should have:

- [ ] Course concept document (Phase 1a)
- [ ] Pedagogical model description (Phase 1b)
- [ ] Research summary with candidate alignments (Phase 1c)
- [ ] Alignment decision (Phase 1d)
- [ ] Complete course specification (Phase 1e), containing all of the above plus course structure outline, assessment plan, and technical decisions

These may be sections of one document (`.course/spec.md`) or separate documents. What matters is that the information exists and has been reviewed before content production begins.
