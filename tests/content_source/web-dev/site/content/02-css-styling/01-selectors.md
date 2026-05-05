---
title: "CSS Selectors"
uid: "webdev-les-003"
---

{{< instructor-guide >}}
**Objectives:** Students will use element, class, and ID selectors to
style HTML elements.

**Time:** 30 minutes

**Materials:** Text editor, browser DevTools

**Tips:** Show the DevTools "Styles" panel so students can see exactly
which selectors are applying to an element. This builds intuition
for specificity.
{{< /instructor-guide >}}

## Adding CSS to Your Page

There are three ways to add CSS[^1]:

[^1]: There's also a fourth way — `@import` inside a CSS file — but it's slower than `<link>` and generally avoided in production.

```html
<!-- Method 1: External stylesheet (recommended) -->
<link rel="stylesheet" href="style.css">

<!-- Method 2: Internal stylesheet -->
<style>
  h1 { color: blue; }
</style>

<!-- Method 3: Inline style (avoid!) -->
<h1 style="color: blue;">Title</h1>
```

{{< callout type="tip" >}}
:bulb: Always use **external stylesheets** (Method 1). They keep your
HTML clean and let you share styles across multiple pages.
{{< /callout >}}

## Selector Types

| Selector | Targets | Example | Matches |
|----------|---------|---------|---------|
| Element | All elements of a type | `p { }` | Every `<p>` |
| Class | Elements with a class | `.highlight { }` | `<p class="highlight">` |
| ID | One specific element | `#header { }` | `<div id="header">` |
| Descendant | Nested elements | `nav a { }` | `<a>` inside `<nav>` |
| Group | Multiple selectors | `h1, h2 { }` | All `<h1>` and `<h2>` |

## Basic Properties

```css
body {
    font-family: Arial, sans-serif;
    color: #333;
    background-color: #f5f5f5;
    line-height: 1.6;
}

h1 {
    color: #0066cc;
    border-bottom: 2px solid #0066cc;
    padding-bottom: 0.5rem;
}

a {
    color: #0066cc;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
```

{{< callout type="warning" >}}
:warning: **Specificity matters!** When two rules conflict, CSS uses
specificity to decide which wins. The order is:
1. Inline styles (highest)
2. ID selectors
3. Class selectors
4. Element selectors (lowest)
{{< /callout >}}

## The Box Model

Every HTML element is a **box** with four layers:

```
┌─────────────────────────────────────────┐
│ margin (space outside the border)       │
│  ┌───────────────────────────────────┐  │
│  │ border                            │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │ padding (space inside)      │  │  │
│  │  │  ┌───────────────────────┐  │  │  │
│  │  │  │ content               │  │  │  │
│  │  │  └───────────────────────┘  │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

```css
.card {
    margin: 1rem;
    border: 1px solid #ddd;
    padding: 1.5rem;
    border-radius: 8px;
}
```

{{< callout type="info" >}}
Add `box-sizing: border-box;` to make `width` include padding and
border. Without it, a `200px` wide box with `20px` padding is actually
`240px` wide — which causes layout headaches.
{{< /callout >}}

{{< readme-shared >}}
## Exercise: Style a Profile Card

Create a styled profile card with:

1. A CSS file linked to your HTML with `<link>`
2. A `.card` class with border, padding, and rounded corners
3. Different colors for headings vs body text
4. A hover effect on at least one element
{{< /readme-shared >}}

{{< readme-only >}}
## Getting Started

Create two files:

- `index.html` — your profile card HTML
- `style.css` — your stylesheet

Link them with `<link rel="stylesheet" href="style.css">` in the `<head>`.
{{< /readme-only >}}
