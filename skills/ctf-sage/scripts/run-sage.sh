#!/usr/bin/env bash
# Local SageMath / CTF-Python runner.
#
# Runs a payload inside the local conda environment `sage10.9` (SageMath 10.9
# with pycryptodome available; pwntools is NOT installed there).
#
# Usage:
#   run-sage.sh <payload>
#   run-sage.sh -f script.sage            # run a .sage/.py file
#   run-sage.sh -                         # read payload from stdin
#
# The payload is executed with:  conda run -n sage10.9 <payload>
# For a one-shot sage command, prefer:   conda run -n sage10.9 sage -q -c "..."
set -euo pipefail

CONDA_ENV="${CTF_SAGE_ENV:-sage10.9}"

# Locate conda
CONDA_BIN="${CONDA_EXE:-}"
if [ -z "$CONDA_BIN" ]; then
  if command -v conda >/dev/null 2>&1; then
    CONDA_BIN="$(command -v conda)"
  elif [ -x "$HOME/miniforge3/bin/conda" ]; then
    CONDA_BIN="$HOME/miniforge3/bin/conda"
  elif [ -x "$HOME/miniconda3/bin/conda" ]; then
    CONDA_BIN="$HOME/miniconda3/bin/conda"
  else
    echo "conda not found on PATH or under \$HOME." >&2
    exit 127
  fi
fi

run_payload() {
  # $1 = payload string
  "$CONDA_BIN" run --no-capture-output -n "$CONDA_ENV" bash -lc "$1"
}

mode="inline"
payload=""
if [ "${1:-}" = "-f" ]; then
  mode="file"; shift; file="$1"; shift
  [ -n "$file" ] || { echo "usage: run-sage.sh -f <script.sage|script.py> [args...]" >&2; exit 64; }
  # .sage -> sage; .py -> python
  case "$file" in
    *.sage) set -- sage -q "$file" "$@";;
    *.py)   set -- python "$file" "$@";;
    *)      set -- python "$file" "$@";;
  esac
  exec "$CONDA_BIN" run --no-capture-output -n "$CONDA_ENV" bash -lc "$*"
elif [ "${1:-}" = "-" ]; then
  mode="stdin"; payload="$(cat)"
else
  payload="$*"
fi

if [ "$mode" = "stdin" ]; then
  "$CONDA_BIN" run --no-capture-output -n "$CONDA_ENV" bash -lc 'cat | bash'
  exit $?
fi

[ -n "$payload" ] || { echo "usage: run-sage.sh <payload> | -f <file> | -" >&2; exit 64; }
run_payload "$payload"
