---
status: in-progress
sprint: '003'
tickets:
- 003-001
---

# Sequester Hugo into `site/` in scaffolded curriculum projects

## Context

When `curik` scaffolds a curriculum project, it dumps Hugo files at the
project root: `hugo.toml`, `themes/curriculum-hugo-theme/`, `content/`,
plus build artifacts (`public/`, `resources/_gen/`, `.hugo_build.lock`)
and an optional `layouts/` override. Mixed in with curik's own files
(`course.yml`, `.course/`, `.claude/`, `CLAUDE.md`, `README.md`) the
root becomes hard to read and authors can't tell at a glance what is
"the curriculum" vs "the Hugo site that renders it."

The fix is to sequester everything Hugo into a `site/` subdirectory:

```
<project root>/
├── course.yml          ← stays at root (curik's source of truth)
├── .course/            ← stays
├── .claude/            ← stays
├── CLAUDE.md           ← stays
├── README.md           ← stays
└── site/               ← NEW: everything Hugo lives here
    ├── hugo.toml
    ├── content/        ← lesson .md files
    ├── themes/curriculum-hugo-theme/
    ├── layouts/        ← optional theme overrides
    ├── public/         ← build output (gitignored)
    ├── resources/      ← Hugo cache (gitignored)
    └── .hugo_build.lock (gitignored)
```

Existing scaffolded repos in the wild keep working as-is until the
stakeholder runs `curik migrate hugo-layout`. Curik detects the legacy
layout on every invocation and warns loudly with a pointer to the
migrate command, but never auto-migrates.

## Decisions (confirmed with stakeholder)

- **Subdir name**: `site/`
- **`content/` moves too**: lesson authoring path becomes `site/content/01-intro/01-hello.md`
- **Migration**: detect-and-warn on every curik run; explicit `curik migrate hugo-layout` opt-in; no auto-migration

## Approach

### 1. Introduce a single source-of-truth path constant

Add to `curik/templates.py`:

```python
SITE_DIR = "site"   # subdirectory holding all Hugo files within a curriculum project
```

Define helpers (probably in a new tiny `curik/paths.py`, or extending
`templates.py`) so no caller hardcodes the string:

```python
def site_root(root: Path) -> Path:        # root / "site"
def hugo_toml_path(root: Path) -> Path:   # root / "site" / "hugo.toml"
def content_dir(root: Path) -> Path:      # root / "site" / "content"
def themes_dir(root: Path) -> Path:       # root / "site" / "themes"
def theme_dir(root: Path) -> Path:        # root / "site" / "themes" / "curriculum-hugo-theme"
```

Every existing `root / "hugo.toml"`, `root / "themes" / ...`,
`root / "content"` site reference gets routed through these helpers.

### 2. Update `hugo.toml` generation for the new layout

[curik/templates.py:91-144](curik/templates.py#L91-L144) — `get_hugo_config()`:

- Mounts stay relative to `hugo.toml`'s dir (now `site/`):
  - `content` mount stays `source = "content"` (now `site/content`).
  - `course.yml` mount becomes `source = "../course.yml"`. Hugo
    supports `..` in module mounts (verified behavior in Hugo 0.120+).

### 3. Update Hugo invocation to run inside `site/`

[curik/hugo.py:133-168](curik/hugo.py#L133-L168) — `hugo_build()`:

- Change `cwd=str(root)` → `cwd=str(site_root(root))`.

[curik/init/deploy-pages.yml:32-37](curik/init/deploy-pages.yml#L32-L37):

- `run: hugo --minify --source site`
- `path: ./site/public`

### 4. Update every read/write site

Each location below currently uses `root / "<hugo path>"`. Replace
with the helper. (Reference inventory in conversation; these are
the load-bearing edits.)

- [curik/templates.py:30](curik/templates.py#L30), [45-67](curik/templates.py#L45-L67),
  [243-291](curik/templates.py#L243-L291): `bump_curriculum_version`,
  `hugo_setup`, `hugo_setup_from_course`. The theme installs into
  `site/themes/curriculum-hugo-theme/`; `hugo.toml` writes to `site/hugo.toml`.
- [curik/scaffolding.py:56-128](curik/scaffolding.py#L56-L128),
  [170-175](curik/scaffolding.py#L170-L175),
  [228](curik/scaffolding.py#L228): `content/` creation routes
  through `content_dir(root)`. Module dirs and lesson stubs land
  under `site/content/`.
- [curik/hugo.py:48-131](curik/hugo.py#L48-L131): `list_content_pages`,
  `create_content_page`, `update_frontmatter` — all read/write
  `site/content/`. Returned paths to callers should remain relative
  to `content_dir` (e.g. `01-intro/01-hello.md`), not include the
  `site/` prefix, so the public CLI surface stays stable.
- [curik/syllabus.py:92](curik/syllabus.py#L92): `docs_dir = content_dir(root)`.
- [curik/readme.py:39-62](curik/readme.py#L39-L62): default `docs_dir`
  becomes `site/content` (or, cleaner, change the parameter default
  from a string to deriving it from `content_dir(root)`).
- [curik/cli.py:686](curik/cli.py#L686), [1009](curik/cli.py#L1009):
  the `--docs-dir` default changes to `site/content`.
- [curik/publish.py:24-81](curik/publish.py#L24-L81),
  [196-258](curik/publish.py#L196-L258),
  [335](curik/publish.py#L335): `has_hugo_toml`, `has_theme`,
  `has_local_baseof`, content scan, base_url read, build call —
  all routed through helpers.
- [curik/migrate.py:30](curik/migrate.py#L30),
  [99-139](curik/migrate.py#L99-L139),
  [157-158](curik/migrate.py#L157-L158): `migrate_structure` writes
  the new layout. Protected names list adds `"site"` (and removes
  `"hugo.toml"`, `"themes"` since they're no longer at root).
  Hugo-presence detection checks `hugo_toml_path(root)`, falling
  back to `root / "hugo.toml"` for legacy-layout detection.

### 5. Add legacy-layout detection that warns on every invocation

New module `curik/layout_check.py` with a single function:

```python
def check_legacy_hugo_layout(root: Path) -> str | None:
    """Return a warning string if Hugo files are at root instead of site/.

    Returns None if layout is correct or no Hugo presence detected.
    """
```

Detection rule: any of `root/hugo.toml`, `root/themes/curriculum-hugo-theme/`,
or `root/content/_index.md` exists AND `root/site/hugo.toml` does NOT
exist.

Wire it into the CLI dispatcher in [curik/cli.py](curik/cli.py)
near the top of `main()` (or wherever `--path` is resolved). Print
the warning to stderr before executing the requested command:

```
WARNING: This project uses the legacy Hugo layout (hugo.toml at root).
Run `curik migrate hugo-layout` to move Hugo files into site/.
The legacy layout will stop working in a future release.
```

The warning fires on every command but does not block execution —
existing projects keep working until the user opts in to migrate.
Suppress when `--quiet` or `CURIK_NO_LAYOUT_WARNING=1` is set, so
CI and scripted callers can silence it after they've acknowledged.

### 6. Add `curik migrate hugo-layout` command

New subcommand in [curik/cli.py](curik/cli.py) that calls a new
`curik/layout_migrate.py` function:

```python
def migrate_hugo_layout(root: Path, *, dry_run: bool = False) -> dict[str, list[str]]:
    """Move Hugo files from root into site/, rewrite hugo.toml mounts,
    update .gitignore. Idempotent: no-op if already on new layout.
    """
```

Steps:

1. **Refuse if dirty**: check `git status --porcelain` in `root`;
   abort if there are uncommitted changes (override with `--force`).
2. **Create `site/`**.
3. **Move** (using `git mv` when in a git repo, otherwise `shutil.move`):
   - `hugo.toml` → `site/hugo.toml`
   - `themes/` → `site/themes/`
   - `content/` → `site/content/`
   - `layouts/` → `site/layouts/` (if exists)
   - `static/`, `data/`, `assets/` → `site/...` (if exists)
4. **Rewrite `site/hugo.toml`** mounts: `course.yml` source becomes
   `../course.yml`. Reuse `_replace_params_section` style logic to
   keep user `[params]` edits intact.
5. **Update root `.gitignore`**: rewrite the `# -- CURIK:START --`
   block so build artifacts are listed as `site/public/`,
   `site/resources/_gen/`, `site/.hugo_build.lock`. Reuse existing
   gitignore-block-rewrite logic if present in `curik/init/`; else
   read template from updated `curik/init/gitignore`.
6. **Verify** by running `hugo --source site` once if the user
   passed `--verify`.
7. **Print summary** of moved paths.

Add `--dry-run` flag that prints the plan without writing. Add
`--force` to bypass dirty-tree check.

### 7. Update the gitignore template

[curik/init/gitignore](curik/init/gitignore):

```
# -- CURIK:START --
# Managed by curik — do not edit this section manually.
# Run `curik init` to update.

# Hugo build output (now under site/)
site/public/
site/resources/_gen/

# OS files
.DS_Store
Thumbs.db

# Hugo lock file
site/.hugo_build.lock
# -- CURIK:END --
```

### 8. Update agent-facing docs and templates

These files tell humans and Claude agents where to find Hugo files.
Each needs a path update:

- [curik/init/claude-section.md:14-19](curik/init/claude-section.md#L14-L19):
  "Hugo Theme" section — theme path `site/themes/curriculum-hugo-theme/`,
  hugo.toml at `site/hugo.toml`.
- [curik/init/claude-section.md:78-84](curik/init/claude-section.md#L78-L84):
  Hugo Site commands group — no command syntax changes (CLI surface
  is unchanged), but the description text mentions paths.
- [curik/references/hugo-conventions.md](curik/references/hugo-conventions.md):
  every reference to `hugo.toml`, `themes/`, `content/` gets a
  `site/` prefix.
- [curik/skills/repo-scaffolding.md:14-27](curik/skills/repo-scaffolding.md#L14-L27):
  scaffolded layout example.
- [curik/agents/start-curik.md:104](curik/agents/start-curik.md#L104):
  paths table.
- [curik/init/deploy-pages.yml](curik/init/deploy-pages.yml):
  see step 3.

### 9. Update tests

Tests assert on specific paths. Each needs the `site/` prefix where
the fixture creates a Hugo file:

- [tests/test_hugo.py](tests/test_hugo.py) — content page fixtures
  create files under `site/content/`; `HugoSetupTest` expects
  `site/hugo.toml` and `site/themes/curriculum-hugo-theme/`.
- [tests/test_scaffolding.py](tests/test_scaffolding.py) — module
  and lesson stub assertions move to `site/content/...`.
- [tests/test_migration.py](tests/test_migration.py) — `migrate_structure`
  output paths become `site/...`. Add new `TestMigrateHugoLayout` cases:
  fresh project (no-op), legacy project (full migration), dirty tree
  (refusal), idempotency (run twice).
- [tests/test_cli.py](tests/test_cli.py) — Hugo CLI handler tests
  unchanged at the CLI level but the temp fixtures need `site/`
  layout.
- [tests/test_publish.py](tests/test_publish.py) — readiness check
  fixtures.
- New `tests/test_layout_check.py` for the warning logic: fires on
  legacy, silent on new layout, silent when env var set.

## Critical files

Path constants and helpers (new):
- `curik/paths.py` (new) or extension of `curik/templates.py`

Migration and detection (new):
- `curik/layout_check.py` (new)
- `curik/layout_migrate.py` (new)

Files modified:
- `curik/templates.py` — mounts, theme path, hugo.toml path
- `curik/hugo.py` — content/ paths, build cwd
- `curik/scaffolding.py` — content/ creation paths
- `curik/migrate.py` — migrate_structure paths, protected names, generator detection
- `curik/publish.py` — readiness checks, baseURL read, build call
- `curik/syllabus.py` — content scan path
- `curik/readme.py` — default docs_dir
- `curik/cli.py` — `--docs-dir` default, new `migrate hugo-layout` subcommand, warning hook
- `curik/init/gitignore` — site/ prefix on artifacts
- `curik/init/deploy-pages.yml` — `--source site`, `./site/public`
- `curik/init/claude-section.md` — agent-facing paths
- `curik/references/hugo-conventions.md` — author-facing paths
- `curik/skills/repo-scaffolding.md` — scaffold layout doc
- `curik/agents/start-curik.md` — paths table

Tests modified or added:
- `tests/test_hugo.py`, `tests/test_scaffolding.py`,
  `tests/test_migration.py`, `tests/test_cli.py`, `tests/test_publish.py`
- `tests/test_layout_check.py` (new)
- `tests/test_layout_migrate.py` (new)

## Verification

End-to-end checks after implementation:

1. **Fresh scaffold**: in a tmp dir, run `curik init` then
   `curik hugo setup`. Confirm `site/hugo.toml`,
   `site/themes/curriculum-hugo-theme/`, no Hugo files at root.
2. **Build**: `curik hugo build` runs Hugo from `site/` and produces
   `site/public/`. Open `site/public/index.html` to verify the theme
   and content render.
3. **Lesson authoring**: `curik hugo create-page mod1/intro.md "Intro"`
   creates `site/content/mod1/intro.md` and the public CLI returns
   `mod1/intro.md` (not `site/content/mod1/intro.md`).
4. **Legacy detection**: copy a curik repo from before this change
   into a tmp dir; run any curik command; confirm the warning fires
   on stderr; confirm `CURIK_NO_LAYOUT_WARNING=1 curik …` suppresses it.
5. **Migration**: in that same legacy tmp repo (committed clean),
   run `curik migrate hugo-layout --dry-run` and inspect the
   planned moves. Then run without `--dry-run`. Confirm
   `git log --follow site/content/...` shows history is preserved
   (because we used `git mv`). Run `curik hugo build` to confirm
   the migrated project still builds.
6. **Migration idempotency**: run `curik migrate hugo-layout` again
   on an already-migrated repo; confirm it reports nothing to do
   and exits 0.
7. **Tests**: `pytest -q` is green.

## Out of scope

- Changing the curik *package* repo's own `curriculum-hugo-theme/`
  directory (that's a `git subtree` source, separate concern).
- Versioning or breaking-change comms beyond the in-CLI warning.
- Hugo theme changes — the theme works the same regardless of
  whether the project root is `.` or `site/`.
