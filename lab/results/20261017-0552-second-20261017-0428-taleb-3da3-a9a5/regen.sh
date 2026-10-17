#!/bin/bash
# Regenerates every number in dossier.md from the shipped code + work/patch.diff.
# The original gold run's `tax` instrument (its work/patch.diff, applied first) plus this
# run's scene knobs (TAX_CANNONS / TAX_ARCHI, same patch). Budget ~15 min; the DNF
# timeouts are themselves data and spend most of it.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
OUT="$HERE/regen-out"; mkdir -p "$OUT"
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$HOME/lab-target-0}"
cd "$REPO"
git apply "$HERE/work/patch.diff" 2>/dev/null || echo "(patch already applied)"
cargo build -p emergent-allocator --release --offline --example tax || exit 1
BIN="$CARGO_TARGET_DIR/release/examples/tax"
echo "== build ok $(date +%T) load $(cut -d' ' -f1-3 /proc/loadavg) =="

run() { # name timeout envs|"" args...
  local name=$1 tmo=$2 envs=$3; shift 3
  echo "== $name load $(cut -d' ' -f1-3 /proc/loadavg) $(date +%T) ==" >>"$OUT/$name.log"
  if [ -n "$envs" ]; then timeout "$tmo" env $envs "$BIN" "$@" >>"$OUT/$name.log" 2>&1
  else timeout "$tmo" "$BIN" "$@" >>"$OUT/$name.log" 2>&1; fi
  local rc=$?
  { grep -E "^RESULT" "$OUT/$name.log" || echo "RESULT DNFTMO(${tmo}s,rc=$rc) $name"
    echo "panics: $(grep -c 'panicked at' "$OUT/$name.log")"; } | tee -a "$OUT/ALL.txt"
}
TSV="TAX_STAGES=1"

echo "== S: shipped panic-basin sweep, plain battery, no scene knobs ==" | tee -a "$OUT/ALL.txt"
run S-st3000     120 "" batch 128 8 3000 2 1500 1
run S-st10000    120 "" batch 128 8 10000 2 1500 1
run S-st30000    120 "" batch 128 8 30000 2 1500 1
run S-st99999    120 "" batch 128 8 99999 2 1500 1

echo "== C: 64-cell quiet sea, coupled (40M) and decoupled (102M), one draw each ==" | tee -a "$OUT/ALL.txt"
run C1-64-shipped 60 "$TSV TAX_ARCHI=64:784:156250" batch 128 8 30 2 1500 1
run C1-64-cap16   60 "ES_CAP=16 $TSV TAX_ARCHI=64:784:156250" batch 128 8 30 2 1500 1
run C1-64-cap64   60 "ES_CAP=64 $TSV TAX_ARCHI=64:784:156250" batch 128 8 30 2 1500 1
run C2-64-shipped 60 "$TSV TAX_ARCHI=64:784:400000" batch 128 8 30 2 1500 1
run C2-64-cap16   60 "ES_CAP=16 $TSV TAX_ARCHI=64:784:400000" batch 128 8 30 2 1500 1
run C2-64-cap64   60 "ES_CAP=64 $TSV TAX_ARCHI=64:784:400000" batch 128 8 30 2 1500 1

echo "== B: the checker's probe at full size: 1,280-cell sea (decoupled cap rows: same class, live in work/) ==" | tee -a "$OUT/ALL.txt"
run D1-1280-shipped 300 "$TSV TAX_ARCHI=1280:784:156250" batch 128 8 30 2 3000 1
run D1-1280-cap16    90 "ES_CAP=16 $TSV TAX_ARCHI=1280:784:156250" batch 128 8 30 2 3000 1
run D1-1280-cap64    90 "ES_CAP=64 $TSV TAX_ARCHI=1280:784:156250" batch 128 8 30 2 3000 1
run D2-1280-shipped 300 "$TSV TAX_ARCHI=1280:784:400000" batch 128 8 30 2 3000 1

echo "== D3: the basin edge at stagger 30000 — draw-flip (2 shipped draws) and the cap64 arm-check ==" | tee -a "$OUT/ALL.txt"
run D3-shipped-a 120 ""          batch 128 8 30000 2 1500 1
run D3-shipped-b 120 ""          batch 128 8 30000 2 1500 1
run D3-cap64     120 "ES_CAP=64" batch 128 8 30000 2 1500 1

echo "== D4: the checker's 28,160-body datum, paired ==" | tee -a "$OUT/ALL.txt"
run D4-cap64   240 "ES_CAP=64" batch 2560 8 30 1 1500 1
run D4-shipped 150 ""          batch 2560 8 30 1 1500 1

echo "== done $(date +%T) load $(cut -d' ' -f1-3 /proc/loadavg) ==" | tee -a "$OUT/ALL.txt"
