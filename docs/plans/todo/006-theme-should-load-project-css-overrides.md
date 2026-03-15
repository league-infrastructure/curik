---
title: Theme should load project-level CSS overrides
status: open
created: 2026-03-14
source: user-reported (Motors curriculum agent feedback)
---

## Problem

The theme's `baseof.html` only loads `css/main.css` and
`css/instructor-guide.css` from the theme. There's no mechanism for
courses to add their own CSS without overriding the entire `baseof.html`
template (which then causes the stale-override problem from TODO #004).

The Motors course had a `nav-override.css` that was only loaded because
it had a local `baseof.html` override. Once the override was removed,
the custom CSS stopped loading.

## Fix

Add a hook in the theme's `baseof.html` to load an optional project-level
CSS file. After the existing CSS loads:

```html
{{ $custom := resources.Get "css/custom.css" }}
{{ if $custom }}<style>{{ $custom.Content | safeCSS }}</style>{{ end }}
```

This gives courses a clean extension point (`assets/css/custom.css`)
without needing to override the template. Document this in the theme's
CLAUDE.md.
