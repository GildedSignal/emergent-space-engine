#!/usr/bin/env bash
# Regenerates every number in the dossier from the shipped tree plus work/patch.diff (applied first by the runner).
# The patch is default-neutral: every change is env-gated (ES_STAGGER, ES_SEED default 1, ES_LADDER_MAX_S default 55).
# Total wall: ~7 min (the two 210 s flights dominate; the census and jacobi arms are seconds).
set -eu
cd "$(git rev-parse --show-toplevel)"
OUT=lab/results/20261014-1859-spacex-cb7b/raw
mkdir -p "$OUT"
B=$(cargo build --release -q -p emergent-universe --examples && echo "${CARGO_TARGET_DIR:-target}/release/examples")
state() { echo "--- $(date -u +%H:%M:%S) load $(cut -d' ' -f1-3 /proc/loadavg) free_mb $(free -m | awk '/^Mem:/{print $7}')"; }

# 1. The census (Table 1): the wave's arrival width, control vs stagger, at 1e5 and the cheap 3e3 arm.
{
state
for N in 100000 3000; do
  echo "=== census control N=$N ==="; "$B/belt_first" "$N"
  echo "=== census stagger N=$N ==="; ES_STAGGER=1 "$B/belt_first" "$N"
done
# 2. The one-shot physics cost (jacobi, the shipped instrument): step 7 and 5, both arms.
#    (The step-7 control can panic on a capture in this scene on long horizons; the step-5 pair is the robust one.)
for s in 7 5; do
  echo "=== jacobi $s control ==="; "$B/jacobi" "$s" 100 6 | tail -2 || true
  echo "=== jacobi $s stagger ==="; ES_STAGGER=1 "$B/jacobi" "$s" 100 6 | tail -2
done
# 3. The flights (Table 2): 1e5 burn, rtf 100, past the wave (>= 16 k game-s).
echo "=== FLIGHT control ==="; ES_LADDER_MAX_S=208 "$B/nladder" 100000 burn 210 100
echo "=== FLIGHT stagger ==="; ES_STAGGER=1 ES_LADDER_MAX_S=208 "$B/nladder" 100000 burn 210 100
state
} | tee "$OUT/regen.log"
