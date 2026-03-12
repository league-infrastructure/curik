---
id: "004"
title: "Implement README generation from comment guards"
status: todo
use-cases: []
depends-on: []
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Implement README generation from comment guards

## Description

Create the `curik/readme.py` module that implements README generation from MkDocs lesson pages using HTML comment guards. The module must parse `<!-- readme-shared -->` / `<!-- /readme-shared -->` and `<!-- readme-only -->` / `<!-- /readme-only -->` comment markers from Markdown files, extract the content within each guarded section, and assemble a README.md by combining `readme-shared` content (which appears in both MkDocs and README) with `readme-only` content (which appears only in the README). The assembled README.md is written to the corresponding repo-root lesson directory. Pages with no guards produce no README. This is needed for Tier 3-4 courses where students browse lesson directories on GitHub or in Codespaces and need README summaries without maintaining separate files that drift from the MkDocs content.

## Acceptance Criteria

- [ ] `curik/readme.py` module exists
- [ ] Function to parse `<!-- readme-shared -->` ... `<!-- /readme-shared -->` guard blocks from Markdown content
- [ ] Function to parse `<!-- readme-only -->` ... `<!-- /readme-only -->` guard blocks from Markdown content
- [ ] Parser handles multiple guard blocks per file, preserving their order
- [ ] Parser handles nested Markdown content within guards (headings, code blocks, lists)
- [ ] Parser handles edge cases: empty guards, unclosed guards (skipped or error)
- [ ] Function to assemble README.md content from extracted shared and readme-only sections
- [ ] Function to write the assembled README.md to a given repo-root lesson directory
- [ ] Pages with no comment guards produce no README output (no empty file written)
- [ ] Generated README content preserves the original Markdown formatting within guards

## Testing

- **Existing tests to run**: `uv run pytest tests/` to verify no regressions
- **New tests to write**: Covered by ticket 007; guard parsing with various inputs, README assembly, file I/O, no-guard handling
- **Verification command**: `uv run pytest tests/test_readme.py -v`
