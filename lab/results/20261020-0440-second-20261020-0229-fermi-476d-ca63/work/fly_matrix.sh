#!/usr/bin/env bash
# The decisive matrix: 15 flights, sequential (timing measurements). Flies only missing arms
# (idempotent — regen.sh reruns it). ~13 min on this box.
# NB: forces CARGO_TARGET_DIR=lab-target-2 — the session env may point elsewhere (lab-target-0)
# at a stale, unpatched binary; the patch's CSV instrument must be the binary that flies.
ROOT="${ES_LAB_ROOT:-/home/glmlab/actions-runner/_work/emergent-space-engine/lab-0}"
cd "$ROOT" || exit 1
R=lab/results/20261020-0440-second-20261020-0229-fermi-476d-ca63
D=$R/work/flights
export CARGO_TARGET_DIR=/home/glmlab/lab-target-2
BIN=$CARGO_TARGET_DIR/release/examples/nladder
mkdir -p "$D"

fly() { # name K seconds fence
  local name=$1 k=$2 secs=$3 fence=$4
  if [ -s "$D/$name.out" ] && [ -s "$D/$name.csv.err" ]; then echo "skip $name (done)"; return 0; fi
  rm -f "$D/$name.out" "$D/$name.csv.err"
  echo "== $name (k=$k s=$secs fence=$fence $(date +%H:%M:%S))"
  if [ "$fence" = yes ]; then export ES_SCAN_TTL_S=16; else unset ES_SCAN_TTL_S || true; fi
  "$BIN" "$k" burn "$secs" 2000 12 2>"$D/$name.csv.err" >"$D/$name.out" \
    || echo "  $name exited nonzero (RSS kill?) — kept for the record"
  unset ES_SCAN_TTL_S || true
}

# idle regime (shipped schedule; fence off)
for i in 1 2 3; do fly "idle${i}_k100000_s17" 100000 17 no; done
for i in 1 2 3; do fly "idle${i}_k200000_s10" 200000 10 no; done
fly idle1_k300000_s10 300000 10 no

# load regime: 16 spinners on 8 vCPU; extended guard (instrument dial) so the flight reaches
# the same game-time under contention
bash "$ROOT/$R/work/loadgen.sh" start 16
sleep 3
for i in 1 2 3; do ES_FLIGHT_MAX_S=130 fly "load${i}_k100000_s25" 100000 25 no; done
for i in 1 2 3; do ES_FLIGHT_MAX_S=130 fly "load${i}_k200000_s45" 200000 45 no; done
bash "$ROOT/$R/work/loadgen.sh" stop

# fence arms (idle, TTL=16): the tail-channel attribution by deletion
fly fence1_k100000_s17 100000 17 yes
fly fence1_k200000_s17 200000 17 yes
echo "matrix done $(date +%H:%M:%S)"
