---
id: "004"
title: "Footer matching Motors Clinic style"
status: done
use-cases: [SUC-001]
depends-on: []
---

# Footer matching Motors Clinic style

## Description

The Motors Clinic footer has:
- Left side: "Copyright © 2024, The League" and "Made with Sphinx and @pradyunsg's Furo"
- Right side: GitHub icon linking to the repo
- A horizontal rule separating it from prev/next nav

Update our footer to match this layout: copyright on the left, "Made with Hugo and curriculum-hugo-theme" credit, and a GitHub repo link on the right (using site params for the repo URL).

## Acceptance Criteria

- [ ] Footer shows copyright on the left
- [ ] Footer shows "Made with Hugo" credit
- [ ] Footer has configurable GitHub repo link on the right
- [ ] Horizontal rule above footer
- [ ] Hugo build succeeds

## Testing

- **Existing tests to run**: `tests/test_integration_hugo.py`
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
