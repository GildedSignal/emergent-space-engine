#!/bin/sh
# Regenerates every number in dossier.md from shipped code + work/patch.diff (applied by the
# runner before this runs). ~10 minutes on the shared Linux box. Arms, in order:
#   1. build;  2. digest control (3 cases x off/on, must be identical lines);
#   3. the timing matrix ({10^4,10^5} x {coast,burn} x {off,on}, 3 interleaved reps each);
#   4. read-term attribution (ES_STATEOF_T, off/on, one flight each);
#   5. the census matrix (comb-scale canonical-tick error, 10^4 coast/burn + 10^5 coast).
# Wall numbers are medians over reps; the digest and kick totals are the exact witnesses.
set -e
cd "$(dirname "$0")/../../.."
OUT=lab/results/20261017-1535-second-20261017-1447-system-6671-a60c
BIN=${CARGO_TARGET_DIR:-target}/release/examples/nladder
DIG=${CARGO_TARGET_DIR:-target}/release/examples/ladder_digest
mkdir -p "$OUT"

echo "== 1. build (patched: memo + census + timer, Linux nladder link) =="
(cd crates/universe && cargo build --release --example nladder --example ladder_digest) > "$OUT/regen-build.log" 2>&1 \
  || { tail -5 "$OUT/regen-build.log"; exit 1; }

echo "== 2. digest control: memo OFF vs ON, 3 cases x 4 schedules =="
: > "$OUT/digest-control.txt"
for f in "coast through" "belt crossing" "key mashing"; do
  echo "-- $f off --" >> "$OUT/digest-control.txt"
  $DIG "N=3000 $f" 2>&1 | grep -E "^N=3000" >> "$OUT/digest-control.txt"
  echo "-- $f memo --" >> "$OUT/digest-control.txt"
  ES_MEMO=1 $DIG "N=3000 $f" 2>&1 | grep -E "^N=3000" >> "$OUT/digest-control.txt"
done
cat "$OUT/digest-control.txt"

echo "== 3. timing matrix =="
sh "$OUT/timing.sh"

echo "== 4. read-term attribution (timer-instrumented, attribution only) =="
{
  echo "== off =="; ES_STATEOF_T=1 $BIN 10000 coast 60 600 2>&1 | grep -E "stateof_t|^ladder"
  echo "== on ==";  ES_STATEOF_T=1 ES_MEMO=1 ES_MEMO_STATS=1 $BIN 10000 coast 60 600 2>&1 | grep -E "stateof_t|memo:|^ladder"
} > "$OUT/stateof-term.txt"
cat "$OUT/stateof-term.txt"

echo "== 5. census matrix (comb-scale canonical-tick error) =="
for a in "10000 coast" "10000 burn" "100000 coast"; do
  set -- $a
  ES_CENSUS=1 $BIN $1 $2 60 600 2>&1 | grep -E "^census|^ladder: " > "$OUT/census-n$1-$2.txt"
  grep -E "canonical-tick" "$OUT/census-n$1-$2.txt"
done
echo done
