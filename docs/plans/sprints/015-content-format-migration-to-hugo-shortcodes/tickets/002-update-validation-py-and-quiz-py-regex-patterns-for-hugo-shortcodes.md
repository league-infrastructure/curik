---
id: "002"
title: "Update validation.py and quiz.py regex patterns for Hugo shortcodes"
status: todo
use-cases: [SUC-002]
depends-on: ["001"]
---

# Update validation.py and quiz.py regex patterns for Hugo shortcodes

## Description

Update all regex patterns in validation.py (4 patterns) and quiz.py (1 pattern)
to match Hugo shortcode syntax. Update readme-shared validation check. Update tests.

## Acceptance Criteria

- [ ] validation.py regex patterns match Hugo shortcodes
- [ ] quiz.py regex pattern matches Hugo shortcode
- [ ] Readme guard validation checks for shortcode syntax
- [ ] All test fixtures updated and passing

## Testing

- **Existing tests to run**: tests/test_validation_enhanced.py, tests/test_validation_quiz.py, tests/test_content.py
- **New tests to write**: none — update existing fixtures
- **Verification command**: `python3 -m pytest tests/ -v`
