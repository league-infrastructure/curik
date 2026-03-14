---
title: "HTML Elements"
uid: "webdev-les-002"
---

{{< instructor-guide >}}
**Objectives:** Students will understand the anatomy of an HTML element
(tag, attributes, content) and use semantic elements for page structure.

**Time:** 35 minutes

**Materials:** Text editor, web browser, MDN reference

**Tips:** Have students inspect elements in the browser DevTools. Seeing
the DOM tree helps them understand nesting.
{{< /instructor-guide >}}

## Anatomy of an Element

Every HTML element has up to three parts:

```
<tag attribute="value">content</tag>
 ^^^                   ^^^^^^^
 opening tag           closing tag
```

For example:

```html
<a href="https://example.com" target="_blank">Visit Example</a>
```

| Part | Value | Purpose |
|------|-------|---------|
| Tag | `a` | Anchor (link) element |
| `href` attribute | `"https://example.com"` | Where the link goes |
| `target` attribute | `"_blank"` | Open in new tab |
| Content | `Visit Example` | Text the user sees |

## Self-Closing Elements

Some elements don't have content and don't need a closing tag[^1]:

[^1]: In HTML5, the trailing slash on self-closing tags (e.g., `<br />`) is optional. Both `<br>` and `<br />` are valid. Most modern style guides omit it.

```html
<img src="photo.jpg" alt="A photo">
<br>
<hr>
<input type="text" placeholder="Enter your name">
```

{{< callout type="warning" >}}
:warning: **Always include `alt` text on images!** Screen readers use
`alt` text to describe images to visually impaired users. It's also
shown when an image fails to load.
{{< /callout >}}

## Semantic Elements

HTML5 introduced **semantic elements** — tags that describe their
*meaning*, not just their appearance:

| Element | Purpose | Instead of... |
|---------|---------|---------------|
| `<header>` | Page or section header | `<div class="header">` |
| `<nav>` | Navigation links | `<div class="nav">` |
| `<main>` | Main content | `<div class="content">` |
| `<article>` | Self-contained content | `<div class="article">` |
| `<section>` | Thematic grouping | `<div class="section">` |
| `<footer>` | Page or section footer | `<div class="footer">` |

```html
<body>
  <header>
    <h1>My Website</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
    </nav>
  </header>
  <main>
    <article>
      <h2>My First Post</h2>
      <p>Hello, world!</p>
    </article>
  </main>
  <footer>
    <p>&copy; 2024 My Name</p>
  </footer>
</body>
```

{{< callout type="tip" >}}
:bulb: **Why semantic HTML?**
1. **Accessibility** — screen readers understand the page structure
2. **SEO** — search engines prioritize well-structured pages
3. **Readability** — easier for developers (including future you!) to
   understand the code
{{< /callout >}}

## Nesting Rules

HTML elements can be **nested** inside each other, but they must be
properly closed in order:

```html
<!-- Correct -->
<p>This is <strong>bold and <em>italic</em></strong> text.</p>

<!-- WRONG — tags overlap! -->
<p>This is <strong>bold and <em>italic</strong></em> text.</p>
```

{{< callout type="danger" >}}
Overlapping tags won't cause an error message, but the browser will
try to "fix" them in unpredictable ways. Always close tags in the
reverse order you opened them — ~~last opened, first closed~~ (LIFO).
{{< /callout >}}

{{< readme-shared >}}
## Exercise: Semantic Page Structure

Build a complete web page using semantic HTML:

1. A `<header>` with your site title and a `<nav>` with at least 3 links
2. A `<main>` with two `<article>` elements, each with a heading and paragraph
3. A `<footer>` with a copyright notice

Your page should use **zero** `<div>` elements — use semantic tags instead!
{{< /readme-shared >}}

{{< readme-only >}}
## Validation

After completing the exercise, validate your HTML at
https://validator.w3.org/ by pasting your code into the "Direct Input" tab.
Fix any errors before submitting.
{{< /readme-only >}}
