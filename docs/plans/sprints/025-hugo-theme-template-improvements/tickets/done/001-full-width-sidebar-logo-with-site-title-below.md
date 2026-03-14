---
id: "001"
title: "Full-width sidebar logo with site title below"
status: todo
use-cases: [SUC-001]
depends-on: []
---

# Full-width sidebar logo with site title below

## Description

In the Motors Clinic theme, the League logo fills the entire sidebar width as a large block element, with the site title ("Motors Clinic") displayed as text below it. Currently our theme has a small inline logo next to the title text.

Update baseof.html and main.css so the logo image fills the sidebar width and the site title appears below it as a separate block.

## Acceptance Criteria

- [ ] Logo image fills full sidebar width
- [ ] Site title appears below the logo as block text
- [ ] Hugo build succeeds
- [ ] Integration tests pass

## Testing

- **Existing tests to run**: `tests/test_integration_hugo.py`
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
