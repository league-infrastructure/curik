---
id: "005"
title: "Copy Motors Clinic theme and add real content to test fixtures"
status: done
use-cases: [SUC-001, SUC-002]
depends-on: ["004"]
---

# Copy Motors Clinic theme and add real content to test fixtures

## Description

1. Fetch the Motors Clinic site (https://league-curriculum.github.io/Motors/)
   and its Hugo theme. Copy the theme's layouts, CSS, and structure into
   curriculum-hugo-theme, replacing the placeholder templates.
2. Add real lesson content to tests/content_source/python-basics/ so the
   test site looks like an actual curriculum, not empty stubs.

## Acceptance Criteria

- [x] curriculum-hugo-theme layouts match the Motors Clinic look and feel
- [x] python-basics test fixture has real lesson content (not just stubs)
- [x] `hugo server` on the test site produces a site that looks like Motors
- [x] Integration tests still pass
- [x] Hugo build succeeds

## Testing

- **Existing tests to run**: `tests/test_integration_hugo.py`
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
