#!/bin/bash
# Regenerates every number in dossier.md from the shipped code + work/patch.diff
# (the prior gold run's `tax` instrument verbatim, plus the ES_CAP arm this run adds).
# Budget: ~12 min worst case (a DNF row is itself a datum and burns its full timeout).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
BIN="${CARGO_TARGET_DIR:-$HOME/lab-target-3}/release/examples/tax"
cd "$REPO"
cargo build -p emergent-allocator --release --offline --example tax || exit 1
echo "== build ok $(date +%T) load $(cut -d' ' -f1 /proc/loadavg) =="

run() { # timeout arm-env... -- bin args...
  local tmo=$1; shift
  local envs=$1; shift
  if [ -z "$envs" ]; then
    timeout "$tmo" "$BIN" "$@" 2>/dev/null | grep '^RESULT' || echo "RESULT DNFTMO(${tmo}s) $*"
  else
    timeout "$tmo" env "$envs" "$BIN" "$@" 2>/dev/null | grep '^RESULT' || echo "RESULT DNFTMO(${tmo}s) env=$envs $*"
  fi
}

echo "== S0: 44-body original geometry, shipped vs cap16 (P1 digest control, cheap) =="
run 60 ""         batch 4 8 2000 17 2000 1
run 60 ES_CAP=16 batch 4 8 2000 17 2000 1

echo "== S1: no-conflict control, stagger 300, 1408 bodies (the cap must be inert) =="
run 120 ES_CAP=16 batch 128 8 300 2 3000 1

echo "== S2: conflict wave, 1408 bodies, horizon 6k, 3 arms =="
run 120 ""         batch 128 8 30 2 3000 1
run 120 ES_CAP=16 batch 128 8 30 2 3000 1
run 120 ES_CAP=64 batch 128 8 30 2 3000 1

echo "== S3: conflict wave, 14080 bodies, horizon 6k, 3 arms (the decisive size) =="
run 200 ""         batch 1280 8 30 2 3000 1
run 200 ES_CAP=16 batch 1280 8 30 2 3000 1
run 200 ES_CAP=64 batch 1280 8 30 2 3000 1

# Stretch (optional; no dossier number depends on it), 28,160 bodies, horizon 1500:
#   run 200 ""         batch 2560 8 30 1 1500 1
#   run 200 ES_CAP=64 batch 2560 8 30 1 1500 1

echo "== done $(date +%T) =="
