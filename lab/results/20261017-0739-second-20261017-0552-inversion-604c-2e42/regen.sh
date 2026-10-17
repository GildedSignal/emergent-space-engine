#!/bin/sh
# Regenerates every number in dossier.md from the shipped tree plus work/patch.diff (applied by the
# runner before this runs): the original 0552 instrument (census + prof stages) plus the second
# author's per-frame channel split. Linux/x86; orders of magnitude only.
# Total: one release build (~15-80 s warm, ~4 min cold) + ~2 min of flights. < 15 min.
set -e
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$DIR/../../.."
cargo build --release --features prof -p emergent-universe --example scanprobe 2>&1 | tail -1
B=$(cargo metadata --format-version 1 2>/dev/null | tr ',' '\n' | grep -o '"target_directory":"[^"]*"' | head -1 | cut -d'"' -f4)/release/examples/scanprobe
[ -x "$B" ] || B=target/release/examples/scanprobe
OUT="$DIR/raw"
mkdir -p "$OUT"
# The matrix (args: form extra wall_s rtf seed). Group A: the original 0552 anchors, seeds 1.
# Group B: the checker's named decisive experiment (K=1000, two seeds, decomposed) and its
# adversarial cases (seed-2 anchors, decade-up 10^4, formation-only 3000, the tier at a 10^5 belt).
for args in "0 0 10 100 1" "50 0 10 100 1" "111 0 10 100 1" "200 0 10 100 1" "0 10000 10 100 1" "0 100000 6 100 1" "200 10000 10 100 1" "3000 10000 10 100 1" "1000 0 10 100 1" "1000 0 10 100 2" "0 0 10 100 2" "200 0 10 100 2" "10000 0 6 100 1" "3000 0 6 100 1" "200 100000 6 100 1"; do
  set -- $args
  echo "=== form=$1 extra=$2 seed=$5"
  "$B" "$@" > "$OUT/f$1_e$2_s$3_seed$5.txt" 2>&1
  grep -E "^(probe:|scan:|chan (late|over|p99|scan-placement))" "$OUT/f$1_e$2_s$3_seed$5.txt"
done
# The 12 worst frames of the decisive flights (the decomposition's evidence).
echo "=== worst frames, form=1000 seed=1 and seed=2; and form=3000 extra=10000"
grep -A13 "chan worst frames" "$OUT/f1000_e0_s10_seed1.txt" | head -8
grep -A13 "chan worst frames" "$OUT/f1000_e0_s10_seed2.txt" | head -4
grep -A13 "chan worst frames" "$OUT/f3000_e10000_s10_seed1.txt" | head -4
# Instrument stability: the census lines must be bit-identical across reruns (digests are
# wall-paced at rtf and end at different ticks; the census is the claim's instrument).
echo "=== census stability (3 reruns, form=200)"
for i in 1 2 3; do "$B" 200 0 10 100 1 | grep "^scan:" | md5sum; done
echo "done."
