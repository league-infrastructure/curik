---
id: '025'
title: Hugo Theme Template Improvements
status: done
branch: sprint/025-hugo-theme-template-improvements
use-cases: []
---

# Sprint 025: Hugo Theme Template Improvements

## Goals

Make the curriculum-hugo-theme visually match the Motors Clinic Furo
theme. This is a rapid-iteration sprint — each ticket is a discrete
visual fix that can be verified by inspecting the test site.

## Problem

The current Hugo theme has the right structural bones (sidebar, content
area, Furo class names) but doesn't visually match the Motors Clinic
site. The logo is small, there's no prev/next navigation, the sidebar
nav structure doesn't match, and several Furo features are missing.

## Solution

A series of targeted template and CSS changes, each in its own ticket,
verified against the test site at `tests/content_test/python-basics/`.

## Success Criteria

- `hugo server` on the test site produces pages that look like the
  Motors Clinic screenshot
- Logo fills sidebar width
- Flat sidebar nav (no section headers for simple sites)
- Prev/next links at bottom of content pages
- Footer matches Motors style
- Integration tests still pass

## Scope

### In Scope

- Layout and CSS changes to curriculum-hugo-theme
- Template logic changes (nav, prev/next, footer)
- Test fixture updates if needed

### Out of Scope

- Dark mode / theme toggle (future sprint)
- Search functionality (future sprint)
- New shortcodes
- Python code changes to curik

## Test Strategy

Visual inspection via `hugo server` on the python-basics fixture.
Existing integration tests must continue to pass.

## Architecture Notes

All changes are in `curriculum-hugo-theme/` — layouts and CSS only.
No Python code changes expected.

## Definition of Ready

Before tickets can be created, all of the following must be true:

- [x] Sprint planning documents are complete (sprint.md, use cases, architecture)
- [x] Architecture review passed
- [x] Stakeholder has approved the sprint plan

## Tickets

1. Full-width sidebar logo with site title below
2. Flat sidebar navigation (remove section headers for flat sites)
3. Prev/next navigation at bottom of content pages
4. Footer matching Motors Clinic style
5. CSS polish — spacing, typography, link colors to match Furo
