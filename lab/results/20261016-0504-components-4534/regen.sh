#!/usr/bin/env bash
# Regenerates every number in dossier.md from the patched tree (work/patch.diff applied by the
# runner before this runs). Budget-free flights (budget_ms 1e6), rtf 1000, coast, 660 frames
# after the first second = 11,000 game-s. Deterministic columns: events/frame p50/p99/max,
# kicks, events, storm frames. ms are this box's (orders of magnitude only).
set -euo pipefail
cd "$(dirname "$0")/../../../.."
T=/home/glmlab/lab-target-3/release/examples/nladder
if [ ! -x "$T" ] || [ crates/universe/src/step.rs -nt "$T" ]; then
  cargo build --release -p emergent-universe --example nladder
fi

run() { # label, N, seed, env...
  local label="$1" n="$2" seed="$3"; shift 3
  echo "== $label (N=$n seed=$seed) =="
  env "$@" "$T" "$n" coast 12 1000 1000000 "$seed" 2>&1 \
    | grep -E "events/frame|worst frames|game .* s after the first second"
}

run "OFF   N=600"        600     1 ES_STAGGER_LOC=0
run "OFF   N=1e4"        10000   1 ES_STAGGER_LOC=0
run "OFF   N=1e5"        100000  1 ES_STAGGER_LOC=0
run "OFF   N=0 (floor)"  0       1 ES_STAGGER_LOC=0
run "BEGIN N=600"        600     1 ES_STAGGER_LOC=1
run "GRID  N=600"        600     1 ES_STAGGER_LOC=2
run "GRID  N=1e4"        10000   1 ES_STAGGER_LOC=2
run "GRID  N=1e5"        100000  1 ES_STAGGER_LOC=2
run "OFF   N=600 seed7 (held out)"  600 7 ES_STAGGER_LOC=0
run "GRID  N=600 seed7 (held out)"  600 7 ES_STAGGER_LOC=2

echo
echo "Dossier table checks:"
echo "  OFF  600/1e4/1e5: max 335 p99 229 p50 28, kicks 17209 (identical columns at all three N)"
echo "  BEGIN 600:        max 335 (frames 317/634 unchanged) — the begin-stagger does not transplant"
echo "  GRID  600/1e4/1e5: max 141 p99 129-131, kicks 17257-17260 (+0.3%), worst frames 74-92 not 317/634"
echo "  seed 7: OFF max 359 -> GRID 177; events 45277 -> 78254 (the named caveat)"
echo "  OFF gate-neutral: unset or 0 reproduces the pre-patch binary's deterministic columns"
