---
title: "Loops"
---

{{< instructor-guide >}}
**Objectives:** Students will use `for` loops to iterate over ranges and
lists, and `while` loops for condition-based repetition.

**Time:** 30 minutes

**Materials:** Python environment

**Tips:** Start with `for` loops since they are safer (no infinite loops).
Introduce `while` only after students are comfortable with `for`.
{{< /instructor-guide >}}

## Why Loops?

Imagine you want to print the numbers 1 through 10. Without a loop you
would need ten `print()` calls. With a loop, you need just two lines:

```python
for number in range(1, 11):
    print(number)
```

## The `for` Loop

A `for` loop repeats a block of code once for each item in a sequence:

```python
colors = ["red", "green", "blue"]

for color in colors:
    print(color)
```

Output:

```
red
green
blue
```

### Using `range()`

`range()` generates a sequence of numbers:

```python
range(5)        # 0, 1, 2, 3, 4
range(2, 6)     # 2, 3, 4, 5
range(0, 10, 2) # 0, 2, 4, 6, 8
```

Example — print a multiplication table for 7:

```python
for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")
```

## The `while` Loop

A `while` loop keeps running as long as its condition is `True`:

```python
countdown = 5

while countdown > 0:
    print(countdown)
    countdown = countdown - 1

print("Liftoff!")
```

{{< callout type="warning" >}}
**Watch out for infinite loops!** If the condition never becomes `False`,
your program will run forever. Always make sure something inside the loop
changes the condition.
{{< /callout >}}

## `break` and `continue`

- `break` exits the loop immediately
- `continue` skips the rest of the current iteration

```python
for number in range(1, 20):
    if number % 7 == 0:
        print(f"Found a multiple of 7: {number}")
        break
```

## Try It Yourself

1. Use a `for` loop to print every even number from 2 to 20.
2. Use a `while` loop to keep asking the user for a password until they
   type `"secret"`.
3. Write a loop that prints numbers 1 to 50 but skips multiples of 3.
