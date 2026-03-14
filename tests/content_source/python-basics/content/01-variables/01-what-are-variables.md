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
memory. Think of it like a labeled box — you put something inside and
later you can look at the label to find it again.

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

Good names describe what the variable holds:

```python
player_name = "Alice"
high_score = 9500
lives_remaining = 3
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

## Try It Yourself

1. Create a variable called `favorite_color` and set it to your favorite color.
2. Create a variable called `lucky_number` and set it to any number.
3. Print a sentence using both variables, for example:
   `"My favorite color is blue and my lucky number is 7."`
