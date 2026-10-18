#!/bin/sh
# The decisive flights (second author, 20261018-0431-…-49e9). All N=10^4, 60 s wall, rtf 1800,
# canonical cut pinned at 1.2e10 ticks. Pairs run concurrently: load coupling is the point.
#   flights.sh <bin> <outdir> [prefix=a]   — author runs use a_, regen uses r_.
# A flight that stalls or dies leaves no digest line; the script fails loudly (16ec's 90-s
# silent-empty-grep failure mode, named by its checker, is guarded here).
set -e
BIN="$1"; OUT="$2"; P="${3:-a}"; mkdir -p "$OUT"
run() { name=$1; shift; ( for e in "$@"; do export "$e"; done
  timeout 150 "$BIN/nladder" 10000 "$MODE" 60 1800 2>&1 | grep -E "^bound:|^rung" > "$OUT/${P}_$name.txt" ); }
MODE=coast run coast_ctl   ES_LIMIT=12000000000 & p1=$!
MODE=coast run coast_fast  ES_BOUND_RANGE=1 ES_LIMIT=12000000000 & wait $p1 $!
MODE=burn  run shipA       ES_LIMIT=12000000000 & p1=$!
MODE=burn  run shipB       ES_LIMIT=12000000000 & wait $p1 $!
MODE=burn  run pin_ctlA    ES_INJECT_TICK=365400000 ES_LIMIT=12000000000 & p1=$!
MODE=burn  run pin_ctlB    ES_INJECT_TICK=365400000 ES_LIMIT=12000000000 & wait $p1 $!
MODE=burn  run pin_fastA   ES_INJECT_TICK=365400000 ES_BOUND_RANGE=1 ES_LIMIT=12000000000 & p1=$!
MODE=burn  run pin_fastB   ES_INJECT_TICK=365400000 ES_BOUND_RANGE=1 ES_LIMIT=12000000000 & wait $p1 $!
MODE=coast run strad_ctl   ES_LEAVE_LOG2=28 ES_LIMIT=12000000000 & p1=$!
MODE=coast run strad_fast  ES_LEAVE_LOG2=28 ES_BOUND_RANGE=1 ES_LIMIT=12000000000 & wait $p1 $!
echo "== digests ($P) =="
for a in coast_ctl coast_fast shipA shipB pin_ctlA pin_ctlB pin_fastA pin_fastB strad_ctl strad_fast; do
  d=$(sed -n "s/^bound: digest \([0-9a-f]*\) .*/\1/p" "$OUT/${P}_$a.txt")
  [ -n "$d" ] || { echo "$a: NO DIGEST (stall?)"; exit 1; }
  echo "$a $d $(grep -o 'total [0-9]* fast [0-9]* slow_cycle [0-9]* passage [0-9]* deaths [0-9]*' "$OUT/${P}_$a.txt" | head -1)"
done
