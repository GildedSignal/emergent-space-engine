#!/bin/bash
# Regen: the cadence ladder on the frozen certificates + the Jacobi invariant sweep.
# All from shipped code (no patch needed: the run changed no engine file — the cadence
# is the shipped --plane-step dial). ~12 min on 8 vCPU.
set -u
cd "$(dirname "$0")/../../.." || exit 1   # the repo root
X=${XTASK:-/home/glmlab/lab-target-3/release/xtask}
[ -x "$X" ] || { cargo build --release -p xtask -p emergent-universe --jobs 4; X=./target/release/xtask; }
OUT="$(dirname "$0")/ladder.txt"
: > "$OUT"
run_gate() {
  echo "=== plane-step $1 gate $2 ===" >> "$OUT"
  /usr/bin/time -f "time %es" timeout 200 "$X" behave --law plane --plane-step "$1" --gates "$2" >> "$OUT" 2>&1
}
# B17 (resonance): the tide-class ladder, fine edge to the cliff
for s in 8 7 6 5 4 3 2 1 0; do run_gate $s B17; done
# B13 (assists): the encounter-class ladder, both sides of the shipped default
for s in 9 8 7 6 5 4 3; do run_gate $s B13; done
# B14: cadence-independence of its timeout (3 witnesses suffice for the dossier row)
for s in 7 4 3; do run_gate $s B14; done
# The Jacobi invariant sweep (the error law; refusals at 7 and 4 are part of the record)
echo "=== jacobi sweep ===" >> "$OUT"
for s in 7 6 5 4 3; do
  echo "--- jacobi step_log2 $s ---" >> "$OUT"
  timeout 150 cargo run --release -p emergent-universe --example jacobi -- $s 100 6 >> "$OUT" 2>&1
done
echo done >> "$OUT"
