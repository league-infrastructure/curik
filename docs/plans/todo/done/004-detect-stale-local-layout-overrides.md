---
title: Detect stale local baseof.html overrides that shadow theme updates
status: done
created: 2026-03-14
source: user-reported (Motors curriculum agent feedback)
sprint: '026'
tickets:
- '002'
---

## Problem

Hugo's lookup order means `layouts/_default/baseof.html` in a course repo
takes precedence over the theme's version. The Motors course had a local
copy that was created during early scaffolding, which silently prevented
theme updates (like the sidebar collapse/expand fix) from taking effect.

There is no warning, validation, or detection mechanism for this.

## Fix Options

1. **Validation check**: Add a check to `validate_course()` or
   `check_publish_ready()` that warns if `layouts/_default/baseof.html`
   exists in the course repo.
2. **Scaffolding**: Ensure scaffolding never creates a local baseof.html.
3. **Staleness detection**: Compare the local override against the theme
   version and warn if they differ.

Option 1 is simplest and most immediately useful.
