---
title: "If Statements"
---

{{< instructor-guide >}}
**Objectives:** Students will write `if`, `elif`, and `else` blocks to
make their programs respond to different conditions.

**Time:** 25 minutes

**Materials:** Python environment, whiteboard for flowchart diagrams

**Teaching tip:** Draw flowcharts on the whiteboard before writing code.
Students understand the *logic* of branching more easily when they can
see the paths visually.
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

{{< callout type="info" >}}
:mag: **Indentation matters!** Python uses indentation (4 spaces) to
know which lines are "inside" the `if` block. This is different from
many other languages that use curly braces `{}`.
{{< /callout >}}

## Comparison Operators

You can compare values using these operators[^1]:

[^1]: These operators always return a **boolean** value: either `True` or `False`. Booleans are actually a special type of integer in Python where `True == 1` and `False == 0`.

| Operator | Meaning                  | Example        | Result |
|----------|--------------------------|----------------|--------|
| `==`     | Equal to                 | `5 == 5`       | `True` |
| `!=`     | Not equal to             | `5 != 3`       | `True` |
| `>`      | Greater than             | `5 > 3`        | `True` |
| `<`      | Less than                | `5 < 3`        | `False` |
| `>=`     | Greater than or equal to | `5 >= 5`       | `True` |
| `<=`     | Less than or equal to    | `5 <= 3`       | `False` |

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

{{< callout type="warning" >}}
:warning: **Order matters!** If you put `score >= 70` before `score >= 90`,
a score of 95 would get a "C" because `95 >= 70` is `True` and Python
stops at the first match. Always put the most specific conditions first.
{{< /callout >}}

## Combining Conditions

You can combine multiple conditions using `and`, `or`, and `not`:

```python
age = 15
has_permission = True

if age >= 13 and has_permission:
    print("You can join the trip!")

temperature = 25

if temperature < 0 or temperature > 40:
    print("Extreme weather warning!")

raining = False

if not raining:
    print("No umbrella needed.")
```

| Operator | Meaning | `True` when... |
|----------|---------|---------------|
| `and` | Both must be true | `True and True` |
| `or` | At least one true | `True or False` |
| `not` | Flips the value | `not False` |

## Nested If Statements

You can put `if` statements inside other `if` statements:

```python
has_ticket = True
age = 10

if has_ticket:
    if age < 12:
        print("Child ticket — enjoy the show!")
    else:
        print("Adult ticket — enjoy the show!")
else:
    print("You need a ticket to enter.")
```

{{< callout type="tip" >}}
:bulb: **Keep it simple!** Deeply nested `if` statements can be hard to
read. If you find yourself nesting more than 2 levels deep, consider
using `and`/`or` to combine conditions instead, or break the logic into
functions (we'll learn about those in [Functions](/02-control-flow/03-functions/)).
{{< /callout >}}

## Try It Yourself

1. Write a program that asks for a number and prints whether it is
   positive, negative, or zero.
2. Write a program that checks if a number is even or odd. (Hint: use
   `number % 2` — the remainder when dividing by 2.)
3. :star: **Challenge:** Write a program that takes a year and determines
   if it's a leap year. Rules:
   - Divisible by 4 → leap year
   - *But* divisible by 100 → **not** a leap year
   - *But* divisible by 400 → leap year again!

   For example: 2024 :white_check_mark:, 1900 :x:, 2000 :white_check_mark:

---

*Next: [Loops](/02-control-flow/02-loops/) — doing things over and over
(without typing the same code over and over).*
