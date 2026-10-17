#!/usr/bin/env bash
# Regenerates every dossier number: apply patch (fleetk + fleetcal, both print-only),
# build, run both instruments (decisive seed 20261017 + held-out 777), compose.
# ~10 min on the lab box.
set -euo pipefail
RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$RUN_DIR/../../.." && pwd)"
SEED="${1:-20261017}"

cd "$ROOT"
# Idempotent patch application (calpatch.diff adds two NEW example files).
PATCH="$RUN_DIR/work/calpatch.diff"
for TARGET in crates/encounters/examples/fleetk.rs crates/encounters/examples/fleetcal.rs; do
  if [ -e "$TARGET" ]; then
    if git apply --reverse --check "$PATCH" 2>/dev/null; then
      git apply --reverse "$PATCH"
    else
      rm -f "$TARGET"
    fi
  fi
done
git apply "$PATCH"

cargo build --release -p emergent-encounters --example fleetk --example fleetcal
BIN="${CARGO_TARGET_DIR:-$ROOT/target}/release/examples"
"$BIN/fleetk" "$SEED" > "$RUN_DIR/work/fleetk.jsonl"
"$BIN/fleetcal" "$SEED" > "$RUN_DIR/work/fleetcal-20261017.jsonl"
"$BIN/fleetcal" 777 > "$RUN_DIR/work/fleetcal-777.jsonl"

cd "$RUN_DIR"
python3 compose.py "work/fleetcal-20261017.jsonl" work/fleetk.jsonl | tee work/composed.txt
echo "--- fleetcal-20261017.jsonl ---"; cat "work/fleetcal-20261017.jsonl"
echo "--- fleetk.jsonl ---"; cat work/fleetk.jsonl
