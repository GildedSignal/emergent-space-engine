#!/bin/sh
# Regen for 20261017-1918-inversion-8994: every dossier number from shipped code + this run's patch
# (wave.rs). Linux/x86; ~6 min single-threaded; peak process ~1.5 GB (the 3e5 arms).
# Patch (work/patch.diff) adds crates/universe/examples/wave.rs — apply before running.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/../../.."                  # repo root (script is lab/results/<id>/regen.sh)
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$HOME/lab-target-1}"
W="$CARGO_TARGET_DIR/release/examples/wave"
B="$CARGO_TARGET_DIR/release/examples/belt_first"
OUT="$HERE/raw"
mkdir -p "$OUT"
echo "== machine: $(uname -r), load $(cut -d' ' -f1 /proc/loadavg), free $(free -g | sed -n 2p | awk '{print $7}')G" > "$OUT/machine.txt"
cargo build --release -p emergent-universe --example wave --example belt_first
# anchor: where the belt's first items are (the wave's address)
"$B" 100000 > "$OUT/belt_first.txt" 2>&1
# budget-free ladder through the first comb (worst rolling 1-s mean = the letter's load)
for N in 0 10000 100000 300000; do "$W" "$N" 45000 > "$OUT/wave_$N.txt" 2>&1; done
# the shipped 12-ms budget path: crest absorption at 1e5 and 3e5, then BOTH combs
"$W" 100000 17000 100 12 > "$OUT/wave_100000_budget12.txt" 2>&1
"$W" 300000 20000 100 12 > "$OUT/wave_300000_budget12.txt" 2>&1
"$W" 300000 46000 100 12 > "$OUT/wave_300000_budget12_long.txt" 2>&1
# headline extraction (the dossier table's columns)
for f in "$OUT"/wave_*.txt; do grep -E "^(LETTER|waveline)" "$f" | sed "s|^|$(basename "$f"): |"; done
