---
id: "003"
title: "Next/previous navigation in sidebar and content"
status: done
use-cases: [SUC-001]
depends-on: ["002"]
---

# Next/previous navigation in sidebar and content

## Description

Add Next/Previous buttons to the sidebar nav. Clicking Next walks
through the entire curriculum sequentially:

1. Module 1 overview (_index.md)
2. Module 1 / Lesson 1
3. Module 1 / Lesson 2
4. Module 2 overview (_index.md)
5. Module 2 / Lesson 1
... and so on.

The order follows the flat nav list from ticket 002. "Next" from the
last lesson in a module goes to the next module's overview. "Next" from
a module overview goes to its first lesson.

Place the Next/Previous buttons at the bottom of the sidebar, below the
nav list. Also keep a simpler prev/next at the bottom of the content
area (like Motors Clinic has).

## Acceptance Criteria

- [ ] Sidebar has Next/Previous buttons below the nav list
- [ ] Clicking Next walks through all sections and lessons sequentially
- [ ] Next from last lesson in module goes to next module overview
- [ ] Content area also has prev/next links at the bottom
- [ ] First page has no Previous, last page has no Next
- [ ] Hugo build succeeds

## Testing

- **Existing tests to run**: `tests/test_integration_hugo.py`
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
