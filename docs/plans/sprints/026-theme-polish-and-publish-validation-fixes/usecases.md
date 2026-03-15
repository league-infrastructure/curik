---
status: final
---

# Sprint 026 Use Cases

## SUC-001: Publish check validates github_repo in hugo.toml
Parent: TODO-003

- **Actor**: Agent running `/curik publish`
- **Preconditions**: course.yml has `repo_url` set, hugo.toml exists
- **Main Flow**:
  1. Agent calls `check_publish_ready()`
  2. Check reads hugo.toml and verifies `github_repo` is under `[params]`
  3. If missing, reports it as a failed check
- **Postconditions**: Publish check catches stale hugo.toml configs
- **Acceptance Criteria**:
  - [ ] `_read_publish_state()` checks for `github_repo` in hugo.toml
  - [ ] `check_publish_ready()` includes `github_repo_in_config` in checks

## SUC-002: Detect stale local layout overrides
Parent: TODO-004

- **Actor**: Agent running publish check or validation
- **Preconditions**: Course repo may have `layouts/_default/baseof.html`
- **Main Flow**:
  1. Publish check scans for local layout overrides
  2. If `layouts/_default/baseof.html` exists, flags it as a warning
- **Postconditions**: Agent is alerted to potential theme shadowing
- **Acceptance Criteria**:
  - [ ] `_read_publish_state()` checks for local baseof.html
  - [ ] Publish guide surfaces the warning

## SUC-003: Inline image CSS class
Parent: TODO-005

- **Actor**: Lesson author using inline images
- **Preconditions**: Author needs small icon in paragraph text
- **Main Flow**:
  1. Author writes `<img class="inline" src="...">` in markdown
  2. Theme CSS styles it as inline, correctly sized
- **Postconditions**: Image renders inline at text height
- **Acceptance Criteria**:
  - [ ] `.content img.inline` class exists in main.css
  - [ ] Styled: inline display, 1.2em height, text-bottom alignment

## SUC-004: Project-level CSS override loading
Parent: TODO-006

- **Actor**: Course developer needing custom CSS
- **Preconditions**: Course has `assets/css/custom.css`
- **Main Flow**:
  1. Theme baseof.html checks for `css/custom.css` resource
  2. If present, loads it after theme CSS
- **Postconditions**: Custom styles apply without overriding baseof.html
- **Acceptance Criteria**:
  - [ ] baseof.html includes custom.css resource loading
  - [ ] CSS loads after main.css and instructor-guide.css
