---
id: "003"
title: "Update readme.py guard parsing for Hugo shortcodes and content path"
status: todo
use-cases: [SUC-003]
depends-on: ["001"]
---

# Update readme.py guard parsing for Hugo shortcodes and content path

## Description

Update _SHARED_RE and _ONLY_RE regex patterns in readme.py to match Hugo
shortcode syntax. Change default docs_dir from "docs/docs" to "content".
Update all test fixtures in test_readme.py.

## Acceptance Criteria

- [ ] _SHARED_RE matches Hugo shortcode syntax
- [ ] _ONLY_RE matches Hugo shortcode syntax
- [ ] Default docs_dir is "content"
- [ ] All tests updated and passing

## Testing

- **Existing tests to run**: tests/test_readme.py
- **New tests to write**: none — update existing fixtures
- **Verification command**: `python3 -m pytest tests/test_readme.py -v`
