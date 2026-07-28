#!/usr/bin/env bash
# Install or verify this checkout's Nature Skills. Modified; see ../NOTICE.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/skills"
DEST_DIR="${CODEX_SKILLS_DIR:-${HOME}/.codex/skills}"
PROFILE="core"
PULL=0
CHECK_ONLY=0

CORE_SKILLS=(
  nature-academic-search
  nature-citation
  nature-data
  nature-figure
  nature-paper-to-patent
  nature-paper2ppt
  nature-polishing
  nature-reader
  nature-response
  nature-reviewer
  nature-writing
)

usage() {
  cat <<'USAGE'
Usage: scripts/update-codex-skills.sh [options]

Options:
  --profile core|all  Install the 11 core skills (default) or all 18 skills.
  --dest PATH         Override the Codex skills directory.
  --pull              Run git pull --ff-only before installing.
  --check             Compare the selected profile without changing files.
  -h, --help          Show this help.

The installer changes only the selected nature-* directories. It does not
install runtime dependencies or remove unrelated skills.
USAGE
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --profile)
      shift
      [ "$#" -gt 0 ] || die "--profile requires core or all"
      PROFILE="$1"
      ;;
    --profile=*) PROFILE="${1#*=}" ;;
    --dest)
      shift
      [ "$#" -gt 0 ] || die "--dest requires a path"
      DEST_DIR="$1"
      ;;
    --dest=*) DEST_DIR="${1#*=}" ;;
    --pull) PULL=1 ;;
    --check|--verify-only) CHECK_ONLY=1 ;;
    -h|--help)
      usage
      exit 0
      ;;
    *) die "unknown argument: $1" ;;
  esac
  shift
done

[ "$PROFILE" = "core" ] || [ "$PROFILE" = "all" ] ||
  die "--profile must be core or all"
[ -d "$SOURCE_DIR" ] || die "missing source directory: $SOURCE_DIR"
[ -n "$DEST_DIR" ] || die "destination must not be empty"
[ "$DEST_DIR" != "/" ] || die "refusing to use the filesystem root as destination"
[ ! -L "$DEST_DIR" ] || die "destination must not be a symbolic link: $DEST_DIR"

if [ "$PULL" = "1" ]; then
  git -C "$REPO_ROOT" rev-parse --git-dir >/dev/null 2>&1 ||
    die "--pull requires a Git checkout"
  git -C "$REPO_ROOT" pull --ff-only
fi

if [ "$PROFILE" = "core" ]; then
  SKILLS=("${CORE_SKILLS[@]}")
else
  mapfile -t SKILLS < <(
    find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -type d -name 'nature-*' \
      -printf '%f\n' | sort
  )
fi

[ "${#SKILLS[@]}" -gt 0 ] || die "profile selected no skills"
for name in "${SKILLS[@]}"; do
  [ -f "$SOURCE_DIR/$name/SKILL.md" ] ||
    die "invalid skill directory: $SOURCE_DIR/$name"
done

verify() {
  local status=0
  local name
  for name in "${SKILLS[@]}"; do
    if [ -L "$DEST_DIR/$name" ]; then
      printf 'UNSAFE   %s (symbolic link)\n' "$name"
      status=1
    elif [ ! -d "$DEST_DIR/$name" ]; then
      printf 'MISSING  %s\n' "$name"
      status=1
    elif diff -qr "$SOURCE_DIR/$name" "$DEST_DIR/$name" >/dev/null; then
      printf 'MATCH    %s\n' "$name"
    else
      printf 'DIFF     %s\n' "$name"
      status=1
    fi
  done
  return "$status"
}

if [ "$CHECK_ONLY" = "1" ]; then
  printf 'Verifying profile=%s in %s\n' "$PROFILE" "$DEST_DIR"
  verify
  exit
fi

command -v rsync >/dev/null 2>&1 || die "rsync is required"
mkdir -p "$DEST_DIR"
for name in "${SKILLS[@]}"; do
  [ ! -L "$DEST_DIR/$name" ] ||
    die "refusing to replace symbolic-link target: $DEST_DIR/$name"
done
for name in "${SKILLS[@]}"; do
  # Recheck immediately before mutation to narrow the local race window.
  [ ! -L "$DEST_DIR/$name" ] ||
    die "refusing to replace symbolic-link target: $DEST_DIR/$name"
  mkdir -p "$DEST_DIR/$name"
  rsync -a --delete "$SOURCE_DIR/$name/" "$DEST_DIR/$name/"
  printf 'SYNCED   %s\n' "$name"
done

verify
printf 'Installed %s Nature Skills (profile=%s). Restart the Agent to reload metadata.\n' \
  "${#SKILLS[@]}" "$PROFILE"
