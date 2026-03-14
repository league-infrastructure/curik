---
title: "Data Types"
---

{{< instructor-guide >}}
**Objectives:** Students will identify the three basic data types
(string, integer, float) and use `type()` to check them.

**Time:** 25 minutes

**Materials:** Python environment
{{< /instructor-guide >}}

## The Three Basic Types

Every value in Python has a **type**. The three types you will use most
are:

| Type    | What It Holds       | Example          |
|---------|---------------------|------------------|
| `str`   | Text (a "string")   | `"hello"`        |
| `int`   | Whole numbers       | `42`             |
| `float` | Decimal numbers     | `3.14`           |

## Checking the Type

Use the built-in `type()` function to find out what type a value is:

```python
print(type("hello"))   # <class 'str'>
print(type(42))        # <class 'int'>
print(type(3.14))      # <class 'float'>
```

## Strings

A **string** is any text wrapped in quotes. You can use single quotes or
double quotes:

```python
name = "Alice"
greeting = 'Hello'
```

You can combine strings with `+`:

```python
full = greeting + ", " + name
print(full)  # Hello, Alice
```

## Integers and Floats

**Integers** are whole numbers — no decimal point. **Floats** have a
decimal point.

```python
apples = 5       # int
price = 1.25     # float
total = apples * price
print(total)     # 6.25
```

Notice that multiplying an `int` by a `float` gives a `float`.

## Converting Between Types

Sometimes you need to convert one type to another:

```python
age_text = "10"
age_number = int(age_text)   # Convert string to int
print(age_number + 1)        # 11

pi = 3.14159
print(str(pi))               # "3.14159" (now a string)
```

## Try It Yourself

1. Create variables for your name (string), age (int), and height in
   meters (float).
2. Use `type()` to print the type of each variable.
3. Try adding your age and height together. What type is the result?
