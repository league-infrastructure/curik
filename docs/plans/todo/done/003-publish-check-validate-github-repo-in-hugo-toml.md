---
title: check_publish_ready() should validate github_repo is in hugo.toml
status: done
created: 2026-03-14
source: user-reported (Motors curriculum agent feedback)
sprint: '026'
tickets:
- '001'
---

## Problem

`check_publish_ready()` validates that `repo_url` is set in `course.yml`
(via `COURSE_YML_REQUIRED_FIELDS`), but doesn't verify that `github_repo`
actually made it into `hugo.toml` `[params]`. If `hugo.toml` was generated
before the `github_repo` wiring existed, the footer GitHub icon won't show
even though `course.yml` looks correct.

## Fix

In `_read_publish_state()`, add a check that reads `hugo.toml` and verifies
`github_repo` is present under `[params]`. Add it to the checks dict in
`tool_check_publish_ready()`.
