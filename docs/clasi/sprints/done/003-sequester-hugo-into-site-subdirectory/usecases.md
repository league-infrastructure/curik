---
sprint: "003"
status: draft
---

# Sprint 003 Use Cases

## SUC-001: Author Scaffolds a New Project

**Actor**: Curriculum author (human or agent)
**Trigger**: Author runs `curik init` then `curik hugo setup` in a fresh directory.

**Main Flow**:
1. `curik init` creates `.course/`, `course.yml`, `.claude/`, and `.gitignore`.
2. `curik hugo setup` reads `course.yml`, calls `hugo_setup(root, ...)`.
3. `hugo_setup` writes `site/hugo.toml` and installs the theme at
   `site/themes/curriculum-hugo-theme/`.
4. Author runs `curik scaffold structure <json>` to create modules and lessons.
5. Lesson stubs land under `site/content/<module>/`.
6. Author runs `curik hugo build`; Hugo runs from `site/` and writes `site/public/`.

**Postconditions**: Project root contains only curik files. All Hugo files live under
`site/`. No Hugo files appear at the project root.

**Acceptance Criteria**:
- [ ] `site/hugo.toml` exists after `curik hugo setup`
- [ ] `site/themes/curriculum-hugo-theme/` exists after `curik hugo setup`
- [ ] `site/content/_index.md` exists after `curik scaffold structure`
- [ ] `site/public/` is created by `curik hugo build`
- [ ] No `hugo.toml`, `themes/`, or `content/` at project root

---

## SUC-002: Author Migrates a Legacy Project

**Actor**: Curriculum author with an existing project using the old root-level layout.
**Trigger**: Author runs `curik migrate hugo-layout`.

**Pre-condition**: Project has `hugo.toml` at root and no `site/hugo.toml`.

**Main Flow**:
1. Author runs any `curik` command. A warning fires to stderr:
   ```
   WARNING: This project uses the legacy Hugo layout (hugo.toml at root).
   Run `curik migrate hugo-layout` to move Hugo files into site/.
   The legacy layout will stop working in a future release.
   ```
2. Author optionally runs `curik migrate hugo-layout --dry-run` to preview changes.
3. Author runs `curik migrate hugo-layout` on a clean git working tree.
4. Command moves `hugo.toml`, `themes/`, `content/`, `layouts/` (if any) into
   `site/` using `git mv` to preserve history.
5. Command rewrites `site/hugo.toml`: `course.yml` mount source changes to
   `../course.yml`.
6. Command rewrites `.gitignore` CURIK block: paths become `site/public/`,
   `site/resources/_gen/`, `site/.hugo_build.lock`.
7. Author optionally passes `--verify` to run a `hugo --source site` build check.

**Postconditions**: Project is on the new layout. Subsequent `curik` commands see
`site/hugo.toml` and emit no warning.

**Acceptance Criteria**:
- [ ] `curik migrate hugo-layout` on legacy project moves files to `site/`
- [ ] `git log --follow site/content/...` shows pre-migration history
- [ ] `site/hugo.toml` mount uses `../course.yml` after migration
- [ ] `.gitignore` CURIK block updated to `site/public/` etc.
- [ ] Running `curik migrate hugo-layout` twice exits 0 with nothing to do
- [ ] Command refuses on dirty git tree (exits non-zero unless `--force`)
- [ ] `--dry-run` prints plan without writing
- [ ] `CURIK_NO_LAYOUT_WARNING=1` suppresses the legacy warning on all commands

---

## SUC-003: Author Runs Hugo Build

**Actor**: Curriculum author (human or agent)
**Trigger**: Author runs `curik hugo build`.

**Main Flow**:
1. `hugo_build(root)` resolves `site_root(root)`.
2. Spawns `hugo` with `cwd=site_root(root)`.
3. Returns `{success, output, error}`.

**Postconditions**: Hugo builds from `site/`, writes output to `site/public/`. The
build finds `site/hugo.toml`, `site/themes/`, `site/content/`, and resolves
`../course.yml` for the data mount.

**Acceptance Criteria**:
- [ ] `curik hugo build` runs Hugo from `site/`, not project root
- [ ] `site/public/` is created on successful build
- [ ] Build succeeds on a freshly scaffolded project

---

## SUC-004: Author Creates a Lesson Page via CLI

**Actor**: Curriculum author (human or agent)
**Trigger**: Author runs `curik hugo create-page mod/intro.md "Intro"`.

**Main Flow**:
1. CLI handler resolves `content_dir(root)` = `root/site/content`.
2. Creates `root/site/content/mod/intro.md` with frontmatter.
3. Returns the path relative to `content_dir`: `mod/intro.md` (no `site/` prefix).

**Postconditions**: Lesson file lands in `site/content/`. The public CLI surface is
unchanged: authors never type `site/content/` in commands.

**Acceptance Criteria**:
- [ ] `curik hugo create-page mod/intro.md "Intro"` creates `site/content/mod/intro.md`
- [ ] Returned path is `mod/intro.md`, not `site/content/mod/intro.md`
- [ ] `curik hugo pages` lists pages from `site/content/`
- [ ] `curik hugo update-frontmatter` resolves paths under `site/content/`
