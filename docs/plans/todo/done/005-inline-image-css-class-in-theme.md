---
title: Add .inline CSS class for inline images in the theme
status: done
created: 2026-03-14
source: user-reported (Motors curriculum agent feedback)
sprint: '026'
tickets:
- '003'
---

## Problem

Courses sometimes need small inline images (e.g., button icons within
paragraph text). Goldmark doesn't support attributes on inline images,
so authors use raw HTML `<img class="inline">` tags. But the theme has
no `.inline` class — the Motors course had to add one via a local
`nav-override.css`.

## Fix

Add to `curriculum-hugo-theme/assets/css/main.css`:

```css
.content img.inline {
  display: inline;
  height: 1.2em;
  vertical-align: text-bottom;
  border-radius: 0;
  margin: 0;
}
```

Optionally also add an `inline-img` shortcode as a cleaner alternative
to raw HTML.
