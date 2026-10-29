#!/usr/bin/env bash
# Safe entry point: no generation, phrase substitution, or automatic publication.
# With no arguments, audit all existing articles; known placeholders fail closed.
# Publish only explicitly selected, reviewed files with --publish --expect-head SHA.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/push_all_articles_api.py" "$@"
