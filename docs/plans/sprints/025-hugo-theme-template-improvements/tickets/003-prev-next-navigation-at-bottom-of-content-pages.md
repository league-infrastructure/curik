---
id: "003"
title: "Prev/next navigation at bottom of content pages"
status: todo
use-cases: [SUC-001]
depends-on: []
---

# Prev/next navigation at bottom of content pages

## Description

The Motors Clinic has prev/next navigation links at the bottom of each content page (e.g. "Next: Getting Started >"). Add this to single.html using Hugo's .PrevInSection / .NextInSection or .Prev / .Next.

## Acceptance Criteria

- [ ] Single pages show "Previous" link when applicable
- [ ] Single pages show "Next" link when applicable
- [ ] Links show the target page title
- [ ] Styled to match Furo's right-aligned prev/next layout
- [ ] Hugo build succeeds

## Testing

- **Existing tests to run**: `tests/test_integration_hugo.py`
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
