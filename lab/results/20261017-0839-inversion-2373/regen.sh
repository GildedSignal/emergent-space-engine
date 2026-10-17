#!/usr/bin/env bash
# Regenerates every dossier number: apply patch, build, run fleetk (seed 20261017), compose.
# Runs in ~1 min on the lab box. `bash regen.sh <seed>` re-runs at another seed.
set -euo pipefail
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$RUN_DIR/../../.." && pwd)"
SEED="${1:-20261017}"

cd "$ROOT"
# Idempotent patch application (patch.diff adds a NEW example file):
# absent -> apply; present & matches -> reverse+reapply; stale -> remove+apply.
TARGET="crates/encounters/examples/fleetk.rs"
PATCH="$RUN_DIR/work/patch.diff"
if [ -e "$TARGET" ]; then
  if git apply --reverse --check "$PATCH" 2>/dev/null; then
    git apply --reverse "$PATCH"
  else
    rm -f "$TARGET"
  fi
fi
git apply "$PATCH"

cargo build --release -p emergent-encounters --example fleetk
BIN="${CARGO_TARGET_DIR:-$ROOT/target}/release/examples/fleetk"
"$BIN" "$SEED" > "$RUN_DIR/work/fleetk.jsonl"

cd "$RUN_DIR"
python3 compose.py work/fleetk.jsonl | tee work/composed.txt
echo "--- fleetk.jsonl ---"
cat work/fleetk.jsonl
