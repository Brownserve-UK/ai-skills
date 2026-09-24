#!/usr/bin/env bash
set -euo pipefail

if [[ ! -e /etc/bsdev-container ]]; then
    echo "mock-up requires the bsdev container; run Claude Code inside bsdev." >&2
    exit 1
fi

if ! command -v bsdev-proto >/dev/null 2>&1; then
    echo "bsdev-proto not found; rebuild/pull the bsdev image (needs commit 3cae5fd or later)." >&2
    exit 1
fi

repo="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
prototypes="$repo/.agents/prototypes"

existing=()
if [[ -d "$prototypes" ]]; then
    shopt -s nullglob
    for dir in "$prototypes"/*/; do
        if [[ -f "${dir}index.html" ]]; then
            existing+=("$(basename "$dir")")
        fi
    done
    shopt -u nullglob
fi

echo "repo: $repo"
echo "prototypes dir: $prototypes"
if (( ${#existing[@]} )); then
    echo "existing prototypes: ${existing[*]}"
else
    echo "existing prototypes: none"
fi
echo "bsdev-proto status:"
bsdev-proto status | sed 's/^/  /'

if ! command -v playwright >/dev/null 2>&1; then
    echo "warning: playwright is not on PATH, so bsdev-proto shot can't run; tell the user screenshots were skipped."
fi
