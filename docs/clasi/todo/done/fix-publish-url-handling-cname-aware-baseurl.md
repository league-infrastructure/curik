---
status: done
---

# Fix publish URL handling: CNAME-aware baseURL, real publish guide, drop unused slug

## Context

Curik currently assumes a `curriculum.jointheleague.org/<slug>/` deployment
model that no site actually uses. Real deployments are one of two shapes:

1. **GitHub Pages default:** `https://league-curriculum.github.io/<repo>/`
2. **Custom domain:** `https://<cname>/` — CNAME present, served at root
   (e.g. `labs.jointheleague.org`).

## Problems

1. `curik/templates.py:77` `_base_url_from_repo` always produces `/<repo>/` —
   wrong for CNAME sites, which need `/`.
2. `curik/publish.py:59` `base_url_ok` greps `hugo.toml` for the literal
   string `"curriculum.jointheleague.org"` — a string the codebase never
   writes. The check is broken for every repo.
3. `curik/publish.py:101` publish guide hardcodes
   `https://curriculum.jointheleague.org/{slug}/` — a URL pattern no site
   uses.
4. `slug` field in `course.yml` is decorative — never written to `hugo.toml`,
   never used for real URLs. Dead weight that creates TBD friction at scaffold
   time.

## Required changes

- **Parse `hugo.toml` as TOML, do not grep it.** Use `tomllib` (stdlib in
  Python 3.11+) to load the file and read the `baseURL` key. String
  matching is fragile (whitespace, quoting, comments, multi-line values)
  and is the proximate cause of bug #2. Apply this rule to every other
  publish/check site that currently substring-matches `hugo.toml`.
- **`get_hugo_config`**: if `site/static/CNAME` exists, write
  `baseURL = "https://<cname>/"`; otherwise keep `/<repo>/`.
- **`base_url_ok`**: rewrite to parse the TOML and check the real
  invariant — CNAME present → baseURL matches `https://<cname>/`;
  no CNAME → baseURL is `/<repo>/` matching `repo_url`.
- **Publish guide**: show the actual target URL (CNAME root or
  `league-curriculum.github.io/<repo>/`), not the fictional
  curriculum.jointheleague.org path.
- **Drop `slug`** from `course.yml` template, from publish state, from
  required fields, and from anywhere else it's referenced.

## Trigger

Sprint 003 review surfaced `labs.jointheleague.org` failing the
`base_url_configured` check. Investigation showed the entire URL model was
wrong — the check has been broken for every repo, not just custom-domain
ones.
