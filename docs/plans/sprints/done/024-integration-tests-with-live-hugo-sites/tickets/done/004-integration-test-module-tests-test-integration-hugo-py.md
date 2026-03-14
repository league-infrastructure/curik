---
id: '004'
title: Integration test module tests/test_integration_hugo.py
status: done
use-cases:
- SUC-001
- SUC-002
- SUC-003
depends-on:
- '001'
- '002'
- '003'
---

# Integration test module tests/test_integration_hugo.py

## Description

Create `tests/test_integration_hugo.py` with integration tests that:
1. Copy fixtures from `content_source/` to `content_test/` (once per class)
2. Run `scaffold_structure()` with a predefined structure
3. Verify `content/` dir, `hugo.toml`, and `themes/` are created
4. Run `hugo_build()` and assert success (skip if Hugo not installed)
5. Leave scratch directories in place for manual inspection

Test classes:
- `PythonBasicsIntegrationTest` — uses python-basics fixture (tier 2)
- `WebDevIntegrationTest` — uses web-dev fixture (tier 3)

Each class tests:
- Scaffold creates `content/` with correct module/lesson structure
- `hugo.toml` is generated with correct title and theme
- Theme is copied to `themes/curriculum-hugo-theme/`
- `content/_index.md` exists as landing page
- Hugo build succeeds (when Hugo is available)

## Acceptance Criteria

- [ ] Test module exists at `tests/test_integration_hugo.py`
- [ ] Fixtures are copied, never modified in place
- [ ] Tests pass when Hugo is installed
- [ ] Tests skip gracefully when Hugo is not installed
- [ ] After running tests, `cd tests/content_test/python-basics && hugo server` works
- [ ] Both tier 2 and tier 3 fixtures produce buildable sites

## Testing

- **Existing tests to run**: Full suite
- **New tests to write**: This IS the new test module
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
