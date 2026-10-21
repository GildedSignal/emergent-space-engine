#!/usr/bin/env bash
# Regenerates every number in dossier.md for run 20261021-0213-q-compile-belt-49ad.
# The runner applies work/patch.diff (which carries this folder) before running this.
# Runtime: < 1 s. No writes outside this run folder.
set -euo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$RUN/../../.." && pwd)"
cd "$ROOT"

# The page as it stood before this compile: git HEAD if readable, else the tree copy.
if git show HEAD:lab/wiki/belt.md > "$RUN/old_belt_snapshot.md" 2>/dev/null; then
  OLD="$RUN/old_belt_snapshot.md"
else
  OLD="lab/wiki/belt.md"
fi

python3 "$RUN/check_compile.py" "$OLD"
