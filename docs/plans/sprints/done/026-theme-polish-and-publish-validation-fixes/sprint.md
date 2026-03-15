---
id: '026'
title: Theme polish and publish validation fixes
status: done
branch: sprint/026-theme-polish-and-publish-validation-fixes
use-cases:
- SUC-001
- SUC-002
- SUC-003
- SUC-004
---

# Sprint 026: Theme polish and publish validation fixes

## Goals

Address four TODOs (003-006) from Motors curriculum agent feedback.
These are small, focused fixes that improve the theme and publishing
validation based on real-world usage.

## Problem

When publishing the Motors curriculum, the agent encountered several
gaps: the publish check didn't catch a missing `github_repo` param,
a stale local layout override silently blocked theme updates, there
was no CSS class for inline images, and no way to add project CSS
without overriding the entire base template.

## Solution

1. Add `github_repo` validation to publish readiness check
2. Add validation warning when local `baseof.html` shadows theme
3. Add `.inline` CSS class for inline images in theme
4. Add `custom.css` loading hook in theme template

## Success Criteria

- `check_publish_ready()` flags missing `github_repo` in hugo.toml
- `validate_course()` or publish check warns about local layout overrides
- Theme ships `.content img.inline` CSS class
- Theme loads `assets/css/custom.css` if present in course repo
- All existing tests pass

## Scope

### In Scope

- TODOs 003, 004, 005, 006
- Tests for new validation checks

### Out of Scope

- Full palette migration
- Any changes to sidebar layout beyond what's already shipped

## Test Strategy

- Unit tests for new publish validation checks
- Verify CSS class exists in theme stylesheet
- Verify custom.css loading in baseof.html template

## Architecture Notes

All changes are small and localized:
- server.py: add checks to `_read_publish_state()`
- main.css: add `.inline` class
- baseof.html: add `custom.css` resource loading

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan
