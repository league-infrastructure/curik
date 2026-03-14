---
id: "006"
title: "Remove links from H1 headings on content pages"
status: todo
use-cases: [SUC-001]
depends-on: []
---

# Remove links from H1 headings on content pages

## Description

The home page and list pages currently wrap section titles in `<a>` tags
inside `<h1>` or `<h2>` headings. When you click them you get a partial
page view. H1 headings should be plain text, not links — the sidebar
nav is for navigation.

Update index.html and list.html to render headings as plain text.

## Acceptance Criteria

- [ ] H1 on home page is plain text, not a link
- [ ] Section headings on list pages are plain text
- [ ] Hugo build succeeds

## Testing

- **Existing tests to run**: `tests/test_integration_hugo.py`
- **Verification command**: `python3 -m pytest tests/test_integration_hugo.py -v`
