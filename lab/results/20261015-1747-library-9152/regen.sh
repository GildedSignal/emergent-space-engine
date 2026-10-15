#!/bin/sh
# Regen: every dossier number, from shipped code + work/patch.diff, in < 15 min.
# The only tree edit the patch carries: nladder.rs footprint() ported to Linux
# (/proc/self/status VmRSS/VmHWM; macOS branch unchanged).
set -e
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
RUN="$ROOT/lab/results/20261015-1747-library-9152"
cd "$ROOT"
# Apply the run's tree edits if the tree is clean (regen runs on a restored tree).
if [ -f "$RUN/work/patch.diff" ] && git apply --check "$RUN/work/patch.diff" 2>/dev/null; then
  git apply "$RUN/work/patch.diff"
fi
echo "== machine state (runs must compare honestly) =="; uptime; free -m | sed -n 1,2p; nproc
cargo build --release -p emergent-universe --example nladder
BIN="$(cargo metadata --no-deps --format-version 1 | python3 -c 'import json,sys; print(json.load(sys.stdin)["target_directory"])')/release/examples/nladder"
: > "$RUN/work/flights.txt"
for n in 0 1000 10000 100000; do
  "$BIN" "$n" coast 10 100 12 2>&1 | grep -E "^rung|ladder:" >> "$RUN/work/flights.txt"
done
python3 "$RUN/work/marginal.py" "$RUN/work/flights.txt"
