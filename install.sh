#!/usr/bin/env bash
# Codex Red installer; Python's standard library handles paths and file copying.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/tools/install_skills.py" "$@"
