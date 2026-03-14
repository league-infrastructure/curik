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

**Common pitfall:** Students forget to update the loop variable in `while`
loops, creating infinite loops. Show them `Ctrl+C` to stop a runaway
program before they start experimenting.
{{< /instructor-guide >}}

## Why Loops?

Imagine you want to print the numbers 1 through 10. Without a loop you
would need ten `print()` calls. With a loop, you need just two lines:

```python
for number in range(1, 11):
    print(number)
```

{{< callout type="info" >}}
Loops are one of the things that make computers powerful. A computer
can execute a loop billions of times without getting tired or making
mistakes. That's something no human can do!
{{< /callout >}}

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

`range()` generates a sequence of numbers[^1]:

[^1]: `range()` doesn't actually create a list in memory — it generates numbers one at a time, which makes it very memory-efficient even for huge ranges.

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

Output:

```
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
...
7 x 10 = 70
```

### Looping with `enumerate()`

Sometimes you need both the item *and* its position:

```python
fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(f"{index + 1}. {fruit}")
```

Output:

```
1. apple
2. banana
3. cherry
```

## The `while` Loop

A `while` loop keeps running as long as its condition is `True`:

```python
countdown = 5

while countdown > 0:
    print(countdown)
    countdown = countdown - 1

print("Liftoff! 🚀")
```

{{< callout type="danger" >}}
**Infinite loops will freeze your program!** If the condition never
becomes `False`, the loop runs forever. Always make sure something inside
the loop changes the condition.

If you accidentally create an infinite loop, press **Ctrl+C** in the
terminal to stop it.

```python
# BAD — infinite loop!
x = 1
while x > 0:
    print(x)
    x = x + 1    # x keeps growing, never reaches 0!
```
{{< /callout >}}

## `for` vs `while` — When to Use Which?

| Use `for` when... | Use `while` when... |
|-------------------|---------------------|
| You know how many times to loop | You don't know how many times |
| Iterating over a list or range | Waiting for a condition to change |
| ~~Processing each item~~ in a collection | Repeating until user says "stop" |

## `break` and `continue`

Two special keywords control loop behavior:

- **`break`** — exits the loop immediately
- **`continue`** — skips the rest of the current iteration

```python
# break — find the first multiple of 7
for number in range(1, 20):
    if number % 7 == 0:
        print(f"Found a multiple of 7: {number}")
        break
```

```python
# continue — skip odd numbers
for number in range(1, 11):
    if number % 2 != 0:
        continue
    print(number)    # Only prints: 2, 4, 6, 8, 10
```

{{< callout type="tip" >}}
:bulb: **Pattern: input validation loop.** A `while` loop is perfect for
asking the user for input until they give a valid answer:

```python
while True:
    answer = input("Enter yes or no: ")
    if answer in ("yes", "no"):
        break
    print("Invalid input, try again.")
```
{{< /callout >}}

## Nested Loops

You can put loops inside loops. The inner loop runs completely for each
iteration of the outer loop:

```python
for row in range(1, 4):
    for col in range(1, 4):
        print(f"({row},{col})", end=" ")
    print()  # New line after each row
```

Output:

```
(1,1) (1,2) (1,3)
(2,1) (2,2) (2,3)
(3,1) (3,2) (3,3)
```

## Try It Yourself

1. Use a `for` loop to print every even number from 2 to 20.
2. Use a `while` loop to keep asking the user for a password until they
   type `"secret"`.
3. Write a loop that prints numbers 1 to 50 but skips multiples of 3.
4. :star: **Challenge:** Write a program that prints this pattern:

   ```
   *
   **
   ***
   ****
   *****
   ```

   Then modify it to print an *upside-down* triangle too!

---

*Next: [Functions](/02-control-flow/03-functions/) — teaching your
programs new tricks.*
