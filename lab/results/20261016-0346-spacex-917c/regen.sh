#!/bin/sh
# Regenerates every dossier number from the shipped tree + work/patch.diff (applied by the runner before this runs).
# Total wall ~14 min (flights are budget-free and run in parallel pairs; the box's 8 cores carry them).
set -e
cd "$(dirname "$0")/../../.."
R=/home/glmlab/lab-target-3/release/examples
OUT=lab/results/20261016-0346-spacex-917c/flights
mkdir -p "$OUT"

# 1. Build patched binaries (patch already applied).
cargo build --release -p emergent-universe --example nladder --example ladder_digest --example belt_first

# 2. Pristine ladder_digest (step.rs reverted), for the off-arm identity check.
git diff crates/universe/src/step.rs > "$OUT/../work/stagger.regendelta" || true
git checkout crates/universe/src/step.rs
cargo build --release -p emergent-universe --example ladder_digest
cp "$R/ladder_digest" "$OUT/../work/ladder_digest_pristine"
git apply "$OUT/../work/stagger.regendelta"
cargo build --release -p emergent-universe --example ladder_digest --example nladder --example belt_first

# 3. Identity: pristine vs patched with ES_STAGGER unset, all 13 cases x 4 schedules.
"$OUT/../work/ladder_digest_pristine" > "$OUT/digest_pristine.txt" 2>&1
env -u ES_STAGGER "$R/ladder_digest" > "$OUT/digest_off.txt" 2>&1
sed "s/ \[[0-9.]* s\]$//" "$OUT/digest_pristine.txt" > "$OUT/digest_pristine.cut"; sed "s/ \[[0-9.]* s\]$//" "$OUT/digest_off.txt" > "$OUT/digest_off.cut"; diff "$OUT/digest_pristine.cut" "$OUT/digest_off.cut" && echo "DIGEST IDENTITY: off-arm bit-identical (13 cases, timings stripped)"

# 4. The four budget-free flights (rtf 100, coast, seed 1, 60 fps; budget 1e6 ms = free).
{ uptime; free -m | head -2; } > "$OUT/state_A_B.txt"
setsid env ES_TLIMIT=500 ES_ROWS=1 "$R/nladder" 100000 coast 200 100 1000000 > "$OUT/A_1e5_unstagger.txt" 2>&1 < /dev/null &
A=$!
setsid env ES_TLIMIT=500 ES_ROWS=1 "$R/nladder" 300000 coast 320 100 1000000 > "$OUT/B_3e5_unstagger.txt" 2>&1 < /dev/null &
B=$!
wait $A $B
{ uptime; free -m | head -2; } > "$OUT/state_C_D.txt"
setsid env ES_TLIMIT=1200 ES_ROWS=1 ES_STAGGER=1 "$R/nladder" 100000 coast 480 100 1000000 > "$OUT/C_1e5_stagger.txt" 2>&1 < /dev/null &
C=$!
setsid env ES_TLIMIT=1200 ES_ROWS=1 ES_STAGGER=1 "$R/nladder" 300000 coast 480 100 1000000 > "$OUT/D_3e5_stagger.txt" 2>&1 < /dev/null &
D=$!
wait $C $D

# 5. The wave's first-item spread under the stagger (shipped belt_first, patched build).
"$R/belt_first" 100000 > "$OUT/belt_first_1e5.txt" 2>&1 || true
ES_STAGGER=1 "$R/belt_first" 100000 > "$OUT/belt_first_1e5_stagger.txt" 2>&1 || true

# 6. Analysis.
python3 lab/results/20261016-0346-spacex-917c/analyze.py "$OUT" | tee "$OUT/analysis.txt"
