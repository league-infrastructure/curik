# Curik User Guide

*For Curriculum Developers*

*Draft — 2026-03-12*

---

## What This Document Is

This guide walks you through using Curik to build curriculum for the League. It covers everything from installation through ongoing updates. It's written from your perspective — what you do, what you see, what choices you make.

There is a companion document — the AI agent guide — that describes the process from the agent's side. You don't need to read it, but it exists so the agent knows how to work with you.

---

## Who You Are

You're a curriculum developer. You might be an instructor who's been teaching a class for years and wants to get the curriculum into proper shape. You might be someone designing a new class from scratch. You might be someone who found a great open-source curriculum and wants to adapt it for the League.

You don't need to be a developer. You need to know what you want to teach. Curik and the AI agent handle the repository structure, the MkDocs site, the file formats, and the mechanical parts of curriculum production. You handle the educational decisions.

---

## Installation

Install Curik with pipx:

```bash
pipx install curik
```

This gives you the `curik` command. You'll use it exactly once to set up a project. After that, you work entirely through Claude Code.

---

## Starting a New Project

### Create the Repository

Start with a GitHub repository. This can be a brand new empty repo or an existing repo that already has curriculum content in it. Clone it locally and `cd` into it.

### Run `curik init`

```bash
curik init
```

This does several things:

1. Creates the `.course/` directory where Curik tracks its state
2. Writes agent instruction files and skill files for Claude Code
3. Configures `.mcp.json` so Claude Code can talk to the Curik MCP server
4. Creates a stub `course.yml` with placeholder metadata

When it finishes, it prints a message telling you what to do next. Something like:

```
Curik is ready. Open Claude Code in this directory and say:

  "Start Curik"
```

### Starting the Agent

Open Claude Code in the repository directory and type the phrase `curik init` displayed — e.g., **"Start Curik"**. This is a plain-language message to the agent, not a slash command. That's deliberate. The agent needs enough context to reason about what's expected. When it sees this phrase, it does two things:

1. **Verifies the Curik MCP server is correctly installed.** The agent checks that it can reach the Curik MCP server and that the `.course/` directory exists. If something is wrong — the MCP server isn't configured, the `.course/` directory is missing, `curik init` didn't complete — the agent tells you what's broken and how to fix it.

2. **Begins the initiation process.** If everything checks out, the agent looks at your repository and figures out which situation you're in.

**Empty repo:** You're starting from scratch. The agent jumps straight into Phase 1 — the course concept conversation. It starts asking you questions about what you want to build.

**Repo with existing content:** The agent notices you have files that aren't Curik-related. It asks you: "I see existing content in this repo. Should I sequester these files and use them as a reference while we rebuild?"

You should almost always say yes.

---

## Working with Existing Content

When you say yes to sequestering, the agent moves your existing files into an `_old/` directory. Nothing is deleted. The original content is preserved as-is, and the agent will read from it throughout the process.

"Existing content" doesn't have to be your own legacy curriculum. It could be:

- An old version of a class you've been teaching
- An open-source curriculum you downloaded (e.g., an AP Computer Science course you want to adapt)
- A collection of lesson plans, slides, or notes you've assembled from various sources
- Someone else's course that you're using as a starting point

Whatever it is, the agent treats it the same way: it analyzes the content, builds an understanding of what the class is about, and uses that understanding to seed the specification process.

### The Analysis Report

After sequestering, the agent reads through the old content and produces an analysis report. This report covers:

- What topics the existing curriculum covers
- How it's structured (lesson sequence, modules, projects, etc.)
- What pedagogical approach it uses
- What's working and what gaps exist
- The target audience and assumed prerequisites

The agent presents this report to you for review. This is your chance to correct misunderstandings — "No, the target audience is actually 6th graders, not 8th graders" or "We don't want to keep the project-based structure, we want to switch to sequential lessons."

### From Analysis into Phase 1

Once you've reviewed the analysis, the agent uses it as the starting point for Phase 1. It's as if you had dictated all that information yourself. But the agent still asks you the Phase 1 questions — it doesn't skip them just because it has old content to work from.

The questions are informed by what the agent found. Instead of asking "What topics should this course cover?" from a blank slate, it asks "The existing curriculum covers variables, loops, functions, and classes. Do you want to keep this scope, expand it, or narrow it?" Instead of "What's the pedagogical approach?" it asks "The current material uses sequential lessons with exercises at the end of each one. Do you want to keep this structure?"

You answer these questions, disagree where you disagree, and direct the agent where you want things to go differently. The agent records everything in `.course/spec.md` as the conversation progresses.

---

## Phase 1: Spec Development

Whether you're starting from scratch or building on existing content, Phase 1 follows the same arc. The agent drives a structured conversation through five sub-phases:

### 1a. Course Concept

The agent asks about the basics: Who are the students? What grade range? What are the educational goals — what should students know or be able to do when they're done? What are the parent goals — what are families paying for? Is this a semester course, a Tech Club, a summer intensive? What's the rough scope?

If you have existing content, these questions are framed around what already exists. If you're starting from scratch, they're open-ended.

You talk through this until the agent has a clear picture. It writes the course concept section of the spec as you go.

### 1b. Pedagogical Model

The agent walks you through choosing the delivery format and pedagogical structure. The League's taxonomy has two dimensions:

**Delivery format** — how students interact with the material: website with lessons, interactive lessons, third-party platform (like MakeCode Arcade), repository with code, or activity/instructor-delivered.

**Pedagogical structure** — how the learning is organized: activity, have fun, sequential lessons, challenge-based, single project, or progressive project. Most courses are hybrids — a mix of these structures.

The agent helps you think through which combinations make sense for your course. It asks about session structure (how does a single class period work?), assessment (quizzes? completed exercises? working projects?), and how you handle students who are ahead or behind.

### 1c. Research

The agent goes and investigates what exists in the space your course occupies. It looks for standards and certification syllabi, existing courses and tutorials, textbooks, exercise sets, and project ideas.

You direct the research. You might say "look for AP Computer Science A resources" or "find what other people have done with MakeCode Arcade for 4th graders" or "I want to align this to the PCEP certification." The agent searches, summarizes findings, and presents them.

Research surfaces your alignment options — the external standards or patterns you might build around. You don't need to know what these are going in; the agent finds them.

### 1d. Alignment Decision

Based on research, you decide whether and how to align the course. Options include aligning to a certification (AP CS A, PCEP), an external course (CS50, freeCodeCamp), specific tutorials or resources, a self-defined topic list, or no formal alignment at all.

This is your decision. The agent presents what it found and makes recommendations. You choose.

### 1e. Spec Synthesis

The agent assembles everything from the prior sub-phases into a complete course specification. This document includes the course overview, pedagogical approach, alignment and standards, research findings, course structure outline, assessment plan, and technical decisions (tier, platform, content format).

The course structure outline section varies depending on your pedagogical choices. A sequential lessons course gets a module-and-lesson breakdown. A challenge-based course gets a challenge sequence. A progressive project course gets a phased project description. Hybrids get a combination.

You review the spec. The agent cannot move to Phase 2 until all required sections are present and you've approved it.

---

## Phase 2: Building the First Version

Once the spec is approved, the agent produces a change plan — a document listing every module, every lesson, and what each one contains. This is the blueprint for the initial build.

How Phase 2 works depends on whether you have existing content.

### Path A: Starting from Scratch

If there's no old content, the process is:

1. **You review and approve the change plan.** This is your chance to reorder things, add or remove lessons, adjust scope.

2. **The agent scaffolds the directory structure.** It creates all the module directories, lesson stub files, and the MkDocs configuration. At this point you have a navigable (but empty) website.

3. **The agent produces outlines.** Before writing full content, it creates an outline for each module — what each lesson covers, the learning objectives, how lessons connect to each other. You review these outlines. This is your last chance to restructure before drafting begins.

4. **The agent writes lessons.** Module by module, lesson by lesson. Each lesson includes both student-facing content and the inline instructor guide section. You can review as lessons arrive or batch-review a module at a time.

5. **The agent creates quiz configuration** for each lesson (if your course uses quizzes).

6. **Validation.** The agent runs a validation check — all lessons present, instructor guide sections filled in, quiz topics aligned with objectives, MkDocs builds without errors, `course.yml` is complete.

### Path B: Existing Content — Convert Then Update

If you have old content and you want to preserve most of it as-is, the agent does an initial AI-driven conversion:

1. **Conversion.** The agent reads the old content and converts it into the standard Curik structure — proper directory layout, MkDocs pages, instructor guide sections added, correct file naming and numbering. The goal is to get the old content into the new format as faithfully as possible, not to rewrite it.

2. **Review.** You look at the converted result. It won't be perfect. Formatting will be off in places. Some content won't map cleanly to the new structure. Things that were implicit in the old format may need to be made explicit.

3. **Update cycle.** From here, you enter the normal update process (described below) to fix what the conversion got wrong and add what's missing. You file issues, the agent collects them into change plans, you approve, the agent executes.

This path is faster if the old content is close to what you want and the main job is reformatting rather than rethinking.

### Path C: Existing Content — Rebuild Informed by Old

If you have old content but you want to substantially rethink the course — different structure, different scope, different pedagogical approach — then you follow Path A (starting from scratch) but the agent has the old content as a reference throughout.

The agent uses the old material as a source: it can pull explanations, examples, exercise ideas, and instructor notes from the old content as it writes new lessons. But the structure, sequence, and scope come from the new spec, not the old curriculum.

This path is the right choice when the old content is useful raw material but the course design is changing significantly.

### Choosing Between Path B and Path C

The agent asks you which approach you want. The question is: "Do you want me to convert the existing content into the new format and then refine it, or do you want to build fresh using the old content as a reference?"

Rules of thumb:

- If the old content is structurally sound and you mainly need it in the new format → Path B
- If you're rethinking the course design, changing the pedagogical structure, or the old content is disorganized → Path C
- If you downloaded someone else's curriculum as a starting point → Path C (you're adapting, not converting)

---

## Phase 3: Updates

After the initial version exists — whether you built from scratch, converted, or rebuilt — the process for making changes is the same. This is the steady-state cycle you'll use for the life of the course.

### Filing Issues

As you read through lessons, use the site, or work through the curriculum yourself, you tell the agent what needs to change. These can be anything:

- "Lesson 3 is too long, split it into two lessons"
- "The exercise in Module 2 Lesson 4 is too hard for this point in the course"
- "We need a new lesson on file I/O between the functions module and the classes module"
- "The instructor guide for Lesson 7 doesn't mention the common mistake where students forget to close the file"
- "Rename Module 3 to 'Data Structures' instead of 'Advanced Topics'"

The agent records each of these as a numbered issue file in `.course/issues/open/`. You don't need to write formal issue descriptions — just tell the agent what's wrong or what you want changed. It turns your comments into properly structured issues.

### Change Plans

When you've accumulated enough issues (or whenever you're ready), ask the agent to collect them into a change plan. The agent reads all open issues, groups related ones together, and produces a plan document in `.course/change-plan/active/`.

The change plan lists structural changes first (file moves, lesson splits, new lessons added, renumbering) and per-lesson content changes second. This ordering matters — the agent needs to get the file structure right before editing content within those files.

You review the change plan. You can modify it, remove items, or add things the agent missed. The agent cannot execute until you approve.

### Execution

Once you approve a change plan, the agent works through it in order. File moves and renaming happen first. Then content edits. Then `syl` regenerates the `.syllabus` file from the updated directory structure (for Tier 3–4 courses).

You can watch this happen or come back when it's done. The agent works through the plan item by item.

### Review and Close

After execution, the agent reviews the change plan line by line to confirm each item was completed. If anything was missed or done incorrectly, it flags those as new issues. You can also review and flag anything you see.

When everything checks out, the change plan moves to `.course/change-plan/done/` and the resolved issues move to `.course/issues/done/`. The cycle restarts — you continue using the curriculum, filing issues as you find them, and periodically collecting them into new change plans.

---

## Validation and Publication

At any point, you can ask the agent to run a full validation check. This verifies:

- Every lesson has an instructor guide section with real content (not just a placeholder)
- Every lesson has learning objectives
- Quiz topics align with lesson objectives (if the course has quizzes)
- The MkDocs site builds without errors
- `course.yml` is complete with actual values, not placeholders
- The `.syllabus` file is consistent with the directory structure (Tier 3–4)

Validation produces a report. If everything passes, the course is ready to publish. If there are failures, they become issues to address in the next change plan cycle.

Publication means triggering the GitHub Action that builds and deploys the MkDocs site, and registering the course with the League's curriculum registry so it appears on the main website.

---

## What You Don't Need to Worry About

Curik and the agent handle these things for you:

- **Repository structure.** The agent creates directories, names files correctly, and maintains the numbering scheme.
- **MkDocs configuration.** The `mkdocs.yml` file, nav structure, theme configuration, and deployment config are generated and maintained by the agent.
- **The `.syllabus` file.** This is maintained by the `syl` tool and Curik together. You never edit it.
- **Instructor guide formatting.** The agent knows the required HTML structure for instructor guide sections and the CSS/JS that makes them show/hide.
- **Quiz file format.** The agent writes `quiz.yml` in the correct schema.
- **`.devcontainer/` setup.** For Tier 3–4 courses that use Codespaces or Code Server, the agent generates the right configuration.
- **README generation.** For Tier 3–4 courses, READMEs in the repo working directories are generated from the web content using comment guards the agent places.

Your job is the educational content and the design decisions. The agent's job is everything structural and mechanical.

---

## Tips

**Talk to the agent in plain language.** You don't need to use technical terminology or format your requests in any special way. "The loop lesson needs more examples" works fine.

**Don't skip the outline review.** The outlines are your last structural checkpoint before the agent starts writing full lessons. Restructuring after content is written is much more expensive than restructuring at the outline stage.

**File issues as you find them.** Don't try to batch everything in your head. Every time you notice something, mention it to the agent. It records the issue. You can always defer execution until you have a meaningful collection.

**Use the site as a student would.** The best way to find problems in curriculum is to work through it. Open the MkDocs development server, follow the lessons, do the exercises. The issues you find this way are the ones that matter most.

**The agent will ask you questions.** It's supposed to. The process has decision points that only you can resolve — pedagogical choices, scope decisions, how hard an exercise should be, whether to split a lesson. These aren't the agent being indecisive; they're the agent doing its job by surfacing decisions that require your judgment.
