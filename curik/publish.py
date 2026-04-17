"""Publish-readiness checks and guide generation for Curik courses."""

from __future__ import annotations

from pathlib import Path

import yaml

from .hugo import hugo_build
from .project import COURSE_YML_REQUIRED_FIELDS, _is_tbd


def _read_publish_state(root: Path) -> dict:
    """Read course metadata and check publish-readiness indicators."""
    state: dict = {
        "slug": "",
        "title": "this course",
        "tier": 0,
        "has_course_yml": False,
        "course_yml_data": {},
        "course_yml_tbd_fields": [],
        "has_workflow": (root / ".github" / "workflows" / "deploy-pages.yml").exists(),
        "has_gitignore": (root / ".gitignore").exists(),
        "has_hugo_toml": (root / "hugo.toml").exists(),
        "base_url_ok": False,
        "has_repo_url": False,
        "has_local_baseof": (root / "layouts" / "_default" / "baseof.html").exists(),
        "has_content": False,
        "content_sections": 0,
        "content_pages": 0,
        "has_theme": (root / "themes" / "curriculum-hugo-theme").exists()
            or (root / "themes" / "curriculum-hugo-theme").is_symlink(),
        "hugo_builds": False,
    }

    course_yml = root / "course.yml"
    if course_yml.is_file():
        state["has_course_yml"] = True
        try:
            data = yaml.safe_load(course_yml.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                state["course_yml_data"] = data
                state["slug"] = data.get("slug", "")
                state["title"] = data.get("title", state["title"])
                state["tier"] = data.get("tier", 0)
                repo_url = data.get("repo_url", "")
                state["has_repo_url"] = bool(repo_url) and repo_url != "TBD"
                # Check required fields for TBD/empty values
                tbd = []
                for field in COURSE_YML_REQUIRED_FIELDS:
                    if _is_tbd(data.get(field)):
                        tbd.append(field)
                state["course_yml_tbd_fields"] = tbd
        except yaml.YAMLError:
            pass

    if state["has_hugo_toml"]:
        content = (root / "hugo.toml").read_text(encoding="utf-8")
        state["base_url_ok"] = "curriculum.jointheleague.org" in content
        # repo_url is now read from course.yml via data mount, not hugo.toml

    content_dir = root / "content"
    if content_dir.is_dir():
        sections = [
            d for d in content_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]
        state["content_sections"] = len(sections)
        pages = list(content_dir.rglob("*.md"))
        state["content_pages"] = len(pages)
        state["has_content"] = len(pages) > 1  # more than just _index.md

    # Try a Hugo build to check for errors
    if state["has_hugo_toml"] and state["has_theme"]:
        try:
            result = hugo_build(root)
            state["hugo_builds"] = result.get("success", False)
            state["build_errors"] = result.get("stderr", "")
        except Exception as e:
            state["hugo_builds"] = False
            state["build_errors"] = str(e)

    return state


def get_publish_guide(root: Path) -> str:
    """Return the publishing guide with pre-publish and post-publish checklists.

    Reads the course state and returns a personalized Markdown guide with:
    - Setup instructions for GitHub Pages
    - Pre-publish checklist (is everything ready?)
    - Post-publish checklist (verify the deployment)
    """
    s = _read_publish_state(root)

    slug = s["slug"]
    title = s["title"]
    has_slug = slug and slug != "TBD"

    if has_slug:
        url = f"https://curriculum.jointheleague.org/{slug}/"
        repo = f"league-curriculum/{slug}"
    else:
        url = "https://curriculum.jointheleague.org/<slug>/"
        repo = "league-curriculum/<slug>"

    lines = [
        f"# Publishing Guide: {title}",
        "",
        f"**Target URL:** {url}",
        f"**GitHub repo:** {repo}",
        "",
        "## Hosting Architecture",
        "",
        "All League curricula are published to GitHub Pages under the",
        "`league-curriculum` GitHub organization with a shared custom domain:",
        "",
        "- **Index:** https://curriculum.jointheleague.org/ (from league-curriculum/league-curriculum)",
        f"- **This course:** {url}",
        "",
        "GitHub Pages automatically routes project repos as subpaths of",
        "the org custom domain.",
        "",

        # ── Pre-publish checklist ──────────────────────────────────
        "## Pre-Publish Checklist",
        "",
        "Everything here must pass before deploying.",
        "",
        "### Configuration",
        "",
    ]

    def check(ok: bool, yes: str, no: str) -> str:
        return f"- [x] {yes}" if ok else f"- [ ] {no}"

    # ── course.yml metadata ────────────────────────────────────
    tbd_fields = s["course_yml_tbd_fields"]
    course_data = s["course_yml_data"]
    course_yml_ok = s["has_course_yml"] and len(tbd_fields) == 0

    lines.append(check(
        s["has_course_yml"],
        "`course.yml` exists",
        "**Create `course.yml`** — run `curik init`",
    ))

    if s["has_course_yml"]:
        lines.append(check(
            course_yml_ok,
            "All required `course.yml` fields are set",
            f"**{len(tbd_fields)} field(s) still TBD** in `course.yml` (see below)",
        ))

        if tbd_fields:
            lines.extend([
                "",
                "#### course.yml Fields to Complete",
                "",
                "The following fields are required for publishing. Set them in",
                "`course.yml` based on the course content, or ask the stakeholder",
                "if unsure. For `curriculum_url` and `repo_url`, use the values",
                "shown in the Target URL and GitHub repo at the top of this guide.",
                "",
                "| Field | Current | Required |",
                "|-------|---------|----------|",
            ])
            field_hints = {
                "title": "Human-readable course title",
                "slug": "URL path segment (lowercase, hyphenated)",
                "tier": "1 (K-2), 2 (3-5), 3 (6-8), or 4 (9-12)",
                "grades": "Grade range, e.g. 'K-2', '6-8'",
                "category": "unplugged, block-programming, text-programming, or advanced",
                "description": "One-line course description",
                "curriculum_url": f"{url}",
                "repo_url": f"https://github.com/{repo}",
            }
            for field in tbd_fields:
                current = course_data.get(field, "missing")
                hint = field_hints.get(field, "Required value")
                lines.append(f"| `{field}` | `{current}` | {hint} |")

            lines.extend([
                "",
                "**Agent instruction:** If you can infer the correct values from",
                "the course content and structure, update `course.yml` with your",
                "best values and present them to the stakeholder for review.",
                "If you cannot determine a value, ask the stakeholder.",
                "",
            ])

    # ── Infrastructure files ───────────────────────────────────
    lines.extend(["", "### Infrastructure", ""])

    lines.append(check(
        s["has_hugo_toml"],
        "`hugo.toml` exists",
        "**Generate `hugo.toml`** — run `tool_hugo_setup()`",
    ))
    lines.append(check(
        s["base_url_ok"],
        f"`baseURL` set to `{url}`",
        "**Fix `baseURL`** in `hugo.toml` — run `tool_hugo_setup()` to regenerate",
    ))
    lines.append(check(
        s["has_theme"],
        "Hugo theme installed",
        "**Install theme** — run `tool_hugo_setup()`",
    ))
    lines.append(check(
        s["has_gitignore"],
        "`.gitignore` installed",
        "**Run `curik init`** to install `.gitignore`",
    ))
    lines.append(check(
        s["has_workflow"],
        "GitHub Actions workflow installed",
        "**Run `curik init`** to install `.github/workflows/deploy-pages.yml`",
    ))

    lines.append(check(
        s["has_repo_url"],
        "`repo_url` set in `course.yml`",
        "**Missing `repo_url`** in `course.yml` — set it to the GitHub repo URL",
    ))

    if s["has_local_baseof"]:
        lines.extend([
            "",
            "### Warning",
            "",
            "- [ ] **Local `layouts/_default/baseof.html` detected** — this overrides",
            "  the theme template and may block theme updates. Delete it unless you",
            "  have a specific reason to keep it.",
        ])

    lines.extend(["", "### Content", ""])

    lines.append(check(
        s["has_content"],
        f"{s['content_sections']} modules, {s['content_pages']} pages",
        "**No content found** — scaffold or create content before publishing",
    ))
    lines.append(check(
        s["hugo_builds"],
        "Hugo builds successfully",
        "**Hugo build fails** — fix build errors before publishing",
    ))
    if not s["hugo_builds"] and s.get("build_errors"):
        # Include first few lines of build error
        err_lines = s["build_errors"].strip().splitlines()[:5]
        for err in err_lines:
            lines.append(f"  > {err}")

    # Summarize readiness
    course_yml_ok = s["has_course_yml"] and len(s["course_yml_tbd_fields"]) == 0
    config_ready = all([
        course_yml_ok, s["has_hugo_toml"], s["base_url_ok"],
        s["has_theme"], s["has_gitignore"], s["has_workflow"],
        s["has_repo_url"],
    ])
    content_ready = s["has_content"] and s["hugo_builds"]
    all_ready = config_ready and content_ready

    lines.extend([
        "",
        f"### Status: {'READY TO PUBLISH' if all_ready else 'NOT READY'}",
        "",
    ])

    if not all_ready:
        lines.append("Fix the unchecked items above before publishing.")
        lines.append("")

    # ── GitHub setup ───────────────────────────────────────────
    lines.extend([
        "## GitHub Repo Setup (one-time, manual)",
        "",
        f"1. Push this repo to `https://github.com/{repo}`",
        "2. Go to **Settings → Pages**",
        "3. Under **Build and deployment → Source**, select **GitHub Actions**",
        "4. Push to `main` to trigger the first deploy",
        "",
        "## DNS (one-time, org-level)",
        "",
        "If not already configured:",
        "",
        "1. Add a CNAME record: `curriculum.jointheleague.org` → `league-curriculum.github.io`",
        "2. In the `league-curriculum` org GitHub settings, configure",
        "   `curriculum.jointheleague.org` as the verified custom domain",
        "",

        # ── Post-publish checklist ─────────────────────────────────
        "## Post-Publish Checklist",
        "",
        "After the first deploy, verify everything works:",
        "",
        f"- [ ] Site loads at {url}",
        "- [ ] All sidebar navigation links work",
        "- [ ] Images and code blocks render correctly",
        "- [ ] Previous/Next navigation works through all lessons",
        f"- [ ] GitHub repo link in footer points to `https://github.com/{repo}`",
    ])
    if s.get("tier") in (1, 2):
        lines.append("- [ ] Instructor guide toggle appears and works")

    lines.extend([
        "- [ ] Site works on mobile (sidebar collapses correctly)",
        f"- [ ] Course added to index at `league-curriculum/league-curriculum`",
        "",
        "## How Deployment Works",
        "",
        "1. You push to `main`",
        "2. GitHub Actions: checkout → Hugo build (minified) → upload → deploy",
        "3. Site is live at the target URL within ~60 seconds",
    ])

    return "\n".join(lines)


def check_publish_ready(root: Path) -> dict:
    """Check if this course is ready to publish to GitHub Pages.

    Returns a dict with pass/fail status for each requirement and an overall
    ``ready`` boolean.
    """
    s = _read_publish_state(root)
    has_slug = bool(s["slug"]) and s["slug"] != "TBD"

    course_yml_complete = s["has_course_yml"] and len(s["course_yml_tbd_fields"]) == 0

    checks = {
        "course_yml_exists": s["has_course_yml"],
        "course_yml_complete": course_yml_complete,
        "hugo_toml_exists": s["has_hugo_toml"],
        "base_url_configured": s["base_url_ok"],
        "repo_url_set": s["has_repo_url"],
        "theme_installed": s["has_theme"],
        "gitignore_installed": s["has_gitignore"],
        "workflow_installed": s["has_workflow"],
        "has_content": s["has_content"],
        "hugo_builds": s["hugo_builds"],
    }

    warnings = {}
    if s["has_local_baseof"]:
        warnings["local_baseof_override"] = (
            "layouts/_default/baseof.html exists and shadows the theme template"
        )

    url = ""
    if has_slug:
        url = f"https://curriculum.jointheleague.org/{s['slug']}/"

    result: dict = {
        "ready": all(checks.values()),
        "checks": checks,
        "slug": s["slug"],
        "title": s["title"],
        "url": url,
        "content_sections": s["content_sections"],
        "content_pages": s["content_pages"],
    }

    if s["course_yml_tbd_fields"]:
        result["course_yml_tbd_fields"] = s["course_yml_tbd_fields"]

    if warnings:
        result["warnings"] = warnings

    return result
