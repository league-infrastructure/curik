---
name: pedagogical-model
description: Delivery format and pedagogical structure decisions for Phase 1b
---

# Pedagogical Model Skill (Phase 1b)

Guide the designer through choosing how the class runs. Present choices
as numbered menus. This phase determines the delivery format, pedagogical
structure, session flow, assessment approach, and tier.

## Step 1: Delivery Format

Present the options as a numbered menu:

```
---

## Phase 1b: Pedagogical Model

### How will students interact with the material?

1. **Website with lessons** — students read MkDocs pages, exercises are
   separate files or embedded
2. **Interactive lessons** — embedded code execution (Pyodide) so students
   run code right in the lesson
3. **Third-party platform** — course links to MakeCode Arcade, Trinket,
   Replit, or similar
4. **Repository with code** — students clone a repo into Codespaces or
   Code Server and work in an IDE
5. **Activity / instructor-delivered** — hands-on, physical, or
   instructor-led with no student computers

Pick a number, or describe a combination.

---
```

## Step 2: Pedagogical Structure

After delivery format, present structure options:

```
---

### How is learning organized?

Most courses combine more than one of these. Pick all that apply:

1. **Activity** — structured hands-on tasks (build this, follow these steps)
2. **Have Fun** — inspiration and exposure, loose structure, engagement first
3. **Sequential Lessons** — topics build on each other, each lesson is distinct
4. **Challenge-Based** — problems with multiple valid solutions
5. **Single Project** — one big project, learning happens as needed
6. **Progressive Project** — one project built over the course, growing in
   complexity each session

**Example combinations:**
- Semester Python course: Sequential Lessons + Progressive Project
- Tech Club robotics: Activity + Have Fun
- AP CS A prep: Sequential Lessons + Challenge-Based

Which combination fits your course?

---
```

## Step 3: Session Structure

Ask about a single class session:

```
---

### How does a single session run?

Describe the flow, or pick a pattern:

1. **Explain → Demonstrate → Practice** — instructor teaches, shows example,
   students practice
2. **Challenge → Explore → Debrief** — present problem, students work,
   discuss solutions
3. **Warm-up → Lesson → Lab → Wrap-up** — structured segments
4. **Open work time** — students work on projects, instructor circulates
5. **Something else** — describe it

---
```

## Step 4: Assessment

```
---

### How will you know students are learning?

1. **Quizzes** — short assessments after lessons or modules
2. **Completed exercises** — students submit working code/solutions
3. **Working project** — a project that demonstrates skills
4. **Instructor observation** — informal, no formal assessment
5. **Combination** — describe which

---
```

## Step 5: Differentiation

Ask briefly:

> How do you handle students who are **ahead** (bored, finishing early)
> or **behind** (struggling, falling off)?

## Step 6: Tier Determination

Based on what was captured, determine the tier and present it:

```
---

### Tier Assignment

Based on your choices:

| Factor | Value | Points to |
|--------|-------|-----------|
| Grade range | 6-8 | Tier 3 |
| Delivery | Repository with code | Tier 3 |
| Assessment | Quizzes + exercises | Tier 3 |

**Recommended tier: 3** (grades 6-10, repo with code, Codespaces)

| Tier | Description | Fits? |
|------|-------------|-------|
| 1 | Grades 2-3, no student computers, instructor guide primary | No |
| 2 | Grades 3-5, website links to external platforms | No |
| **3** | **Grades 6-10, repo with code, notebooks, Codespaces** | **Yes** |
| 4 | Grades 10-12, reference docs, independent work | No |

Does tier 3 sound right?

---
```

## Completion

Show the full pedagogical model summary:

```
---

## Phase 1b Summary: Pedagogical Model

| Decision | Choice |
|----------|--------|
| Delivery format | Repository with code (Codespaces) |
| Structure | Sequential Lessons + Progressive Project |
| Session flow | Warm-up → Lesson → Lab → Wrap-up |
| Assessment | Quizzes + completed exercises |
| Differentiation | Extension challenges for advanced, scaffolded hints for struggling |
| Tier | 3 |

---

**Does this look right?**
```

When confirmed, call `record_pedagogical_model` with the formatted content
and `tool_advance_sub_phase()` to move to Phase 1c.
