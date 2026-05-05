---
title: "Control Flow"
---

Control flow lets your program make decisions and repeat actions.
In this module you will learn about `if` statements, `for` and `while`
loops, and how to write your own functions.

{{< callout type="info" >}}
:rocket: **Why does this matter?** Without control flow, programs can only
run one line after another, top to bottom. With control flow, your programs
can react to input, handle different situations, and do repetitive work
automatically.
{{< /callout >}}

## Module Goals

- [ ] Write `if`/`elif`/`else` blocks
- [ ] Use `for` and `while` loops
- [ ] Define and call functions with parameters and return values

## What You'll Build

By the end of this module you will be able to write programs like:

```python
def grade_score(score):
    """Return a letter grade for a numeric score."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"

for student_score in [95, 82, 67, 91, 74]:
    print(f"Score {student_score} → {grade_score(student_score)}")
```

> "First, solve the problem. Then, write the code."
> — John Johnson

{{< instructor-guide >}}
**Module Notes:** This module has three lessons and takes approximately
85 minutes total. If you need to split it across sessions, a natural
break point is between Loops and Functions.

**Pacing guide:**
- If Statements: 25 min
- Loops: 30 min
- Functions: 30 min

Leave at least 10 minutes per lesson for the "Try It Yourself" exercises.
{{< /instructor-guide >}}
