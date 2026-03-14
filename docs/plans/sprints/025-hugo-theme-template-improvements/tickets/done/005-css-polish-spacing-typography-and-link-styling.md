---
id: "005"
title: "CSS polish — spacing, typography, and link styling"
status: todo
use-cases: [SUC-001]
depends-on: ["001", "002", "003", "004"]
---

# CSS polish — spacing, typography, and link styling

## Description

Final pass on CSS to ensure visual consistency with the Motors Clinic Furo theme. Compare the test site side-by-side with the Motors screenshot and adjust:
- Sidebar background color and border
- Link colors (brand blue, visited purple)
- Content area max-width and padding
- Heading sizes and weights
- Code block styling
- Overall spacing and rhythm

## Acceptance Criteria

- [ ] Sidebar colors match Furo light theme
- [ ] Link colors match Furo defaults
- [ ] Content area width and padding match
- [ ] Typography is consistent
- [ ] Hugo build succeeds
- [ ] Integration tests pass

## Testing

- **Existing tests to run**: `tests/test_integration_hugo.py`
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
