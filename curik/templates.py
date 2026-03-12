"""Reusable templates for course scaffolding: mkdocs, devcontainer, course.yml."""

from __future__ import annotations

import json


def get_mkdocs_yml(title: str, tier: int) -> str:
    """Return a tier-appropriate mkdocs.yml configuration string.

    All tiers use MkDocs Material theme. Tiers 1-2 include instructor guide
    CSS/JS for the instructor-guide-primary layout.
    """
    lines = [
        f"site_name: {title}",
        "",
        "theme:",
        "  name: material",
        "  features:",
        "    - navigation.tabs",
        "    - navigation.sections",
        "    - content.code.copy",
        "",
        "plugins:",
        "  - search",
        "",
        "markdown_extensions:",
        "  - admonition",
        "  - pymdownx.highlight",
        "  - pymdownx.superfences",
    ]

    if tier in (1, 2):
        lines.extend([
            "",
            "extra_css:",
            "  - css/instructor-guide.css",
            "",
            "extra_javascript:",
            "  - js/instructor-guide.js",
        ])

    lines.append("")
    return "\n".join(lines)


def get_devcontainer_json(language: str) -> str:
    """Return a .devcontainer/devcontainer.json string for the given language.

    Supported languages: python, java.
    """
    language = language.lower()

    if language == "python":
        image = "mcr.microsoft.com/devcontainers/python:3.11"
        extensions = [
            "ms-python.python",
            "ms-python.vscode-pylance",
        ]
    elif language == "java":
        image = "mcr.microsoft.com/devcontainers/java:17"
        extensions = [
            "vscjava.vscode-java-pack",
        ]
    else:
        image = "mcr.microsoft.com/devcontainers/base:ubuntu"
        extensions = []

    config = {
        "name": f"{language.title()} Development",
        "image": image,
        "customizations": {
            "vscode": {
                "extensions": extensions,
            }
        },
        "postCreateCommand": "echo 'Container ready.'",
    }

    return json.dumps(config, indent=2) + "\n"


def get_course_yml_template(tier: int) -> str:
    """Return a course.yml template string with tier-appropriate defaults."""
    if tier == 1:
        grades = "K-2"
        category = "unplugged"
        estimated_weeks = 4
    elif tier == 2:
        grades = "3-5"
        category = "block-programming"
        estimated_weeks = 6
    elif tier == 3:
        grades = "6-8"
        category = "text-programming"
        estimated_weeks = 9
    elif tier == 4:
        grades = "9-12"
        category = "advanced"
        estimated_weeks = 12
    else:
        grades = "TBD"
        category = "TBD"
        estimated_weeks = 0

    lines = [
        "title: TBD",
        "slug: TBD",
        f"tier: {tier}",
        f"grades: {grades}",
        f"category: {category}",
        "topics: []",
        "prerequisites: []",
        "lessons: 0",
        f"estimated_weeks: {estimated_weeks}",
        "curriculum_url: TBD",
        "repo_url: TBD",
        "description: TBD",
        "",
    ]
    return "\n".join(lines)
