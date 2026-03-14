---
id: "002"
title: "Flat sidebar navigation matching Motors Clinic"
status: done
use-cases: [SUC-001]
depends-on: ["001"]
---

# Flat sidebar navigation matching Motors Clinic

## Description

The Motors Clinic has a flat list of page links in the sidebar — section
titles are clickable links that go to the section overview page, and
lessons appear at the same level below them.

Our current template has two problems:
1. Section titles are rendered as non-clickable `<p class="caption">`
   headers — you can't click "Control Flow" to go to its overview page
2. Lessons are nested in sub-`<ul>` elements under section headers

Update the sidebar nav in baseof.html to render a flat list where:
- Each section's `_index.md` page appears as a clickable link
- Each lesson appears as a clickable link at the same nesting level
- The current page is visually highlighted
- The list order follows Hugo's default weight/alphabetical ordering

## Acceptance Criteria

- [ ] Section titles in sidebar are clickable links to the section page
- [ ] All pages (sections + lessons) appear in a single flat list
- [ ] Current page is visually highlighted
- [ ] Hugo build succeeds

## Testing

- **Existing tests to run**: `tests/test_integration_hugo.py`
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
