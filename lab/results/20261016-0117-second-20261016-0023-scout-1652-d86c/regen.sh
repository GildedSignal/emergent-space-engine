#!/bin/bash
# Regen (20261016-0117-second-20261016-0023-scout-1652-d86c): every dossier number from shipped
# code + work/patch.diff (applied by the runner before this runs). One build, six flights, ~5 min.
# The four ES_DET flights are the record (deterministic frames: identical digests across the
# ES_DROP_FLOOR toggle are the D1 evidence); the two wall flights demonstrate the observer-fallback
# view mode (their magnitude and their digests are schedule-dependent by nature — the dossier and
# wall_selfcheck.txt say why).
set -e
cd "$(dirname "$0")/../../.."   # the repo root
cargo build --release -p emergent-universe --example history_floor
BIN="${CARGO_TARGET_DIR:-$HOME/lab-target}/release/examples/history_floor"
R=lab/results/20261016-0117-second-20261016-0023-scout-1652-d86c
CUTS="15000 20000 32000 48000 60000"
mkdir -p "$R/logs"
# The record: deterministic frame budget, coast and burn, floor on and floor off.
ES_DET=1 "$BIN" 10000 1500 coast $CUTS | gzip > "$R/logs/cdet_on.log.gz"
ES_DET=1 ES_DROP_FLOOR=1 "$BIN" 10000 1500 coast $CUTS | gzip > "$R/logs/cdet_off.log.gz"
ES_DET=1 "$BIN" 10000 1500 burn $CUTS | gzip > "$R/logs/det_on.log.gz"
ES_DET=1 ES_DROP_FLOOR=1 "$BIN" 10000 1500 burn $CUTS | gzip > "$R/logs/det_off.log.gz"
for p in "cdet_on cdet_off coast" "det_on det_off burn"; do
  set -- $p
  gunzip -c "$R/logs/$1.log.gz" > /tmp/_a.log
  gunzip -c "$R/logs/$2.log.gz" > /tmp/_b.log
  python3 "$R/compare.py" /tmp/_a.log /tmp/_b.log > "$R/compare_$3.txt"
done
# The wall-budget pair (burn only): the observer-fallback mode's demonstration.
"$BIN" 10000 1500 burn $CUTS | gzip > "$R/logs/wall_on.log.gz"
ES_DROP_FLOOR=1 "$BIN" 10000 1500 burn $CUTS | gzip > "$R/logs/wall_off.log.gz"
gunzip -c "$R/logs/wall_on.log.gz" > /tmp/_a.log
gunzip -c "$R/logs/wall_off.log.gz" > /tmp/_b.log
python3 "$R/compare.py" /tmp/_a.log /tmp/_b.log > "$R/compare_wall.txt"
# The wall self-check: the SAME floor-on build, two wall runs, digests differ (schedule noise).
"$BIN" 10000 1500 burn 15000 20000 32000 48000 60000 2>&1 | grep "^cut game_s" | awk '{print $2, $3}' > /tmp/_wa.txt
{ echo "-- wall floor-on digests, two independent runs of the SAME build and script --"; paste /tmp/_wa.txt <(gunzip -c "$R/logs/wall_on.log.gz" | grep "^cut game_s" | awk '{print $2, $3}') | awk '{d=($2==$4)?"SAME":"DIFF"; print $1, "runA:"$2, "runB:"$4, d}'; } > "$R/wall_selfcheck.txt"
# The census/reads table for the dossier (both scripts, both builds, one line per cut).
gunzip -c "$R/logs/cdet_on.log.gz" "$R/logs/cdet_off.log.gz" "$R/logs/det_on.log.gz" "$R/logs/det_off.log.gz" | grep -E "^(cut|   reads)" > "$R/census_reads.txt"
echo "regen done"
