#!/bin/sh
# Regenerates every number in dossier.md. Run from anywhere; expects the run's work/patch.diff
# already applied (the runner does that) and a writable checkout. Wall ≈ 6-8 min.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../../.." && pwd)
BIN="${XTASK:-${CARGO_TARGET_DIR:-$ROOT/target}/release/xtask}"
cd "$ROOT"
# the probe lives in work/patch.diff; the runner applies it, self-heal if the tree lacks it
if ! grep -q "RUIN_PROBE" xtask/src/universe/session.rs 2>/dev/null; then
  git apply "$HERE/work/patch.diff"
fi
cargo build --release -p xtask
cd "$HERE"
run() { # run <cpus> <name> <extra args...>  [RUIN_* env via prefix]
  cpus=$1; name=$2; shift 2
  echo "== $name"
  RUIN_PROBE=1 RUIN_EVERY=30 taskset -c "$cpus" "$BIN" universe --bench --unpaced --no-record "$@" \
    > "arms/$name.json" 2> "arms/$name.probe"
}
# quiet baselines: cpus 6,7 (spinners stopped; isolates from the window's other runs,
# whose ambient load would collapse quiet service and void the pin(m) subtraction)
./spin.sh stop >/dev/null 2>&1 || true; sleep 1
run 6,7 a1-m400-quiet  --seed 1 --members 400 --rtf 100 --seconds 30
run 6,7 a100-quiet     --seed 1 --members 100 --rtf 100 --seconds 12
run 6,7 a200-quiet     --seed 1 --members 200 --rtf 100 --seconds 12
run 6,7 r1-m400-quiet-rtf600 --seed 1 --members 400 --rtf 600 --seconds 10
# loaded arms (6 spinners on cpus 0..5; bench pinned to 0,1 as designed)
./spin.sh start 6; sleep 1
run 0,1 a2-m400-load6  --seed 1 --members 400 --rtf 100 --seconds 30
run 0,1 a2s2-m400-load6 --seed 2 --members 400 --rtf 100 --seconds 30
run 0,1 a100-load6     --seed 1 --members 100 --rtf 100 --seconds 30
run 0,1 a200-load6     --seed 1 --members 200 --rtf 100 --seconds 30
run 0,1 e12-m400-load6 --seed 1 --members 400 --rtf 100 --seconds 20 --engine-ms 12
run 0,1 e16-m400-load6 --seed 1 --members 400 --rtf 100 --seconds 20 --engine-ms 16
# instrument arms: RUIN_BACKLOG overrides the held-scans cap (a disclosed probe constant)
export RUIN_BACKLOG=48
run 0,1 l2-m400-load6-backlog48   --seed 1 --members 400 --rtf 120 --seconds 55 --engine-ms 8
unset RUIN_BACKLOG
./spin.sh stop; sleep 1
export RUIN_BACKLOG=256
run 0,1 l1-m400-load6-backlog256  --seed 1 --members 400 --rtf 120 --seconds 55 --engine-ms 25
unset RUIN_BACKLOG
cp arms/a2-m400-load6.probe arms/a400-load6.probe
cp arms/a1-m400-quiet.probe  arms/a400-quiet.probe
python3 analyze.py
echo "done: summary.json"
