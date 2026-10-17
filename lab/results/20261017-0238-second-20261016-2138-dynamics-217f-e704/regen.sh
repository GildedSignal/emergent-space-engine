#!/bin/bash
# Regenerates every number in dossier.md from the shipped code + work/patch.diff.
# Patch assumed applied (the runner applies work/patch.diff first). Budget: <= 14 min.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
BIN="${CARGO_TARGET_DIR:-$HOME/lab-target-0}/release/examples/tax"
cd "$REPO"
cargo build -p emergent-allocator --release --offline --example tax || exit 1
echo "== build ok $(date +%T) load $(cut -d' ' -f1 /proc/loadavg) =="

run() { # arm-env... -- bin args...   (60-s-budget rows print wall; DNF rows print DNF)
  local tmo=$1; shift
  local envs=$1; shift
  if [ -z "$envs" ]; then
    timeout "$tmo" "$BIN" "$@" 2>/dev/null | grep '^RESULT' || echo "RESULT DNFTMO(${tmo}s) $*"
  else
    timeout "$tmo" env "$envs" "$BIN" "$@" 2>/dev/null | grep '^RESULT' || echo "RESULT DNFTMO(${tmo}s) env=$envs $*"
  fi
}

echo "== S1: 4-cell original geometry, 3 reps (nondeterminism of the latch) =="
for r in 1 2 3; do run 60 "" batch 4 8 2000 17 2000 1; done

echo "== S2: 128 cells / 1408 bodies, horizon 20k, 2 reps x 3 arms (interleaved) =="
for r in 1 2; do
  run 120 ""        batch 128 8 30 5 4000 1
  run 120 ES_DECAY=1 batch 128 8 30 5 4000 1
  run 120 ES_LOCAL=1 batch 128 8 30 5 4000 1
done

echo "== S2b: 128 cells, horizon 6k, decay wedge census (3 tries, 60 s each) =="
for r in 1 2 3; do run 60 ES_DECAY=1 batch 128 8 30 2 3000 1; done

echo "== S3: 1280 cells / 14080 bodies, horizon 6k, 1 rep x 3 arms =="
run 300 ""         batch 1280 8 30 2 3000 1
run 240 ES_DECAY=1 batch 1280 8 30 2 3000 1
run 240 ES_LOCAL=1 batch 1280 8 30 2 3000 1

echo "== S4: frames harness, 128 cells, 2 s, rate 600, 1 rep x 3 arms =="
run 60 ""         frames 128 8 30 2 2.0 1 600 60
run 60 ES_DECAY=1 frames 128 8 30 2 2.0 1 600 60
run 60 ES_LOCAL=1 frames 128 8 30 2 2.0 1 600 60

echo "== S5: relativistic no-conflict control, 1280 cells, horizon 6k =="

TAX_LAW=relativistic run 150 "" batch 1280 8 30 2 3000 1

echo "== done $(date +%T) =="
