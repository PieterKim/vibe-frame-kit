#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for PYTHON_BIN in python3 python; do
  if command -v "$PYTHON_BIN" >/dev/null 2>&1 && "$PYTHON_BIN" -c 'import sys; sys.exit(sys.version_info < (3, 11))' >/dev/null 2>&1; then
    exec "$PYTHON_BIN" "$SCRIPT_DIR/install.py" "$@"
  fi
done
printf '%s\n' 'Python 3.11+ is required.' >&2
exit 1
