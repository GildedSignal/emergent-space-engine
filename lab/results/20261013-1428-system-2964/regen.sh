#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied before
# this runs). Total wall ≈ 5–6 min on the lab's shared x86 (8 vCPU).
# Arms: ship = shipped bits (≡ env unset, verified bit-identical digests), f8 = 1/256,
# fine = 1/1024, off = the clamp deleted.
set -e
cd "$(dirname "$0")"
ROOT=../../..
CP="${CARGO_TARGET_DIR:-}/release/examples/burn_cadence"
[ -x "$CP" ] || CP="$(cd "$ROOT" && cargo metadata --format-version 1 2>/dev/null | tr ',' '\n' | grep -o '"target_directory":"[^"]*"' | cut -d'"' -f4)/release/examples/burn_cadence"
[ -x "$CP" ] || CP=$(find /home/glmlab -maxdepth 4 -path "*release/examples/burn_cadence" -type f 2>/dev/null | head -1)
echo "probe: $CP"
cd work
run() { # arm seconds seed tag
  echo "=== $4 (arm $1, $2 s, seed $3)"; timeout 500 env ES_BURN_CADENCE=$1 "$CP" "$2" "" "$3" | tee "table_$4.txt" | tail -7
}
# The equivalence control: ship ≡ unset, digest for digest (wall times are machine noise).
timeout 120 env ES_BURN_CADENCE=ship "$CP" 2 "" 1 | sed -n '3p' | grep -oE '[0-9a-f]{64}' > equiv_ship.txt
timeout 120 env -u ES_BURN_CADENCE "$CP" 2 "" 1 | sed -n '3p' | grep -oE '[0-9a-f]{64}' > equiv_unset.txt
if cmp -s equiv_ship.txt equiv_unset.txt; then echo "EQUIVALENCE: ship == unset, digest $(cat equiv_ship.txt)"; else echo "EQUIVALENCE FAILED"; cat equiv_ship.txt equiv_unset.txt; fi
for arm in ship off fine f8; do run $arm 8 1 "8s_${arm}_seed1"; done
run ship 16 1 16s_ship_seed1
run off 16 1 16s_off_seed1
run fine 16 1 16s_fine_seed1
run ship 8 3 8s_ship_seed3
run off 8 3 8s_off_seed3
echo "=== the staleness envelopes (max owed |dv| a reader sees between flushes)"
../analyze.sh .
