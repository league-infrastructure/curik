---
title: curriculum-hugo-theme sidebar nav is flat, not hierarchical
status: open
created: 2026-03-13
---

## Bug Report — upstream for league-infrastructure/curriculum-hugo-theme

### Summary

The sidebar navigation in `baseof.html` renders all sections and pages as a flat list. Modules and lessons appear at the same indentation level with no visual hierarchy. This makes the nav unusable for any course with more than a few pages.

### Expected Behavior

The sidebar should render modules as parent items with lessons nested underneath:

```
Getting Started          (bold, module)
  Kit Contents           (indented, lesson)
  Micro:bit Setup        (indented, lesson)
Signals and Power        (bold, module)
  Voltage and PWM        (indented, lesson)
  Oscilloscope           (indented, lesson)
```

### Actual Behavior

All items render at the same level:

```
Getting Started
Kit Contents
Micro:bit Setup
Signals and Power
Voltage and PWM
Oscilloscope
```

### Root Cause

In `layouts/_default/baseof.html`, lines 57-61, the nav iterates over `$allPages` (a flat slice of all sections and pages) and renders every item as a sibling `<li>`:

```html
{{ range $allPages }}
<li{{ if eq $.RelPermalink .RelPermalink }} class="current"{{ end }}>
  <a href="{{ .RelPermalink }}">{{ .Title }}</a>
</li>
{{ end }}
```

The `$allPages` slice is built correctly (sections interleaved with their pages), but the template doesn't distinguish between sections (modules) and regular pages (lessons). It should use nested `<ul>` elements.

### Fix Applied Locally

We overrode `baseof.html` locally to replace the flat loop with a hierarchical one that iterates over `$sections`, renders each as a module-level `<li>`, and nests its `.Pages` in a child `<ul class="sidebar-lessons">`:

```html
{{ range $sections }}
<li class="sidebar-module{{ if eq $.RelPermalink .RelPermalink }} current{{ end }}">
  <a href="{{ .RelPermalink }}" class="sidebar-module-link">{{ .Title }}</a>
  {{ $pages := sort .Pages "File.Path" }}
  {{ if $pages }}
  <ul class="sidebar-lessons">
    {{ range $pages }}
    <li{{ if eq $.RelPermalink .RelPermalink }} class="current"{{ end }}>
      <a href="{{ .RelPermalink }}">{{ .Title }}</a>
    </li>
    {{ end }}
  </ul>
  {{ end }}
</li>
{{ end }}
```

The existing CSS already handles `ul ul` indentation (`.sidebar-tree ul ul { padding-left: var(--sidebar-item-spacing-horizontal); }`), so the fix mostly works with existing styles. We added a small `nav-override.css` to bold module links and size lesson links slightly smaller.

### Additional Notes

- The `$allPages` flat sequence is still needed for prev/next navigation and should be preserved
- Only the nav rendering loop needs to change from flat to nested
- The theme's CSS already has `sidebar-tree ul ul` rules anticipating nesting, but the template never generates nested `<ul>` elements

### Environment
- curriculum-hugo-theme (submodule from league-infrastructure/curriculum-hugo-theme)
- Curik 0.20260313.8
- Hugo 0.157.0+extended
- Course: Motors Clinic, Tier 2, 6 modules / 11 lessons
