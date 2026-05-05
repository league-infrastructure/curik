---
title: "CSS Layout"
uid: "webdev-les-004"
---

{{< instructor-guide >}}
**Objectives:** Students will use flexbox to create common page layouts
(navigation bars, card grids, holy grail layout).

**Time:** 40 minutes

**Materials:** Text editor, browser DevTools (flexbox inspector)

**Tips:** Chrome and Firefox have excellent flexbox inspectors built into
DevTools. Show students how to toggle `display: flex` in the Styles panel
to see the immediate effect.
{{< /instructor-guide >}}

## The Layout Problem

By default, HTML elements stack vertically. But most designs need
elements side by side — navigation links, image galleries, card grids.

**Flexbox** solves this elegantly[^1].

[^1]: Before flexbox, developers used `float`, `inline-block`, and even HTML `<table>` elements for layout. These were all hacks. Flexbox was the first CSS feature designed specifically for layout.

## Flexbox Basics

Turn any element into a flex container with `display: flex`:

```css
.navbar {
    display: flex;
    gap: 1rem;
}
```

```html
<nav class="navbar">
    <a href="/">Home</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
</nav>
```

The three links now sit side by side instead of stacking!

## Key Flex Properties

### Container Properties

| Property | Values | What It Does |
|----------|--------|-------------|
| `display` | `flex` | Enables flexbox |
| `flex-direction` | `row`, `column` | Main axis direction |
| `justify-content` | `start`, `center`, `space-between` | Align along main axis |
| `align-items` | `start`, `center`, `stretch` | Align along cross axis |
| `gap` | `1rem`, `10px` | Space between items |
| `flex-wrap` | `nowrap`, `wrap` | Allow items to wrap |

### Item Properties

| Property | Values | What It Does |
|----------|--------|-------------|
| `flex` | `1`, `0 0 auto` | How items grow/shrink |
| `align-self` | `start`, `center`, `end` | Override container alignment |
| `order` | `0`, `1`, `-1` | Reorder without changing HTML |

{{< callout type="tip" >}}
:bulb: **The `flex: 1` shortcut** makes an item grow to fill available
space. Use it for the main content area in a sidebar layout:

```css
.main { flex: 1; }  /* Takes all remaining space */
.sidebar { width: 250px; }  /* Fixed width */
```
{{< /callout >}}

## Common Layouts

### Navigation Bar

```css
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: #333;
    color: white;
}
```

### Card Grid

```css
.card-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
}

.card {
    flex: 1 1 300px;  /* Grow, shrink, min 300px */
    padding: 1rem;
    border: 1px solid #ddd;
}
```

{{< callout type="warning" >}}
Don't use flexbox for **everything**. Simple stacking (the default)
needs no flexbox. Grid layout (2D grids with rows AND columns) is
better handled by `display: grid`, which we'll cover in advanced CSS.
{{< /callout >}}

### Centering (the holy grail of CSS)

```css
/* Center anything, both horizontally and vertically */
.centered {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}
```

{{< callout type="info" >}}
:trophy: **Fun fact:** "How to center a div in CSS" has been one of the
most searched programming questions for over a decade. With flexbox,
it's just three lines!
{{< /callout >}}

{{< readme-shared >}}
## Exercise: Flexbox Page Layout

Build a page with this layout:

1. A horizontal **navigation bar** with your site name on the left and
   links on the right (use `justify-content: space-between`)
2. A **main area** with a sidebar (250px) and content area (flexible)
3. A **card grid** with at least 4 cards that wrap responsively

All layout must use `display: flex` — no floats or inline-block!
{{< /readme-shared >}}

{{< readme-only >}}
## Hints

- The page layout (sidebar + content) needs a wrapper div with `display: flex`
- The sidebar gets a fixed `width: 250px`
- The content area gets `flex: 1` to fill remaining space
- Cards use `flex: 1 1 300px` to wrap nicely
{{< /readme-only >}}
