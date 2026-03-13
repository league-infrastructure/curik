---
id: "001"
title: "Update scaffolding.py lesson stubs to emit Hugo shortcodes"
status: todo
use-cases: [SUC-001]
depends-on: []
---

# Update scaffolding.py lesson stubs to emit Hugo shortcodes

## Description

Replace `<div class="instructor-guide">...</div>` with Hugo shortcode syntax
in all 3 locations that generate lesson content in scaffolding.py. Update tests.

## Acceptance Criteria

- [ ] scaffold_structure() lesson stubs use Hugo shortcode
- [ ] create_lesson_stub() tier 1-2 stubs use Hugo shortcode
- [ ] create_lesson_stub() tier 3-4 stubs use Hugo shortcode
- [ ] Tests updated and passing

## Testing

- **Existing tests to run**: tests/test_scaffolding.py
- **New tests to write**: none — update existing assertions
- **Verification command**: `python3 -m pytest tests/test_scaffolding.py -v`
