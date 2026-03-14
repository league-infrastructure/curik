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

**Assessment idea:** Have students write a function that takes a
temperature in Fahrenheit and returns it in Celsius. Tests whether they
understand parameters, return values, and the formula.
{{< /instructor-guide >}}

## What Is a Function?

A **function** is a reusable block of code with a name[^1]. You have already
used built-in functions like `print()` and `type()`. Now you will learn
to write your own.

[^1]: Functions in Python are *first-class objects*, meaning they can be passed around like any other value. You can store a function in a variable, put it in a list, or pass it to another function. We won't go deep into this now, but it's one of the things that makes Python powerful.

{{< callout type="info" >}}
:dart: **Why functions?** Imagine you need to calculate the area of a
rectangle in five different places in your program. Without a function,
you'd copy-paste the formula five times. With a function, you write it
once and *call* it five times. If the formula ever changes, you only
fix it in one place.
{{< /callout >}}

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

### Default Parameters

You can give parameters default values:

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Alice", "Good morning")  # Good morning, Alice!
```

{{< callout type="tip" >}}
:bulb: **F-strings in functions** are a great combination. Notice how
`f"{greeting}, {name}!"` is much cleaner than `greeting + ", " + name + "!"`.
{{< /callout >}}

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

{{< callout type="warning" >}}
`print()` and `return` are **not the same thing!**

- `print()` displays text on the screen — the value is gone after that
- `return` sends a value *back to the caller* so it can be stored or used

A function can `print()` *and* `return`, but usually you want `return`
so the caller can decide what to do with the result.
{{< /callout >}}

## Why Use Functions?

1. **Reuse** — Write code once, use it many times
2. **Organization** — Break a big problem into small pieces
3. **Readability** — Give meaningful names to blocks of logic
4. **Testing** — Small functions are easier to test and debug

```python
def is_even(n):
    return n % 2 == 0

def is_positive(n):
    return n > 0

number = 8
if is_even(number) and is_positive(number):
    print(f"{number} is a positive even number")
```

## Putting It All Together

Here's a complete example that uses everything from this module —
`if` statements, loops, *and* functions:

```python
def fizzbuzz(n):
    """Return 'Fizz', 'Buzz', 'FizzBuzz', or the number as a string."""
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)

for i in range(1, 21):
    print(fizzbuzz(i))
```

{{< callout type="info" >}}
:trophy: **FizzBuzz** is one of the most famous programming exercises.
It's often used in job interviews! If you can write this program, you
already know more than some interview candidates.
{{< /callout >}}

## Quick Reference

```python
# Define a function
def function_name(param1, param2="default"):
    """Docstring describing what the function does."""
    # ... code ...
    return result

# Call a function
result = function_name(arg1, arg2)

# Functions that return True/False are called "predicates"
def is_adult(age):
    return age >= 18
```

## Try It Yourself

1. Write a function `area(width, height)` that returns the area of a
   rectangle.
2. Write a function `is_leap_year(year)` that returns `True` if the year
   is a leap year[^2].
3. Use your `area` function to calculate the areas of three different
   rectangles and print the results.
4. :star: **Challenge:** Write a function `celsius_to_fahrenheit(c)` and
   another `fahrenheit_to_celsius(f)`. Test them by converting 100°C to
   Fahrenheit and then back to Celsius — you should get 100 again!

[^2]: Leap year rules: divisible by 4, except centuries (divisible by 100), unless also divisible by 400. So 2024 is a leap year, 1900 is not, but 2000 is.

---

:tada: **Congratulations!** You've completed the Python Basics course.
You now know about variables, data types, if statements, loops, and
functions — the building blocks of every Python program.

> "The best way to learn to code is to code."
> — Unknown
