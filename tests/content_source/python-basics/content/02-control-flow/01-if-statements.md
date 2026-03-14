---
title: "If Statements"
---

{{< instructor-guide >}}
**Objectives:** Students will write `if`, `elif`, and `else` blocks to
make their programs respond to different conditions.

**Time:** 25 minutes

**Materials:** Python environment, whiteboard for flowchart diagrams
{{< /instructor-guide >}}

## Making Decisions

Programs often need to choose what to do based on some condition. Python
uses `if` statements for this:

```python
temperature = 35

if temperature > 30:
    print("It's hot outside!")
```

The code inside the `if` block only runs when the condition is `True`.

## Comparison Operators

You can compare values using these operators:

| Operator | Meaning                  | Example        |
|----------|--------------------------|----------------|
| `==`     | Equal to                 | `x == 5`       |
| `!=`     | Not equal to             | `x != 5`       |
| `>`      | Greater than             | `x > 5`        |
| `<`      | Less than                | `x < 5`        |
| `>=`     | Greater than or equal to | `x >= 5`       |
| `<=`     | Less than or equal to    | `x <= 5`       |

## Adding `else`

Use `else` to run code when the condition is `False`:

```python
age = 8

if age >= 13:
    print("You can create an account.")
else:
    print("Sorry, you must be 13 or older.")
```

## Multiple Conditions with `elif`

When you have more than two possibilities, use `elif` (short for
"else if"):

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print("Your grade is " + grade)
```

Python checks each condition from top to bottom and runs the first one
that is `True`.

## Try It Yourself

1. Write a program that asks for a number and prints whether it is
   positive, negative, or zero.
2. Write a program that checks if a number is even or odd. (Hint: use
   `number % 2` — the remainder when dividing by 2.)
