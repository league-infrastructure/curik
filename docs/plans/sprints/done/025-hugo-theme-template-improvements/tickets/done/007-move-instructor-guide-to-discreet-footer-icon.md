---
id: "007"
title: "Move instructor guide to discreet footer icon"
status: done
use-cases: [SUC-001]
depends-on: []
---

# Move instructor guide to discreet footer icon

## Description

The instructor guide shortcode currently renders inline as a collapsible
`<details>` element in the lesson content. Students don't need to see it
and instructors can do a bit more work to find it.

Change the approach: the instructor guide content should be hidden from
the main page body and accessible via a small discreet icon in the footer
area. Clicking the icon reveals the instructor content (e.g., a slide-up
panel, modal, or toggled section at the bottom).

This affects:
- `layouts/shortcodes/instructor-guide.html` — rendering approach
- `assets/css/instructor-guide.css` — styling
- `layouts/_default/baseof.html` — footer area for the toggle icon

## Acceptance Criteria

- [ ] Instructor guide content is not visible in the main lesson body
- [ ] A small icon in the footer area toggles instructor content
- [ ] Instructor content is readable when toggled open
- [ ] Pages without instructor guides don't show the icon
- [ ] Hugo build succeeds
- [ ] Integration tests pass

## Testing

- **Existing tests to run**: `tests/test_integration_hugo.py`
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
