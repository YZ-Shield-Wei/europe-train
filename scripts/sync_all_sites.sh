#!/usr/bin/env bash
# Legacy alias. Never overwrite localized pages with the English redirect.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/sync_articles_index.sh" "$@"
