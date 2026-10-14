#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by the runner).
# The bounded arm exits by itself on the horizon stall (~15 s); pristine arms are cut by timeout:
# on this box pristine cannot reach the cut inside the budget (that fact is one of the findings).
# Budget: about 10 minutes.
set -e
cd "$(dirname "$0")/../../.." || exit 1  # repo root
cargo build --release -p emergent-universe --example wave_probe
B="${CARGO_TARGET_DIR:-target}/release/examples/wave_probe"
R=lab/results/20261014-1719-system-3fc0
: > "$R/wave_runs.txt"; : > "$R/p1.log"
# The measured pair (dossier's headline): 2e4 members, cut 5000 game-s, rtf 200, 12 ms wall budget.
echo "== m20000 ES_PULL_MAX=256 (held scan)" >> "$R/wave_runs.txt"
ES_PULL_MAX=256 timeout 200 "$B" 20000 5000 200 >> "$R/wave_runs.txt" 2>>"$R/p1.log" || true
echo "== m20000 pristine" >> "$R/wave_runs.txt"
timeout 200 "$B" 20000 5000 200 >> "$R/wave_runs.txt" 2>>"$R/p1.log" || true
# The 1e5 stall + pre-wave monster (worst_ms in the progress lines; no cut is reached).
echo "== m100000 ES_PULL_MAX=256" >> "$R/wave_runs.txt"
ES_PULL_MAX=256 timeout 150 "$B" 100000 5000 200 >> "$R/wave_runs.txt" 2>>"$R/p1.log" || true
echo "== m100000 pristine" >> "$R/wave_runs.txt"
timeout 150 "$B" 100000 5000 200 >> "$R/wave_runs.txt" 2>>"$R/p1.log" || true
echo DONE >> "$R/wave_runs.txt"
echo "--- runs:"; cat "$R/wave_runs.txt"
echo "--- progress tails:"; tail -6 "$R/p1.log"
