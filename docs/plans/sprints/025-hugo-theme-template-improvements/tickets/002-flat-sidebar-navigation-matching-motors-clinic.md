---
id: "002"
title: "Flat sidebar navigation matching Motors Clinic"
status: todo
use-cases: [SUC-001]
depends-on: ["001"]
---

# Flat sidebar navigation matching Motors Clinic

## Description

The Motors Clinic has a flat list of page links in the sidebar — no nested section headers. Our current template groups pages under section headers with nested `<ul>` elements.

Update the sidebar nav in baseof.html to render a flat list: iterate over all pages across all sections in weight/alphabetical order, outputting a single-level `<ul>`. Highlight the current page.

## Acceptance Criteria

- [ ] Sidebar shows a flat list of all lesson pages
- [ ] Current page is visually highlighted
- [ ] No nested section headers in sidebar
- [ ] Hugo build succeeds

## Testing

- **Existing tests to run**: `tests/test_integration_hugo.py`
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
