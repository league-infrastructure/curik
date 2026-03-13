---
status: complete
---

# Sprint 017 Use Cases

## TUC-001: Hugo Renders Instructor Guide Shortcode

- **Actor**: Curriculum developer running `hugo server`
- **Preconditions**: Course scaffolded with Curik, theme referenced in hugo.toml
- **Main Flow**:
  1. Developer runs `hugo server` on a curriculum repo
  2. Hugo finds `{{< instructor-guide >}}` shortcode in lesson pages
  3. Theme's shortcode template wraps content in a collapsible div
  4. Instructor guide is hidden by default, toggleable by instructors
- **Postconditions**: Instructor guide renders correctly with show/hide toggle
- **Acceptance Criteria**:
  - [x] instructor-guide.html shortcode template exists
  - [x] CSS for toggle behavior exists

## TUC-002: Hugo Renders README Guard Shortcodes

- **Actor**: Curriculum developer running `hugo server`
- **Preconditions**: Tier 3-4 lesson pages with readme-shared/readme-only guards
- **Main Flow**:
  1. Hugo encounters `{{< readme-shared >}}` shortcode
  2. Content renders normally on the site
  3. Hugo encounters `{{< readme-only >}}` shortcode
  4. Content is hidden from the rendered site
- **Postconditions**: Shared content visible on site, only content hidden
- **Acceptance Criteria**:
  - [x] readme-shared.html renders inner content
  - [x] readme-only.html hides inner content
