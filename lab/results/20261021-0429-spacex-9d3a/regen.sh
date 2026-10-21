#!/bin/sh
# Regenerates every number in dossier.md (run 20261021-0429-spacex-9d3a) from shipped code + work/patch.diff.
# About 1 min of build and 2.5 min of runs on the 8-vCPU lab box; peak under 2.6 GB (the 1e6 arm).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../../.." && pwd)
cd "$ROOT"
git apply "$HERE/work/patch.diff" 2>/dev/null || true   # already applied is fine
cargo build --release -p emergent-universe --example rcensus
BIN=$(cargo metadata --format-version 1 | python3 -c "import json,sys; print(json.load(sys.stdin)['target_directory'])")/release/examples/rcensus
# arms: dense control (N=0, per-frame view gathers), 1e5 and 1e6 (a view gather once per 10 s)
ES_RCENSUS=1 "$BIN" 0       20 frame  | tee "$HERE/work/arm_0_20_frame.txt"
ES_RCENSUS=1 "$BIN" 100000  20 sparse | tee "$HERE/work/arm_100000_20_sparse.txt"
ES_RCENSUS=1 "$BIN" 300000  20 sparse | tee "$HERE/work/arm_300000_20_sparse.txt"
# the 1e6 arm needs ~2.6 GB peak (the population itself) and the lab box watchdogs at ~2 GB on a busy
# window: it is best-effort here. Its completed run is kept in work/arm_1000000_20_sparse.txt; the claim's
# numbers do not depend on it (1e5 and 3e5 carry them; 1e6 corroborates the live curve at scale).
ES_RCENSUS=1 "$BIN" 1000000 20 sparse > "$HERE/work/arm_1e6_rerun.txt" || echo "1e6 arm killed by the box watchdog (see dossier note); the completed run's log is work/arm_1000000_20_sparse.txt"
python3 "$HERE/work/parse.py" "$HERE/work"
