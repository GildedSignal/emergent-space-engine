#!/bin/sh
# Regen: every dossier number from shipped code + work/patch.diff. ~4 min.
set -e
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261019-0435-fermi-0659
mkdir -p "$R/logs"
# 1. apply the probe patch if the tree is clean of it
if ! grep -q CENSUS_N crates/universe/src/step.rs; then
  git apply "$R/work/patch.diff"
fi
# 2. build the patched example (the shipped one does not link on Linux: proc_pid_rusage is macOS-only)
cargo build --release -p emergent-universe --example nladder
BIN="${CARGO_TARGET_DIR:-target}/release/examples/nladder"
# 3. the five arms of the dossier (each <= 60 s)
ES_KICKCENSUS=1 LADDER_CAP_S=54 "$BIN" 30000 coast 52 280  > "$R/logs/a1_k3e4_wave1.txt"  2>&1
ES_KICKCENSUS=1 LADDER_CAP_S=54 "$BIN" 30000 coast 46 1050 > "$R/logs/a3_k3e4_waves12.txt" 2>&1
ES_KICKCENSUS=1 LADDER_CAP_S=54 "$BIN" 10000 coast 52 280  > "$R/logs/a2_k1e4_wave1.txt"  2>&1
LADDER_CAP_S=54 "$BIN" 30000 coast 20 100                   > "$R/logs/a5_off.txt"         2>&1
ES_KICKCENSUS=1 LADDER_CAP_S=54 "$BIN" 30000 coast 20 100   > "$R/logs/a6_on.txt"          2>&1
# 4. summary
grep -H -E "kickcensus|^game " "$R/logs"/a1_k3e4_wave1.txt "$R/logs"/a3_k3e4_waves12.txt "$R/logs"/a2_k1e4_wave1.txt
echo "--- control (OFF vs ON must match on kicks/events/opens/boundaries/game):"
grep -o "kicks [0-9]*\|events [0-9]*\|opens [0-9]*\|boundaries [0-9]*\|game [0-9.]*" "$R/logs"/a5_off.txt "$R/logs"/a6_on.txt
