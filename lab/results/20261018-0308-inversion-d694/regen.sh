#!/usr/bin/env bash
# Regenerates every number in dossier.md from shipped main + work/patch.diff (applied by the
# runner before this runs). Wall cost: one warm build (~15 s) + two flights (~50 s together;
# the loop is compute-paced, rtf is simulated) + belt_first + the analysis. ~2 min total.
set -euo pipefail
cd "$(dirname "$0")/../../.." # repo root
R=lab/results/20261018-0308-inversion-d694

cargo build --release -p emergent-universe --example nladder -p emergent-universe --example belt_first 2>&1 | tail -1

run() { # run <bin> <csv> <N> ; binaries carry a hash suffix under CARGO_TARGET_DIR
  local bin csv n
  bin="$1"; csv="$2"; n="$3"
  LADDER_MAX_S=1100 LADDER_CSV="$R/$csv" "$bin" "$n" coast 900 100 12 > "$R/${csv%.csv}.out" 2>&1
}
B="$(ls "${CARGO_TARGET_DIR:-target}/release/examples/"nladder-* | grep -v '\.d$' | head -1)"
BF="$(ls "${CARGO_TARGET_DIR:-target}/release/examples/"belt_first-* | grep -v '\.d$' | head -1)"
run "$B" flight_1e5.csv 100000
run "$B" flight_0.csv 0
run "$B" flight_1e5_run3.csv 100000
"$BF" 3000 | tee "$R/belt_first.out"

python3 "$R/beats.py" "$R/flight_1e5.csv" "$R/flight_1e5_run3.csv" "$R/flight_0.csv" | tee "$R/beats_final.txt"
echo "regen done: see $R/beats_final.txt, flight_1e5.out, flight_0.out, belt_first.out"
