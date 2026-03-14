---
title: "Data Types"
---

{{< instructor-guide >}}
**Objectives:** Students will identify the three basic data types
(string, integer, float) and use `type()` to check them.

**Time:** 25 minutes

**Materials:** Python environment

**Common misconception:** Students often think `"42"` and `42` are the
same thing. Spend time showing that `"42" + "8"` gives `"428"` while
`42 + 8` gives `50`.
{{< /instructor-guide >}}

## The Three Basic Types

Every value in Python has a **type**[^1]. The three types you will use most
are:

[^1]: Python is a *dynamically typed* language, meaning you don't have to declare types — Python figures them out automatically. Other languages like Java and C++ require you to declare types explicitly.

| Type    | What It Holds       | Example          | Created with |
|---------|---------------------|------------------|-------------|
| `str`   | Text (a "string")   | `"hello"`        | Quotes `"` or `'` |
| `int`   | Whole numbers       | `42`             | Just type the number |
| `float` | Decimal numbers     | `3.14`           | Include a decimal point |

## Checking the Type

Use the built-in `type()` function to find out what type a value is:

```python
print(type("hello"))   # <class 'str'>
print(type(42))        # <class 'int'>
print(type(3.14))      # <class 'float'>
```

{{< callout type="tip" >}}
You can also check if something is a specific type using `isinstance()`:
```python
isinstance(42, int)      # True
isinstance("hi", int)    # False
isinstance(3.14, float)  # True
```
{{< /callout >}}

## Strings

A **string** is any text wrapped in quotes. You can use single quotes or
double quotes:

```python
name = "Alice"
greeting = 'Hello'
```

You can combine strings with `+` (this is called **concatenation**):

```python
full = greeting + ", " + name
print(full)  # Hello, Alice
```

### Useful String Tricks

```python
# Length of a string
print(len("Python"))  # 6

# Uppercase and lowercase
print("hello".upper())  # HELLO
print("HELLO".lower())  # hello

# F-strings — the modern way to build strings
name = "Alice"
age = 10
print(f"My name is {name} and I am {age} years old.")
```

{{< callout type="info" >}}
**F-strings** (formatted string literals) were added in Python 3.6.
They start with `f` before the opening quote and use `{curly braces}`
to embed expressions. They're much cleaner than using `+` to build
strings!
{{< /callout >}}

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

### Arithmetic Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `3 + 2` | `5` |
| `-` | Subtraction | `3 - 2` | `1` |
| `*` | Multiplication | `3 * 2` | `6` |
| `/` | Division | `7 / 2` | `3.5` |
| `//` | Floor division | `7 // 2` | `3` |
| `%` | Modulo (remainder) | `7 % 2` | `1` |
| `**` | Exponentiation | `3 ** 2` | `9` |

{{< callout type="warning" >}}
:warning: **Division always returns a float!** Even `6 / 2` gives `3.0`,
not `3`. Use `//` (floor division) if you want an integer result.
{{< /callout >}}

## Converting Between Types

Sometimes you need to convert one type to another[^2]:

[^2]: Type conversion is also called *type casting*. It creates a new value — it doesn't change the original variable.

```python
age_text = "10"
age_number = int(age_text)   # Convert string to int
print(age_number + 1)        # 11

pi = 3.14159
print(str(pi))               # "3.14159" (now a string)
print(int(pi))               # 3 (truncates, doesn't round!)
```

{{< callout type="danger" >}}
Not all conversions work! Trying to convert a non-numeric string to a
number will crash your program:

```python
int("hello")  # ValueError: invalid literal for int()
```

Always make sure the string actually contains a number before converting.
{{< /callout >}}

## Quick Reference

Here's a cheat sheet for this lesson:

```python
# Creating variables of each type
name = "Alice"          # str
age = 10                # int
height = 4.5            # float

# Checking types
type(name)              # <class 'str'>
isinstance(age, int)    # True

# Converting types
str(42)                 # "42"
int("42")               # 42
float("3.14")           # 3.14

# F-strings
f"Name: {name}, Age: {age}"
```

## Try It Yourself

1. Create variables for your name (string), age (int), and height in
   meters (float).
2. Use `type()` to print the type of each variable.
3. Try adding your age and height together. What type is the result?
4. :star: **Challenge:** What happens when you do `"3" * 3`? What about
   `3 * "hello"`? Can you explain why?

---

*Next up: [Control Flow](/02-control-flow/) — making your programs smart
enough to make decisions!*
