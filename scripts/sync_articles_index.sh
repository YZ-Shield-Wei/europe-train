#!/usr/bin/env bash
# Compatibility entry point: preserve existing localized indices without copying.
# articles/index.html is an English redirect, NOT a translation template.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/publication_guard.py" --indices
