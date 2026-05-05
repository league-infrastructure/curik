---
title: "What Are Variables?"
---

{{< instructor-guide >}}
**Objectives:** Students will understand what a variable is and how to
assign values. Use the candy-jar analogy: a variable is a jar with a
label, and the candy inside is the value.

**Time:** 20 minutes

**Materials:** Whiteboard, colored markers, Python environment
{{< /instructor-guide >}}

## What Is a Variable?

A **variable** is a name that refers to a value stored in the computer's
memory[^1]. Think of it like a labeled box — you put something inside and
later you can look at the label to find it again.

[^1]: Technically, Python variables are *references* to objects in memory, not containers. But the "labeled box" analogy works well for beginners.

{{< callout type="tip" >}}
:bulb: **Analogy time!** Think of a variable like a sticky note on a jar.
The sticky note is the *name*, the jar is the *memory location*, and
what's inside the jar is the *value*.
{{< /callout >}}

## Creating a Variable

In Python you create a variable by picking a name and using the `=` sign:

```python
message = "Hello, World!"
age = 10
pi = 3.14
```

The name goes on the left, and the value goes on the right.

## Naming Rules

Variable names must follow a few rules:

1. Start with a letter or underscore (`_`)
2. Can contain letters, numbers, and underscores
3. Cannot contain spaces or special characters
4. Are **case-sensitive** — `score` and `Score` are different variables

{{< callout type="warning" >}}
These are **reserved words** that you cannot use as variable names:
`if`, `else`, `for`, `while`, `def`, `return`, `import`, `class`, `True`,
`False`, `None`, and [others](https://docs.python.org/3/reference/lexical_analysis.html#keywords).
{{< /callout >}}

Good names describe what the variable holds:

```python
# Good names — descriptive and clear
player_name = "Alice"
high_score = 9500
lives_remaining = 3

# Bad names — avoid these!
x = "Alice"       # too vague
pn = "Alice"      # unclear abbreviation
PLAYERNAME = 42    # misleading (looks like text, holds a number)
```

## Using a Variable

Once you have created a variable, you can use it anywhere you would use
the value itself:

```python
greeting = "Hello"
name = "World"
print(greeting + ", " + name + "!")
```

This prints: `Hello, World!`

You can also **reassign** a variable — change its value:

```python
score = 0
print(score)   # 0

score = 100
print(score)   # 100

score = score + 50
print(score)   # 150
```

{{< callout type="info" >}}
In Python, `=` means "assign" (put a value into a variable), not
"equals." The equals comparison operator is `==` (two equal signs).
We'll use this more in the [If Statements](/02-control-flow/01-if-statements/) lesson.
{{< /callout >}}

## Common Mistakes

Here are mistakes that beginners often make:

| Mistake | What happens | Fix |
|---------|-------------|-----|
| `123abc = "hi"` | `SyntaxError` | Names can't start with a digit |
| `my name = "Jo"` | `SyntaxError` | No spaces in names — use `my_name` |
| `print(Name)` when you defined `name` | `NameError` | Python is case-sensitive |
| ~~`score == 10`~~ to assign | Nothing happens | Use `=` for assignment, not `==` |

## Try It Yourself

1. Create a variable called `favorite_color` and set it to your favorite color.
2. Create a variable called `lucky_number` and set it to any number.
3. Print a sentence using both variables, for example:
   `"My favorite color is blue and my lucky number is 7."`
4. Reassign `lucky_number` to a new value and print it again.

---

> :star: **Challenge:** Can you swap the values of two variables without
> using a third variable? (Hint: Python has a neat trick for this!)
>
> ```python
> a = 1
> b = 2
> # After swapping: a should be 2, b should be 1
> ```
