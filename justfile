# Curik — build and publish automation
#
# Targets:
#   just publish         — bump version, publish curik + theme
#   just publish-curik   — tag and push curik (pyproject.toml)
#   just publish-theme   — push curriculum-hugo-theme subtree to its repo
#   just version         — show current version
#   just bump            — bump version without publishing

set shell := ["bash", "-euo", "pipefail", "-c"]

theme_dir := "curriculum-hugo-theme"
theme_remote := "https://github.com/league-infrastructure/curriculum-hugo-theme.git"

# Show current version
version:
    @grep '^version = ' pyproject.toml | head -1 | sed 's/version = "\(.*\)"/\1/'

# Bump version in pyproject.toml and theme.toml (does not commit or tag)
bump:
    @./scripts/bump-version.sh

# Bump version dry run — show what the next version would be
bump-dry:
    @./scripts/bump-version.sh --dry

# Full publish: bump version, publish curik, publish theme
publish: _ensure-clean-master
    #!/usr/bin/env bash
    set -euo pipefail
    NEW_VERSION=$(./scripts/bump-version.sh)
    echo "Version: $NEW_VERSION"

    # Commit the version bump
    git add pyproject.toml {{ theme_dir }}/theme.toml
    git commit -m "chore: bump version to v${NEW_VERSION}"

    # Publish both
    just publish-curik "$NEW_VERSION"
    just publish-theme "$NEW_VERSION"

    echo ""
    echo "Published v${NEW_VERSION}"
    echo "  curik:  tagged and pushed"
    echo "  theme:  tagged and pushed"

# Tag and push curik
publish-curik version="":
    #!/usr/bin/env bash
    set -euo pipefail
    VERSION="{{ version }}"
    if [ -z "$VERSION" ]; then
        VERSION=$(grep '^version = ' pyproject.toml | head -1 | sed 's/version = "\(.*\)"/\1/')
    fi

    just _ensure-clean-master

    # Tag and push
    git tag -a "v${VERSION}" -m "Release v${VERSION}"
    git push origin master
    git push origin "v${VERSION}"

    # Reinstall via pipx
    pipx install --force .
    echo "curik v${VERSION} tagged, pushed, and installed"

# Push the theme subdirectory to its standalone repo and tag it
publish-theme version="":
    #!/usr/bin/env bash
    set -euo pipefail
    VERSION="{{ version }}"
    if [ -z "$VERSION" ]; then
        VERSION=$(grep '^version = ' pyproject.toml | head -1 | sed 's/version = "\(.*\)"/\1/')
    fi

    REMOTE_NAME="theme-origin"
    REMOTE_URL="{{ theme_remote }}"

    # Ensure the theme remote exists
    if ! git remote get-url "$REMOTE_NAME" &>/dev/null; then
        git remote add "$REMOTE_NAME" "$REMOTE_URL"
    fi

    # Push the subdirectory to the theme repo's main branch
    git subtree push --prefix={{ theme_dir }} "$REMOTE_NAME" main

    # Tag the theme repo: split to get the subtree commit, then tag it remotely
    # We create a local lightweight ref, push it as an annotated tag
    SUBTREE_COMMIT=$(git subtree split --prefix={{ theme_dir }})
    git tag -f "theme-v${VERSION}" "$SUBTREE_COMMIT"
    git push "$REMOTE_NAME" "theme-v${VERSION}:refs/tags/v${VERSION}" --force

    echo "theme v${VERSION} pushed and tagged"

# Guard: ensure master is clean and checked out
_ensure-clean-master:
    #!/usr/bin/env bash
    set -euo pipefail
    BRANCH=$(git branch --show-current)
    if [ "$BRANCH" != "master" ]; then
        echo "Error: not on master branch (on $BRANCH)"
        exit 1
    fi
    if [ -n "$(git status --porcelain)" ]; then
        echo "Error: working tree has uncommitted changes"
        exit 1
    fi
