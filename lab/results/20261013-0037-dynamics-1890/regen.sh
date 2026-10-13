#!/bin/sh
# Regen (lab 20261013-0037-dynamics-1890): rebuilds every dossier number from the shipped tree
# plus the three example files added by work/patch.diff. ~5 min on the lab runner.
set -e
cd "$(dirname "$0")/../../.."   # repo root
cargo build --release -p emergent-universe --example clock_domain --example clock_regimes --example clock_disc --example clock_debug
BIN=$(ls -d ./target/release/examples 2>/dev/null || echo ~/lab-target-1/release/examples)
OUT=lab/results/20261013-0037-dynamics-1890
"$BIN/clock_domain"  > "$OUT/domain_sweep.txt" 2>&1   # 22x22 (E, peri) acceptance map, ~0.1 s
timeout 360 "$BIN/clock_regimes" > "$OUT/flights.txt" 2>&1   # 5 flights x <=55 s wall cap
"$BIN/clock_disc"    > "$OUT/discriminator.txt" 2>&1   # from_state vs from_invariants, ~6 s
"$BIN/clock_debug"   > "$OUT/debug_states.txt" 2>&1
# Headline numbers quoted in the dossier:
grep -c "REFUSE" "$OUT/domain_sweep.txt"
grep -E "LOST|SWITCH|TIMEOUT" "$OUT/flights.txt"
awk '/^# brake_g30/,/^# brake_g300/' "$OUT/flights.txt" | grep -o "gamma=[0-9.]*" | sort -t= -k2 -g | sed -n '1p;$p'
grep -c "refusals" "$OUT/flights.txt" >/dev/null && awk '/turnburn/{if (match($0,/refusals=[0-9]+/)) {v=substr($0,RSTART+10,RLENGTH-10)+0; if (v>m) m=v}} END {print "turnburn max refusals:", m}' "$OUT/flights.txt"
