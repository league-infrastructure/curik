---
status: final
---

# Architecture

## Architecture Overview

Curik is a Python MCP server that guides AI agents through curriculum
development. This sprint adds integration test infrastructure that operates
on real curriculum fixtures and fixes `scaffold_structure()` to produce
runnable Hugo sites.

```
tests/
  content_source/                    ← Checked into git, never modified
    python-basics/                   ← Tier 2 fixture
      course.yml
      .course/state.json, spec.md
    web-dev/                         ← Tier 3 fixture
      course.yml
      .course/state.json, spec.md
  content_test/                      ← Gitignored scratch area
    python-basics/                   ← Copied from content_source/
      content/                       ← Created by scaffold_structure()
        _index.md
        01-variables/
        02-control-flow/
      hugo.toml                      ← Generated during scaffolding
      themes/curriculum-hugo-theme/  ← Copied during scaffolding
  test_integration_hugo.py           ← New integration test module
```

## Technology Stack

- **Python 3.10+** — existing project language
- **Hugo** — static site generator (required for build tests, optional skip)
- **shutil.copytree** — fixture copying
- **unittest** — existing test framework

## Component Design

### Component: scaffold_structure() fix (scaffolding.py)

**Purpose**: Place content under `content/` instead of repo root.

**Use Cases**: SUC-001

Current behavior (line 57):
```python
mod_dir = root / mod_name  # creates 01-intro/ at repo root
```

New behavior:
```python
mod_dir = root / "content" / mod_name  # creates content/01-intro/
```

Also needs to:
- Create `content/_index.md` as the site landing page (created by
  `scaffold_structure()` before the module loop, with Hugo frontmatter:
  `title` from course.yml, `weight: 1`)
- Resource collections still go under `resources/` (unchanged)

### Component: create_lesson_stub() update (scaffolding.py)

**Purpose**: Align standalone lesson creation with the `content/` convention.

`create_lesson_stub()` (line 158) currently places files at
`root / module / lesson`. After this sprint it must use
`root / "content" / module / lesson` so that independently created
lessons land inside Hugo's content directory, consistent with
`scaffold_structure()`.

### Component: hugo_setup() (new function in templates.py)

**Purpose**: Generate hugo.toml and copy the theme into a course repo.

**Location**: `curik/templates.py` — keeps config/theme generation cohesive
with the existing `get_hugo_config()` and `get_theme_source()` functions.

**Use Cases**: SUC-001

```python
def hugo_setup(root: Path, title: str, tier: int) -> dict[str, list[str]]:
    """Generate hugo.toml and copy the theme into a course repo."""
```

Steps:
1. Calls `get_hugo_config(title, tier)` to generate `hugo.toml`
2. Writes `hugo.toml` to the project root
3. Copies `curriculum-hugo-theme/` from curik's bundled copy to
   `themes/curriculum-hugo-theme/` in the course repo

Called by `scaffold_structure()` as an orchestration step. Also exposed
as a standalone `tool_hugo_setup()` MCP tool for cases where the agent
needs to regenerate the Hugo config without re-scaffolding.

### Component: test fixtures (tests/content_source/)

**Purpose**: Realistic curriculum projects for integration testing.

**Use Cases**: SUC-002, SUC-003

Each fixture directory contains:
- `course.yml` — course metadata (title, tier, slug, etc.)
- `.course/state.json` — phase state (set to phase2 so scaffolding works)
- `.course/spec.md` — minimal spec document

Fixtures do NOT contain `content/`, `hugo.toml`, or `themes/` — those
are created by the operations under test.

Two fixtures:
1. **python-basics** — Tier 2 (instructor-guide primary, no devcontainer)
   - 2 modules, 2-3 lessons each
2. **web-dev** — Tier 3 (student content + instructor guide, devcontainer)
   - 2 modules, 2-3 lessons each

### Component: test harness (tests/test_integration_hugo.py)

**Purpose**: Copy fixtures, run operations, verify Hugo builds.

**Use Cases**: SUC-002

Test class structure:
```python
class HugoIntegrationTest(unittest.TestCase):
    FIXTURE = "python-basics"

    @classmethod
    def setUpClass(cls):
        """Copy fixture to content_test/ once for the whole class."""
        src = CONTENT_SOURCE / cls.FIXTURE
        cls.root = CONTENT_TEST / cls.FIXTURE
        if cls.root.exists():
            shutil.rmtree(cls.root)
        shutil.copytree(src, cls.root)

    def test_scaffold_creates_content_dir(self):
        ...

    def test_hugo_toml_generated(self):
        ...

    @unittest.skipUnless(shutil.which("hugo"), "Hugo not installed")
    def test_hugo_build_succeeds(self):
        result = hugo_build(self.root)
        self.assertTrue(result["success"], result["error"])
```

Key design decisions:
- `setUpClass` (not `setUp`) — copy once per test class, not per test
- Don't clean up `content_test/` after tests — developer can inspect
- Separate test class per fixture (or parameterize)

### Component: .gitignore update

Add `tests/content_test/` to `.gitignore`.

## Dependency Map

```
test_integration_hugo.py
  ├── tests/content_source/*     (fixtures, read-only)
  ├── tests/content_test/*       (scratch, gitignored)
  ├── curik/scaffolding.py       (scaffold_structure — modified)
  ├── curik/templates.py         (get_hugo_config, get_theme_source)
  └── curik/hugo.py              (hugo_build)
```

## Data Model

No data model changes.

## Security Considerations

None — test infrastructure only. Theme copy uses `shutil.copytree` on
local paths within the repo.

## Decisions

1. **`hugo_setup()` lives in `templates.py`** and is called by
   `scaffold_structure()` automatically. Also exposed as standalone
   `tool_hugo_setup()` MCP tool. Rationale: keeps config/theme generation
   cohesive with existing template functions.

2. **`content/_index.md`** is created by `scaffold_structure()` before the
   module loop. Content: Hugo frontmatter with `title` (from course.yml)
   and a "Course overview" placeholder body.

3. **`create_lesson_stub()`** is updated to use `content/` prefix,
   consistent with `scaffold_structure()`.

## Sprint Changes

### New Components

- `tests/content_source/python-basics/` — Tier 2 curriculum fixture
- `tests/content_source/web-dev/` — Tier 3 curriculum fixture
- `tests/test_integration_hugo.py` — Integration test module
- `hugo_setup()` function — generates hugo.toml and copies theme

### Changed Components

- **scaffolding.py**: `scaffold_structure()` places content under `content/`
  instead of repo root; calls `hugo_setup()`. `create_lesson_stub()` also
  updated to use `content/` prefix.
- **templates.py**: New `hugo_setup()` function
- **server.py**: New `tool_hugo_setup()` MCP tool
- **tests/test_scaffolding.py**: Update path assertions in
  `ScaffoldStructureTest` (~6 tests), `ScaffoldTierMirrorTest` (~3 tests),
  `ScaffoldDevcontainerTest` (~2 tests), plus `LessonStubTest`
- **.gitignore**: Add `tests/content_test/`

### Migration Concerns

Changing `scaffold_structure()` to use `content/` will break existing unit
tests that expect modules at the repo root. These tests must be updated
in the same ticket. Approximately 15+ assertions need path prefix changes.
