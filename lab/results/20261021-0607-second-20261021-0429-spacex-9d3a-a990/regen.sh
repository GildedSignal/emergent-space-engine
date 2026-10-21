#!/bin/sh
# Regenerates every number in dossier.md (run 20261021-0607-second-20261021-0429-spacex-9d3a-a990)
# from shipped code + work/patch.diff (the 9d3a census + the flyable-frame gold's row-set patch +
# this run's `rows` mode and idle probe). ~8 min on the 8-vCPU box; every arm under 1.2 GB.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../../.." && pwd)
cd "$ROOT"
git apply "$HERE/work/patch.diff" 2>/dev/null || true   # already applied is fine
cargo build --release -p emergent-universe --example rcensus
BIN=$(cargo metadata --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/rcensus
# controls (must reproduce 9d3a and its checker digit for digit), then the decisive arms
ES_RCENSUS=1 "$BIN" 100000  20 none  | tee "$HERE/work/arm_100000_20_none.txt"
ES_RCENSUS=1 "$BIN" 100000  20 sparse | tee "$HERE/work/arm_100000_20_sparse.txt"
ES_RCENSUS=1 "$BIN" 100000  20 rows 280 | tee "$HERE/work/arm_100000_20_rows.txt"
ES_RCENSUS=1 "$BIN" 300000  20 rows 280 | tee "$HERE/work/arm_300000_20_rows.txt"
# the steady-state horizon (the wheel's cap is 16384 frames = 273 s; 300 s and 600 s bracket it)
ES_RCENSUS=1 "$BIN" 100000 300 rows 580 | tee "$HERE/work/arm_100000_300_rows.txt"
ES_RCENSUS=1 "$BIN" 100000 600 rows 580 | tee "$HERE/work/arm_100000_600_rows.txt"
# the wheel's own idle law (the probe that separates ramp from steady cadence)
ES_RCENSUS=1 "$BIN" 100000 400 rows 580 | tee "$HERE/work/arm_100000_400_rows_probe.txt"
python3 "$HERE/work/parse.py"
