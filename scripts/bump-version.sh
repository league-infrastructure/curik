#!/usr/bin/env bash
# bump-version.sh — Update version in pyproject.toml and theme.toml
#
# Version format: 0.YYYYMMDD.revision
#   - Major is always 0 (pre-release)
#   - Date is today's date
#   - Revision increments if there's already a release today, otherwise resets to 1
#
# Usage:
#   ./scripts/bump-version.sh          # auto-increment
#   ./scripts/bump-version.sh --dry    # print new version without writing

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYPROJECT="$REPO_ROOT/pyproject.toml"
THEME_TOML="$REPO_ROOT/curriculum-hugo-theme/theme.toml"

TODAY="$(date +%Y%m%d)"

# Read current version from pyproject.toml
CURRENT=$(grep '^version = ' "$PYPROJECT" | head -1 | sed 's/version = "\(.*\)"/\1/')
CURRENT_DATE=$(echo "$CURRENT" | cut -d. -f2)
CURRENT_REV=$(echo "$CURRENT" | cut -d. -f3)

# Compute new version
if [ "$CURRENT_DATE" = "$TODAY" ]; then
    NEW_REV=$((CURRENT_REV + 1))
else
    NEW_REV=1
fi
NEW_VERSION="0.${TODAY}.${NEW_REV}"

if [ "${1:-}" = "--dry" ]; then
    echo "$NEW_VERSION"
    exit 0
fi

# Update pyproject.toml
sed -i '' "s/^version = \".*\"/version = \"$NEW_VERSION\"/" "$PYPROJECT"

# Update theme.toml
sed -i '' "s/^version = \".*\"/version = \"$NEW_VERSION\"/" "$THEME_TOML"

echo "$NEW_VERSION"
