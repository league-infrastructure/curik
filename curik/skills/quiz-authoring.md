---
name: quiz-authoring
description: Schema, question types, and alignment checking procedure for quiz authoring
---

# Quiz Authoring Skill

This skill covers how to create, validate, and manage quiz files for
curriculum lessons.

## Quiz Schema (quiz.yml)

Each quiz file follows this YAML schema:

```yaml
lesson_id: <string>        # ID matching the lesson this quiz covers
status: drafted             # One of: drafted, reviewed, complete
difficulty: beginner        # Difficulty level
question_types:             # List of allowed question formats
  - multiple-choice
  - short-answer
  - true-false
  - fill-in-the-blank
topics:                     # Topics this quiz covers (from objectives)
  - <topic 1>
  - <topic 2>
questions: []               # Populated after stub generation
```

## Question Types

| Type | Description | When to Use |
|------|-------------|-------------|
| multiple-choice | 4 options, 1 correct | Factual recall, concept recognition |
| short-answer | Free-text response | Explanation, application |
| true-false | Binary choice | Quick concept checks |
| fill-in-the-blank | Complete a statement | Terminology, syntax |

## Authoring Procedure

1. **Read the lesson** to identify learning objectives.
2. **Derive topics** from each objective. Each objective should map to
   at least one quiz topic.
3. **Generate the stub** using `generate_quiz_stub(root, lesson_id, topics)`.
4. **Check alignment** using `validate_quiz_alignment(root, lesson_path, quiz_path)`.
5. **Fix gaps** — if any objectives are uncovered, add topics and
   regenerate or update the quiz file.
6. **Set status** — mark as `drafted` initially, then `reviewed` after
   peer review, and `complete` when finalized.

## Alignment Rules

- Every learning objective in the lesson MUST have at least one quiz
  topic that covers it.
- Topic matching is case-insensitive and checks for substring overlap.
- If alignment fails, the quiz is not ready for review.

## Status Lifecycle

```
drafted → reviewed → complete
```

- **drafted**: Initial generation, topics filled in, questions may be empty.
- **reviewed**: A peer or the content designer has reviewed the quiz.
- **complete**: Quiz is finalized and ready for student use.

Use `set_quiz_status(root, quiz_path, status)` to transition between states.
