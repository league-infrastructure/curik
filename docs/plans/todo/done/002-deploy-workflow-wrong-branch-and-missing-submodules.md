---
title: Deploy workflow uses wrong branch and missing submodule checkout
status: done
created: 2026-03-14
source: https://github.com/league-infrastructure/curik/issues/2
github_issue: 2
---

## Problem

The GitHub Actions deploy workflow (`curik/init/deploy-pages.yml`) has two
issues found while publishing the Motors course:

1. **Triggers on `main` instead of `master`** — League repos use `master`
   as the default branch, so pushes never trigger the workflow.
2. **Does not fetch submodules** — The theme may live in
   `themes/curriculum-hugo-theme/` as a git submodule. Without
   `submodules: true` on the checkout step, Hugo fails with missing
   template errors.

## Fix

In `curik/init/deploy-pages.yml`:
- Change `branches: [main]` to `branches: [main, master]` (support both)
- Add `submodules: true` to the `actions/checkout@v4` step

## Notes

- The workflow template is in `curik/init/deploy-pages.yml`
- It gets installed into course repos by `curik init` via `_write_github_workflow()`
- Existing course repos will pick up the fix on next `curik init` run
  (the workflow updater now replaces the file if content differs)
