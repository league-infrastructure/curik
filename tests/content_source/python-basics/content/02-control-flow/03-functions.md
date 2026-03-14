---
title: "Functions"
---

{{< instructor-guide >}}
**Objectives:** Students will define functions with `def`, use parameters
and return values, and understand why functions make code reusable.

**Time:** 30 minutes

**Materials:** Python environment

**Tips:** Emphasize the difference between *defining* a function and
*calling* it. Use the recipe analogy: a function definition is the recipe,
calling it is actually cooking the dish.
{{< /instructor-guide >}}

## What Is a Function?

A **function** is a reusable block of code with a name. You have already
used built-in functions like `print()` and `type()`. Now you will learn
to write your own.

## Defining a Function

Use the `def` keyword:

```python
def greet():
    print("Hello!")
    print("Welcome to Python Basics.")
```

This *defines* the function but does not run it yet. To run it, **call**
the function by name:

```python
greet()
```

## Parameters

Functions can accept **parameters** — values you pass in when calling:

```python
def greet(name):
    print("Hello, " + name + "!")

greet("Alice")   # Hello, Alice!
greet("Bob")     # Hello, Bob!
```

You can have multiple parameters:

```python
def add(a, b):
    print(a + b)

add(3, 5)   # 8
```

## Return Values

Use `return` to send a value back from a function:

```python
def square(n):
    return n * n

result = square(4)
print(result)   # 16
```

Without `return`, a function gives back `None`:

```python
def say_hi():
    print("Hi!")

x = say_hi()
print(x)   # None
```

## Why Use Functions?

1. **Reuse** — Write code once, use it many times
2. **Organization** — Break a big problem into small pieces
3. **Readability** — Give meaningful names to blocks of logic

```python
def is_even(n):
    return n % 2 == 0

def is_positive(n):
    return n > 0

number = 8
if is_even(number) and is_positive(number):
    print(f"{number} is a positive even number")
```

## Try It Yourself

1. Write a function `area(width, height)` that returns the area of a
   rectangle.
2. Write a function `is_leap_year(year)` that returns `True` if the year
   is a leap year. (Hint: a year is a leap year if it is divisible by 4,
   except for years divisible by 100 — unless also divisible by 400.)
3. Use your `area` function to calculate the areas of three different
   rectangles and print the results.
