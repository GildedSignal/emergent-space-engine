#!/bin/sh
# The decisive depth matrix (predictions pre-registered in predictions.md before these runs).
# Each flight prints arm, digest, event counters, the standing-arc census (current vs history,
# by class), mint-cause counters and rss. One process per flight, frozen private binary.
R="$(cd "$(dirname "$0")" && pwd)"
BIN="$R/work/bin/arc_pin"
OUT="$R/flights"
mkdir -p "$OUT"
run() { # run <label> <env> <N> <flight> <cut> [seed]
  lbl="$1"; env="$2"; n="$3"; fl="$4"; cut="$5"; seed="${6:-1}"
  echo "== $lbl =="
  env $env "$BIN" "$n" "$fl" "$cut" "$seed" 2>&1 | tee "$OUT/$lbl.txt" | grep -E "^arm|current-bindings|pinned_total"
}
run c10k_coast_20k_ctl "" 10000 coast 20000
run c10k_coast_20k_seam ES_LAZY_ENTRY=1 10000 coast 20000
run c10k_coast_20k_var "ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1" 10000 coast 20000
run c10k_coast_48k_seam ES_LAZY_ENTRY=1 10000 coast 48000
run c10k_coast_48k_var "ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1" 10000 coast 48000
run c10k_coast_96k_var "ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1" 10000 coast 96000
run c10k_burn_20k_var "ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1" 10000 burn 20000
run c10k_burn_48k_var "ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1" 10000 burn 48000
run c100k_coast_20k_var "ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1" 100000 coast 20000
run mixed1k_1k2_var "ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1" 1000 mixed 1200
V="ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1"
env $V "$BIN" 10000 burn 48000 > "$OUT/c10k_burn_48k_var.txt" 2>&1
env $V "$BIN" 100000 coast 20000 > "$OUT/c100k_coast_20k_var.txt" 2>&1
env $V "$BIN" 500 stargraze 4800 > "$OUT/stargraze500_4k8_var.txt" 2>&1
env $V "$BIN" 10000 coast 48000 3 > "$OUT/c10k_coast_48k_seed3_var.txt" 2>&1
grep -E "^arm |current-bindings|pinned_total" "$OUT"/*.txt
echo "MATRIX DONE"
