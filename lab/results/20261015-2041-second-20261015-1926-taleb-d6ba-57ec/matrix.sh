#!/bin/sh
# The second-author matrix on d6ba's frozen binary (patch = 3dc8 verbatim + the census, unchanged):
# (a) the belt rows d6ba's regen missed or the checker had to fly solo (ctl burn 20k, the 26k
#     pulse instant, the 48k floor anchor, the 10^5 N-floor), and
# (b) the checker's named gold experiment: the comet depth ladder past the ~28k first settle
#     (stargraze 100 at 32k/48k, mixed 50 at 48k, shipped ctl at 32k), all census'd.
# Predictions for (b) pre-registered in predictions.md before the ladder flew.
# The comet arms launch FIRST (each is a single-threaded process; the 48k arm is the critical
# path ~700 s CPU) and the cheap belt arms fill the same wall window serially; the ctl comet
# arm (rss ~2.8 GB by design — shipped is the ruin case) runs last and best-effort.
R="$(cd "$(dirname "$0")" && pwd)"
BIN="$R/work/bin/arc_pin"
OUT="$R/flights"
V="ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1"
mkdir -p "$OUT"

echo "== launch the comet ladder (parallel) =="
env $V "$BIN" 100 stargraze 32000 > "$OUT/sg100_32k_var.txt" 2>&1 &
P1=$!
env $V "$BIN" 100 stargraze 48000 > "$OUT/sg100_48k_var.txt" 2>&1 &
P2=$!
env $V "$BIN" 50 mixed 48000 > "$OUT/mixed50_48k_var.txt" 2>&1 &
P4=$!

echo "== belt: the regen gaps and anchors (serial, inside the comet window) =="
"$BIN" 10000 burn 20000 > "$OUT/c10k_burn_20k_ctl.txt" 2>&1
env $V "$BIN" 10000 coast 26000 > "$OUT/c10k_coast_26k_var.txt" 2>&1
env $V "$BIN" 10000 coast 48000 > "$OUT/c10k_coast_48k_var.txt" 2>&1
env $V "$BIN" 100000 coast 48000 > "$OUT/c100k_coast_48k_var.txt" 2>&1
grep -hE "^arm |pinned_total" "$OUT"/c10k_burn_20k_ctl.txt "$OUT"/c10k_coast_26k_var.txt \
  "$OUT"/c10k_coast_48k_var.txt "$OUT"/c100k_coast_48k_var.txt

echo "== the shipped-ctl comet contrast, last and best-effort (rss ~2.8 GB: the ruin case) =="
"$BIN" 100 stargraze 32000 > "$OUT/sg100_32k_ctl.txt" 2>&1 &
P5=$!
wait $P1 $P2 $P4 $P5 || true
grep -hE "^arm |pinned_total" "$OUT"/sg100_32k_var.txt "$OUT"/sg100_48k_var.txt \
  "$OUT"/mixed50_48k_var.txt "$OUT"/sg100_32k_ctl.txt
echo "MATRIX DONE"
